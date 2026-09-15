from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QTreeView, QMainWindow, QSlider, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PySide6.QtCore import Qt, QDir, Signal, QSize
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QMediaPlayer
from file_system_manager import AudioFilterModel, is_supported_audio, AudioFileSystemModel
from audio_player import AudioPlayer
from waveform_widget import WaveformWidget
from waveform_generator import WaveformGenerator
from pathlib import Path

class AudioTreeView(QTreeView):
    space_pressed = Signal(object)

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            current_index = self.currentIndex()

            if event.key() == Qt.Key_Up:
                previous_folder = self.find_previous_folder(current_index)

                if previous_folder is not None:
                    self.setCurrentIndex(previous_folder)

                return

            if event.key() == Qt.Key_Down:
                next_folder = self.find_next_folder(current_index)

                if next_folder is not None:
                    self.setCurrentIndex(next_folder)

                return

        if event.key() == Qt.Key_Space:
            current_index = self.currentIndex()

            source_index = self.model().mapToSource(current_index)
            is_dir = self.model().sourceModel().isDir(source_index)

            if is_dir:
                if self.isExpanded(current_index):
                    self.collapse(current_index)
                else:
                    self.expand(current_index)

                return

            self.space_pressed.emit(current_index)
            return

        super().keyPressEvent(event)

    def find_next_folder(self, index):
        next_index = self.indexBelow(index)

        while next_index.isValid():
            source_index = self.model().mapToSource(next_index)
            source_model = self.model().sourceModel()

            if source_model.isDir(source_index):
                return next_index

            next_index = self.indexBelow(next_index)

        return None

    def find_previous_folder(self, index):
        previous_index = self.indexAbove(index)

        while previous_index.isValid():
            source_index = self.model().mapToSource(previous_index)
            source_model = self.model().sourceModel()

            if source_model.isDir(source_index):
                return previous_index

            previous_index = self.indexAbove(previous_index)

        return None

    def move_next(self):
        current_index = self.currentIndex()
        next_index = self.indexBelow(current_index)
        source_model = self.model().sourceModel()

        while next_index.isValid():
            source_index = self.model().mapToSource(next_index)

            if not source_model.isDir(source_index):
                self.setCurrentIndex(next_index)
                return

            next_index = self.indexBelow(next_index)

    def move_previous(self):
        current_index = self.currentIndex()
        previous_index = self.indexAbove(current_index)
        source_model = self.model().sourceModel()

        while previous_index.isValid():
            source_index = self.model().mapToSource(previous_index)

            if not source_model.isDir(source_index):
                self.setCurrentIndex(previous_index)
                return

            previous_index = self.indexAbove(previous_index)