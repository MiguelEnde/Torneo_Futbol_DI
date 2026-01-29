# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'participante.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(900, 600)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_superior = QFrame(self.frame)
        self.frame_superior.setObjectName(u"frame_superior")
        self.frame_superior.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_superior.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_superior.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_superior)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.titulo = QLabel(self.frame_superior)
        self.titulo.setObjectName(u"titulo")
        font = QFont()
        font.setFamilies([u"Times New Roman"])
        font.setPointSize(32)
        font.setBold(True)
        font.setItalic(True)
        self.titulo.setFont(font)

        self.horizontalLayout.addWidget(self.titulo)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_anadir = QPushButton(self.frame_superior)
        self.btn_anadir.setObjectName(u"btn_anadir")
        font1 = QFont()
        font1.setFamilies([u"Times New Roman"])
        font1.setPointSize(13)
        font1.setBold(True)
        self.btn_anadir.setFont(font1)

        self.horizontalLayout.addWidget(self.btn_anadir)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.btn_editar = QPushButton(self.frame_superior)
        self.btn_editar.setObjectName(u"btn_editar")
        self.btn_editar.setFont(font1)

        self.horizontalLayout.addWidget(self.btn_editar)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.btn_eliminar = QPushButton(self.frame_superior)
        self.btn_eliminar.setObjectName(u"btn_eliminar")
        self.btn_eliminar.setFont(font1)

        self.horizontalLayout.addWidget(self.btn_eliminar)


        self.verticalLayout_2.addWidget(self.frame_superior)

        self.frame_contenido = QFrame(self.frame)
        self.frame_contenido.setObjectName(u"frame_contenido")
        self.frame_contenido.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_contenido.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_contenido)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.frame_contenido)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_lista = QWidget()
        self.tab_lista.setObjectName(u"tab_lista")
        self.verticalLayout_4 = QVBoxLayout(self.tab_lista)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tabla_participantes = QTableWidget(self.tab_lista)
        if (self.tabla_participantes.columnCount() < 6):
            self.tabla_participantes.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tabla_participantes.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tabla_participantes.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tabla_participantes.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tabla_participantes.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tabla_participantes.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tabla_participantes.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.tabla_participantes.setObjectName(u"tabla_participantes")

        self.verticalLayout_4.addWidget(self.tabla_participantes)

        self.tabWidget.addTab(self.tab_lista, "")
        self.tab_estadisticas = QWidget()
        self.tab_estadisticas.setObjectName(u"tab_estadisticas")
        self.verticalLayout_5 = QVBoxLayout(self.tab_estadisticas)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_goleadores = QLabel(self.tab_estadisticas)
        self.label_goleadores.setObjectName(u"label_goleadores")
        font2 = QFont()
        font2.setPointSize(14)
        font2.setBold(True)
        self.label_goleadores.setFont(font2)

        self.verticalLayout_5.addWidget(self.label_goleadores)

        self.tabla_goleadores = QTableWidget(self.tab_estadisticas)
        if (self.tabla_goleadores.columnCount() < 3):
            self.tabla_goleadores.setColumnCount(3)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tabla_goleadores.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tabla_goleadores.setHorizontalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tabla_goleadores.setHorizontalHeaderItem(2, __qtablewidgetitem8)
        self.tabla_goleadores.setObjectName(u"tabla_goleadores")

        self.verticalLayout_5.addWidget(self.tabla_goleadores)

        self.label_tarjetas = QLabel(self.tab_estadisticas)
        self.label_tarjetas.setObjectName(u"label_tarjetas")
        self.label_tarjetas.setFont(font2)

        self.verticalLayout_5.addWidget(self.label_tarjetas)

        self.tabla_tarjetas = QTableWidget(self.tab_estadisticas)
        if (self.tabla_tarjetas.columnCount() < 4):
            self.tabla_tarjetas.setColumnCount(4)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tabla_tarjetas.setHorizontalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tabla_tarjetas.setHorizontalHeaderItem(1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tabla_tarjetas.setHorizontalHeaderItem(2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tabla_tarjetas.setHorizontalHeaderItem(3, __qtablewidgetitem12)
        self.tabla_tarjetas.setObjectName(u"tabla_tarjetas")

        self.verticalLayout_5.addWidget(self.tabla_tarjetas)

        self.tabWidget.addTab(self.tab_estadisticas, "")

        self.verticalLayout_3.addWidget(self.tabWidget)


        self.verticalLayout_2.addWidget(self.frame_contenido)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 5)

        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.titulo.setText(QCoreApplication.translate("Form", u"Participantes", None))
        self.btn_anadir.setText(QCoreApplication.translate("Form", u"A\u00f1adir", None))
        self.btn_editar.setText(QCoreApplication.translate("Form", u"Editar", None))
        self.btn_eliminar.setText(QCoreApplication.translate("Form", u"Eliminar", None))
        ___qtablewidgetitem = self.tabla_participantes.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"ID", None));
        ___qtablewidgetitem1 = self.tabla_participantes.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"NOMBRE", None));
        ___qtablewidgetitem2 = self.tabla_participantes.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"CURSO", None));
        ___qtablewidgetitem3 = self.tabla_participantes.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"TIPO", None));
        ___qtablewidgetitem4 = self.tabla_participantes.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"POSICI\u00d3N", None));
        ___qtablewidgetitem5 = self.tabla_participantes.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"ESTAD\u00cdSTICAS", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_lista), QCoreApplication.translate("Form", u"Lista General", None))
        self.label_goleadores.setText(QCoreApplication.translate("Form", u"\U0001f3c6 M\U000000e1ximos Goleadores", None))
        ___qtablewidgetitem6 = self.tabla_goleadores.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"JUGADOR", None));
        ___qtablewidgetitem7 = self.tabla_goleadores.horizontalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"EQUIPO", None));
        ___qtablewidgetitem8 = self.tabla_goleadores.horizontalHeaderItem(2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Form", u"GOLES", None));
        self.label_tarjetas.setText(QCoreApplication.translate("Form", u"\u26a0\ufe0f Tarjetas", None))
        ___qtablewidgetitem9 = self.tabla_tarjetas.horizontalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Form", u"JUGADOR", None));
        ___qtablewidgetitem10 = self.tabla_tarjetas.horizontalHeaderItem(1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Form", u"EQUIPO", None));
        ___qtablewidgetitem11 = self.tabla_tarjetas.horizontalHeaderItem(2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Form", u"AMARILLAS", None));
        ___qtablewidgetitem12 = self.tabla_tarjetas.horizontalHeaderItem(3)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Form", u"ROJAS", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_estadisticas), QCoreApplication.translate("Form", u"Estad\u00edsticas", None))
    # retranslateUi

