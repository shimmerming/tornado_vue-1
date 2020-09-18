#!coding=utf-8
from tornadoweb import *
from logic.model import *
from logic.utility import *

@url(r"/project/upsert", category = "项目")
class ProjectUpsert(LoginedRequestHandler):
    """
        添加项目

        id: 项目id
        name*:用户名
        password: 用户密码
    """
    def post(self):
        _id = self.args.get('id')
        name = self.args.get('name')
        desc = self.args.get('desc')

        doc = dict(name = name, desc = desc, owner_id = 1)

        if _id:
            Project.update(**doc). \
                            where(Project.id == _id). \
                            execute()

            self.write(dict(status = True, message = '编辑成功'))
        else:
            project = Project.get_or_none(Project.name == name)
            if project:
                self.write(dict(status = False, message = "项目已存在"))
            else:
                Project(**doc).save()
                self.write(dict(status = True, message = '添加成功'))


@url(r"/project/del", category = "项目")
class ProjectDel(LoginedRequestHandler):
    """
        项目删除

        id: 项目id[]
    """
    def post(self):
        _id = self.args.get('id')
        Project.delete().where(Project.id.in_(_id)).execute()
        self.write(dict(status = True, message = '删除成功'))


@url(r"/project/list", category = "项目")
class ProjectList(LoginedRequestHandler):
    """
        项目列表

        search: 查询条件
        page: 页码
        limit: 每页条数
        sort: 排序字段
    """
    def get(self):
        search = self.get_argument('search', None)
        page_index = int(self.get_argument('page', 1))
        page_size = int(self.get_argument('limit', 10))

        _sort = self.get_argument('sort', "+id")
        sort = _sort[1:]
        # 方向 desc
        direction = _sort[0:1]

        cond = []

        if search:
            cond.append(Project.name.contains(search))

        if not cond:
            cond = (None, )

        if sort:
            sort = getattr(Project, sort)
            direction = 'desc' if direction == '-' else 'asc'
            if direction == 'desc':
                sort = sort.desc()
        else:
            sort = Project.id.desc()

        total = Project.select().where(*cond).count()

        projects = Project.select().where(*cond). \
                        order_by(sort).\
                        paginate(page_index, page_size)

        projects = [model_to_dict(project) for project in projects]

        self.write(dict(status = True, total = total, data = projects))


