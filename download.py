import time
import requests


class Download:
    def __init__(self, filename, src, infoPrefix):
        self.filename = filename
        self.src = src
        self.infoPrefix = infoPrefix

    # 生成远程图片方法
    def downloadImage(self):
        start = time.time()
        # 获取图片地址
        img_data = requests.get(self.src).content
        with open(self.filename, 'wb') as handler:
            handler.write(img_data)
            end = time.time()
            print(self.infoPrefix, ' cost :', end - start, 's')
