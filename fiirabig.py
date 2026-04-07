import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QTimeEdit, QWidget,
                                QGridLayout, QPushButton, QLabel, QVBoxLayout,
                                QHBoxLayout, QSpinBox)
from PySide6.QtGui import QKeySequence, QShortcut, QKeyEvent, QPainter, QLinearGradient, QColor, QBrush
from PySide6.QtCore import QTime, Qt, QEvent


class GradientWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#2b2b2b"))
        gradient.setColorAt(1.0, QColor("#1e1e1e"))
        painter.fillRect(self.rect(), QBrush(gradient))


class EnterTimeEdit(QTimeEdit):
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            fake = QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.NoModifier)
            QApplication.sendEvent(self, fake)
        else:
            super().keyPressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fiirabig Poggers v2")
        self.setMinimumWidth(420)

        escQuit = QShortcut(QKeySequence("Escape"), self)
        escQuit.activated.connect(self.close)

        def makeField(labelText, widget):
            lbl = QLabel(labelText)
            box = QVBoxLayout()
            box.setSpacing(5)
            box.addWidget(lbl)
            box.addWidget(widget)
            return box

        self.startIN = EnterTimeEdit()
        self.startIN.setDisplayFormat("HH:mm")
        self.startIN.setTime(QTime(8, 0))

        self.mittagIN = EnterTimeEdit()
        self.mittagIN.setDisplayFormat("HH:mm")
        self.mittagIN.setTime(QTime(12, 0))

        self.pauseIN = QSpinBox()
        self.pauseIN.setValue(30)
        self.pauseIN.setRange(0, 480)
        self.pauseIN.returnPressed.connect(self.calculate)

        self.pensumIN = EnterTimeEdit()
        self.pensumIN.setDisplayFormat("HH:mm")
        self.pensumIN.setTime(QTime(8, 24))

        self.restzeitOUT = QLabel("— h")
        self.restzeitOUT.setObjectName("restzeitOUT")
        self.restzeitOUT.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        restzeitRow = QHBoxLayout()
        restzeitRow.setContentsMargins(12, 0, 12, 0)
        restzeitRow.addWidget(QLabel("Restzeit"))
        restzeitRow.addWidget(self.restzeitOUT)
        restzeitBox = QWidget()
        restzeitBox.setObjectName("restzeitBox")
        restzeitBox.setLayout(restzeitRow)
        restzeitBox.setFixedHeight(46)

        inputGrid = QGridLayout()
        inputGrid.setSpacing(12)
        inputGrid.addLayout(makeField("BEGINN",           self.startIN),  0, 0)
        inputGrid.addLayout(makeField("MITTAG",           self.mittagIN), 0, 1)
        inputGrid.addLayout(makeField("PAUSENDAUER (MIN)", self.pauseIN), 1, 0)
        inputGrid.addLayout(makeField("PENSUM",           self.pensumIN), 1, 1)
        inputGrid.addLayout(makeField("RESTZEIT",         restzeitBox),   2, 0, 1, 2)

        self.ergebnisOUT = QLabel("— h")
        self.ergebnisOUT.setObjectName("ergebnisOUT")
        self.ergebnisOUT.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        ergebnisRow = QHBoxLayout()
        ergebnisRow.setContentsMargins(12, 0, 12, 0)
        ergebnisRow.addWidget(QLabel("Ergebnis"))
        ergebnisRow.addWidget(self.ergebnisOUT)
        ergebnisBox = QWidget()
        ergebnisBox.setObjectName("ergebnisBox")
        ergebnisBox.setLayout(ergebnisRow)
        ergebnisBox.setFixedHeight(52)

        self.calculateButton = QPushButton("Berechnen")
        self.calculateButton.clicked.connect(self.calculate)
        self.calculateButton.setFixedHeight(48)

        titleLabel = QLabel("Fiirabig Poggers")
        titleLabel.setObjectName("title")

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(24, 24, 24, 24)
        mainLayout.setSpacing(12)
        mainLayout.addWidget(titleLabel)
        mainLayout.addSpacing(4)
        mainLayout.addLayout(inputGrid)
        mainLayout.addSpacing(4)
        mainLayout.addWidget(ergebnisBox)
        mainLayout.addWidget(self.calculateButton)

        bg = GradientWidget()
        bg.setLayout(mainLayout)
        self.setCentralWidget(bg)

    def calculate(self):
        startTime    = QTime(0, 0, 0).secsTo(self.startIN.time())
        lunchTime    = QTime(0, 0, 0).secsTo(self.mittagIN.time())
        pauseDuration = self.pauseIN.value() * 60

        workedSoFar = lunchTime - startTime - pauseDuration

        pensum    = self.pensumIN.time()
        pensumSec = QTime(0, 0, 0).secsTo(pensum)
        restSec   = pensumSec - workedSoFar
        maxH, maxM = divmod(abs(restSec) // 60, 60)

        feierabend = QTime(0, 0).addSecs(lunchTime + restSec)
        feierabendStr = feierabend.toString("HH:mm")

        self.restzeitOUT.setText(f"{int(maxH)}h {int(maxM)}min")
        self.ergebnisOUT.setText(f"{feierabendStr} Uhr")

app = QApplication(sys.argv)

app.setStyleSheet("""
    QWidget {
        background: transparent;
        font-family: 'Segoe UI', Arial, sans-serif;
        color: #ffffff;
        font-size: 13px;
    }

    QLabel#title {
        font-size: 20px;
        font-weight: 500;
        color: #ffffff;
        background: transparent;
    }

    QLabel {
        font-size: 11px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.5);
        background: transparent;
        letter-spacing: 0.5px;
    }

    QTimeEdit, QSpinBox {
        background-color: #3a3a3a;
        border: 1px solid #4a4a4a;
        border-radius: 8px;
        padding: 10px 12px;
        font-size: 15px;
        color: #ffffff;
        min-height: 22px;
    }

    QTimeEdit:focus, QSpinBox:focus {
        border-color: #4a80d4;
        background-color: #404040;
    }

    QTimeEdit::up-button, QTimeEdit::down-button,
    QSpinBox::up-button, QSpinBox::down-button {
        width: 18px;
        background: transparent;
        border: none;
    }

    QWidget#restzeitBox {
        background-color: #3a3a3a;
        border: 1px solid #4a4a4a;
        border-radius: 8px;
    }

    QWidget#ergebnisBox {
        background-color: #1a3a5c;
        border: 1px solid #2a5a8c;
        border-radius: 10px;
    }

    QLabel#restzeitOUT {
        font-size: 15px;
        font-weight: 500;
        color: #ffffff;
        background: transparent;
    }

    QLabel#ergebnisOUT {
        font-size: 15px;
        font-weight: 500;
        color: #7ab8f5;
        background: transparent;
    }

    QPushButton {
        background-color: #2a6dd4;
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 14px;
        font-weight: 500;
    }

    QPushButton:hover {
        background-color: #3a7de4;
    }

    QPushButton:pressed {
        background-color: #1a5db4;
    }
""")

window = MainWindow()
window.show()
app.exec()