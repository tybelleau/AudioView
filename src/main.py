import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QListWidget, QMainWindow, QProgressBar, QVBoxLayout, QWidget, QPushButton

def button_clicked():
    print("Button clicked!")

# Creates the application instance
app = QApplication(sys.argv)

# Creates the main window
window = QMainWindow()

# central widget and layout
central_widget = QWidget()
window.setCentralWidget(central_widget)

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
folder_header = QLabel("Current Folder: /path/to/folder")  # placeholder for the folder path
file_explorer = QListWidget()
file_section_layout.addWidget(explorer_header)
file_section_layout.addWidget(folder_header, alignment=Qt.AlignCenter)
file_section_layout.addWidget(file_explorer)

# file section header layout
    # sets the horizontal layout for the file section header
explorer_header_layout = QHBoxLayout()
explorer_header.setLayout(explorer_header_layout)
    # adds label and button to header layout
explorer_title = QLabel("Explorer")
choose_folder_button = QPushButton("Choose Folder")
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
file_name = QLabel("File Name: example.wav")    # placeholder for the file name
file_waveform = QLabel("Waveform Display Placeholder")  #placeholder for the waveform
view_section_layout.addWidget(file_name,  alignment=Qt.AlignCenter)
view_section_layout.addWidget(file_waveform, alignment=Qt.AlignCenter)

# play section layout
    # sets the horizontal layout for the play section
play_section_layout = QHBoxLayout()
play_section.setLayout(play_section_layout)
    # adds action buttons to play section layout
previous_button = QPushButton("Previous")
play_button = QPushButton("Play")
next_button = QPushButton("Next")
progress_bar = QProgressBar()
play_section_layout.addWidget(previous_button)
play_section_layout.addWidget(play_button)
play_section_layout.addWidget(next_button)
play_section_layout.addWidget(progress_bar)

window.setWindowTitle("AudioView")
window.resize(900, 700)
window.show()

# Starts Qt's event loop
sys.exit(app.exec())