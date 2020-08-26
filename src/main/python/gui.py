import os
from fbs_runtime.application_context.PyQt5 import (ApplicationContext,
                                                   cached_property)
from PyQt5.QtWidgets import (QMainWindow, QFileDialog)
from PyQt5 import QtSvg, uic
from table_transformer import TableTransformer, get_extractors


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

        self.statusBar().showMessage('Ready')
        self.inputButton.clicked.connect(self.select_input_file)
        self.outputButton.clicked.connect(self.select_output_folder)
        self.exitButton.clicked.connect(self.close)

        # Configure check boxes
        self.summaries.setChecked(True)
        self.summaries.setEnabled(False)
        self.summaries.toggled.connect(self.disable_if_last)
        self.measurements.toggled.connect(self.disable_if_last)

        self.startButton.clicked.connect(self.start)

    def start(self):
        input_file = self.inputLine.text()
        output_folder = self.outputLine.text()
        if not os.path.isfile(input_file):
            self.statusBar().showMessage('No valid input file!')
        elif not os.path.isdir(output_folder):
            self.statusBar().showMessage('No valid output directory!')
        else:
            extractors = get_extractors(
                                    measurements=self.measurements.isChecked(),
                                    summaries=self.summaries.isChecked())
            self.transformer = TableTransformer(input_file, *extractors)
            self.transformer.run()

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
