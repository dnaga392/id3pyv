import id3
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog


class _Ui_MainWindow(object):
    def setupUi(self, mainwindow):
        if not mainwindow.objectName():
            mainwindow.setObjectName('mainwindow')
        mainwindow.resize(1600, 1200)
        self.centralWidget = QtWidgets.QWidget(mainwindow)
        self.centralWidget.setObjectName('centralWidget')
        self.centralLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.pathWidget = QtWidgets.QWidget(self.centralWidget)
        self.centralLayout.addWidget(self.pathWidget)
        self.pathLayout = QtWidgets.QHBoxLayout(self.pathWidget)
        self.pathEdit = QtWidgets.QLineEdit(self.pathWidget)
        self.pathLayout.addWidget(self.pathEdit)
        self.pathButton = QtWidgets.QPushButton(self.pathWidget)
        self.pathButton.setObjectName('pathButton')
        self.pathLayout.addWidget(self.pathButton)
        self.labelVersion = QtWidgets.QLabel(self.centralWidget)
        self.centralLayout.addWidget(self.labelVersion)
        self.frameTable = QtWidgets.QTableView(self.centralWidget)
        self.centralLayout.addWidget(self.frameTable)
        mainwindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(mainwindow)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def retranslateUi(self, mainwindow):
        mainwindow.setWindowTitle('mp3ed')
        self.pathButton.setText('Open... (&O)')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = _Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.frameTable.setModel(QtGui.QStandardItemModel())

    def setID3(self, id3):
        # バージョンを表示する
        self.ui.labelVersion.setText("ID3v2 version: {0}.{1}".format(*id3.version))
        # タグ情報を表示する
        self.ui.frameTable.model().setRowCount(0)
        self.ui.frameTable.model().setRowCount(len(id3.frames))
        for i, frame in enumerate(id3.frames):
            # 0. Frame ID
            item = QtGui.QStandardItem()
            item.setText(frame.id)
            self.ui.frameTable.model().setItem(i, 0, item)
            # 1. Size
            item = QtGui.QStandardItem()
            item.setText(str(frame.size))
            self.ui.frameTable.model().setItem(i, 1, item)
            # 2. Flags
            flags = [format(x, '08b') for x in frame.flags]
            item = QtGui.QStandardItem(''.join(flags))
            self.ui.frameTable.model().setItem(i, 2, item)
            # 3. Information
            item = QtGui.QStandardItem()
            if frame.id[0] == 'T':
                text_encoding = frame.info[0]
                frame_info = frame.info[1:]
                encoding_map = {'00': 'cp932',
                                '01': 'UTF-16'}
                item.setText(frame_info.decode(encoding_map[format(text_encoding, '02x')]))
            elif frame.id == 'APIC':
                # picture data まで読み飛ばす
                text_encoding = frame.info[0]
                frame_info = frame.info[1:]
                mime_type, frame_info = frame_info.split(int(0).to_bytes(1, 'big'), 1)
                picture_type = frame_info[0]
                frame_info = frame_info[1:]
                description, picture_data = frame_info.split(int(0).to_bytes(1, 'big'), 1)
                # picture data を表示する
                qp = QtGui.QPixmap()
                qp.loadFromData(picture_data)
                item.setData(qp, Qt.DecorationRole)
            self.ui.frameTable.model().setItem(i, 3, item)

    @pyqtSlot(name='on_pathButton_clicked')
    def _on_pathButton_clicked(self):
        fileName = self.ui.pathEdit.text()
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open', fileName)
        if not fileName:
            return
        self.ui.pathEdit.setText(fileName)
        self.setID3(id3.read_raw_id3(fileName))
