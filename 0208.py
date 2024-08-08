# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import sys
import time


class downloader(object):

    def __init__(self):
        self.target = "https://big5.quanben5.io/amp/n/anhechuan/xiaoshuo.html"  # 章节页
        self.names = []  # 存放章节名
        self.urls = []  # 存放章节链接
        self.nums = 0  # 章节数

    def get_one_text(self, url_i):

        text = ' '
        r = requests.get(url=url_i)
        r.encoding = r.apparent_encoding

        html = r.text
        html_bf = BeautifulSoup(html, features='html.parser')
        texts = html_bf.find_all('ul', class_='list')
        #texts = html_bf.find_all('div', class_='post_entry')
        for t in texts:
            text += str(t)
        text = text.replace('<li class="c3">', ' ')
        #text = text.replace('<div class="post_entry">', ' ')
        text = text.replace('</li>', '\n')
        text = text.replace('<br/>', '\n')
        text = text.replace('<p>', '\n')
        text = text.replace('</p>', '\n')
        #text = text.replace('<\p>', '\n')

        return text

    def get_name_address_list(self):
        list_a_bf = []
        list_a = []
        r = requests.get(self.target)
        r.encoding = r.apparent_encoding
        html = r.text
        div_bf = BeautifulSoup(html, features='html.parser')
        div = div_bf.find_all('div', class_='c3')
        #div = div_bf.find_all('div', class_='container')
        div = div[2:]
        for i in range(len(div)):
            list_a_bf.append(BeautifulSoup(
                str(div[i]), features='html.parser'))  # div[0]是前100章
            list_a.append(list_a_bf[i].find_all('a'))  # 返回列表
            self.nums += len(list_a[i][:])
            for each in list_a[i][:]:
                self.names.append(each.string)  # string方法返回章节名
                self.urls.append(each.get('href'))  # get（‘href’）返回子地址串
        print(self.names)
        print(self.urls)

    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:  # 打开目标路径文件
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')




if __name__ == "__main__":

    dl = downloader()
    dl.get_name_address_list()
    
    print('《xxx》开始下载: ')
    for i in range(dl.nums):
        time.sleep(0.2)
        try:
            dl.writer(dl.names[i], r'20240209.txt', dl.get_one_text(dl.urls[i]))
        except IndexError as e:
            print(repr(e))
        sys.stdout.write("  已下载:%.3f%%" % float((i/dl.nums)*100) + '\r')
        sys.stdout.flush()
    print('《XXX》下载完成')
