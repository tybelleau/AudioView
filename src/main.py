import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow


# Creates the application instance
app = QApplication(sys.argv)

# Creates the main window
window = MainWindow()
window.show()

# Starts Qt's event loop
sys.exit(app.exec())