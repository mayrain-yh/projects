#encoding: utf-8

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from first_project import app
from exts import db
from models import User,Video,Answer
#video 和 answer的建立出了问题  不知道怎么解决 故评论功能无法实现

manager = Manager(app)

#使用Migrate绑定app和db
migrate = Migrate(app,db)

#添加迁移脚本的命令到manager中
manager .add_command('db',MigrateCommand)

if __name__ == "__main__":
    manager.run()
