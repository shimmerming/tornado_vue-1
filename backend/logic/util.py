#!encoding=utf-8
import sys
from uuid import uuid1
from random import randint

def conv_object(d):
    from datetime import datetime
    if isinstance(d, (datetime,)):
        return str(d)
    if isinstance(d, (bytes,)):
        if sys.version_info.major == 3:
            return d.decode()
        else:
            return d
    elif isinstance(d, (list, tuple)):
        return [conv_object(x) for x in d]
    elif isinstance(d, dict):
        return dict([(conv_object(k), conv_object(v)) for k, v in d.items()])
    else:
        return d

def gen_code():
    from captcha.image import ImageCaptcha
    CODE = "abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
    code, out = "", ""

    for i in range(4):
        code += CODE[randint(0, len(CODE) - 1)]

    out = "/tmp/{}.png".format(str(uuid1()))

    #image = ImageCaptcha(width=100, height=30, font_sizes = (40, 46, 50))
    image = ImageCaptcha()
    data = image.generate(code)

    image.write(code, out)
    return code, out

