import sys
import urllib.request

import bs4 as bs
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi


class Main(QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('scraper_form.ui', self)

        self.pushButton_scrap.clicked.connect(self.scrap)
        self.pushButton_clear.clicked.connect(self.clear)
        self.pushButton_exit.clicked.connect(self.exit)

    def scrap(self):
        try:
            self.label_status.setText('Данные загружаются')
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            self.label_status.setStyleSheet('color: rgb(100, 100, 100); font: bold')
            username = str(self.lineEdit_username.text())
            url = "https://github.com/" + username
            sauce = urllib.request.urlopen(url).read()
            soup = bs.BeautifulSoup(sauce, 'lxml')  # lxml это парсер
            repoNo = int(soup.find('span', class_='Counter').text)
            self.textEdit_info.setText("Количество репозиториев: " + str(repoNo))
            url2 = url + "?tab=repositories"
            sauce = urllib.request.urlopen(url2).read()
            soup = bs.BeautifulSoup(sauce, 'lxml')
            arr = [0]
            tags = soup.find_all('a', itemprop="name codeRepository")
            for tag in tags:
                if tag.text != "":
                    arr.append(tag.text.lstrip())
            k = 2
            while len(arr) <= repoNo:
                url3 = url + "?page=" + str(k) + "&tab=repositories"
                k += 1
                sauce = urllib.request.urlopen(url3).read()
                soup = bs.BeautifulSoup(sauce, 'lxml')
                tags = soup.find_all('a', itemprop="name codeRepository")
                for tag in tags:
                    if tag.text != "":
                        arr.append(tag.text.lstrip())
            for i in range(1, len(arr)):
                h1 = str(i) + ". " + str(arr[i])
                self.textEdit_info.append(h1)
            self.label_status.setText('Данные загружены')
            self.label_status.setStyleSheet('color: rgb(0, 200, 0); font: bold')
            QApplication.restoreOverrideCursor()
        except Exception:
            QApplication.restoreOverrideCursor()
            self.label_status.setText("Введено неверное имя пользователя")
            self.textEdit_info.setText('')
            self.label_status.setStyleSheet('color: rgb(200, 0, 0); font: bold')

    def clear(self):
        self.lineEdit_username.setText('')
        self.textEdit_info.setText('')
        self.label_status.setText('')

    def exit(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
