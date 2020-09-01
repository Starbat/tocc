import os
from logging import getLogger, INFO, Handler
from fbs_runtime.application_context.PyQt5 import (ApplicationContext,
                                                   cached_property)
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QCheckBox)
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from transformer import (TableTransformer, SummaryExtractor,
                         MeasurementExtractor)


class AppContext(ApplicationContext):

    @cached_property
    def gui(self):
        return self.get_resource('gui.ui')

    @cached_property
    def img_folder(self):
        resource = 'images/iconmonstr-folder-9-240.png'
        return QPixmap(self.get_resource(resource))

    @cached_property
    def img_door(self):
        resource = 'images/iconmonstr-door-6-240.png'
        return QPixmap(self.get_resource(resource))

    @cached_property
    def img_arrow(self):
        resource = 'images/iconmonstr-arrow-34-240.png'
        return QPixmap(self.get_resource(resource))

    @cached_property
    def img_check(self):
        resource = 'images/iconmonstr-checkbox-30-240.png'
        return QPixmap(self.get_resource(resource))

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

        # Log feedback to gui
        handler = FeedbackHandler(self.feedback)
        handler.setLevel(INFO)
        self.logger = self.configure_root_logger(handler)

        self.create_column_checkboxes()

        self.inputButton.clicked.connect(self.select_input_file)
        self.outputButton.clicked.connect(self.select_output_folder)
        self.exitButton.clicked.connect(self.close)

        # Configure check boxes
        self.summaries.setChecked(True)
        self.summaries.setEnabled(False)
        self.summaries.toggled.connect(self.disable_if_last_extractor)
        self.measurements.toggled.connect(self.disable_if_last_extractor)

        self.startButton.clicked.connect(self.start)

    def create_column_checkboxes(self):
        for feature in SummaryExtractor().get_features_names():
            c = QCheckBox(feature)
            c.toggled.connect(self.disable_if_last_summary_col)
            c.setChecked(True)
            self.summaryCols.addWidget(c)
        self.summaryCols.setEnabled(False)
        for feature in MeasurementExtractor().get_features_names():
            c = QCheckBox(feature)
            c.toggled.connect(self.disable_if_last_measurement_col)
            c.setChecked(True)
            self.measurementCols.addWidget(c)

    def start(self):
        input_file = self.inputLine.text()
        output_folder = self.outputLine.text()
        extractors = self.get_extractors()
        self.transformer = TableTransformer(input_file, *extractors,
                                            output_dir=output_folder)
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

    def disable_if_last_extractor(self):
        self.disable_if_last_checked_in_layout(self.outputTables)

    def disable_if_last_summary_col(self):
        self.disable_if_last_checked_in_layout(self.summaryCols)

    def disable_if_last_measurement_col(self):
        self.disable_if_last_checked_in_layout(self.measurementCols)

    def disable_if_last_checked_in_layout(self, layout):
        checkboxes = self.get_children(layout)
        boxes_check = {box: box.isChecked() for box in checkboxes}
        if sum(boxes_check.values()) == 1:
            for box, checked in boxes_check.items():
                if checked:
                    box.setEnabled(False)
        else:
            for box, checked in boxes_check.items():
                box.setEnabled(True)

    def configure_root_logger(self, handler):
        logger = getLogger('')
        logger.setLevel(INFO)
        logger.addHandler(handler)
        return logger


class FeedbackHandler(Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)
