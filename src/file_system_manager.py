from pathlib import Path
from PySide6.QtCore import QSortFilterProxyModel

SUPPORTED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".aac",
    ".m4a"
}

def is_supported_audio(file_path):
    return file_path.suffix.lower() in SUPPORTED_EXTENSIONS

def folder_contains_audio(folder_path):
    try:
        for path in folder_path.rglob("*"):
            if path.is_file() and is_supported_audio(path):
                return True
    except OSError:
        return False

    return False

def get_audio_files(folder_path):
    audio_files = []

    for path in folder_path.rglob("*"):
        if path.is_file() and is_supported_audio(path):
            audio_files.append(path)

    return sorted(audio_files)

class AudioFilterModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, source_row, source_parent):
        source_model = self.sourceModel()

        index = source_model.index(
            source_row,
            0,
            source_parent
        )

        path = Path(source_model.filePath(index))

        if path.is_file():
            return is_supported_audio(path)

        if path.is_dir():
            return folder_contains_audio(path)

        return False