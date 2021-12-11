运行步骤：
1.执行数据库脚本：pipeline_monitor.sql，修改数据库配置文件为本地mysql地址和账号;

2.解压缩文件FlaskVideo-master-lite\app\mrcnn\h5\shapes20210726T1823下面的rar文件，生成mask_rcnn的.h5模型文件；

3.启动flask框架，manage.py;

4.访问localhost:5000/admin

5.账号/密码：admin/flaskadmin

执行“检测”，即调用模型文件。


对应csdn地址：https://blog.csdn.net/shanxiderenheni/article/details/121820110
