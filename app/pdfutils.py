# -*- coding: utf-8 -*-

"""
@author: tjm
@software: PyCharm
@file: pdfutils.py
@time: 2021/10/9 16:09
"""

# 1.导包
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import pandas as pd
import numpy as np
import os


class pdfutils:
    def __init__(self, title, data=None):
        self.title = title
        self.data = data
        # 设置中文字体为微软雅黑
        pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttf'))


    # TODO 需要增加两个参数：标题（视频名称）、缺陷图片文件夹路径
    def doPdf(self):
        # 容纳所有的PDF内容
        elements = []

        # 2.添加标题文字
        # 读取reportlab定义好的样式表
        styles = getSampleStyleSheet()
        style = styles['Normal']

        title = "<para><font face='msyh'>西安市高新区数据</font></para>"
        elements.append(Paragraph(title, styles['Title']))
        elements.append(Spacer(1, 0.2 * inch))

        # 3.添加正文

        # 4.添加表格
        # TODO 需补充管道缺陷检测的分类统计信息（类别，名称......）

        # 5.添加图片
        path = r"D:\python-workspace\FlaskVideo-master\app\mrcnn\results"
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        for root, dirs, files in os.walk(path):
            # 遍历文件
            # TODO 图片布局需要完善
            for f in files:
                img_path = os.path.join(root, f)
                img = Image(img_path, width=600, height=550)

                elements.append(img)
                # elements.append(Spacer(1, 0.2 * inch))

        # 6.生成PDF文件
        doc = SimpleDocTemplate(
            "2021西安全运会.pdf",
            pagesize=(A4[0], A4[1]),
            topMargin=30,
            bottomMargin=30
        )

        doc.build(elements)

    def doPdf2(self):
        # 容纳所有的PDF内容
        elements = []

        # 2.添加标题文字
        # 读取reportlab定义好的样式表
        style = getSampleStyleSheet()

        title = "<para><font face='msyh'>西安市高新区数据</font></para>"
        elements.append(Paragraph(title, style['Title']))
        elements.append(Spacer(1, 0.2 * inch))

        # 3.添加正文
        description = "<para><font face='msyh'>全运会欢迎您，千年古都，常来长安</font></para>"
        elements.append(Paragraph(description, style['BodyText']))
        elements.append(Spacer(1, 0.2 * inch))

        # 4.添加表格
        df = pd.read_excel("黄河水库水情_100.xls")
        print(df.head())
        # 表格样式
        table_style = [
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, -1), (-1, -1), 'LEFT'),
            ('FONT', (0, 0), (-1, -1), 'msyh')
        ]
        # 表格对象
        mytable = Table(df.to_numpy().tolist())
        mytable_style = TableStyle(table_style)
        mytable.setStyle(mytable_style)

        # 添加对象
        elements.append(mytable)
        elements.append(Spacer(1, 0.2 * inch))

        # 5.添加图片
        img = Image('hole.jpg')
        elements.append(img)
        elements.append(Spacer(1, 0.2 * inch))

        # 6.生成PDF文件
        doc = SimpleDocTemplate(
            "2021西安全运会.pdf",
            pagesize=(A4[0], A4[1]),
            topMargin=30,
            bottomMargin=30
        )

        doc.build(elements)


class ConditionalSpacer(Spacer):

    def wrap(self, availWidth, availHeight):
        height = min(self.height, availHeight - 1e-8)
        return (availWidth, height)


if __name__ == "__main__":
    pdf = pdfutils("西安")
    pdf.doPdf()
