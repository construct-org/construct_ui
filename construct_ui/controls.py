# -*- coding: utf-8 -*-
from __future__ import absolute_import
'''
Controls
========
Wraps all standard control widgets providing a unified api.

- Controls send a **changed** message when the controls value changes
- `Control.get` gets the value of a control
- `Control.set` sets the value of a control
'''
from Qt import QtWidgets, QtCore, QtGui
from abc import abstractmethod
from construct_ui.utils import ABCNonMeta, is_implemented, not_implemented
from bands import channel


class Control(ABCNonMeta):

    changed = channel('changed')

    def __init__(self, name, parent=None):
        super(Control, self).__init__(parent=parent)

        self.setObjectName(name)
        self.name = name
        self.create()

    def send_changed(self):
        self.changed.send(self)

    @abstractmethod
    def create(self):
        return NotImplemented

    @abstractmethod
    def get(self):
        return NotImplemented

    @abstractmethod
    def set(self, value):
        return NotImplemented


class SpinControl(Control, QtWidgets.QSpinBox):

    default_range = (0, 99)

    def __init__(self, name, range=None, parent=None):
        self.range = range or self.default_range
        super(SpinControl, self).__init__(name, parent)

    def create(self):
        self.set_range(self.range)
        self.valueChanged.connect(self.send_changed)

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

    default_range = (0, 99)

    def __init__(self, name, range=None, parent=None):
        self.range = range or self.default_range
        super(FloatControl, self).__init__(name, parent)

    def create(self):
        self.set_range(self.range)
        self.valueChanged.connect(self.send_changed)

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
            box.valueChanged.connect(self.send_changed)
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

    def __init__(self, name, placeholder=None, parent=None):
        super(StringControl, self).__init__(name, parent)

    def create(self):
        self.textEdited.connect(self.send_changed)

    def get(self):
        return self.text()

    def set(self, value):
        return self.setText(value)


class BoolControl(Control, QtWidgets.QCheckBox):

    def __init__(self, name, parent=None):
        super(BoolControl, self).__init__(name, parent)

    def create(self):
        self.clicked.connect(self.send_changed)

    def get(self):
        return self.isChecked()

    def set(self, value):
        self.setChecked(value)


class OptionControl(Control, QtWidgets.QComboBox):

    def __init__(self, name, options=None, parent=None):
        self.options = options
        super(OptionControl, self).__init__(name, parent)

    def create(self):
        self.activated.connect(self.send_changed)
        if self.options:
            self.set_options(self.options)

        # Allow items to be styled
        self.setItemDelegate(QtWidgets.QStyledItemDelegate())

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


class AnyCompleter(QtWidgets.QCompleter):

    def __init__(self, *args, **kwargs):
        super(AnyCompleter, self).__init__(*args, **kwargs)
        self.local_completion_prefix = ''
        self.source_model = None

    def setModel(self, model):
        self.source_model = model
        super(AnyCompleter, self).setModel(self.source_model)

    def updateModel(self):
        pattern = self.local_completion_prefix

        class ProxyModel(QtCore.QSortFilterProxyModel):
            def filterAcceptsRow(self, sourceRow, sourceParent):
                i = self.sourceModel().index(sourceRow, 0, sourceParent)
                data = self.sourceModel().data(i).lower()
                data_parts = data.split('/')
                pattern_parts = pattern.split('/')
                while pattern_parts:
                    part = pattern_parts.pop(0)
                    for i, data_part in enumerate(data_parts):
                        if part in data_part:
                            data_parts = data_parts[i:]
                            break
                    else:
                        return False
                return True

        model = ProxyModel()
        model.setSourceModel(self.source_model)
        super(AnyCompleter, self).setModel(model)

    def splitPath(self, path):
        self.local_completion_prefix = path
        self.updateModel()
        return ''


class EntryOptionControl(Control, QtWidgets.QComboBox):

    def __init__(self, name, root=None, tags=None, parent=None):
        self.root = root
        self.tags = tags
        self.entries = self.query()
        self.options = [self.format_entry(e) for e in self.entries]
        super(EntryOptionControl, self).__init__(name, parent)

    def query(self):
        import fsfs
        if self.root:
            query = fsfs.search(self.root)
            if self.tags:
                query = query.tags(*self.tags)
            return list(query)
        return []

    def format_entry(self, entry):
        parents = list(entry.parents())[::-1]
        if parents:
            parts = parents[max(0, len(parents) - 3):] + [entry]
            return '/'.join([p.name for p in parts])
        else:
            return entry.name

    def create(self):

        self.setEditable(True)
        self.setInsertPolicy(self.NoInsert)
        self.activated.connect(self.send_changed)
        self.addItems(self.options)

        self.completer = AnyCompleter(self)
        self.completer.setModel(self.model())
        self.completer.activated.connect(self.send_changed)
        self.setCompleter(self.completer)

    def get(self):
        index = self.currentIndex()
        return self.entries[index]

    def set(self, value):
        try:
            index = self.entries.index(value)
            self.setCurrentIndex(index)
        except ValueError:
            pass


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
    IntOptionControl,
    EntryOptionControl,
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
