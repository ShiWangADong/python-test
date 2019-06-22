
from bs4 import BeautifulSoup
import time
import requests
import json
import re
import os
import argparse
import threading
import threadpool  #线程池

# Create ArgumentParser() object
parser = argparse.ArgumentParser()

# Add argument
parser.add_argument('--s', required=True, type=str, help='search key')
parser.add_argument('--t', type=int, default=1, help='search type')
parser.add_argument('--index', type=int, default=1, help='page index')
parser.add_argument('--size', type=int, default=500, help='page size')

# Parse argument
args = parser.parse_args()

errorInfo = ''
folder = "d:/download/jp/" + args.s

# 判断文件夹是否存在
def createFolder(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


# 追加内容到文件
def appendFile(filename, info):
    with open(filename, "a", encoding='UTF-8') as myfile:
        myfile.write(info)


# 生成远程图片方法
def downloadImage(filename, src, infoPrefix):
    try:
        start = time.time()
        # 获取图片地址
        img_data = requests.get(src).content
        with open(filename, 'wb') as handler:
            handler.write(img_data)
            end = time.time()
            print(infoPrefix, ' cost :', end - start, 's')
    except:        
        appendFile('/'.join([folder,'error.txt']), itemNo + ' ' + itemName + '\n')


def threadDownloadImage(filePath, image_url, infoPrefix):
    t = threading.Thread(target=downloadImage,
                         args=(filePath, image_url, infoPrefix))
    t.setDaemon(True)
    t.start()
    t.join()


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

# 如果已经存在表示已经查找过
if os.path.exists(folder):
    print(args.s, ' ', '已经查找过')
    # exit()

# 创建主目录
createFolder(folder)

# 提交的查询参数
params = {
    "s": args.s,
    "t": args.t,
    "pageIndex": args.index,
    "pageSize": args.size
}

poolParams=[]


host = "http://jp.myav.tv/"

print('start request, params: ', params)

start = time.time()
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

for index, itemSoup in enumerate(itemResults):
    hrefas = itemSoup.find_all('a')
    hrefimgs = itemSoup.find_all('img')
    # 影片详情地址
    locationhref = host + hrefas[0]['href']
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
        artInfo = host + arta['href']
    # 系统编号
    itemNo = ""
    try:
        indexStr = str(index + 1).rjust(4, '0')
        infoPrefix = indexStr + '、处理完成: ' + itemName
        itemNo = re.findall(r'(\d{4,})', locationhref)[0]

        # 追加影片信息
        currentInfo = (indexStr + '、' + '\n      '.join([
            '片名：' + itemName, '地址：' + locationhref, '演员：' + artName,
            '演员简介：' + artInfo
        ]) + '\n')
        appendFile('/'.join([folder,'download.txt']), currentInfo)

        # 图片地址
        imgFolder = '/'.join([folder, 'view'])
        filePath = '/'.join([imgFolder, itemNo + '.jpg'])
        createFolder(imgFolder)
        # 使用多线程现在图片，图片信息
        #threadDownloadImage(filePath, image_url, infoPrefix)
        # downloadImage(filePath, image_url, infoPrefix)
        poolParams.append((None,{'filename':filePath, 'src':image_url, 'infoPrefix':infoPrefix}))
    except:
        appendFile('/'.join([folder,'error.txt']), itemNo + ' ' + itemName + '\n')

# 波多野結衣

# 启动线程池处理
pool=threadpool.ThreadPool(20)
tasks = threadpool.makeRequests(downloadImage, poolParams)
#makeRequests构造线程task请求,第一个参数是线程函数,第二个是参数数组
[pool.putRequest(task) for task in tasks]
#列表推导式,putRequest向线程池里加task,让pool自己去调度task
pool.wait() #等所有任务结束
end = time.time()
print('total cost: ', end - start, 's')

