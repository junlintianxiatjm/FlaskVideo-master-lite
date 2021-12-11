import datetime  # 生成时间
import ntpath
import os  # 文件操作，及zip文件操作
import uuid  # 生成唯一字符串
import zipfile
import shutil
from functools import wraps

from flask import render_template, redirect, url_for, flash, session, request, abort, send_from_directory, send_file
from pypinyin import lazy_pinyin  # 中文转拼音
from werkzeug.utils import secure_filename

from app import db, app
from app.admin.forms import LoginFrom, TagForm, VideoForm, PreviewForm, PwdForm, AuthForm, RoleForm, AdminForm
from app.models import Tag, Preview, User, Comment, VideoCollect, Auth, Role, Admin, Video
from app.mrcnn.detect import detect_video
from . import admin


# 要求登录才能访问
def admin_login_require(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('login_admin', None) is None:
            # 如果session中未找到该键，则用户需要登录
            return redirect(url_for('admin.login', next=request.url))
        return func(*args, **kwargs)

    return decorated_function


# 权限控制装饰器
def permission_control(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        login_admin = Admin.query.join(
            Role
        ).filter(
            Role.id == Admin.role_id,
            Admin.name == session['login_admin']
        ).first()
        # 若是超级管理员角色
        if login_admin.is_super == 0:
            return func(*args, **kwargs)

        all_auth = Auth.query.all()  # 数据库所有权限
        auths = login_admin.role.auths

        auths = list(map(lambda item: int(item), auths.split(',')))  # 用户权限id列表
        urls = [auth.url for auth in all_auth for admin_auth_id in auths if admin_auth_id == auth.id]

        print(urls)
        rule = request.url_rule
        print(rule)  # 需要转为str判断是否在list中
        if str(rule) not in urls and login_admin.is_super != 0:  # 权限不存在，且不是超级管理员
            abort(401)
        return func(*args, **kwargs)

    return decorated_function


# 修改文件名称
def change_filename(filename):
    print("======================", filename)
    fileinfo = os.path.splitext(filename)  # 分离包含路径的文件名与包含点号的扩展名
    filename = str(uuid.uuid4().hex + fileinfo[-1])
    print('函数中修改后的文件名：', filename)
    return filename


@admin.route("/")
@admin_login_require
@permission_control
def index():
    return render_template('admin/index.html')


@admin.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        # 提交的时候验证表单
        data = form.data  # 获取表单的数据
        # print(data)
        login_admin = Admin.query.filter_by(name=data['account']).first()
        if not login_admin.check_pwd(data['pwd']):
            # 判断密码错误，然后将错误信息返回，使用flash用于消息闪现
            flash('密码错误！')
            return redirect(url_for('admin.login'))
        # 如果密码正确，session中添加账号记录，然后跳转到request中的next，或者是跳转到后台的首页
        session['login_admin'] = data['account']
        return redirect(request.args.get('next') or url_for('admin.video_list', page=1))
    return render_template('admin/login.html', form=form)


@admin.route("/logout/")
@admin_login_require
def logout():
    session.pop('login_admin', None)  # 删除session中的登录账号
    return redirect(url_for("admin.login"))


@admin.route("/pwd/", methods=['GET', 'POST'])
@admin_login_require
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        login_name = session['login_admin']
        admin = Admin.query.filter_by(name=login_name).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data['new_pwd'])
        db.session.commit()  # 提交新密码保存，然后跳转到登录界面
        flash('密码修改成功，请重新登录！', category='ok')
        return redirect(url_for('admin.logout'))
    return render_template('admin/pwd.html', form=form)


# 上传视频
@admin.route("/video/add/", methods=['GET', 'POST'])
@admin_login_require
@permission_control
def video_add():
    form = VideoForm()
    if form.validate_on_submit():
        data = form.data

        # 提交的片名在数据库中已存在
        if Video.query.filter_by(title=data['title']).count() >= 1:
            flash('视频片名已存在，请检查', category='err')
            return redirect(url_for('admin.video_add'))

        print("----------------", form.url.data.filename)

        # 获取上传文件的名称
        file_url = secure_filename(''.join(lazy_pinyin(form.url.data.filename)))

        print('-------------------------------------------------------')
        print("file_url=", file_url)

        file_logo = secure_filename(''.join(lazy_pinyin(form.logo.data.filename)))
        # 文件保存路径操作
        date_path = datetime.datetime.now().strftime("%Y-%m-%d")
        root_path = app.config['UP_DIR']  # 文件上传保存路径
        file_save_path = os.path.join(root_path, date_path, data['title']) + '/'
        print("file_save_path: ", file_save_path)
        if not os.path.exists(file_save_path):
            os.makedirs(file_save_path)  # 如果文件保存路径不存在，则创建一个多级目录
            import stat
            os.chmod(file_save_path, stat.S_IRWXU)  # 授予可读写权限
        # 对上传的文件进行重命名
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        # 保存文件，需要给文件的保存路径+文件名
        form.url.data.save(file_save_path + url)
        form.logo.data.save(file_save_path + logo)

        relative_path = date_path + '/' + data['title'] + '/'
        video = Video(
            title=data['title'],
            url=relative_path + url,
            info=data['info'],
            logo=logo,
            star=data['star'],
            play_num=0,
            comment_num=0,
            tag_id=data['tag_id'],
            area=data['area'],
            release_time=data['release_time'],
            length=data['length']
        )
        db.session.add(video)
        db.session.commit()
        flash('添加视频成功', 'ok')
        return redirect(url_for('admin.video_add'))
    return render_template('admin/video_add.html', form=form)


@admin.route("/video/list/<int:page>/", methods=['GET'])
@admin_login_require
@permission_control
def video_list(page=None):
    if page is None:
        page = 1
    # 查询的时候关联标签Tag进行查询：使用join(Tag)
    # 单表过滤使用filter_by，多表关联使用filter，将Tag.id与video的tag_id进行关联
    page_videos = Video.query.join(Tag).filter(
        Tag.id == Video.tag_id
    ).order_by(
        Video.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/video_list.html', page_videos=page_videos)


@admin.route("/video/delete/<int:delete_id>/", methods=['GET'])
@admin_login_require
@permission_control
def video_delete(delete_id=None):
    if delete_id:
        video = Video.query.filter_by(id=delete_id).first_or_404()
        print(video.logo)
        # 删除视频同时要从磁盘中删除视频的文件和封面文件
        file_save_path = app.config['UP_DIR']  # 文件上传保存路径
        # 如果存在将进行删除，不判断，如果文件不存在删除会报错
        if os.path.exists(os.path.join(file_save_path, video.url)):
            os.remove(os.path.join(file_save_path, video.url))
        if os.path.exists(os.path.join(file_save_path, video.logo)):
            os.remove(os.path.join(file_save_path, video.logo))

        # 删除数据库，提交修改，注意后面要把与视频有关的评论都要删除
        db.session.delete(video)
        db.session.commit()
        # 删除后闪现消息
        flash('删除视频成功！', category='ok')
    return redirect(url_for('admin.video_list', page=1))


@admin.route("/video/update/<int:update_id>/", methods=['GET', 'POST'])
@admin_login_require
@permission_control
def video_update(update_id=None):
    video = Video.query.get_or_404(int(update_id))
    # print(video)

    # 给表单赋初始值，文件表单不处理
    form = VideoForm(
        title=video.title,
        url=video.url,  # 上传文件，这样赋初始值无效，在前端可以通过上传路径+video.url来获取文件的保存路径，显示在页面上
        info=video.info,
        logo=video.logo,  # 上传图片和文件类似
        star=video.star,
        tag_id=video.tag_id,
        area=video.area,
        release_time=video.release_time,
        length=video.length,
    )
    # 对于修改数据，视频文件和封面图已存在，可以非必填:按照教程上测试了validators参数，但始终不行，最终修改required的值就可以了
    form.url.validators = []
    print(form.url)  # <input id="url" name="url" required type="file">
    if form.url.render_kw:
        form.url.render_kw['required'] = False
    else:
        form.url.render_kw = {'required': False}
    print(form.url)  # <input id="url" name="url" type="file">

    form.logo.validators = []  # 验证列表为空
    form.logo.render_kw = {'required': False}  # 直接修改required为False表明不要求输入

    if form.validate_on_submit():
        data = form.data
        # 提交的片名在数据库中已存在，且不是当前的视频名称
        if video.query.filter_by(title=data['title']).count() == 1 and video.title != data['title']:
            flash('视频片名已存在，请检查', category='err')
            return redirect(url_for('admin.video_update', update_id=update_id))
        # 以下和直接修改的数据
        video.title = data['title']
        video.info = data['info']
        video.star = data['star']
        video.tag_id = data['tag_id']
        video.area = data['area']
        video.release_time = data['release_time']
        video.length = data['length']

        # 文件保存路径操作
        date_path = datetime.datetime.now().strftime("%Y-%m-%d")
        root_path = app.config['UP_DIR']  # 文件上传保存路径
        file_save_path = os.path.join(root_path, date_path, data['title']) + '/'
        print("file_save_path: ", file_save_path)
        if not os.path.exists(file_save_path):
            os.makedirs(file_save_path)  # 如果文件保存路径不存在，则创建一个多级目录
            import stat
            os.chmod(file_save_path, stat.S_IRWXU)  # 授予可读写权限

        print(form.url.data, type(form.url.data))
        # <FileStorage: 'ssh.jpg' ('image/jpeg')> <class 'werkzeug.datastructures.FileStorage'>
        # 处理视频文件逻辑：先从磁盘中删除旧文件，然后保存新文件
        if form.url.data:  # 上传文件不为空，才进行保存
            # 删除以前的文件
            if os.path.exists(os.path.join(file_save_path, video.url)):
                os.remove(os.path.join(file_save_path, video.url))
            # 获取上传文件的名称
            file_url = secure_filename(''.join(lazy_pinyin(form.url.data.filename)))
            # 对上传的文件进行重命名
            video.url = change_filename(file_url)
            # 保存文件，需要给文件的保存路径+文件名
            form.url.data.save(file_save_path + video.url)

        # 处理封面图
        if form.logo.data:
            if os.path.exists(os.path.join(file_save_path, video.logo)):
                os.remove(os.path.join(file_save_path, video.logo))
            file_logo = secure_filename(''.join(lazy_pinyin(form.logo.data.filename)))
            video.logo = change_filename(file_logo)
            form.logo.data.save(file_save_path + video.logo)
        db.session.merge(video)  # 调用merge方法，此时video实体状态并没有被持久化，但是数据库中的记录被更新了（暂时不明白）
        db.session.commit()
        flash('修改视频成功', 'ok')
        return redirect(url_for('admin.video_update', update_id=update_id))
    return render_template('admin/video_update.html', form=form, video=video)


# 缺陷检测
@admin.route("/video/detect/<int:detect_id>/", methods=['GET', 'POST'])
@admin_login_require
@permission_control
def video_detect(detect_id=None):
    video = Video.query.get_or_404(int(detect_id))
    root_path = app.config['UP_DIR']  # 文件上传保存路径
    print('文件保存路径', root_path)
    file_save_path = os.path.join(root_path, video.url)
    print('是否检测ID', video.is_detect)
    # 检查detect字段，如果是1，则表示该视频已经检测过, 运行检测的时候将该字段变为1
    if video.is_detect == 0:
        det = detect_video(file_save_path)
        result_path = det.do_detect()
        # 检测之后将是否检测字段置位1
        video.is_detect = 1
        # 同时存入结果储存地址文件夹（相对路径，根路径）
        video.save_path = result_path
        db.session.commit()
    else:
        print("file_save_path: ", file_save_path)
        # 这种情况是在用户点击再次检测之后，运行该部分，detect字段已经为1，但需要重新记录保存地址
        # TODO 用户点击确定再次检测后，弹框消失
        det = detect_video(file_save_path)
        result_path = det.do_detect()
        video.save_path = result_path
        # 点击重复检测后，返回视频列表页
        return redirect("/admin/video/list/1/")
    return redirect("/admin/video/list/1/")


# TODO 结果下载
# 结果下载
@admin.route("/video/download/<int:video_id>/", methods=['GET', 'POST'])
@admin_login_require
@permission_control
def video_download(video_id=None):
    # 根据传回来的视频id获取数据库里其他信息（主要是保存地址）
    video = Video.query.get_or_404(int(video_id))
    # 获取结果图片保存地址
    file_url = video.save_path
    # 获取文件夹内的所有文件
    files = os.listdir(file_url)
    # 如果里面只有一张图片，直接下载
    if len(files) == 1:
        # 返回单张图片，也就是文件夹内的文件
        return send_from_directory(file_url, files, as_attachment=True)
    else:
        # 如果里面有多张图片，进行压缩后下载
        f = shutil.make_archive(video.title, "zip", file_url)
        # 直接返回压缩包
        return send_file(f, as_attachment=True)
    # 在下载成功后，删除压缩包，释放存储空间，再次下载时候重新生成即可
    os.remove(f)
    # 下载后返回视频列表页
    return redirect("/admin/video/list/1/")


# 报告发布
@admin.route("/video/publish/<int:publish_id>/", methods=['GET', 'POST'])
@admin_login_require
@permission_control
def video_publish(publish_id=None):
    pass


@admin.route("/preview/list/<int:page>/")
@admin_login_require
@permission_control
def preview_list(page=None):
    page_previews = Preview.query.paginate(page=page, per_page=10)
    return render_template('admin/preview_list.html', page_previews=page_previews)


@admin.route("/auth/add/", methods=['GET', 'POST'])
@admin_login_require
@permission_control
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        if Auth.query.filter_by(name=data['name']).count() == 1:
            flash('权限名称已存在！', category='err')
            return redirect(url_for('admin.auth_add'))
        if Auth.query.filter_by(url=data['url']).count() == 1:
            flash('权限链接地址已存在！', category='err')
            return redirect(url_for('admin.auth_add'))
        auth = Auth(
            name=data['name'],
            url=data['url']
        )
        db.session.add(auth)
        db.session.commit()
        flash('权限地址添加成功！', category='ok')
    return render_template('admin/auth_edit.html', form=form)


@admin.route("/auth/list/<int:page>/")
@admin_login_require
@permission_control
def auth_list(page=None):
    if not page:
        page = 1
    page_auths = Auth.query.order_by(Auth.add_time.desc()).paginate(page=page, per_page=10)
    return render_template('admin/auth_list.html', page_auths=page_auths)


@admin.route("/role/add/", methods=['GET', 'POST'])
@admin_login_require
@permission_control
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        if Role.query.filter_by(name=data['name']).count() >= 1:
            flash('角色名称已存在！', category='err')
            return redirect(url_for('admin.role_add'))
        # print(data['auths'])  # 权限id列表形式[1, 2]
        role = Role(
            name=data['name'],
            auths=','.join(map(lambda item: str(item), data['auths']))  # 数字转换为字符串形式
        )
        db.session.add(role)
        db.session.commit()
        flash('角色添加成功', category='ok')
    return render_template('admin/role_edit.html', form=form)


@admin.route("/role/list/<int:page>/")
@admin_login_require
@permission_control
def role_list(page=None):
    if not page:
        page = 1
    page_roles = Role.query.order_by(
        Role.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/role_list.html', page_roles=page_roles)




@admin.route("/admin/list/<int:page>")
@admin_login_require
@permission_control
def admin_list(page=None):
    if not page:
        page = 1
    page_admins = Admin.query.order_by(
        Admin.add_time.desc()
    ).join(
        Role
    ).filter(
        Role.id == Admin.role_id  # 关联查询
    ).paginate(page=page, per_page=10)
    return render_template('admin/admin_list.html', page_admins=page_admins)
