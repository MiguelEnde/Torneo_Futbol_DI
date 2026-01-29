# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setMinimumSize(QSize(1000, 700))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_superior = QFrame(self.centralwidget)
        self.frame_superior.setObjectName(u"frame_superior")
        self.frame_superior.setMinimumSize(QSize(0, 80))
        self.frame_superior.setMaximumSize(QSize(16777215, 80))
        self.frame_superior.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_superior.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_superior.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_superior)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.titulo = QLabel(self.frame_superior)
        self.titulo.setObjectName(u"titulo")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(28)
        font.setBold(True)
        font.setItalic(False)
        self.titulo.setFont(font)
        self.titulo.setStyleSheet("color: white; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);")
        self.titulo.setText("⚽ GESTOR DE TORNEO DE FÚTBOL ⚽")

        self.horizontalLayout.addWidget(self.titulo)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_creditos = QPushButton(self.frame_superior)
        self.btn_creditos.setObjectName(u"btn_creditos")
        self.btn_creditos.setMinimumSize(QSize(120, 40))
        self.btn_creditos.setMaximumSize(QSize(150, 50))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(11)
        font1.setBold(True)
        self.btn_creditos.setFont(font1)
        self.btn_creditos.setText("📋 Créditos")

        self.horizontalLayout.addWidget(self.btn_creditos)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.btn_ayuda = QPushButton(self.frame_superior)
        self.btn_ayuda.setObjectName(u"btn_ayuda")
        self.btn_ayuda.setMinimumSize(QSize(120, 40))
        self.btn_ayuda.setMaximumSize(QSize(150, 50))
        self.btn_ayuda.setFont(font1)
        self.btn_ayuda.setText("❓ Ayuda")

        self.horizontalLayout.addWidget(self.btn_ayuda)


        self.verticalLayout.addWidget(self.frame_superior)

        self.frame_medio = QFrame(self.centralwidget)
        self.frame_medio.setObjectName(u"frame_medio")
        self.frame_medio.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_medio.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_medio)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.imagen_principal = QLabel(self.frame_medio)
        self.imagen_principal.setObjectName(u"imagen_principal")
        self.imagen_principal.setMinimumSize(QSize(0, 300))
        self.imagen_principal.setMaximumSize(QSize(16777215, 350))
        self.imagen_principal.setPixmap(QPixmap(u"RESOURCES/img/futbol.png"))
        self.imagen_principal.setScaledContents(True)
        self.imagen_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.imagen_principal)


        self.verticalLayout.addWidget(self.frame_medio)

        self.frame_inferior = QFrame(self.centralwidget)
        self.frame_inferior.setObjectName(u"frame_inferior")
        self.frame_inferior.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_inferior.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_inferior)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame_equipos = QFrame(self.frame_inferior)
        self.frame_equipos.setObjectName(u"frame_equipos")
        self.frame_equipos.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_equipos.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_equipos)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.img_equipos = QLabel(self.frame_equipos)
        self.img_equipos.setObjectName(u"img_equipos")
        self.img_equipos.setPixmap(QPixmap(u"RESOURCES/img/eq.jpg"))
        self.img_equipos.setScaledContents(True)

        self.verticalLayout_3.addWidget(self.img_equipos)

        self.btn_equipos = QPushButton(self.frame_equipos)
        self.btn_equipos.setObjectName(u"btn_equipos")
        self.btn_equipos.setMinimumSize(QSize(0, 50))
        self.btn_equipos.setFont(font1)

        self.verticalLayout_3.addWidget(self.btn_equipos)


        self.horizontalLayout_2.addWidget(self.frame_equipos)

        self.frame_participantes = QFrame(self.frame_inferior)
        self.frame_participantes.setObjectName(u"frame_participantes")
        self.frame_participantes.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_participantes.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_participantes)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.img_participantes = QLabel(self.frame_participantes)
        self.img_participantes.setObjectName(u"img_participantes")
        self.img_participantes.setPixmap(QPixmap(u"RESOURCES/img/par.jpg"))
        self.img_participantes.setScaledContents(True)

        self.verticalLayout_4.addWidget(self.img_participantes)

        self.btn_participantes = QPushButton(self.frame_participantes)
        self.btn_participantes.setObjectName(u"btn_participantes")
        self.btn_participantes.setMinimumSize(QSize(0, 50))
        self.btn_participantes.setFont(font1)

        self.verticalLayout_4.addWidget(self.btn_participantes)


        self.horizontalLayout_2.addWidget(self.frame_participantes)

        self.frame_partidos = QFrame(self.frame_inferior)
        self.frame_partidos.setObjectName(u"frame_partidos")
        self.frame_partidos.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_partidos.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_partidos)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.img_calendario = QLabel(self.frame_partidos)
        self.img_calendario.setObjectName(u"img_calendario")
        self.img_calendario.setPixmap(QPixmap(u"RESOURCES/img/cal.jpg"))
        self.img_calendario.setScaledContents(True)

        self.verticalLayout_5.addWidget(self.img_calendario)

        self.btn_partidos = QPushButton(self.frame_partidos)
        self.btn_partidos.setObjectName(u"btn_partidos")
        self.btn_partidos.setMinimumSize(QSize(0, 50))
        self.btn_partidos.setFont(font1)

        self.verticalLayout_5.addWidget(self.btn_partidos)


        self.horizontalLayout_2.addWidget(self.frame_partidos)

        self.frame_eliminatorias = QFrame(self.frame_inferior)
        self.frame_eliminatorias.setObjectName(u"frame_eliminatorias")
        self.frame_eliminatorias.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_eliminatorias.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_eliminatorias)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.img_eliminatorias = QLabel(self.frame_eliminatorias)
        self.img_eliminatorias.setObjectName(u"img_eliminatorias")
        self.img_eliminatorias.setPixmap(QPixmap(u"RESOURCES/img/eliminatoria.jpg"))
        self.img_eliminatorias.setScaledContents(True)

        self.verticalLayout_6.addWidget(self.img_eliminatorias)

        self.btn_eliminatorias = QPushButton(self.frame_eliminatorias)
        self.btn_eliminatorias.setObjectName(u"btn_eliminatorias")
        self.btn_eliminatorias.setMinimumSize(QSize(0, 50))
        self.btn_eliminatorias.setFont(font1)

        self.verticalLayout_6.addWidget(self.btn_eliminatorias)


        self.horizontalLayout_2.addWidget(self.frame_eliminatorias)


        self.verticalLayout.addWidget(self.frame_inferior)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Gestor de Torneo de Fútbol", None))
        self.titulo.setText(QCoreApplication.translate("MainWindow", u"App Torneo de Fútbol", None))
        self.btn_creditos.setText(QCoreApplication.translate("MainWindow", u"📋 Créditos", None))
        self.btn_ayuda.setText(QCoreApplication.translate("MainWindow", u"❓ Ayuda", None))
        self.imagen_principal.setText("")
        self.img_equipos.setText("")
        self.btn_equipos.setText(QCoreApplication.translate("MainWindow", u"Equipos", None))
        self.img_participantes.setText("")
        self.btn_participantes.setText(QCoreApplication.translate("MainWindow", u"Participantes", None))
        self.img_calendario.setText("")
        self.btn_partidos.setText(QCoreApplication.translate("MainWindow", u"Partidos", None))
        self.img_eliminatorias.setText("")
        self.btn_eliminatorias.setText(QCoreApplication.translate("MainWindow", u"Eliminatorias", None))
    # retranslateUi

