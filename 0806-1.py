#ch16_1.py
import requests, bs4

url = 'https://www.uuread.tw/uu1/54478/54478632'
htmlfile = requests.get(url)
print('元編碼 : ',htmlfile.encoding)

objSoup = bs4.BeautifulSoup(htmlfile.text, 'lxml')

#print(type(objSoup),'AAA')
#objtag = objSoup.find('meta' ,content='description')

book_author = objSoup.find('meta',property='og:novel:author')
book_title = objSoup.find('meta',property='og:novel:book_name')
book_description = objSoup.find('meta',property='og:description')
print('作者     :',book_author['content'])
print('書名     :',book_title['content'])
print('內文描述 :', book_description['content'])

print()

url01 = 'https://big5.quanben5.io/n/anhechuan/xiaoshuo.html'
htmlfile01 = requests.get(url01)
print('元編碼 : ',htmlfile.encoding)

objSoup01 = bs4.BeautifulSoup(htmlfile01.text, 'lxml')

#獲取description
#md_desc = objSoup.find('head').find('meta', attrs={'name': 'description'})['content']

#獲取keywords
book_description01 = objSoup.find('head').find('meta', attrs={'name': 'keywords'})

#print(type(objSoup),'AAA')
#objtag = objSoup.find('meta' ,content='description')

#book_author01 = objSoup01.find('meta',property='og:novel:author')
#book_title01 = objSoup01.find('meta',property='og:novel:book_name')
#book_description01 = objSoup01.find('meta',name = 'description')
#book_description01 = objSoup01.find('meta',attrs={'name':'description'})
#print('作者     :',book_author01['content'])
#print('書名     :',book_title01['content'])
print('內文描述 :', book_description01['content'])
print('內文描述 :', book_description01['content'])

