'''
Parameter Controls
==================
'''
from Qt import QtWidgets, QtCore


class Control(QtCore.QObject):

    changed = QtCore.Signal(object)

    def __init__(self, name, parent=None):
        super(Control, self).__init__(parent=parent)

        self.setObjectName(name)
        self.name = name
        self.widget = self.create()

    def emit_changed(self):
        self.changed.emit(self)

    def create(self):
        return NotImplemented

    def get(self):
        return NotImplemented

    def set(self, value):
        return NotImplemented


class SpinControl(Control):

    widget_cls = QtWidgets.QSpinBox

    def __init__(self, name, range=None, parent=None):
        super(SpinControl, self).__init__(name, parent)
        self.set_range(range)

    def create(self):
        box = self.widget_cls(parent=self.parent())
        box.setFixedHeight(30)
        box.valueChanged.connect(self.emit_changed)
        return box

    def set_range(self, range=None):
        range = range or (0, 99)
        self.widget.setRange(*range)
        self.range = range

    def get(self):
        return self.widget.value()

    def set(self, value):
        self.widget.setValue(value)


class MultiSpinControl(Control):

    widget_cls = QtWidgets.QSpinBox
    num_controls = 2

    def __init__(self, name, range1=None, range2=None, parent=None):
        super(Spin2Control, self).__init__(name, parent)
        self.set_range1(range1)
        self.set_range2(range2)

    def create(self):

        w = QtWidgets.QWidget()
        w.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        l = QtWidgets.QHBoxLayout()
        l.setSpacing(20)
        l.setContentsMargins(0, 0, 0, 0)
        w.setLayout(l)

        self.boxes = []
        for i in range(self.num_controls):
            box = self.widget_cls(parent=self.parent())
            box.setFixedHeight(30)
            box.valueChanged.connect(self.emit_changed)
            l.addWidget(box)
            self.boxes.append(box)

        return w

    def set_range(self, index, range=None):
        range = range or (0, 99)
        self.boxes[index].setRange(*range)

    def get_range(self, index):
        return self.boxes[index].minimum(), self.boxes[index].maximum()

    def get(self):
        return tuple([box.value() for box in self.boxes])

    def set(self, value):
        if len(value) != self.num_controls:
            raise ValueError(
                'Expected %d values, got %d' % (len(value), self.num_controls)
            )
        for box, value in zip(self.boxes, value):
            box.setValue(value)


class IntControl(SpinControl):

    widget_cls = QtWidgets.QSpinBox


class Int2Control(MultiSpinControl):

    widget_cls = QtWidgets.QSpinBox
    num_controls = 2


class Int3Control(MultiSpinControl):

    widget_cls = QtWidgets.QSpinBox
    num_controls = 3


class FloatControl(SpinControl):

    widget_cls = QtWidgets.QDoubleSpinBox


class Float2Control(MultiSpinControl):

    widget_cls = QtWidgets.QDoubleSpinBox
    num_controls = 2


class Float3Control(MultiSpinControl):

    widget_cls = QtWidgets.QDoubleSpinBox
    num_controls = 3


class StringControl(Control):

    def create(self):
        line = QtWidgets.QLineEdit(parent=self.parent())
        line.textEdited.connect(self.emit_changed)
        return line

    def get(self):
        return self.widget.text()

    def set(self, value):
        return self.widget.setText(value)


class BoolControl(Control):

    def create(self):
        box = QtWidgets.QCheckBox(parent=self.parent())
        box.setFixedSize(20, 20)
        box.clicked.connect(self.emit_changed)
        return box

    def get(self):
        return self.widget.isChecked()

    def set(self, value):
        self.widget.setChecked(value)


class OptionControl(Control):

    def __init__(self, name, options=None, parent=None):
        super(OptionControl, self).__init__(name, parent)
        if options:
            self.set_options(options)

    def create(self):
        combo = QtWidgets.QComboBox(parent=self.parent())
        combo.activated.connect(self.emit_changed)
        return combo

    def get_options(self, options):
        return self.options

    def set_options(self, options):
        self.widget.clear()
        self.widget.addItems(options)
        self.options = options

    def get_data(self):
        return self.widget.itemData(
            self.widget.currentIndex(),
            QtCore.Qt.UserRole
        )

    def get(self):
        return self.widget.currentText()

    def set(self, value):
        self.widget.setCurrentIndex(self.widget.findText(value))


class StringOptionControl(OptionControl)
    pass


class IntOptionControl(OptionControl):

    def get(self):
        return self.widget.currentIndex()

    def set(self, value):
        self.widget.setCurrentIndex(value)


# parameters = dict(
#     task={
#         'label': 'Task',
#         'required': True,
#         'type': types.Entry,
#         'help': 'Task',
#     },
#     workspace={
#         'label': 'Workspace',
#         'required': False,
#         'type': types.Entry,
#         'help': 'Workspace to save to'
#     },
#     name={
#         'label': 'Name',
#         'required': False,
#         'type': types.String,
#         'help': 'Filename',
#     },
#     version={
#         'label': 'Version',
#         'required': True,
#         'type': types.Integer,
#         'help': 'File Version'
#     }
# )
