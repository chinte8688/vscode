# -*- coding:UTF-8 -*-

#导入必要的库
from bs4 import BeautifulSoup #用于解析HTML和XML文档
import requests #用于发送网络请求获取网页
import sys 
import time

# 定义下载器类
class downloader(object):

    # 初始化方法
    def __init__(self):
        self.target = 'view-source:https://m.xszj.org/b/313055/cs/1' #存放所有章节链接的网页
        self.names = [] #用于存储每一章的名称
        self.urls = [] #用于存储每一章的链接
        self.nums = 0 #用于记录总章节数
        
    # 获取所有章节的名称和链接,保存到self.names和self.urls中
    def get_name_address_list(self):
        
        #list_a_bf用于临时存储bs4解析后的节点
        list_a_bf = [] 
        
        #list_a用于存储最终得到的a标签节点列表
        list_a = []
        
        #发送网络请求,获取包含章节列表的网页
        r = requests.get(self.target)
        
        #显式设置文本编码,防止解析错误
        r.encoding = r.apparent_encoding 
        
        #获取网页文本
        html = r.text
        
        # 使用bs4解析网页文本
        div_bf = BeautifulSoup(html, features='html.parser')
        
        #找到所有class为container的div标签
        div = div_bf.find_all('div', class_='box_con')
        #div = div_bf.find_all('div', class_='container') 原來2024/8/6
        #div = div_bf.find_all('div', class_='chaptername')

        #第1、2个div忽略,从第3个开始包含章节信息 
        div = div[2:]
        
        #循环解析每个div容器
        for i in range(len(div)):
            
            #将div转换成bs4对象保存到list_a_bf中
            list_a_bf.append(BeautifulSoup(str(div[i]), features='html.parser'))   
            
            #从bs4对象中查找所有的a标签,保存到list_a中 
            #list_a.append(list_a_bf[i].find_all('a')) 2024/8/6
            list_a.append(list_a_bf[i].find_all('content_1'))    
            
            #累计总章节数
            self.nums += len(list_a[i][:])
            
            #从a标签中提取章节名称和链接
            for each in list_a[i][:]:
                self.names.append(each.string) 
                self.urls.append(each.get('href'))  

    # 根据章节链接url,获取该章节正文内容    
    def get_one_text(self, url_i):
        
        #存储文本内容的变量
        text = ' '  
        
        #发送网络请求,获取该章节链接所指向页面
        r = requests.get(url=url_i)
        
        r.encoding = r.apparent_encoding
        
        html = r.text
        
        #使用bs4解析页面
        html_bf = BeautifulSoup(html, features='html.parser')
        
        #找到正文div容器 
        texts = html_bf.find_all('div', class_='c3')
        #texts = html_bf.find_all('div', class_='post_entry') 2024/8/6
        #texts = html_bf.find_all('div', class_='chaptername')
        #拼接div容器内所有文本 
        for t in texts:
           text += str(t)
           
        #替换、删除多余的HTML标签等
        text = text.replace('<div class="post_entry">', ' ')  
        #text = text.replace('<div class="chaptername">', ' ') 
        text = text.replace('</div>', '\n')
        text = text.replace('<br/>', '\n')
        text = text.replace('<p>', '\n')
        text = text.replace('</p>', '\n')
        text = text.replace('<\p>', '\n')

        #返回解析后的文本
        return text

    # 将单章标题和内容写入文件
    def writer(self, name, path, text):
        
        #打开文件准备写入
        with open(path, 'a', encoding='utf-8') as f:   
            
            #先写入章节名称
            f.write(name + '\n')  
            
            #写入章节内容
            f.writelines(text)
            
            #每章之间空两行
            f.write('\n\n')


if __name__ == "__main__":

    #初始化Downloader
    dl = downloader()  
    
    #获取章节名称和链接列表
    dl.get_name_address_list()
    
    print('《xxx》开始下载: ')
    
    #逐章下载
    for i in range(dl.nums):
        
        #睡0.2秒防止服务器限速
        time.sleep(0.2)
        
        try:
            #保存文件    
            dl.writer(dl.names[i], r'xxx.txt', dl.get_one_text(dl.urls[i]))
            
        except IndexError as e:
            print(repr(e))  
          
        #打印下载进度  
        sys.stdout.write("  已下载:%.3f%%" % float((i/dl.nums)*100) + '\r') 
        #sys.stdout.write('\r' + " 已下载:%.3f%%" % float(i / ss.nums))
        sys.stdout.flush()
        
    print('《XXX》下载完成')