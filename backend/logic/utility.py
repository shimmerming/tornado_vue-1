#-*- coding:utf-8 -*-
import sys
import time
import json
import copy
import uuid
import hashlib
from datetime import datetime

import tornado.web
from playhouse.shortcuts import model_to_dict

from tornadoweb import *
from logic.model import *
from logic.define import *

from redis import Redis
mq = Redis(host = __conf__.REDIS_HOST, port = __conf__.REDIS_PORT, \
            password = __conf__.REDIS_PASS, db = __conf__.REDIS_DB)

class BaseHandler(tornado.web.RequestHandler):
    args = {}

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


    def get(self, *args, **kwargs):
        self.send_error(404)

    def options(self):
        self.write(dict(status = True, msg = ""))

    def get_sessionid(self):
        __session__ = self.get_secure_cookie("__S__")
        if not __session__:
            __session__ = hashlib.md5(str(uuid.uuid1()).encode()).hexdigest()
            self.set_secure_cookie("__S__", __session__)
        return __session__


    def prepare(self):
        if self.request.body:
            self.args = json.loads(self.request.body)

        if db.is_closed():
            db.connect()

        username = getattr(self, "username") if hasattr(self, "username") else ""


        if True:
            __session__ = self.get_sessionid()
            print(datetime.now(), self.get_status(),
                    self.request.method,
                    round(self.request.request_time(), 4),
                    self.request.uri,
                    self.request.remote_ip,
                    username,
                    self.request.host,
                    __session__
                )
            sys.stdout.flush()

    def on_finish(self):
        """
            REQUEST FINISH HOOK
        """

        if not db.is_closed():
            db.close()

    def send_error(self, status_code, msg = "无权限", **kwargs):
        exc_info = kwargs.get("exc_info")
        if exc_info:
            a, b, c = exc_info
            if issubclass(a, DatabaseError):
                status_code = b.args[0]
                self.write(dict(status_code = status_code, msg = b.args[1]))
                self.finish()
            elif issubclass(a, tornado.web.MissingArgumentError):
                self.write(dict(status_code = 10001, msg = str(b)))
                self.finish()
            else:
                self.write(dict(status_code = 10002, msg = str(b)))
                self.finish()
        else:
            if status_code == 403:
                self.write(dict(status_code = status_code, msg = msg))
            else:
                self.write(dict(status_code = status_code, msg = msg))
            self.finish()

class LoginedRequestHandler(BaseHandler):
    uid = property(lambda self: self.get_uid())
    username = property(lambda self: (self.get_secure_cookie("__USERNAME__") or '').decode())

    def get_uid(self):
        token = self.get_argument("token", None)
        if token:
            user = User.get_or_none(User.token == token, User.token_enable == 1)
            if user:
                return user.id

        return (self.get_secure_cookie("__UID__") or b'').decode()

    def prepare(self):
        """
            REQUEST BEFORE HOOK
        """

        #if not self.uid:
        #    self.send_error(403)
        #    return

        super(LoginedRequestHandler, self).prepare()

        #User.update(active_time = time.time()).where(User.id == int(self.uid)).execute()
        #self.check_url()

    def check_url(self):
        user = User.get_or_none(User.id == self.uid)
        if not user:
            self.clear_cookie("__UID__")
            self.clear_cookie("__USERNAME__")
            self.send_error(403)
            return

        uri = self.request.path.replace(__conf__.API_VERSION + "/", "/")
        uris = dict((item[0], item) for item in self.__class__.__urls__)

        # uri [uri, order, needcheck, category]
        if not uris.get(uri)[2]:
            return

        accesses = user.role.accesses
        access_name = "{}.{}".format(self.__class__.__module__, self.__class__.__name__)

        if access_name not in accesses.split(","):
            self.send_error(403)

    def check_role_level(self, level):
        """
            Check Role
        """
        user = User.get_or_none(User.id == self.uid)
        if level < user.role.level:
            # no have authorized
            self.send_error(403)

    def check_role_id(self, role_id):
        """
            Check Role
        """
        current_user = User.get_or_none(User.id == self.uid)
        current_user_level = current_user.level

        role = Role.get_or_none(Role.id == role_id)
        role_level = role.level

        if role_level < current_user_level:
            # not have authorized
            self.send_error(403)


def access_list(accesses = None, uid = None):
    _r = copy.deepcopy(ACL)
    result = {}
    for k, v in _r.items():
        result[k] = {}
        for p, h in v.items():
            doc = h.handler.__doc__ or h.handler.__name__
            result[k][p] = [item for item in doc.strip().split("\n")][0]

        if not result.get(k):
            result.pop(k)

    ret = []
    for k, role in result.items():
        data = dict(id = k, label = k, children = [])
        for obj, desc in role.items():
            if uid != '1' and accesses != None and obj not in accesses:
                continue
            data['children'].append(dict(id = obj, label = desc))

        if data.get('children'):
            ret.append(data)

    return ret


from inspect import isclass
def get_handlers():
    members = {}
    for d in __conf__.ACTION_DIR_NAME:
        members.update(get_members(d,
                       None,
                       lambda m: isclass(m) and issubclass(m, RequestHandler) and hasattr(m, "__urls__") and m.__urls__))

    return members
    #handlers = [(item[0], item[1], h) for h in members.values() for item in h.__urls__]

    #return handlers


