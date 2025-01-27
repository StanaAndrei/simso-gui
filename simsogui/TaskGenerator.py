from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QCheckBox, QComboBox, QTextEdit, QDialogButtonBox, QDialog, QDoubleSpinBox, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QRadioButton, QSlider, QSpinBox, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal, QRegExp
from PyQt5 import QtCore, QtWidgets
from simso.generator.task_generator import StaffordRandFixedSum, \
    gen_periods_loguniform, gen_periods_uniform, gen_periods_discrete, \
    gen_tasksets, UUniFastDiscard, gen_kato_utilizations

from PyQt5 import QtGui
from simsogui.Global import GlobalData


from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QFileDialog, QVBoxLayout, QWidget  
import sys, json, textwrap

class _DoubleSlider(QSlider):
    doubleValueChanged = pyqtSignal([float])

    def __init__(self, orient, parent):
        QSlider.__init__(self, orient, parent)

        self.valueChanged.connect(
            lambda x: self.doubleValueChanged.emit(x / 100.0))

    def setMinimum(self, val):
        QSlider.setMinimum(self, val * 100)

    def setMaximum(self, val):
        QSlider.setMaximum(self, val * 100)

    def setValue(self, val):
        QSlider.setValue(self, int(val * 100))


class IntervalSpinner(QWidget):
    def __init__(self, parent, min_=1, max_=1000, step=1, round_option=True):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)
        hlayout = QHBoxLayout()
        self.start = QDoubleSpinBox(self)
        self.start.setMinimum(min_)
        self.start.setMaximum(max_)
        self.end = QDoubleSpinBox(self)
        self.end.setMinimum(min_)
        self.end.setMaximum(max_)
        self.end.setValue(max_)
        self.start.setSingleStep(step)
        self.end.setSingleStep(step)

        self.start.valueChanged.connect(self.on_value_start_changed)
        self.end.valueChanged.connect(self.on_value_end_changed)

        hlayout.addWidget(self.start)
        hlayout.addWidget(self.end)
        layout.addLayout(hlayout)

        if round_option:
            self.integerCheckBox = QCheckBox("Round to integer values", self)
            layout.addWidget(self.integerCheckBox)

    def on_value_start_changed(self, val):
        if self.end.value() < val:
            self.end.setValue(val)

    def on_value_end_changed(self, val):
        if self.start.value() > val:
            self.start.setValue(val)

    def getMin(self):
        return self.start.value()

    def getMax(self):
        return self.end.value()

    def getRound(self):
        return self.integerCheckBox.isChecked()


class TaskGeneratorDialog(QDialog):
    def __init__(self, nbprocessors):
        QDialog.__init__(self)
        self.layout = QVBoxLayout(self)
        self.taskset = None

        # Utilizations:
        vbox_utilizations = QVBoxLayout()
        group = QGroupBox("Task Utilizations:")

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Generator:", self))
        self.comboGenerator = QComboBox()
        self.comboGenerator.addItem("RandFixedSum")
        self.comboGenerator.addItem("UUniFast-Discard")
        self.comboGenerator.addItem("Kato's method")
        self.comboGenerator.currentIndexChanged.connect(self.generator_changed)
        hbox.addWidget(self.comboGenerator)
        vbox_utilizations.addLayout(hbox)

        # Load slider + spinner:
        hbox_load = QHBoxLayout()
        sld = _DoubleSlider(QtCore.Qt.Horizontal, self)
        sld.setMinimum(0)
        sld.setMaximum(32)
        self.spin_load = QDoubleSpinBox(self)
        self.spin_load.setMinimum(0)
        self.spin_load.setMaximum(32)
        self.spin_load.setSingleStep(0.1)
        hbox_load.addWidget(QLabel("Total utilization: ", self))
        hbox_load.addWidget(sld)
        hbox_load.addWidget(self.spin_load)
        sld.doubleValueChanged.connect(self.spin_load.setValue)
        self.spin_load.valueChanged.connect(sld.setValue)
        self.spin_load.setValue(nbprocessors / 2.)
        vbox_utilizations.addLayout(hbox_load)

        # Number of periodic tasks:
        self.hbox_tasks = QHBoxLayout()
        self.spin_tasks = QSpinBox(self)
        self.spin_tasks.setMinimum(0)
        self.spin_tasks.setMaximum(999)  # That's arbitrary.
        self.hbox_tasks.addWidget(QLabel("Number of periodic tasks: ", self))
        self.hbox_tasks.addStretch(1)
        self.hbox_tasks.addWidget(self.spin_tasks)
        vbox_utilizations.addLayout(self.hbox_tasks)

        # Number of sporadic tasks:
        self.hbox_sporadic_tasks = QHBoxLayout()
        self.spin_sporadic_tasks = QSpinBox(self)
        self.spin_sporadic_tasks.setMinimum(0)
        self.spin_sporadic_tasks.setMaximum(999)  # That's arbitrary.
        self.hbox_sporadic_tasks.addWidget(
            QLabel("Number of sporadic tasks: ", self))
        self.hbox_sporadic_tasks.addStretch(1)
        self.hbox_sporadic_tasks.addWidget(self.spin_sporadic_tasks)
        vbox_utilizations.addLayout(self.hbox_sporadic_tasks)

        # number of custom created task
        self.spin_custom_tasks = {}
        for key in GlobalData.d:
            self.hbox_custom_tasks = QHBoxLayout()
            self.spin_custom_tasks[key] = QSpinBox(self)
            self.spin_custom_tasks[key].setMinimum(0)
            self.spin_custom_tasks[key].setMaximum(999)  # That's arbitrary.
            self.hbox_custom_tasks.addWidget(
                QLabel(f"Number of {key} tasks: ", self))
            self.hbox_custom_tasks.addStretch(1)
            self.hbox_custom_tasks.addWidget(self.spin_custom_tasks[key])
            vbox_utilizations.addLayout(self.hbox_custom_tasks)


        # Min / Max utilizations
        self.hbox_utilizations = QHBoxLayout()
        self.hbox_utilizations.addWidget(QLabel("Min/Max utilizations: ",
                                                self))
        self.interval_utilization = IntervalSpinner(
            self, min_=0, max_=1, step=.01, round_option=False)
        self.hbox_utilizations.addWidget(self.interval_utilization)
        vbox_utilizations.addLayout(self.hbox_utilizations)

        group.setLayout(vbox_utilizations)
        self.layout.addWidget(group)

        # Periods:
        vbox_periods = QVBoxLayout()
        group = QGroupBox("Task Periods:")

        # Log uniform
        self.lunif = QRadioButton("log-uniform distribution between:")
        vbox_periods.addWidget(self.lunif)
        self.lunif.setChecked(True)

        self.lunif_interval = IntervalSpinner(self)
        self.lunif_interval.setEnabled(self.lunif.isChecked())
        self.lunif.toggled.connect(self.lunif_interval.setEnabled)
        vbox_periods.addWidget(self.lunif_interval)

        # Uniform
        self.unif = QRadioButton("uniform distribution between:")
        vbox_periods.addWidget(self.unif)

        self.unif_interval = IntervalSpinner(self)
        self.unif_interval.setEnabled(self.unif.isChecked())
        self.unif.toggled.connect(self.unif_interval.setEnabled)
        vbox_periods.addWidget(self.unif_interval)

        # Discrete
        discrete = QRadioButton("chosen among these (space separated) values:")
        vbox_periods.addWidget(discrete)

        self.periods = QLineEdit(self)
        self.periods.setValidator(QRegExpValidator(
            QRegExp("^\\d*(\.\\d*)?( \\d*(\.\\d*)?)*$")))

        vbox_periods.addWidget(self.periods)
        self.periods.setEnabled(discrete.isChecked())
        discrete.toggled.connect(self.periods.setEnabled)
        vbox_periods.addStretch(1)

        group.setLayout(vbox_periods)
        self.layout.addWidget(group)

        buttonBox = QDialogButtonBox()
        cancel = buttonBox.addButton(QDialogButtonBox.Cancel)
        generate = buttonBox.addButton("Generate", QDialogButtonBox.AcceptRole)
        cancel.clicked.connect(self.reject)
        generate.clicked.connect(self.generate)
        self.layout.addWidget(buttonBox)

        self.show_randfixedsum_options()

    def generator_changed(self, value):
        if value == 2:
            self.show_kato_options()
        else:
            self.show_randfixedsum_options()

    def show_randfixedsum_options(self):
        for i in range(self.hbox_utilizations.count()):
            self.hbox_utilizations.itemAt(i).widget().hide()
        for i in range(self.hbox_tasks.count()):
            if self.hbox_tasks.itemAt(i).widget():
                self.hbox_tasks.itemAt(i).widget().show()
        for i in range(self.hbox_sporadic_tasks.count()):
            if self.hbox_sporadic_tasks.itemAt(i).widget():
                self.hbox_sporadic_tasks.itemAt(i).widget().show()

    def show_kato_options(self):
        for i in range(self.hbox_utilizations.count()):
            if self.hbox_utilizations.itemAt(i).widget():
                self.hbox_utilizations.itemAt(i).widget().show()
        for i in range(self.hbox_tasks.count()):
            if self.hbox_tasks.itemAt(i).widget():
                self.hbox_tasks.itemAt(i).widget().hide()
        for i in range(self.hbox_sporadic_tasks.count()):
            if self.hbox_sporadic_tasks.itemAt(i).widget():
                self.hbox_sporadic_tasks.itemAt(i).widget().hide()

    def get_min_utilization(self):
        return self.interval_utilization.getMin()

    def get_max_utilization(self):
        return self.interval_utilization.getMax()

    def generate(self):

        n = self.get_nb_tasks()
        if (n == 0):
            QMessageBox.warning(
                    self, "Generation failed",
                    "Please check the utilization and the number of tasks.")
            return

        if self.comboGenerator.currentIndex() == 0:
            u = StaffordRandFixedSum(n, self.get_utilization(), 1)
        elif self.comboGenerator.currentIndex() == 1:
            u = UUniFastDiscard(n, self.get_utilization(), 1)
        else:
            u = gen_kato_utilizations(1, self.get_min_utilization(),
                                      self.get_max_utilization(),
                                      self.get_utilization())
            n = len(u[0])

        p_types = self.get_periods()
        if p_types[0] == "unif":
            p = gen_periods_uniform(n, 1, p_types[1], p_types[2], p_types[3])
        elif p_types[0] == "lunif":
            p = gen_periods_loguniform(n, 1, p_types[1], p_types[2],
                                       p_types[3])
        else:
            p = gen_periods_discrete(n, 1, p_types[1])
        
        if u and p:
            self.taskset = gen_tasksets(u, p)[0]
            self.accept()
        elif not u:
            QMessageBox.warning(
                self, "Generation failed",
                "Please check the utilization and the number of tasks!")
        else:
            QMessageBox.warning(
                self, "Generation failed",
                "Pleache check the periods.")

    def get_nb_custom_tasks(self, name):
        return self.spin_custom_tasks[name].value()

    def get_nb_tasks(self):
        s = 0
        for key in GlobalData.d:
            s += self.get_nb_custom_tasks(key)
        return self.spin_tasks.value() + self.spin_sporadic_tasks.value() + s

    def get_nb_periodic_tasks(self):
        return self.spin_tasks.value()

    def get_nb_sporadic_tasks(self):
        return self.spin_sporadic_tasks.value()

    def get_utilization(self):
        return self.spin_load.value()

    def get_periods(self):
        if self.unif.isChecked():
            return ("unif", self.unif_interval.getMin(),
                    self.unif_interval.getMax(), self.unif_interval.getRound())
        elif self.lunif.isChecked():
            return ("lunif", self.lunif_interval.getMin(),
                    self.lunif_interval.getMax(),
                    self.lunif_interval.getRound())
        else:
            return ("discrete", map(float, str(self.periods.text()).split()))

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class TaskCreateDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.txt = ''
        self.layout = QVBoxLayout(self)

        boldFont = QtGui.QFont()
        boldFont.setBold(True)
        h3_title = QLabel("Create Custom Task", self)
        h3_title.setFont(boldFont)
        self.layout.addWidget(h3_title)

        self.layout.addWidget(QLabel('Enter the new task type name:', self))
        self._field_name_edit = QLineEdit(self)
        self._field_name_edit.textChanged.connect(self._text_changed)

        self.layout.addWidget(self._field_name_edit)

        # Add standard dialog buttons
        buttonBox = QDialogButtonBox()
        cancel = buttonBox.addButton(QDialogButtonBox.Cancel)
        ok = buttonBox.addButton(QDialogButtonBox.Ok)

        # Connect the buttons
        cancel.clicked.connect(self.reject)
        ok.clicked.connect(self.accept)

        fields = ['activation_date', 'list_activation_dates', 'period',
                      'deadline', 'wcet', 'acet', 'et_stddev', 'base_cpi', 'n_instr', 'mix', 'sdp', 'preemption_cost']
        self.enabled_fields = []
        for i in range(len(fields)):
            checkbox = QCheckBox(fields[i], self)
            self.layout.addWidget(checkbox)
            checkbox.stateChanged.connect(self.checkbox_state_changed)

        # code zone


        self.codeBox = QTextEdit()
        self.codeBox.setAcceptRichText(False)
        self.codeBox.textChanged.connect(self.on_text_changed)
        self.codeBox.setText(textwrap.dedent(GlobalData.EXAMPLE_CODE))

        self.layout.addWidget(self.codeBox)

        # Add button box to layout
        self.layout.addWidget(buttonBox)

        loadBtn = QPushButton("Load saved task")
        loadBtn.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(loadBtn)

    def on_text_changed(self):
        codeTxt = self.codeBox.toPlainText()    
        if self.txt != '':
            GlobalData.customTaskNameToCode[self.txt] = codeTxt

    def open_file_dialog(self):  
        # Open a file dialog and get the selected file path  
        options = QFileDialog.Options()  
        options |= QFileDialog.ReadOnly  # Open in read-only mode  
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File", "", "All Files (*);;Text Files (*.txt)", options=options)  

        if file_path:  
            # Display the selected file path in the QLineEdit  
            print(file_path)
            with open(file_path, 'r') as file:
                data = json.load(file)
                txt = file_path
                txt = txt[txt.rfind('/')+1:]
                txt = txt[:txt.find('.')]
                self.txt = txt
                self.enabled_fields = data['fields']
                self.accept()
                GlobalData.d[txt] = self.enabled_fields
                if 'code' in data:
                    GlobalData.customTaskNameToCode[txt] = data['code']

    def checkbox_state_changed(self, state):
        print(self.enabled_fields)
        checkbox = self.sender()
        text = checkbox.text()
        if state == 2:
            self.enabled_fields.append(text)
        else:
            self.enabled_fields = list(filter(lambda e: e != text, self.enabled_fields))

        GlobalData.enabled_fields = self.enabled_fields
        GlobalData.d[self.txt] = self.enabled_fields
        

    def _text_changed(self, text):
        self.txt = self._field_name_edit.text()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = TaskGeneratorDialog(5)
    if ex.exec_():
        print(ex.taskset)
