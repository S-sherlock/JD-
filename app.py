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
    # print(data)
    return render_template('index.html', data=data)


@app.route('/comment')
def comment():
    from jdcomment_多线程 import Jdcomment
    args = request.args
    _id = args['id']
    print(id)
    cursor.execute("SELECT COUNT(productColor) FROM phone_comment1 WHERE phone_id='%s'" % _id)
    num = cursor.fetchone()
    print(num)
    if num[0] > 100:
        return '爬取已数据完成%s' % _id
    else:
        spider = Jdcomment()
        spider.run_and_save(_id)
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
    if q:
        return render_template('fenxi.html')
    else:
        x = Jdcm()
        x.out_word_cloud(phone_id)
        filename1 = phone_id+'.png'
        # filename = '100002332162.svg'
        return render_template('fenxi.html', filename=filename1)


@app.route('/chart')
def chart():
    from jdcomment_fenxi import Jdcm
    x = Jdcm()
    args = request.args
    phone_id = args['id']
    os.chdir('C:/Users/Administrator/PycharmProjects/untitled2/static/svg')
    q = os.path.exists(f'{phone_id}.svg')
    if q:
        return 'chart already Successfully!!!'
    else:
        x.out_chart(phone_id)
        return 'chart successfully'


if __name__ == '__main__':
    app.run()
