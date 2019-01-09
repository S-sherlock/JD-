# coding:utf-8
__author__ = 'ym'
import requests
from CrawlerUtility import ChromeHeaders2Dict
import json
import time
from multiprocessing.dummy import Pool


class Jdcomment(object):

    def __init__(self):
        self.header = """
:authority: sclub.jd.com
:method: GET
:path: /comment/productPageComments.action?callback=fetchJSON_comment98vv15260&productId=100000287113&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=a2cc2478caba42fc&fold=1
:scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
cache-control: no-cache
cookie: __jdc=122270672; __jdu=1241630742; PCSYCityID=412; shshshfpa=55b0af51-02c3-1e40-a310-1c57890f85e9-1545875426; TrackID=1CBs1NgwoA4kdyJ_DHv_k4eV1rM83Ka0EnopIXoJARMAhbARg7uNGSxvBqh4wcVwOxlpYwH4NqrIv9eA6Xryy2Z62BJKkdAxeFsA3UQGaoo4; user-key=8abc6212-d9b5-44ff-bc2c-ddd9e8be0554; ipLoc-djd=1-72-2799-0; unpl=V2_ZzNtbRdRFkJ8WBJSLxxUBmICRVpLVEIWJwwVAyseDgFuAEFUclRCFXwURldnGlUUZwIZXkVcRxVFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VHgcXAJlAhRYQWdzEkU4dlN9HVoNZTMTbUNnAUEpDERccx5USGcAF11FVUITcAt2VUsa; __jda=122270672.1241630742.1543824136.1545880963.1545964078.3; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_d7df8ae7e49240f68202c5bfa6c582b8|1545964077739; pinId=7i7kN8FksT-lGMqtUbaimQ; pin=49817795-598178; ceshi3.com=000; _tp=5PStYdOEJwZICWIaFuxuUQ%3D%3D; _pst=49817795-598178; cn=5; _gcl_au=1.1.730340221.1545964394; thor=868BA4D0E4372F9130214B99DAB50625903B38F62B09C4BFFE47A360066B6295AF2286835649C9BC0EEEA10E4D3BDE45417D3EC64FAEEB7A30A4D918DA20ECF70EB138078B097F1CDE60DFA73DE9283BAFE14E351C3A104B97A5938B40D73BF923C68F6A8F7E1D3AF3A6D470BB2C9FCB883981D5C5191432D91806B45D7E6AD1B342418803092685C52BD439BDD8F14E6723ACCE0916C39EEE017B7A9171BDCF; 3AB9D23F7A4B3C9B=5LFBQ2OIQGNALF4257ZN4K2W63PZ3AYMFTJ5TD5LNKU3G3QYXGREWS7J4XBXPOFPFGUOUTIBKPOC2FY4D465O7NOAA; shshshfp=26620f2aeddc936158d73d66697b4aff; shshshsID=ef24363d4037bc94ef352ce87cc44eaa_3_1545964456703; __jdb=122270672.6.1241630742|3.1545964078; shshshfpb=ow5Ddp1hdUuLFIWx0fLMELw%3D%3D; JSESSIONID=0372305F9FCCC2C53B077FD07DBD5F98.s1
pragma: no-cache
referer: https://item.jd.com/100000287113.html
user-agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
"""
        self.headers = ChromeHeaders2Dict(self.header)
        self.url = "https://sclub.jd.com/comment/productPageComments.action?"

    @staticmethod
    def get_json_thread(url):
        headers = ChromeHeaders2Dict("""
:authority: sclub.jd.com
:method: GET
:path: /comment/productPageComments.action?callback=fetchJSON_comment98vv15260&productId=100000287113&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=a2cc2478caba42fc&fold=1
:scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
cache-control: no-cache
cookie: __jdc=122270672; __jdu=1241630742; PCSYCityID=412; shshshfpa=55b0af51-02c3-1e40-a310-1c57890f85e9-1545875426; TrackID=1CBs1NgwoA4kdyJ_DHv_k4eV1rM83Ka0EnopIXoJARMAhbARg7uNGSxvBqh4wcVwOxlpYwH4NqrIv9eA6Xryy2Z62BJKkdAxeFsA3UQGaoo4; user-key=8abc6212-d9b5-44ff-bc2c-ddd9e8be0554; ipLoc-djd=1-72-2799-0; unpl=V2_ZzNtbRdRFkJ8WBJSLxxUBmICRVpLVEIWJwwVAyseDgFuAEFUclRCFXwURldnGlUUZwIZXkVcRxVFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VHgcXAJlAhRYQWdzEkU4dlN9HVoNZTMTbUNnAUEpDERccx5USGcAF11FVUITcAt2VUsa; __jda=122270672.1241630742.1543824136.1545880963.1545964078.3; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_d7df8ae7e49240f68202c5bfa6c582b8|1545964077739; pinId=7i7kN8FksT-lGMqtUbaimQ; pin=49817795-598178; ceshi3.com=000; _tp=5PStYdOEJwZICWIaFuxuUQ%3D%3D; _pst=49817795-598178; cn=5; _gcl_au=1.1.730340221.1545964394; thor=868BA4D0E4372F9130214B99DAB50625903B38F62B09C4BFFE47A360066B6295AF2286835649C9BC0EEEA10E4D3BDE45417D3EC64FAEEB7A30A4D918DA20ECF70EB138078B097F1CDE60DFA73DE9283BAFE14E351C3A104B97A5938B40D73BF923C68F6A8F7E1D3AF3A6D470BB2C9FCB883981D5C5191432D91806B45D7E6AD1B342418803092685C52BD439BDD8F14E6723ACCE0916C39EEE017B7A9171BDCF; 3AB9D23F7A4B3C9B=5LFBQ2OIQGNALF4257ZN4K2W63PZ3AYMFTJ5TD5LNKU3G3QYXGREWS7J4XBXPOFPFGUOUTIBKPOC2FY4D465O7NOAA; shshshfp=26620f2aeddc936158d73d66697b4aff; shshshsID=ef24363d4037bc94ef352ce87cc44eaa_3_1545964456703; __jdb=122270672.6.1241630742|3.1545964078; shshshfpb=ow5Ddp1hdUuLFIWx0fLMELw%3D%3D; JSESSIONID=0372305F9FCCC2C53B077FD07DBD5F98.s1
pragma: no-cache
referer: https://item.jd.com/100000287113.html
user-agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
        """)
        json_data = requests.get(url, headers=headers).text
        comment = json.loads(json_data)
        return comment

    def save_data(self, comment):
        import pymysql
        conn = pymysql.connect(user='root', password='123', host='127.0.0.1', db='test')
        cursor = conn.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS phone_comment1(id INTEGER PRIMARY KEY AUTO_INCREMENT,comment VARCHAR (1000),username VARCHAR (50),create_time VARCHAR (50),productColor VARCHAR (10),phone_id VARCHAR (30))')
        for i in comment['comments']:
            cursor.execute(
                'INSERT INTO phone_comment1(comment,username,create_time,productColor,phone_id) VALUES (%s,%s,%s,%s,%s)',
                [i['content'], i['nickname'], i['creationTime'], i['productColor'], i['referenceId']])
        conn.commit()
        conn.close()

    def run_and_save(self, id):
        time1 = time.time()
        url_list = []
        num = 51
        for i in range(1, num):
            url = "https://sclub.jd.com/comment/productPageComments.action?productId="+str(id)+"&score=0&sortType=5&pageSize=10&page=" + str(
                i)
            url_list.append(url)
        pool = Pool(4)
        results = pool.map(self.get_json_thread, url_list)
        x = 0
        for comment in results:
            self.save_data(comment)
            x += 1
        print(f'共写入{x*10}条记录,耗时：{time.time()-time1}秒')


if __name__ == '__main__':
    pass
    # x = Jdcomment()
    # url_list = []
    # num = 21
    # for i in range(1, num):
    #     url = "https://sclub.jd.com/comment/productPageComments.action?productId=100002332162&score=0&sortType=5&pageSize=10&page="+ str(i)
    #     url_list.append(url)
    # pool = Pool(4)
    # time13 = time.time()
    # results = pool.map(x.get_json_thread, url_list)
    # for comment in results:
    #     x.save_data(comment)
    # print(f'多线程耗时：{time.time()-time13}')
    # pool.close()
    # pool.join()
    # time2 = time.time()
    # for url in url_list:
    #     results2 = x.get_json_thread(url)
    #     x.save_data(results2)
    # print(f'单线程耗时：{time.time()-time2}')
