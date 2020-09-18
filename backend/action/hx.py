#!coding=utf-8
from tornadoweb import *
from logic.model import *
from logic.utility import *

from logic import data as DATA


@url(r"/product/server", needcheck = False, category = "hx")
class ProductServer(BaseHandler):
    """
        服务器产品查询

    """
    def get(self):
        search = self.get_argument("search", "")
        print (search)
        data = DATA.华信鼎成服务器产品目录
        data = [[i.strip() for i in item.split("|")] for item in data.split("\n") if item]

        data = [item + [""] * (len(data[0]) - len(item)) for item in data]

        data = data[1:]
        searchOptions = [item[1] for item in data]

        if search:
            data = [item for item in data if item[1] == search]

        self.write(dict(status = True, total = len(data), data = data, searchOptions = searchOptions))
