
import requests
import json
import re
import os
# 查询关键字
search_str = 'SSNI388'
# 提交的查询参数
params = {
    "rsz": "filtered_cse",
    "num": 20,
    "hl": "zh-CN",
    "source": "gcsc",
    "gss": ".com",
    "cselibv": "d35a6008cf40f285",
    "cx": "009341400208504726543:qg1lhh9kw1y",
    "q": search_str,
    "safe": "off",
    "cse_tok": "AKaTTZjNDImSRUC5dDhWQNUYmSpC:1556180286544",
    "sort": "",
    "exp": "csqr,4229469,4231019",
    "oq": search_str,
    "gs_l": "partner-generic.12...0.0.3.5132.0.0.0.0.0.0.0.0..0.0.gsnos,n=13...0.0jj1....34.partner-generic..10.1.252.O15jUA5hTvc",
    "callback": "google.search.cse.api11012"
}
# 提交参数
r = requests.get('https://cse.google.com/cse/element/v1', params=params)
r.encoding = 'UTF-8'
rtext = r.text
# 解析放回的数据字符串，用于生成json
m = re.findall(r'api11012\(([\s\S]*)\)', rtext)
# 转义成为json
results = json.loads(m[0])['results']
# 将数据保存在指定的文件中
filename = ''.join(['d:/download/', search_str, '.txt'])
dirname = os.path.dirname(filename)
if not os.path.exists(dirname):
    os.makedirs(dirname)
file = open(filename, 'w', encoding='UTF-8')
for item in results:
    content_str = item['contentNoFormatting']
    url_str = item['unescapedUrl']
    if content_str.find('中文') > -1:
        file.write(content_str.replace('\n', '')+'\n')
        file.write(url_str.replace(
            'www.sexinsex.net', '67.220.90.4').replace('sexinsex.net', '67.220.90.4')+'\n')
print('download success!')
file.close()
