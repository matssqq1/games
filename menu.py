import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QDialog, QLabel
from PyQt5.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setFixedSize(300, 150)  # Уменьшен размер окна настроек

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Центрируем лэйаут

        self.label = QLabel("Выберите режим:")
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

        self.fullscreen_button = QPushButton("Включить на полный экран")
        self.normal_button = QPushButton("Оставить как есть")

        # Устанавливаем стиль кнопок
        self.set_button_style(self.fullscreen_button)
        self.set_button_style(self.normal_button)

        # Устанавливаем ограничения размера кнопок
        self.fullscreen_button.setFixedSize(250, 40)  # Уменьшен размер кнопок
        self.normal_button.setFixedSize(250, 40)

        # Центрируем кнопки и собираем их по близости
        layout.addWidget(self.fullscreen_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.normal_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        # Устанавливаем прозрачный фон окна
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)  # Без рамки окна

        # Подключаем кнопки к функциям
        self.fullscreen_button.clicked.connect(self.enable_fullscreen)
        self.normal_button.clicked.connect(self.keep_normal)

    def set_button_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: #FFEB3B; /* Ярко-жёлтый фон */
                color: black;
                padding: 10px;  /* Уменьшен padding для большей компактности */
                font-size: 16px;  /* Уменьшен размер шрифта */
                border-radius: 5px; /* Скругленные углы */
            }
            QPushButton:hover {
                background-color: #FBC02D; /* Цвет при наведении */
            }
        """)

    def enable_fullscreen(self):
        self.parent().showFullScreen()
        self.parent().settings_button.setText("Настройки экрана")
        self.close()

    def keep_normal(self):
        self.parent().showNormal()
        self.parent().settings_button.setText("Настройки экрана")
        self.close()

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем кнопки
        self.start_button = QPushButton('Начать')
        self.settings_button = QPushButton('Настройки экрана')
        self.exit_button = QPushButton('Выход')

        # Устанавливаем стиль кнопок
        self.set_button_style(self.start_button)
        self.set_button_style(self.settings_button)
        self.set_button_style(self.exit_button)

        # Устанавливаем ограничения размера кнопок
        self.start_button.setFixedSize(250, 40)  # Уменьшен размер кнопок
        self.settings_button.setFixedSize(250, 40)
        self.exit_button.setFixedSize(250, 40)

        # Подключаем кнопку "Exit" к функции выхода 
        self.exit_button.clicked.connect(self.close)

        # Подключаем кнопку "Settings" к функции открытия окна настроек
        self.settings_button.clicked.connect(self.toggle_windows)

        # Создаем вертикальный лэйаут и добавляем кнопки
        layout = QVBoxLayout()
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.settings_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.exit_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        # Устанавливаем прозрачный фон окна
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)  # Без рамки окна

        self.setWindowTitle('My Application')
        self.resize(300, 200)  # Размер окна совпадает с размерами кнопок

        self.settings_dialog = None  # Храним ссылку на диалог настроек

    def set_button_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: #FFEB3B; /* Ярко-жёлтый фон */
                color: black;
                padding: 10px;  /* Уменьшен padding для большей компактности */
                font-size: 16px;  /* Уменьшен размер шрифта */
                border-radius: 5px; /* Скругленные углы */
            }
            QPushButton:hover {
                background-color: #FBC02D; /* Цвет при наведении */
            }
        """)

    def toggle_windows(self):
        if self.settings_dialog is None:
            self.settings_dialog = SettingsDialog(self)
            self.hide()  # Прячем текущее окно
            self.settings_dialog.show()  # Показываем диалог настроек
            
            # Подключаем сигнал, чтобы вернуть основное окно обратно
            self.settings_dialog.finished.connect(self.show_main_window)
        else:
            self.show_main_window()

    def show_main_window(self):
        self.settings_dialog = None  # Сбрасываем ссылку на диалог настроек
        self.show()  # Показываем основное окно

# Запуск приложения
app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
