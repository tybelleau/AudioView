
STYLESHEET = """
QWidget#central_widget {
    background-color: #1b1b1b;
}

QWidget#file_section {
    background-color: #2B2B2B;
    border-radius: 4px;
}

QLabel#folder_header {
    padding-left: 6px;
}

QTreeView {
    background-color: rgba(255, 255, 255, 0.00);
    border: 0px solid;
    border-radius: 4px;
    padding: 4px;
    outline: none;
    font-family: "Sora";
    font-size: 9pt;
}

QTreeView::item {
    padding: 2px;
}

QTreeView::item:hover {
    background-color: rgba(255, 255, 255, 0.06);
}

QTreeView::item:selected {
    background-color: rgba(255, 255, 255, 0.10);
    color: white;
}

QPushButton#progress_buttons {
    background: transparent;
    border: none;
    padding: 4px;
}

QPushButton#progress_buttons:hover {
}

QPushButton#progress_buttons:pressed {
}

QSlider#progress_slider {
    background: transparent;
}

QSlider#progress_slider::groove:horizontal {
    height: 3px;
    background: #2B2B2B;
    border-radius: 1px;
}

QSlider#progress_slider::sub-page:horizontal {
    background: #7ebcc4;
    border-radius: 2px;
}

QSlider#progress_slider::handle:horizontal {
    width: 3px;
    height: 14px;
    margin: -6px 0;
    background: #ffffff;
    border: none;
    border-radius: 0px;
}

QSlider#progress_slider::handle:horizontal:hover {
    width: 4px;
    height: 16px;
    margin: -7px 0;
}

"""
