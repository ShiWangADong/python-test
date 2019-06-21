
from bs4 import BeautifulSoup
import time
import requests
import json
import re
import os

# 生成文件方法


def downloadFile(name, info):
    filename = '/'.join([folder, name])
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    file = open(filename, 'w', encoding='UTF-8')
    file.write(info)
    file.close()

# 生成远程图片方法


def downloadImage(name, src):
    filename = '/'.join([folder, name])
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    # 获取图片地址
    img_data = requests.get(src).content
    with open(filename, 'wb') as handler:
        handler.write(img_data)

# 生成远程图片方法


def transferName(str):
    result = eval(repr(str).replace('\\', ''))
    result = eval(repr(result).replace('/', ''))
    result = eval(repr(result).replace(' ', ''))
    result = eval(repr(result).replace('.', ''))
    result = eval(repr(result).replace('*', ''))
    result = eval(repr(result).replace('?', ''))
    result = eval(repr(result).replace('>', ''))
    result = eval(repr(result).replace('<', ''))
    result = eval(repr(result).replace('|', ''))
    result = eval(repr(result).replace(',', ''))
    return result


errorInfo = ''
folder = "d:/download/jp/"+time.strftime("%Y%m%d%H%M", time.localtime())
host = "http://jp.myav.tv/"
# 提交的查询参数
params = {
    "s": "藤浦めぐ",
    "t": 1,
    "pageIndex": 1,
    "pageSize": 1000
}
print('start request, params: ',params)
# 提交参数
r = requests.get('http://jp.myav.tv/zh-TW/Search/Product', params=params)
r.encoding = 'UTF-8'
rtext = r.text
print('finish request')
# 获取beautifulsoup 对象
soup = BeautifulSoup(rtext, 'html.parser')
# 每一个item的class name
itemclass = "resultBox"
# title class name
titleclass = "highlightText"
# 获取所有的item
itemResults = soup.find_all('div', itemclass)

for itemSoup in itemResults:
    hrefas = itemSoup.find_all('a')
    hrefimgs = itemSoup.find_all('img')
    # 影片详情地址
    locationhref = host+hrefas[0]['href']
    # 预览图位置
    image_url = 'http:' + hrefimgs[0]['src']
    # 修改为大图
    image_url = image_url.replace('_ch', '_c')
    # 影片名称
    itemName = transferName(hrefas[1].string)
    # 演员名称
    artName = ''
    # 演员影片
    artInfo = ''
    arta = itemSoup.find('a', titleclass)
    if arta != None:
        artName = arta.string
        artInfo = arta['href']
    # 系统编号
    itemNo = ""
    try:
        print('start download : '+itemName)
        itemNo = re.findall(r'(\d{4,})', locationhref)[0]
        # 文本信息
        downloadFile('/'.join([itemName, itemNo+'.txt']), '\n'.join(
            ['片名：'+itemName, '地址：'+locationhref, '演员：'+artName, '简介：'+artInfo]))
        # 图片信息
        downloadImage('/'.join([itemName, itemNo+'.jpg']), image_url)        
        print('finish download : '+itemName)
    except:
        errorInfo = itemNo+' '+itemName+'\n'

# 输出错误信息
downloadFile('error.text',errorInfo)
        
print('success!')
