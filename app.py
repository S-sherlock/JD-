from flask import Flask, render_template, url_for, request
import pymysql
import os

app = Flask(__name__)
conn = pymysql.connect(user='root', password='123', db='test')
cursor = conn.cursor()


@app.route('/')
def hello_world():
    cursor.execute('SELECT * FROM phone WHERE id>0 AND id<=20')
    data = cursor.fetchall()
    print(data)
    return render_template('index.html', data=data)


@app.route('/comment')
def comment():
    from comment_spider import Jdcomment
    args = request.args
    _id = args['id']
    print(id)
    cursor.execute("SELECT COUNT(productColor) FROM phone_comment1 WHERE phone_id='%s'" % _id)
    num = cursor.fetchone()
    print(num)
    if num[0] > 200:
        return '爬取已数据完成%s' % _id
    else:
        spider = Jdcomment()
        spider.save_data(50, _id)
        return '爬取数据完成%s' % _id


@app.route('/data_fenxi')
def data_fenxi():
    from jdcomment_fenxi import Jdcm
    args = request.args
    phone_id = args['id']
    pa = str(phone_id)+'.png'
    print(pa)
    os.chdir('C:/Users/Administrator/PycharmProjects/untitled2/static/images')
    q = os.path.exists(pa)
    # print(q)
    # print(os.getcwd())
    if q == True:
        return render_template('fenxi.html')
    else:
        x = Jdcm()
        x.out_word_cloud(phone_id)
        return render_template('fenxi.html')


if __name__ == '__main__':
    app.run()
