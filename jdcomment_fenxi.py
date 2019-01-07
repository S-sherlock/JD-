# coding:utf-8
# __author__ = 'ym'
import jieba
import pymysql
from PIL import Image
from wordcloud import WordCloud
import pygal
import os


class Jdcm(object):

    def __init__(self):
        self.conn = pymysql.connect(user='root', password='123', db='test')
        self.cursor = self.conn.cursor()

    def get_comments(self, phone_id):
        self.cursor.execute("""SELECT comment FROM phone_comment1 WHERE phone_id='%s'""" % phone_id)
        x = self.cursor.fetchall()
        return x

    def cut_word(self, phone_id):
        x = self.get_comments(phone_id)
        list1 = []
        for i in x:
            list1.append(i[0])
        a = ''.join(list1)
        xx = jieba.cut(a, cut_all=False)
        word1 = ' '.join(xx)
        return word1

    def out_word_cloud(self, phone_id):
        print('生成词云')
        word1 = self.cut_word(phone_id)
        font = 'simkai.ttf'
        wc = WordCloud(font_path=font,
                       background_color='white',
                       width=2000,
                       height=1500,
                       max_font_size=300,
                       min_font_size=50
                       ).generate(word1)
        os.chdir("C:/Users/Administrator/PycharmProjects/untitled2/static/images")
        wc.to_file(f'{phone_id}.png')
        print(f"OK!path\t{os.getcwd()}\{phone_id}.png")

    def out_chart(self, phone_id):
        self.cursor.execute("SELECT COUNT(id) FROM phone_comment1 WHERE phone_id='%s'" % phone_id)
        count_all = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT DISTINCT productColor FROM phone_comment1 WHERE phone_id='%s'" % phone_id)
        color_list = self.cursor.fetchone()
        print(count_all)
        print(color_list)
        list1 = []
        for i in color_list:
            print(i)
            self.cursor.execute(
                "SELECT COUNT(productColor) FROM phone_comment1 WHERE phone_id='%s' AND productColor='%s'" % (phone_id, i))
            count_num = self.cursor.fetchone()[0]
            list1.append((i, count_num))
        print('正在生成饼状图')
        pie_chart = pygal.Pie()
        pie_chart.title = '手机颜色分析 (in %)'
        for a in list1:
            pie_chart.add(a[0], a[1]/count_all*100)
        pie_chart.render_to_file(f'{phone_id}.svg')
        print(f'OK!path\t{phone_id}.svg')


if __name__ == '__main__':
    jd = Jdcm()
    phone_id = 100002332138
    jd.out_chart(phone_id)
    # jd.out_word_cloud()
    # jd.out_chart()
    # im = Image.open('test.png')
    # im.show()
    jd.conn.close()  # 关闭数据库连接
