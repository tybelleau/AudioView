from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtCore import Qt, Signal


class WaveformWidget(QWidget):
    seek_requested = Signal(int)

    def __init__(self):
        super().__init__()

        self.waveform = []
        self.playback_position = 0
        self.duration = 0

        self.setFixedSize(500, 200)

    def set_waveform(self, waveform):
        self.waveform = waveform
        self.update()

    def set_playback_position(self, position, duration):
        self.playback_position = position
        self.duration = duration
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.duration > 0:
            position = int(
                (event.position().x() / self.width()) * self.duration
            )

            self.seek_requested.emit(position)

        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)

        try:
            painter.setRenderHint(QPainter.Antialiasing)

            waveform_pen = QPen(QColor("#696969"))
            waveform_pen.setWidth(2)
            position_pen = QPen(QColor("#7ebcc4"))

            if not self.waveform:
                return

            center_y = self.height() / 2
            half_height = self.height() / 2
            width = self.width()

            painter.setPen(waveform_pen)

            for x in range(width):
                waveform_index = int(
                    x * len(self.waveform) / width
                )

                minimum, maximum = self.waveform[waveform_index]

                top = center_y - (maximum * half_height)
                bottom = center_y - (minimum * half_height)

                painter.drawLine(
                    x,
                    int(top),
                    x,
                    int(bottom)
                )

            if self.duration > 0:
                position_x = (
                    self.playback_position / self.duration
                ) * width

                painter.setPen(position_pen)

                painter.drawLine(
                    int(position_x),
                    0,
                    int(position_x),
                    self.height()
                )

        finally:
            painter.end()