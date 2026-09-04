from PySide6.QtWidgets import QHBoxLayout, QLabel, QTreeView, QMainWindow, QSlider, QVBoxLayout, QWidget, QPushButton, QFileDialog, QFileSystemModel
from PySide6.QtCore import Qt, QDir, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtMultimedia import QMediaPlayer
from file_system_manager import AudioFilterModel, is_supported_audio
from audio_player import AudioPlayer, QMediaPlayer
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AudioView")
        self.resize(900, 700)

        self.current_root_folder = None
        self.current_file = None
        self.current_index = None

        self.audio_player = AudioPlayer()

        self.create_ui()

        self.audio_player.player.playbackStateChanged.connect(self.playback_state_changed)
        self.audio_player.player.positionChanged.connect(self.position_changed)
        self.audio_player.player.durationChanged.connect(self.duration_changed)
        self.progress_slider.sliderMoved.connect(self.seek_audio)
        self.audio_player.player.mediaStatusChanged.connect(self.media_status_changed)

    def playback_state_changed(self, state):
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setText("Pause")

        elif state == QMediaPlayer.PlaybackState.PausedState:
            self.play_button.setText("Play")

        elif state == QMediaPlayer.PlaybackState.StoppedState:
            self.play_button.setText("Play")

    def space_pressed(self, index):
        if self.current_file is not None:
            self.audio_player.toggle_playback()

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Choose Audio Folder"
        )
        if folder:
            self.current_root_folder = folder
            source_index = self.file_model.setRootPath(folder)
            proxy_index = self.audio_filter_model.mapFromSource(source_index)
            self.file_tree.setRootIndex(proxy_index)
            self.folder_header.setText(f"Current Folder: {Path(folder).name}")

    def file_selected(self, current_index, previous_index):
        self.current_index = current_index

        source_index = self.audio_filter_model.mapToSource(current_index)
        file_path = self.file_model.filePath(source_index)

        # checks if file is a supported audio before assigning name and current file
        path = Path(file_path)
        if path.is_file() and is_supported_audio(path):
            self.current_file = file_path
            self.file_name.setText(path.name)
            self.time_label.setText("00:00 / 00:00")
            self.audio_player.play_file(file_path)
        else:
            self.current_file = None
            self.file_name.setText("No file selected")

    # Makes the progress slider advance with the audio
    def position_changed(self, position):
        self.progress_slider.setValue(position)

        duration = self.audio_player.player.duration()

        self.time_label.setText(
            f"{self.format_time(position)} / {self.format_time(duration)}"
        )

    # Matches the length of the slider to the audio
    def duration_changed(self, duration):
        self.progress_slider.setRange(0, duration)

        position = self.audio_player.player.position()

        self.time_label.setText(
                    f"{self.format_time(position)} / {self.format_time(duration)}"
                )

    def seek_audio(self, position):
        self.audio_player.player.seek(position)

    def media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.progress_slider.setValue(0)

    def format_time(self, milliseconds):
        total_seconds = milliseconds // 1000

        minutes = total_seconds // 60
        seconds = total_seconds % 60

        return f"{minutes:02}:{seconds:02}"
    

    def create_ui(self):

        # central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

            # Horizontal layout for the central widget
        central_widget_layout = QHBoxLayout()
        central_widget.setLayout(central_widget_layout)
            # Adds both widgets to the horizontal layout
        file_section = QWidget()
        view_play_section = QWidget()

        central_widget_layout.addWidget(file_section, 1)
        central_widget_layout.addWidget(view_play_section, 2)


        # file section layout
            # sets the vertical layout for the file section
        file_section_layout = QVBoxLayout()
        file_section.setLayout(file_section_layout)
            # adds widgets and text to the file section layout
        explorer_header = QWidget()
        self.folder_header = QLabel("Current folder: No folder selected")
        self.file_tree = AudioTreeView()
        self.file_tree.space_pressed.connect(self.space_pressed)

        self.file_model = QFileSystemModel()
        self.audio_filter_model = AudioFilterModel()
        self.audio_filter_model.setSourceModel(self.file_model)
        self.file_model.setRootPath("")
        self.file_tree.setModel(self.audio_filter_model)
        self.file_tree.setColumnHidden(1, True)
        self.file_tree.setColumnHidden(2, True)
        self.file_tree.setColumnHidden(3, True)
        self.file_tree.header().setStretchLastSection(True)
        self.file_tree.selectionModel().currentChanged.connect(self.file_selected)
        self.file_model.setFilter(
              QDir.AllDirs |
              QDir.NoDotAndDotDot |
              QDir.Files
        )

        file_section_layout.addWidget(explorer_header)
        file_section_layout.addWidget(self.folder_header, alignment=Qt.AlignCenter)
        file_section_layout.addWidget(self.file_tree)


        # file section header layout
            # sets the horizontal layout for the file section header
        explorer_header_layout = QHBoxLayout()
        explorer_header.setLayout(explorer_header_layout)
            # adds label and button to header layout
        explorer_title = QLabel("Explorer")
        choose_folder_button = QPushButton("Choose Folder")

        choose_folder_button.clicked.connect(self.choose_folder)

        explorer_header_layout.addWidget(explorer_title, alignment=Qt.AlignLeft)
        explorer_header_layout.addWidget(choose_folder_button, alignment=Qt.AlignRight)

        # view & play section layout
            # sets the vertical layout for view & play section
        view_play_section_layout = QVBoxLayout()
        view_play_section.setLayout(view_play_section_layout)
            # adds widgets to the vertical layout
        play_section = QWidget()
        view_section = QWidget()

        view_play_section_layout.addWidget(view_section, 9, alignment=Qt.AlignCenter)
        view_play_section_layout.addWidget(play_section, 1)


        # view section Layout
            # sets the vertical layout for the view section
        view_section_layout = QVBoxLayout()
        view_section.setLayout(view_section_layout)
            # adds placeholder text to the view section
        self.file_name = QLabel("No file selected")
        file_waveform = QLabel("Waveform Display Placeholder")  #placeholder for the waveform

        view_section_layout.addWidget(self.file_name,  alignment=Qt.AlignCenter)
        view_section_layout.addWidget(file_waveform, alignment=Qt.AlignCenter)


        # play section layout
            # sets the horizontal layout for the play section
        play_section_layout = QHBoxLayout()
        play_section.setLayout(play_section_layout)
            # adds action buttons to play section layout
        previous_button = QPushButton("Previous")
        previous_button.clicked.connect(self.file_tree.move_previous)
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.audio_player.toggle_playback)
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.file_tree.move_next)
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setRange(0, 0)
        self.time_label = QLabel("00:00 / 00:00")

        play_section_layout.addWidget(previous_button)
        play_section_layout.addWidget(self.play_button)
        play_section_layout.addWidget(next_button)
        play_section_layout.addWidget(self.progress_slider)
        play_section_layout.addWidget(self.time_label)