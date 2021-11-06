import sys
# noinspection PyCompatibility
from urllib.request import urlopen  # Для загрузки содержимого страницы с заданного URL

import PyQt6.QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from bs4 import BeautifulSoup as bs


# noinspection PyCompatibility

class Main(PyQt6.QtWidgets.QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('scraper_form.ui', self)

        self.pushButton_scrap.clicked.connect(self.scrap)
        self.pushButton_clear.clicked.connect(self.clear)
        self.pushButton_exit.clicked.connect(self.exit)

    def scrap(self):
        try:
            self.label_status.setText('Данные загружаются')
            PyQt6.QtWidgets.QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            self.label_status.setStyleSheet('color: rgb(100, 100, 100); font: bold')
            username = str(self.lineEdit_username.text())
            url = "https://github.com/" + username
            sauce = urlopen(url).read()
            soup = bs(sauce, 'lxml')  # lxml это парсер
            repo_amount = int(soup.find('span', class_='Counter').text)
            self.textEdit_info.setText("Количество репозиториев: " + str(repo_amount))
            url2 = url + "?tab=repositories"
            sauce = urlopen(url2).read()
            soup = bs(sauce, 'lxml')
            arr = [0]
            tags = soup.find_all('a', itemprop="name codeRepository")
            for tag in tags:
                if tag.text != "":
                    arr.append(tag.text.lstrip())
            k = 2
            while len(arr) <= repo_amount:
                url3 = url + "?page=" + str(k) + "&tab=repositories"
                k += 1
                sauce = urlopen(url3).read()
                soup = bs(sauce, 'lxml')
                tags = soup.find_all('a', itemprop="name codeRepository")
                for tag in tags:
                    if tag.text != "":
                        arr.append(tag.text.lstrip())
            for i in range(1, len(arr)):
                h1 = str(i) + ". " + str(arr[i])
                self.textEdit_info.append(h1)
            self.label_status.setText('Данные загружены')
            self.label_status.setStyleSheet('color: rgb(0, 200, 0); font: bold')
            PyQt6.QtWidgets.QApplication.restoreOverrideCursor()
        except Exception:
            PyQt6.QtWidgets.QApplication.restoreOverrideCursor()
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
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
