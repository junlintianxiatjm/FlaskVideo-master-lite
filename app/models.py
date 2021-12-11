import datetime
from app import db


# 定义会员模型
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号码
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符
    userlogs = db.relationship('UserLog', backref='user')  # 会员日志外键关系关联，backref互相绑定user表
    comments = db.relationship('Comment', backref='user')  # 用户评论外键关系关联
    # videocollects = db.relationship('videoCollect', backref='user')  # 用户收藏视频外键关系关联

    def __repr__(self):  # 查询的时候返回
        return "<User %r>" % self.name

    def check_pwd(self, pwd):
        """验证密码是否正确"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 会员日志
class UserLog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录IP
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 登录时间

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 标签
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间
    videos = db.relationship('Video', backref='tag')  # 视频外键关系关联

    def __repr__(self):
        return "<Tag %r>" % self.name


# 视频
class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)  # 播放地址
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    play_num = db.Column(db.BigInteger)  # 播放量
    comment_num = db.Column(db.BigInteger)  # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    area = db.Column(db.String(255))  # 检测区域
    release_time = db.Column(db.Date)  # 检测时间
    length = db.Column(db.String(100))  # 播放时长
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间
    comments = db.relationship('Comment', backref='video')  # 用户评论外键关系关联
    is_detect = db.Column(db.Integer)  # 是否检测
    save_path = db.Column(db.String(255), unique=True)   # 保存地址
    # videocollects = db.relationship('videoCollect', backref='video')  # 用户收藏视频外键关系关联

    def __repr__(self):
        return "<video %r>" % self.title


class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间

    def __repr__(self):
        return "<Preview %r>" % self.title


# 用户评论视频
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 评论内容
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))  # 所属视频，在video表中创建关联
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户，在user表中创建外键关联
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间

    def __repr__(self):
        return "<Comment %r>" % self.id


# 用户收藏视频
class VideoCollect(db.Model):
    __tablename__ = 'videocollect'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))  # 所属视频，在video表中创建关联
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户，在user表中创建外键关联
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间

    def __repr__(self):
        return "<videoCollect %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 权限名称
    url = db.Column(db.String(255), unique=True)  # 权限地址
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 角色名称
    auths = db.Column(db.String(600))  # 权限列表
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间
    admins = db.relationship('Admin', backref='role')  # 管理员外键关系关联，backref互相绑定role表

    def __repr__(self):
        return "<Role %r>" % self.name


# 定义管理员模型
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员，0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间
    adminlogs = db.relationship('AdminLog', backref='admin')  # 管理员日志外键关系关联，backref互相绑定admin表
    operatelogs = db.relationship('OperateLog', backref='operatelog')  # 管理员操作日志外键关系关联

    def __repr__(self):  # 查询的时候返回
        return "<Admin %r>" % self.name

    def check_pwd(self, input_pwd):
        """验证密码是否正确，直接将hash密码和输入的密码进行比较，如果相同则，返回True"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, input_pwd)


# 管理员日志
class AdminLog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 登录时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 操作日志
class OperateLog(db.Model):
    __tablename__ = "operatelog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录ip
    reason = db.Column(db.String(600))  # 操作原因
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 时间

    def __repr__(self):
        return "Operatelog %r" % self.id


# if __name__ == '__main__':
#     # 创建数据表
#     print(db)
#     db.create_all()
#     print('创建表')
#
#     # 添加角色
#     role = Role(
#         name="超级管理员",
#         auths="",
#     )
#     db.session.add(role)
#     db.session.commit()
#
#     # 添加管理员
#     from werkzeug.security import generate_password_hash
#
#     admin = Admin(
#         name='admin',
#         pwd=generate_password_hash('flaskadmin'),  # 加密密码
#         is_super=0,
#         role_id=1,
#     )
#     db.session.add(admin)
#     db.session.commit()
