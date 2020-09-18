#!coding=utf-8
import os
import uuid
import time
import base64
from hashlib import md5

from tornadoweb import *
from logic.model import *
from logic.utility import *

def password_md5(o):
    return md5('{}.{}'.format(md5(md5(o.encode()).hexdigest().encode()).hexdigest(),
                                "U2FsdGVkX1/u1YaeTuRdWM9adoqFpGm9seFRccbhRR/O2qyTwP78Cok=").encode()).hexdigest()


@url(r"/login", needcheck = False, category = "用户")
class Login(BaseHandler):
    """
        用户登陆

        username*: 用户名
        password*: 密码
    """
    def get(self):
        """
        GET DOC
        """
        self.post()

    def post(self):
        username = self.args.get('username').strip()
        password = self.args.get('password')
        #code = self.get_argument('code', '')

        #if not code:
        #    self.write(dict(status = False, message = "请输入验证码"))
        #    return

        #__session__ = self.get_sessionid()
        #store_code = mq.get(__session__)
        #if not store_code:
        #    self.write(dict(status = False, message = "验证码过期,重新生成", refresh = 1))
        #    return

        #if code.lower() != store_code.decode().lower():
        #    self.write(dict(status = False, message = "验证码错误,重新生成", refresh = 1))
        #    return


        if "@" in username:
            username = username.split("@")[0]

        password = password_md5(password)
        user = User.get_or_none(User.username == username, \
                                User.password == password)

        if not user:
            self.write(dict(status = False, message = "用户名或密码错误"))
        elif user.enable == 0:
            self.write(dict(status = False, message = "用户无法正常登陆，请联系管理员!"))
        else:
            self.set_secure_cookie("__UID__", str(user.id))
            self.set_secure_cookie("__USERNAME__", str(user.username))
            User.update(login_time = time.time()).where(User.id == user.id).execute()
            role = model_to_dict(user.role)
            self.write(dict(status = True, message = "登陆成功", data = {"token": user.id, "role": role}))


@url(r"/gencode", needcheck = False, category = "用户")
class Gencode(BaseHandler):
    """
        获取验证码
    """
    def get(self):
        __session__ = self.get_sessionid()
        code, p = gen_code()
        mq.setex(__session__, 60 * 3, code)
        with open(p, "rb") as f:
            data = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode())

        os.remove(p)
        self.write(dict(status = True, image = data))

@url(r"/user/info", needcheck = False, category = "用户")
class UserInfo(BaseHandler):
    """
        用户登陆
    """
    def get(self):
        self.write(dict(status = True, data = {"roles": ['admin'], "name": "admin", "avatar": "", "introduction": "intro"}))

@url(r"/logout", needcheck = False, category = "用户")
class Logout(LoginedRequestHandler):
    """
        用户登出
    """
    def post(self):
        uid = self.uid
        self.clear_cookie("__UID__")
        self.clear_cookie("__USERNAME__")

        self.write(dict(message="登出成功", status = True))

@url(r"/user/add", category = "用户")
class UserAdd(LoginedRequestHandler):
    """
        用户设置

        id: 用户id
        username*:用户名
    """
    def post(self):
        print (self.args)
        _id = self.args.get('id')
        username = self.args.get('username')
        nickname = self.args.get('nickname', '')
        email = self.args.get('email', "")
        tel = self.args.get('tel', "")
        role_id = self.args.get('role_id', 1)
        password = self.args.get('password', '')
        enable = self.args.get('enable', 1)
        project = self.args.get('project')


        doc = dict(nickname = nickname, email = email, tel = tel, role_id = role_id)

        if password:
            doc['password'] = password

        def project_user(project, user_id):
            ProjectUser.delete().where(ProjectUser.user_id == user_id).execute()
            for p_id in project:
                ProjectUser(project_id = p_id, user_id = user_id).save()

        if _id:
            User.update(update_time = time.time(), **doc). \
                            where(User.id == _id). \
                            execute()

            project_user(project, _id)
            self.write(dict(status = True, message = '编辑成功'))
        else:
            user = User.get_or_none(User.username == username)
            if user:
                self.write(dict(status = False, message = "用户已注册"))
            else:
                user = User(username = username, **doc)
                user.save()
                project_user(project, user.id)
                self.write(dict(status = True, message = '添加成功'))



@url(r"/user/password", needcheck = False, category = "用户")
class UserPassword(LoginedRequestHandler):
    """
        密码设置

        old_password*: 旧密码
        new_password*: 新密码
        re_password*: 重复新密码
    """
    def post(self):
        old_password = self.get_argument('old_password', '')
        new_password = self.get_argument('new_password')
        re_password = self.get_argument('re_password')

        if new_password != re_password:
            self.write(dict(status = False, message = "新密码输入不一致"))
            return

        from logic.password_judge import passwd_judge
        advice = passwd_judge(new_password)
        if advice:
            self.write(dict(status = False, message = advice))
            return

        user = User.get_or_none(User.id == self.uid)
        if user.password != password_md5(old_password):
            self.write(dict(status = False, message = "密码错误"))
            return

        User.update(password = password_md5(new_password)).where(User.id == int(self.uid)).execute()
        self.write(dict(status = True, message = "设置成功"))


@url(r"/user/del", category = "用户")
class UserDel(LoginedRequestHandler):
    """
        用户删除

        id: 用户id[]
    """
    def post(self):
        _id = self.args.get('id')

        if 1 in _id:
            self.write(dict(status = False, message = '不能删除admin'))
            return

        User.delete().where(User.id.in_(_id)).execute()

        self.write(dict(status = True, message = '删除成功'))


@url(r"/user/list", category = "用户")
class UserList(LoginedRequestHandler):
    """
        用户列表

        search: 查询条件
        page_index: 页码
        page_size: 每页条数
        sort: 排序字段
        direction: 排序方向

        response: [{'id': '用户id', 'username': '用户名', 'role': {'id': '角色id', 'name': '角色名'}}]
    """
    def get(self):
        search = self.get_argument('search', None)
        page_index = int(self.get_argument('page', 1))
        page_size = int(self.get_argument('limit', 10))

        _sort = self.get_argument('sort', None)
        sort = _sort[1:]
        # 方向 desc
        direction = _sort[0:1]

        cond = []

        if search:
            cond.append(User.username.contains(search))

        if not cond:
            cond = (None, )

        if sort:
            sort = getattr(User, sort)
            direction = 'desc' if direction == '-' else 'asc'
            if direction == 'desc':
                sort = sort.desc()
        else:
            sort = User.id.desc()

        total = User.select().where(*cond).count()

        users = User.select().where(*cond). \
                        order_by(sort).\
                        paginate(page_index, page_size)

        #users = [model_to_dict(user) for user in users]
        users = [dict(id = user.id, username = user.username, nickname = user.nickname, email = user.email, tel = user.tel, login_time = user.login_time) for user in users]
        for user in users:
            user['project'] = [p.project_id for p in ProjectUser.select().where(ProjectUser.user_id == user.get("id"))]
            user['project_name'] = [p.project.name for p in ProjectUser.select().where(ProjectUser.user_id == user.get("id"))]

        self.write(dict(status = True, page_index = page_index, \
                            total = total, \
                            data = users))

@url(r"/transaction/list", category = "用户")
class TransactionList(LoginedRequestHandler):
    def get(self):
        self.write(dict(status = True, data = [{"order_no": str(no), "price": str(0.23 * no), "status": str(no % 2)} for no in range(10)]))
