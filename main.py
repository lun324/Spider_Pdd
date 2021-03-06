"""
@author:Administrator
@file:main.py
@time:2020/05/09
"""

import sys

from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from Win_Ui import Ui_Form  # main界面
from Spider import SpiderPdd    # 爬虫
import load_excel   # 文本处理
import ctypes


class Main(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.show_UI()
        self.sp = SpiderPdd()
        self.dia_log = QFileDialog()
        self.excel = load_excel


    def show_UI(self):
        """ 附加UI """
        root = QFileInfo(__file__).absolutePath()
        self.setWindowTitle("拼多多爬虫")
        self.setWindowIcon(QIcon(r'./pdd.ico'))
        self.resize(964, 635)   # 设置尺寸表
        self.setFixedSize(964, 635)     # 设置固定尺寸

    def get_line_url(self):
        """1. 获取用户输入的url"""
        url = self.ui.url_ipt.text()
        url = url.strip()   # 清除空格
        print('main: get_line_url: 成功获取 1 url')
        return url

    def get_save_image_path(self):
        """2. 获取用户输入的保存文件路径"""
        print('main: get_save_image_path: 开始获取保存路径成功')
        save_image_path = self.ui.line_url_save.text()
        save_image_path = r'{}'.format(save_image_path.strip())   # 去除空格并转义
        print('main: get_save_image_path: 正在获取保存路径成功')
        if save_image_path == '':
            QMessageBox.information(self, '提示', '未选择保存路径', QMessageBox.Ok)
            print('main: get_save_image_path: 错误，未选择保存路径')
            raise FileNotFoundError('错误556')
        print('main: get_save_image_path: 获取保存路径成功')
        return save_image_path

    def get_ipt_cookie(self):
        """2-1. 获取用户输入的cookies,没有则不返回"""
        print('main: get_ipt_cookie: 开始获取用户cookie')
        cookie = self.ui.lineEdit.text()
        print('main: get_ipt_cookie: 正在获取用户cookie')
        if cookie == '':
            QMessageBox.information(self, '提示', '未输入cookie', QMessageBox.Ok)
            print('main: get_ipt_cookie: 用户cookie未输入')
            return 0
        print('main: get_ipt_cookie: 获取用户cookie成功')
        return cookie

    def info_image_url(self):
        """3. url 输入有误提示"""
        QMessageBox.information(self, '提示', '图片地址有误已，请重新输入', QMessageBox.Ok)

    def get_excel_path(self):
        """3-2. 用户未输入url,主动抛出导入文件"""
        global name
        try:
            print('main: get_excel_path: 开始获取excel数据')
            filenames = self.dia_log.getOpenFileName(self, 'open file', '../', 'xlsx(*.xlsx)')
            print('main: get_excel_path: 获得表明，开始打开excel数据')
            name = filenames[0]
            name = r'{}'.format(name)
            print('main: get_excel_path: excel数据获取成功')
            return self.get_excel_url(name)
        except FileNotFoundError as e:
            print('main: get_excel_path: 错误， excel数据获失败')
            print(e)
            pass

    def get_excel_url(self, name):
        """3-2-1. 获取单独的url"""
        print('main: get_excel_path: 开始获取真正excel数据')
        item_urls = self.excel.OpenExcel(book_name=name).run()
        print('main: get_excel_path: 成功获取真正excel数据')
        return item_urls

    def start_spider(self, url, save_image_path, cookie):
        """4. 开始爬虫获取图片"""
        print('main: 爬虫开始')
        status = self.sp.run(url=url, path_image=save_image_path, cookie=cookie)
        print('main: 爬虫结束')
        return status

    def save_excel(self, url_status):
        """5. 保存爬取成功的"""
        print('main: save_excel: 开始更改excel信息')
        for i in url_status:
            if i['status'] == 1:
                self.excel.OpenExcel(book_name=name).modify_excel(i['rown'])
                print('main: save_excel: 更改excel信息 成功')
            else:
                print('main: save_excel: 更改excel信息 意外')
                pass

    def run(self):
        try:
            # 1. 获取用户输入的url
            print('main: 开始')
            url = self.get_line_url()
            # 2. 获取用户保存的路径
            print('main: 获取用户输入的保存路径')
            save_image_path = self.get_save_image_path()
            # 2-1. 获取用户输入的cookie
            print('main: 获取cookie')
            cookie = self.get_ipt_cookie()
            if cookie == 0:
                print('main: 用户cookie未输入')
                self.ui.lineEdit.clear()
                print('main: 错误，用户cookie未输入')
                raise FileNotFoundError('错误555')
            else:
                # 3. 如果用户url输入有误，提醒用户重新输入
                if url == '':
                    print('main: 用户未输入url')
                    try:
                        QMessageBox.information(self, '提示', '未添加单个url,将选择导入excel', QMessageBox.Ok)
                        # 3-2, 用户未输入url,主动抛出导入excel表格
                        url_status = []
                        print('main: 获取excel表格数据')
                        item_urls = self.get_excel_path()
                        print('main: 表格数据获取成功，正在清洗，获取单个url')
                        for i in item_urls:
                            url_item = {'编号': '', '名称': '', 'url': '', 'type': '', 'rown': '', 'status': ''}
                            url = i['url']
                            print('main: 开始访问批量 1 url~~~')
                            status = self.start_spider(url=url, save_image_path=save_image_path, cookie=cookie)
                            url_item['编号'] = i['编号']
                            url_item['名称'] = i['名称']
                            url_item['url'] = i['url']
                            url_item['type'] = i['type']
                            url_item['rown'] = i['rown']
                            url_item['status'] = status
                            url_status.append(url_item)

                        self.ui.progressBar.setValue(80)
                        print('main: 开始存入表格')
                        self.save_excel(url_status)
                        print('main: 保存完成')
                        status = 1
                    except Exception as e:
                        print('main: 错误 获取excel失败')
                        print(e)
                        pass
                        status = 2

                elif url[:4] == 'http':
                    # 3-1. 用户输入正确的url,爬虫开始
                    # 4. 爬虫开始
                    self.ui.progressBar.setValue(50)
                    print('main: 开始访问单个url')
                    status = self.start_spider(url=url, save_image_path=save_image_path, cookie=cookie)
                    print('main: 单个url爬虫成功')
                else:
                    # 3-3. 输入错误，需重新输入
                    print('main: 错误，用户url输入错误')
                    self.info_image_url()
                    status = 0

                if status == 1:
                    # 当前图片下载完成
                    print('main: 程序即将结束，完美运行')
                    self.ui.progressBar.setValue(100)
                    QMessageBox.information(self, '提示', '图片已成功下载', QMessageBox.Ok)
                elif status == 2:
                    print('main: 程序即将结束，程序出错')
                    QMessageBox.information(self, '提示', '图片下载失败，请稍后重试', QMessageBox.Ok)
                else:
                    print('main: 用户输入的不是url')
                    self.ui.url_ipt.clear()
        except FileNotFoundError as e:
            print('main: 整体错误')
            print(e)
            pass


if __name__ == '__main__':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("main")
    app = QApplication(sys.argv)
    ma = Main()
    ma.show()
    sys.exit(app.exec_())
