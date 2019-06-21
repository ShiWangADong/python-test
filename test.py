
from bs4 import BeautifulSoup
import time
import requests
import json
import re
import os

m = re.findall(r'(\d{1,})', '/zh-TW/Product/Index/233234')
print(m,{})
