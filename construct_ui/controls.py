'''
Parameter Controls
==================
'''
from Qt import QtWidgets, QtCore


class Control(object):

    def __init__(self, name, parent=None):
        super(Control, self).__init__(parent=parent)

        self.setObjectName(name)
        self.name = name
        self.create()

    def emit_changed(self):
        print('CHANGE', self)
        self.changed.emit(self)

    def create(self):
        return NotImplemented

    def get(self):
        return NotImplemented

    def set(self, value):
        return NotImplemented


class SpinControl(Control, QtWidgets.QSpinBox):

    changed = QtCore.Signal(object)
    default_range = (0, 99)

    def __init__(self, name, range=None, parent=None):
        self.range = range or self.default_range
        super(SpinControl, self).__init__(name, parent)

    def create(self):
        self.set_range(self.range)
        self.valueChanged.emit(self.emit_changed)

    def get_range(self):
        return self.minimum(), self.maximum()

    def set_range(self, range=None):
        range = range or self.default_range
        self.setRange(*range)
        self.range = range

    def get(self):
        return self.value()

    def set(self, value):
        self.setValue(value)


class IntControl(SpinControl):
    pass


class FloatControl(Control, QtWidgets.QDoubleSpinBox):

    changed = QtCore.Signal(object)
    default_range = (0, 99)

    def __init__(self, name, range=None, parent=None):
        self.range = range or self.default_range
        super(FloatControl, self).__init__(name, parent)

    def create(self):
        self.set_range(self.range)
        self.valueChanged.emit(self.emit_changed)

    def get_range(self):
        return self.minimum(), self.maximum()

    def set_range(self, range=None):
        range = range or self.default_range
        self.setRange(*range)
        self.range = range

    def get(self):
        return self.value()

    def set(self, value):
        self.setValue(value)


class MultiSpinControl(Control, QtWidgets.QWidget):

    changed = QtCore.Signal(object)
    widget_cls = QtWidgets.QSpinBox
    default_range = (0, 99)
    num_controls = 2

    def __init__(self, name, ranges=None, parent=None):
        self.ranges = ranges or [
            self.default_range for i in range(self.num_controls)
        ]
        super(MultiSpinControl, self).__init__(name, parent)

    def create(self):
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.widgets = []
        for i in range(self.num_controls):
            box = self.widget_cls(parent=self.parent())
            box.valueChanged.connect(self.emit_changed)
            self.layout.addWidget(box)
            self.widgets.append(box)

        self.set_ranges(self.ranges)

    def get_range(self, index):
        return self.ranges[index][0], self.ranges[index][1]

    def get_ranges(self):
        return self.ranges

    def set_range(self, index, range=None):
        range = range or self.default_range
        self.widgets[index].setRange(*range)
        self.ranges[index] = range

    def set_ranges(self, ranges):
        if len(ranges) != self.num_controls:
            raise ValueError('Expected %d ranges, got %d' %
                             (len(ranges), self.num_controls))
        for i, range in enumerate(ranges):
            self.set_range(i, range)

    def get(self):
        return tuple([box.value() for box in self.widgets])

    def set(self, value):
        if len(value) != self.num_controls:
            raise ValueError('Expected %d values, got %d' %
                             (len(value), self.num_controls))
        for box, value in zip(self.widgets, value):
            box.setValue(value)


class Int2Control(MultiSpinControl):

    widget_cls = QtWidgets.QSpinBox
    num_controls = 2


class Int3Control(MultiSpinControl):

    widget_cls = QtWidgets.QSpinBox
    num_controls = 3


class Float2Control(MultiSpinControl):

    widget_cls = QtWidgets.QDoubleSpinBox
    num_controls = 2


class Float3Control(MultiSpinControl):

    widget_cls = QtWidgets.QDoubleSpinBox
    num_controls = 3


class StringControl(Control, QtWidgets.QLineEdit):

    changed = QtCore.Signal(object)

    def __init__(self, name, placeholder=None, parent=None):
        super(StringControl, self).__init__(name, parent)

    def create(self):
        self.textEdited.connect(self.emit_changed)

    def get(self):
        return self.text()

    def set(self, value):
        return self.setText(value)


class BoolControl(Control, QtWidgets.QCheckBox):

    changed = QtCore.Signal(object)

    def __init__(self, name, parent=None):
        super(BoolControl, self).__init__(name, parent)

    def create(self):
        self.clicked.connect(self.emit_changed)

    def get(self):
        return self.isChecked()

    def set(self, value):
        self.setChecked(value)


class OptionControl(Control, QtWidgets.QComboBox):

    changed = QtCore.Signal(object)

    def __init__(self, name, options=None, parent=None):
        self.options = options
        super(OptionControl, self).__init__(name, parent)

    def create(self):
        self.activated.connect(self.emit_changed)
        if self.options:
            self.set_options(options)

    def get_options(self, options):
        return self.options

    def set_options(self, options):
        self.clear()
        self.addItems(options)
        self.options = options

    def get_data(self):
        return self.itemData(
            self.currentIndex(),
            QtCore.Qt.UserRole
        )

    def get(self):
        return self.currentText()

    def set(self, value):
        self.setCurrentIndex(self.findText(value))


class StringOptionControl(OptionControl):
    pass


class IntOptionControl(OptionControl):

    def get(self):
        return self.currentIndex()

    def set(self, value):
        self.setCurrentIndex(value)


CONTROL_TYPES = [
    IntControl,
    Int2Control,
    Int3Control,
    FloatControl,
    Float2Control,
    Float3Control,
    StringControl,
    BoolControl,
    StringOptionControl,
    IntOptionControl
]


CONTROL_MAP = {
    int: IntControl,
    (int, int): Int2Control,
    (int, int, int): Int3Control,
    float: FloatControl,
    (float, float): Float2Control,
    (float, float, float): Float3Control,
    str: StringControl,
    bool: BoolControl,
    (str,): StringOptionControl,
}


def control_for_value(value):
    if value is None:
        return

    if type(value) in CONTROL_MAP:
        return CONTROL_MAP[type(value)]

    if isinstance(value, (list, tuple)):
        if not value:
            return

        key = tuple([type(v) for v in value])
        if key in CONTROL_MAP:
            return CONTROL_MAP[key]
        if key[0] is str:
            return CONTROL_MAP[(str,)]
        if key[0] is int:
            return CONTROL_MAP[(int,)]


def map_controls():

    data = {
        'bool': True,
        'int': 10,
        'int2': [10, 20],
        'int3': [10, 20, 30],
        'float': 10,
        'float2': [10, 20],
        'float3': [10, 20, 30],
        'string': 'hello world!',
        'option': ['one', 'two', 'three', 'four']
    }

    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QWidget()
    layout = QtWidgets.QFormLayout()
    controls = []

    for name, value in data.items():
        control = control_for_value(value)
        c = control(name, parent=win)
        controls.append(c)
        if isinstance(c, OptionControl):
            c.set_options(value)
        else:
            c.set(value)
        layout.addRow(c.name, c)

    win.setLayout(layout)
    win.show()
    def closeEvent(event):
        print({c.name: c.get() for c in controls})
        event.accept()
    win.closeEvent = closeEvent
    sys.exit(app.exec_())


def show_controls():

    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QWidget()
    layout = QtWidgets.QFormLayout()

    for control in CONTROL_TYPES:
        c = control(control.__name__, parent=win)
        layout.addRow(c.name, c)

    win.setLayout(layout)
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    map_controls()
