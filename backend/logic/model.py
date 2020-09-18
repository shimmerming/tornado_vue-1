#!encoding=utf-8
import os
import json
import time
import uuid
from datetime import datetime
from hashlib import md5

from peewee import *
from playhouse.shortcuts import model_to_dict

from logic.objectid import ObjectId
from logic.util import *

db = MySQLDatabase(__conf__.DB_NAME,
                    host = __conf__.DB_HOST,
                    port = __conf__.DB_PORT,
                    user = __conf__.DB_USER,
                    password = __conf__.DB_PASS)

id_func = lambda :str(ObjectId())

class LongTextField(TextField):
    field_type = 'LONGTEXT'


class BaseModel(Model):
    class Meta:
        database = db

class Role(BaseModel):
    id = AutoField()
    _id = CharField(default = id_func)
    name = CharField()
    level = IntegerField(default = 0)
    accesses = TextField(null = True)
    desc = CharField(default = "")
    type = IntegerField(default = 0)
    default = IntegerField(default = 0)


class User(BaseModel):
    id = AutoField()
    _id = CharField(default = id_func)
    username = CharField(unique = True)
    nickname = CharField(default = "")
    tel = CharField(default = "")
    role = ForeignKeyField(Role)
    avatar = CharField(default = "")
    token = CharField(default = "")
    token_enable = IntegerField(default = 1)
    is_del = IntegerField(default = 0)
    email = CharField(default = "")
    password = CharField(default = "")
    enable = IntegerField(default = 1)
    create_time = DoubleField(default = time.time)
    update_time = DoubleField(default = time.time)
    active_time = DoubleField(default = time.time)
    login_time = DoubleField(default = 0)

class Group(BaseModel):
    id = AutoField()
    _id = CharField(default = id_func)
    name = CharField()
    desc = CharField()
    owner = ForeignKeyField(User)
    parent = IntegerField(default = 0)
    create_time = DoubleField(default = time.time)
    update_time = DoubleField(default = time.time)

class GroupUser(BaseModel):
    _id = CharField(default = id_func)
    user = ForeignKeyField(User)
    group = ForeignKeyField(Group)
    role = ForeignKeyField(Role)
    create_time = DoubleField(default = time.time)

class Project(BaseModel):
    id = AutoField()
    _id = CharField(default = id_func)
    name = CharField()
    desc = CharField()
    owner = ForeignKeyField(User)
    create_time = DoubleField(default = time.time)

class ProjectUser(BaseModel):
    _id = CharField(default = id_func)
    project = ForeignKeyField(Project)
    user = ForeignKeyField(User)
    create_time = DoubleField(default = time.time)

def init_db():
    db.drop_tables([Role, User, Group, GroupUser, Project, ProjectUser])
    db.create_tables([Role, User, Group, GroupUser, Project, ProjectUser])

    Role(name = "超级管理员", level = 1, accesses = "").save()
    Role(name = "普通用户", level = 2, accesses = "").save()

    User(username = "admin", password = "131183217f782f0a302b7c165efbdca2", role_id = 1).save()
    for i in range(22):
        User(username = "admin{}".format(i), password = "131183217f782f0a302b7c165efbdca2", role_id = 1).save()

    Group(name = "测试", owner = 1, desc = "测试 ...").save()
    GroupUser(group_id = 1, user_id = 1, role_id = 1).save()

    from logic.utility import access_list
    accesses = []
    for item in access_list():
        accesses.extend([_.get('id') for _ in item.get('children')])

    accesses = ",".join(accesses)
    Role.update(accesses = accesses).where(Role.id == 1).execute()





