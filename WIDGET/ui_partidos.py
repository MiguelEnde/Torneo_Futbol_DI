# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'partidos.ui'
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
    QTabWidget, QTableWidget, QTableWidgetItem, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(873, 600)
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
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.titulo = QLabel(self.frame_2)
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

        self.btn_nuevo = QPushButton(self.frame_2)
        self.btn_nuevo.setObjectName(u"btn_nuevo")
        font1 = QFont()
        font1.setFamilies([u"Times New Roman"])
        font1.setPointSize(13)
        font1.setBold(True)
        self.btn_nuevo.setFont(font1)

        self.horizontalLayout.addWidget(self.btn_nuevo)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.btn_resultado = QPushButton(self.frame_2)
        self.btn_resultado.setObjectName(u"btn_resultado")
        self.btn_resultado.setFont(font1)

        self.horizontalLayout.addWidget(self.btn_resultado)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.btn_eliminar = QPushButton(self.frame_2)
        self.btn_eliminar.setObjectName(u"btn_eliminar")
        self.btn_eliminar.setFont(font1)

        self.horizontalLayout.addWidget(self.btn_eliminar)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.frame_3)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_calendario = QWidget()
        self.tab_calendario.setObjectName(u"tab_calendario")
        self.verticalLayout_4 = QVBoxLayout(self.tab_calendario)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tabla_partidos = QTableWidget(self.tab_calendario)
        if (self.tabla_partidos.columnCount() < 7):
            self.tabla_partidos.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.tabla_partidos.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tabla_partidos.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tabla_partidos.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tabla_partidos.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tabla_partidos.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tabla_partidos.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tabla_partidos.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tabla_partidos.setObjectName(u"tabla_partidos")

        self.verticalLayout_4.addWidget(self.tabla_partidos)

        self.tabWidget.addTab(self.tab_calendario, "")
        self.tab_eliminatorias = QWidget()
        self.tab_eliminatorias.setObjectName(u"tab_eliminatorias")
        self.verticalLayout_5 = QVBoxLayout(self.tab_eliminatorias)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tree_eliminatorias = QTreeWidget(self.tab_eliminatorias)
        self.tree_eliminatorias.setObjectName(u"tree_eliminatorias")

        self.verticalLayout_5.addWidget(self.tree_eliminatorias)

        self.tabWidget.addTab(self.tab_eliminatorias, "")
        self.tab_resultados = QWidget()
        self.tab_resultados.setObjectName(u"tab_resultados")
        self.verticalLayout_6 = QVBoxLayout(self.tab_resultados)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.tabla_resultados = QTableWidget(self.tab_resultados)
        if (self.tabla_resultados.columnCount() < 6):
            self.tabla_resultados.setColumnCount(6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tabla_resultados.setHorizontalHeaderItem(0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tabla_resultados.setHorizontalHeaderItem(1, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tabla_resultados.setHorizontalHeaderItem(2, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tabla_resultados.setHorizontalHeaderItem(3, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tabla_resultados.setHorizontalHeaderItem(4, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tabla_resultados.setHorizontalHeaderItem(5, __qtablewidgetitem12)
        self.tabla_resultados.setObjectName(u"tabla_resultados")

        self.verticalLayout_6.addWidget(self.tabla_resultados)

        self.tabWidget.addTab(self.tab_resultados, "")

        self.verticalLayout_3.addWidget(self.tabWidget)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 5)

        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.titulo.setText(QCoreApplication.translate("Form", u"Partidos y Eliminatorias", None))
        self.btn_nuevo.setText(QCoreApplication.translate("Form", u"Nuevo Partido", None))
        self.btn_resultado.setText(QCoreApplication.translate("Form", u"Resultado", None))
        self.btn_eliminar.setText(QCoreApplication.translate("Form", u"Eliminar", None))
        ___qtablewidgetitem = self.tabla_partidos.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"ID", None));
        ___qtablewidgetitem1 = self.tabla_partidos.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"FECHA/HORA", None));
        ___qtablewidgetitem2 = self.tabla_partidos.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"EQUIPO LOCAL", None));
        ___qtablewidgetitem3 = self.tabla_partidos.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"EQUIPO VISITANTE", None));
        ___qtablewidgetitem4 = self.tabla_partidos.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"\u00c1RBITRO", None));
        ___qtablewidgetitem5 = self.tabla_partidos.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"ELIMINATORIA", None));
        ___qtablewidgetitem6 = self.tabla_partidos.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"ESTADO", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_calendario), QCoreApplication.translate("Form", u"Calendario", None))
        ___qtreewidgetitem = self.tree_eliminatorias.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"Enfrentamientos", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Eliminatoria", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_eliminatorias), QCoreApplication.translate("Form", u"Cuadro Eliminatorio", None))
        ___qtablewidgetitem7 = self.tabla_resultados.horizontalHeaderItem(0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"FECHA", None));
        ___qtablewidgetitem8 = self.tabla_resultados.horizontalHeaderItem(1)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Form", u"EQUIPO LOCAL", None));
        ___qtablewidgetitem9 = self.tabla_resultados.horizontalHeaderItem(2)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Form", u"RESULTADO", None));
        ___qtablewidgetitem10 = self.tabla_resultados.horizontalHeaderItem(3)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Form", u"EQUIPO VISITANTE", None));
        ___qtablewidgetitem11 = self.tabla_resultados.horizontalHeaderItem(4)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Form", u"ELIMINATORIA", None));
        ___qtablewidgetitem12 = self.tabla_resultados.horizontalHeaderItem(5)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Form", u"\u00c1RBITRO", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_resultados), QCoreApplication.translate("Form", u"Resultados", None))
    # retranslateUi

