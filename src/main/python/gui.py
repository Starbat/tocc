import os
from fbs_runtime.application_context.PyQt5 import (ApplicationContext,
                                                   cached_property)
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QCheckBox)
from PyQt5 import QtSvg, uic
from transformer import TableTransformer, SummaryExtractor, MeasurementExtractor


class AppContext(ApplicationContext):

    @cached_property
    def gui(self):
        return self.get_resource('gui.ui')

    @cached_property
    def img_folder(self):
        resource = 'images/iconmonstr-folder-9.svg'
        return QtSvg.QSvgWidget(self.get_resource(resource))

    @cached_property
    def img_door(self):
        resource = 'images/iconmonstr-door-6.svg'
        return QtSvg.QSvgWidget(self.get_resource(resource))

    @cached_property
    def img_arrow(self):
        resource = 'images/iconmonstr-arrow-34.svg'
        return QtSvg.QSvgWidget(self.get_resource(resource))

    @cached_property
    def main_window(self):
        return MainWindow(self)

    def run(self):
        self.app.setStyle('Fusion')
        self.main_window.show()
        return self.app.exec_()


class MainWindow(QMainWindow):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        uic.loadUi(ctx.gui, self)
        self.create_column_checkboxes()

        self.statusBar().showMessage('Ready')
        self.inputButton.clicked.connect(self.select_input_file)
        self.outputButton.clicked.connect(self.select_output_folder)
        self.exitButton.clicked.connect(self.close)

        # Configure check boxes
        self.summaries.setChecked(True)
        self.summaries.setEnabled(False)
        self.summaries.toggled.connect(self.disable_if_last)
        self.summaries.toggled.connect(self.depending_summary_checkboxes)
        self.measurements.toggled.connect(self.disable_if_last)
        self.measurements.toggled.connect(self.depending_measurement_checkboxes)
        self.startButton.clicked.connect(self.start)

    def create_column_checkboxes(self):
        for feature in SummaryExtractor().get_features_names():
            c = QCheckBox(feature)
            c.setChecked(True)
            self.summaryCols.addWidget(c)
        self.summaryCols.setEnabled(False)
        for feature in MeasurementExtractor().get_features_names():
            c = QCheckBox(feature)
            c.setChecked(True)
            c.setEnabled(False)
            self.measurementCols.addWidget(c)

    def start(self):
        input_file = self.inputLine.text()
        output_folder = self.outputLine.text()
        if not os.path.isfile(input_file):
            self.statusBar().showMessage('No valid input file!')
        elif not os.path.isdir(output_folder):
            self.statusBar().showMessage('No valid output directory!')
        else:
            extractors = self.get_extractors()
            self.transformer = TableTransformer(input_file, *extractors)
            self.transformer.run()

    def get_children(self, layout):
        children = []
        for i in range(0, layout.count()):
            children.append(layout.itemAt(i).widget())
        return children

    def get_extractors(self):
        extractors = []
        if self.measurements.isChecked():
            me = MeasurementExtractor()
            checkboxes = self.get_children(self.measurementCols)
            print(checkboxes)
            selected_cols = [c.text() for c in checkboxes if c.isChecked()]
            me.select_cols(selected_cols)
            extractors.append(me)
        if self.summaries.isChecked():
            se = SummaryExtractor()
            checkboxes = self.get_children(self.summaryCols)
            selected_cols = [c.text() for c in checkboxes if c.isChecked()]
            se.select_cols(selected_cols)
            extractors.append(se)
        return extractors

    def select_input_file(self):
        path = QFileDialog.getOpenFileName(self, 'Select File')
        if path[0]:
            self.inputLine.setText(path[0])
        if self.outputLine.text() == '':
            self.outputLine.setText(os.path.dirname(path[0]))

    def select_output_folder(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if path:
            self.outputLine.setText(path)

    def disable_if_last(self):
        if self.summaries.isChecked() and not self.measurements.isChecked():
            self.summaries.setEnabled(False)
        elif self.measurements.isChecked() and not self.summaries.isChecked():
            self.measurements.setEnabled(False)
        elif self.summaries.isChecked() and self.measurements.isChecked():
            self.summaries.setEnabled(True)
            self.measurements.setEnabled(True)

    def depending_summary_checkboxes(self):
        children = self.get_children(self.summaryCols)
        if not self.summaries.isChecked():
            for c in children:
                c.setEnabled(False)
        else:
            for c in children:
                c.setEnabled(True)

    def depending_measurement_checkboxes(self):
        children = self.get_children(self.measurementCols)
        if not self.measurements.isChecked():
            for c in children:
                c.setEnabled(False)
        else:
            for c in children:
                c.setEnabled(True)
