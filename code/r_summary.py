# coding: utf-8
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import os
import svm
import numpy as np



current_directory = os.path.dirname(os.path.abspath(__file__))
summ_form, base_class = loadUiType(os.path.join(current_directory, 'mainwindow.ui'))
class MainWindow(QMainWindow, summ_form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center()) # Center Display
        self._scan_threadpool = QThreadPool()

    @pyqtSlot()
    def on_pushButton_open_clicked(self):
        """训练集打开文件夹，文件路径显示到lineEdit中"""

        fileName1, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./", "All Files (*);;Text Files (*.txt)")
        # 设置文件扩展名过滤,注意用双分号间隔
        if fileName1:
            self.lineEdit_open.setText(fileName1)
            self.business = np.load(fileName1)
            self.lineEdit_open.setStyleSheet('color: black')
            self.label_load.setText("Data loading has completed, here contains " + str(len(self.business)) + " products.")
            self.lineEdit_select.setText("Please enter the product number！(1 - " + str(len(self.business)) + ")")
            self.lineEdit_select.setStyleSheet('color: red')
            self.label_load.setStyleSheet('font: 75 12pt "Times New Roman" ')

        else:
            self.lineEdit_open.setText("None")

    @pyqtSlot()
    def on_pushButton_select_clicked(self):

        if self.lineEdit_open.text() and self.lineEdit_open.text() != "None":
            index = int(self.lineEdit_select.text())
            self.textEdit_summary.setText("")
            self.textEdit_review.setText("")
            if index >= 1 and index <= len(self.business):
                self.product = self.business[index]
                self.textEdit_review.setText(self.product.reviews[0].text)
                self.label_review_number.setText("0/" + str(len(self.product.reviews[0].text)))
                self.review_index = 0

            else:
                self.lineEdit_select.setText("Input error, Please enter the product number！(1 - " + str(len(self.business)) + ")")
                self.lineEdit_select.setStyleSheet('font: 75 12pt "Times New Roman" ')
                self.lineEdit_select.setStyleSheet('color: red')

        else:
            self.lineEdit_select.setText("Please load the data first！")
            self.lineEdit_select.setStyleSheet('font: 75 12pt "Times New Roman" ')
            self.lineEdit_select.setStyleSheet('color: red')


    @pyqtSlot()
    def on_pushButton_previous_clicked(self):
        if self.product != "None":
            self.review_index = max(0, self.review_index - 1)
            self.textEdit_review.setText(self.product.reviews[self.review_index].text)
            self.label_review_number.setText(str(self.review_index) + "/" + str(len(self.product.reviews[0].text)))
        else:
            self.lineEdit_select.setText("hahaha")
            self.lineEdit_select.setStyleSheet('font: 75 12pt "Times New Roman" ')
            self.lineEdit_select.setStyleSheet('color: red')



    @pyqtSlot()
    def on_pushButton_next_clicked(self):
        if self.product:
            self.review_index = min(len(self.product.reviews), self.review_index + 1)
            self.textEdit_review.setText(self.product.reviews[self.review_index].text)
            self.label_review_number.setText(str(self.review_index) + "/" + str(len(self.product.reviews[0].text)))
        else:
            self.lineEdit_select.setText("hahaha")
            self.lineEdit_select.setStyleSheet('font: 75 12pt "Times New Roman" ')
            self.lineEdit_select.setStyleSheet('color: red')

    @pyqtSlot()
    def on_pushButton_show_summary_clicked(self):
        if self.product:

            V = np.load('../data/vocab.txt')
            res = svm.svm_predict(self.product, V)
            self.textEdit_summary.setText(res)
        else:
            self.lineEdit_select.setText("hahaha")
            self.lineEdit_select.setStyleSheet('font: 75 12pt "Times New Roman" ')
            self.lineEdit_select.setStyleSheet('color: red')




if __name__ == "__main__":

    app = QApplication(sys.argv)
    scanform = MainWindow()
    scanform.show()
    sys.exit(app.exec_())
