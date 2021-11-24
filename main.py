import sys

import requests  # Для загрузки содержимого страницы с заданного URL
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from bs4 import BeautifulSoup  # Для навигации по HTML-разметке страницы


class Main(QtWidgets.QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('scraper_form.ui', self)  # Загрузка пользовательского интерфейса

        # Привязка кнопок к методам при нажатии
        self.pushButton_scrap.clicked.connect(self.scrap)
        self.pushButton_clear.clicked.connect(self.clear)
        self.pushButton_exit.clicked.connect(self.exit)

    def scrap(self):
        try:
            QtWidgets.QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)  # Изменение формы курсора
            self.label_status.setStyleSheet('color: rgb(100, 100, 100); bold')  # Установка стиля (цвета и жариности)
            username = str(self.lineEdit_username.text())
            # Ссылка на страницу с репозиториями пользователя
            user_repositories = 'https://github.com/' + username + "?tab=repositories"
            sauce = requests.get(user_repositories)  # Метод get() отправляет GET-запрос на указанный url.
            soup = BeautifulSoup(sauce.text, 'lxml')  # lxml это парсер
            # Возврат содержимого из компонента разметки "span" и класса "Counter"
            repo_amount = int(soup.find('span', class_='Counter').text)
            self.textEdit_info.setText("Количество репозиториев: " + str(repo_amount))
            repo_arr = [0]
            #  Находит все компоненты <a>, со свойством itemprop="name codeRepository"
            tags = soup.find_all('a', itemprop="name codeRepository")
            while len(repo_arr) <= repo_amount:
                for tag in tags:
                    repo_arr.append(tag.text.lstrip())  # Убирает лишние пробелы и переносы строк слева от тэгов
            for i in range(1, len(repo_arr)):
                header = str(i) + ". " + str(repo_arr[i])
                self.textEdit_info.append(header)
            self.label_status.setText("Данные загружены")
            self.label_status.setStyleSheet('color: rgb(0, 200, 0); font: bold')
            QtWidgets.QApplication.restoreOverrideCursor()
        except Exception:
            QtWidgets.QApplication.restoreOverrideCursor()
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
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
