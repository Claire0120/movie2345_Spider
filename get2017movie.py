# -*- coding:utf-8 -*-
#Created on 2017.3.13
import re
import urllib
import urllib2
import zope.interface
import w3lib
import xlwt
from bs4 import BeautifulSoup
import lxml
from _codecs import encode
from attr import attrs
from twisted.test.process_getenv import items
from warnings import catch_warnings
from selenium import  webdriver

class Item(object):
    movieName = None
    movieScore = None
    movieStarring =None
    
    
    
class get2017movie(object):
    def __init__(self):
        self.urlBase = 'http://dianying.2345.com/list/----2017---1.html'
        self.pages = self.getPages()
        self.urls = []
        self.items = []
        self.getUrls(self.pages)
        self.spider(self.urls)
        self.pipelines(self.items)
    #�õ�ÿһҳ����ַ��ͨ���ı�pn�������
    
    def getPages(self):
        htmlcontent = self.getResponseContent(self.urlBase)
        soup = BeautifulSoup(htmlcontent,'lxml')
        tag = soup.find('div', attrs = {'class':'v_page'})
        pageNum = tag.find_all('a')
        print '获取页数成功~~~~'
        return pageNum[-2].get_text()
    
    
    def getUrls(self,pageSum):
        ul = self.urlBase.split('---')
        for i in range(1,int(pageSum)+1):
            ul[-1] = str(i) + '.html'
            url = '---'.join(ul)
            self.urls.append(url)
        print 'urls获取成功~~~~~'
    
    
    
    def spider(self,urls):
        for url in urls:
            htmlContent = self.getResponseContent(url)
            soup = BeautifulSoup(htmlContent,'lxml')
            tagsul = soup.find('ul',attrs = {'class':'v_picTxt pic180_240 clearfix'})
            tagsli = tagsul.find_all('li')
            for tag in tagsli:
                item = Item()   #����һ����Ϣ��
#                 print tag
                try:
                    item.movieName = tag.find('span',attrs = {'class':'sTit'}).get_text().strip()
                    item.movieScore = tag.find('span',attrs  = {'class':'pRightBottom'}).em.get_text()
                    item.movieStarring = tag.find('span',attrs = {'class':'sDes'}).get_text().replace(u'主演：', '')
                    self.items.append(item)
                    print '成功获取'+item.movieName+'的数据~~~~~'
                except:
                    print '获取失败！！'
    
    
    #
    def pipelines(self,items):
        fileName = u'2017movie.txt'.encode('GBK')
        with open(fileName,'w') as fp:
            for item in items:
                fp.write('%s \t %s \t %s \r\n' %(item.movieName,item.movieScore,item.movieStarring))
                print '成功将'+item.movieName+'存进txt~~~~~'
                
                
                
    def getResponseContent(self,url):
        try:
            response = urllib2.urlopen(url,encode('utf-8'))
        except:
            print '连接失败'
        else :
            print '连接成功'
            return response.read()
        
           
if __name__ == '__main__':
    movie = get2017movie()