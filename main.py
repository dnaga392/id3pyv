import sys
from PyQt5 import QtWidgets
from mainwindow import MainWindow


def _main(argv):
    app = QtWidgets.QApplication(argv)
    m = MainWindow()
    m.show()
    # id3 = read_raw_id3(path)
    # m.setID3(id3)
    return app.exec_()


if __name__ == '__main__':
    # import locale
    # print(locale.getdefaultlocale())
    # When 'Language for non-Unicode programs' is 'English (United States)', => ('ja_JP', 'cp1252')
    # When 'Language for non-Unicode programs' is 'Japanese (Japan)', => ('ja_JP', 'cp932')

    # test_easy_id3()
    # test_id3()
    # id3 = read_raw_id3(path)
    sys.exit(_main(sys.argv))
