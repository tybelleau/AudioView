import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QPalette, QColor, QFontDatabase, QFont
from pathlib import Path
from main_window import MainWindow
from styles import STYLESHEET

BASE_DIR = Path(__file__).resolve().parent.parent
FONT_DIR = BASE_DIR / "assets" / "fonts" / "Sora" / "static"


# Creates the application instance
app = QApplication(sys.argv)

QFontDatabase.addApplicationFont(
    str(FONT_DIR / "Sora-Light.ttf")
)

app.setFont(QFont("Sora", 9))
palette = app.palette()
palette.setColor(QPalette.Accent, QColor("#7ebcc4"))
app.setPalette(palette)
app.setWindowIcon(QIcon(str(BASE_DIR / "assets" / "icons" / "wavemap_logo.ico")))

app.setStyleSheet(STYLESHEET)

# Creates the main window
window = MainWindow()
window.show()

# Starts Qt's event loop
sys.exit(app.exec())