# coding:utf-8
__author__ = 'ym'
import requests
from CrawlerUtility import ChromeHeaders2Dict
from lxml.html import fromstring
import json
import time
import pymysql


class Jd_spider(object):

    def __init__(self):
        self.header = """
        :authority: search.jd.com
:method: GET
:path: /Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&suggest=1.his.0.0&wq=&pvid=3fa6cf05bc7b4ed883850597889bf9cb
:scheme: https
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
cache-control: no-cache
cookie: __jdc=122270672; __jdu=1241630742; PCSYCityID=412; shshshfpa=55b0af51-02c3-1e40-a310-1c57890f85e9-1545875426; user-key=8abc6212-d9b5-44ff-bc2c-ddd9e8be0554; xtest=8923.cf6b6759; ipLoc-djd=1-72-2799-0; rkv=V0600; qrsc=3; pinId=7i7kN8FksT-lGMqtUbaimQ; pin=49817795-598178; ceshi3.com=000; _tp=5PStYdOEJwZICWIaFuxuUQ%3D%3D; _pst=49817795-598178; cn=5; mt_xid=V2_52007VwMRV11fUFsZTBpsBTQAGlNfXFNGFkgRCxliVhIFQQgGWhtVTV8DYAEVBlUKBgkdeRpdBW8fE1JBWVBLH00SXQJsAhRiX2hSahxBGFwDYwoRUG1YV1wY; unpl=V2_ZzNtbRIEQ0YgD0BTcxhbUGIGFQgSV0sXdFwWBngfVFE1ABsIclRCFX0UR1RnGFgUZwIZX0ZcQhJFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHsaWQVgARNbR1RzJXI4dmR8H1oFYgQiXHJWc1chVENUfRpUAyoDEVhCUEEUcw1FZHopXw%3d%3d; __jda=122270672.1241630742.1543824136.1546498960.1546655783.8; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_ab1bd676906d446da1930eac279ec28d|1546655782633; shshshfpb=ia%2Fipmkq%20uEmaWGI9vABqmw%3D%3D; shshshfp=850d6ace5efa78fd1bd375293fae9892; wlfstk_smdl=oyyx8u2bn6u48y20xb30kh0zfn74qtge; TrackID=1yFzo9hVXDb5sYmjz88m7mDTBOQiU9-8wSxDCsvsfozupChP6b0txJSpDBryynDnB1Hd7vBHjG2TGDGtJ4afKX-WsILItKfiNzwrXuvBaOPI; thor=9E80B4267F722B17DE5385E2D532B08A5BA85E511D0BB02FC5A68E03263DEBC93CB503E873F38980439324F13AFB698048A2E43E5429762E899F3EDA5C09434CE568260D132CF84EE6A283C4C767B51ECF6EEF3487406D2F3B5EE33FFDDA1C1EC57875A443E6EAE91912927CF1965844A0CCA6C78519208274D68ABF910F14308A631DE89546DD694A0FAFBB725E8F0C955F3434194F78BF0C61C7B0A0FC391E; __jdb=122270672.6.1241630742|8.1546655783; shshshsID=d7f655406d676904e5d96bc8bcef842b_4_1546655870297; 3AB9D23F7A4B3C9B=IDED2DFPH3K5BOI7I7TKDOSOEHN4R2EZHM5IT5DZOFB6SANC525KYQ3RYPWVBM6OCJJ7UB7BQU2BUDWSMNKYCJ63ZU
pragma: no-cache
referer: https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fsearch.jd.com%2FSearch%3Fkeyword%3D%25E6%2589%258B%25E6%259C%25BA%26enc%3Dutf-8%26suggest%3D1.his.0.0%26wq%3D%26pvid%3D3fa6cf05bc7b4ed883850597889bf9cb
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
        """
        self.headers = ChromeHeaders2Dict(self.header)
        self.conn = pymysql.connect(user='root', password='123', db='test')
        self.cursor = self.conn.cursor()

    def get_phone_1(self, page_num):
        """获取前三十条数据
        :return：phone_name_list,product_id_list price_list
        """
        url = 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=' + str(page_num*2-1)
        html_1 = requests.get(url, headers=self.headers).content.decode('utf-8')
        dom_1 = fromstring(html_1)
        product_id_list = dom_1.xpath('//*[@id="J_goodsList"]/ul/li/@data-sku')
        phone_name_list1 = dom_1.xpath('//*[@id="J_goodsList"]/ul/li/div/div[4]/a/em')
        price_list = dom_1.xpath('//*[@id="J_goodsList"]/ul/li/div/div[3]/strong/i/text()')
        img_list = dom_1.xpath('//li[@class="gl-item"]/div[@class="gl-i-wrap"]/div[@class="p-img"]/a/img/@source-data-lazy-img')
        phone_name_list = []
        for phone_name in phone_name_list1:
            phonename = phone_name.xpath('string(.)')  # 使用关键字string(.)把em标签下所有字符串合并成一项。
            phone_name_list.append(phonename)  # 添加到list1列表返回
        phone_data = []
        for i in range(len(phone_name_list)):
            # 拼接成字典，添加phone_data列表中作为返回值
            imgurl = 'http:' + img_list[i]
            phone_data.append({'name': phone_name_list[i], 'price': price_list[i], 'phone_id': product_id_list[i], 'img_url': imgurl})
        return phone_data

    def get_phone_2(self, page_num):
        """获取后三十条数据
        :return：phone_name_list,product_id_list price_list
        """
        time_sign = "%.5f" % time.time()
        url = "https://search.jd.com/s_new.php?"
        params = {
            'keyword': '手机',
            'enc': 'utf-8',
            'qrst': '1',
            'rt': '1',
            'stop': '1',
            'vt': '2',
            'wq': '%E6%89%8B%E6%9C%BA',
            'cid2': '65',
            'cid3': '655',
            'page': 2*page_num,
            's': str(48*1-20),
            'scrolling': 'y',
            'log_id': time_sign,
        }
        headers = {
            'authority': 'search.jd.com',
            'method': 'GET',
            'path': '/im.php?r=1000584726&t=1545893804.4034&cs=73b49de6c0173b329039f16acff38f17',
            'scheme': 'https',
            'referer': 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=1&s=1&click=0',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'Cookie': '__jdu=1001003686; unick=DoubleKill123; pin=18736121873_p; _tp=AqZVwquCFN%2BkQt5wImXqJQ%3D%3D; pinId=nZ9v9v-23C49OvzpU1CgCQ; PCSYCityID=412; shshshfpa=caef170b-6664-8d60-208e-d3dc47479bd6-1545874760; __jdc=122270672; cn=0; user-key=4836ddac-15c8-4e6f-a17d-2402ff4d211a; xtest=1275.cf6b6759; ipLoc-djd=1-72-2799-0; shshshfpb=b8Eytj7NvElOV%2BsenFBKQaQ%3D%3D; rkv=V0300; qrsc=3; unpl=V2_ZzNtbRVfRRB9X0YHfBgOBGJRFwoRUxcXfFhHUnxJCQFgAEJbclRCFXwURldnGloUZwcZWEVcQRZFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VHoYXARmARVURWdzEkU4dld6HloHYzMTbUNnAUEpCEJTchhVSGcCE11DVkESfA92VUsa; __jdv=122270672|baidu|-|organic|not set|1545896793922; shshshfp=374d8b27315c2317cc4a68414503a923; 3AB9D23F7A4B3C9B=C5RLFPEU7JJC5L4PDAVFPJLXA57BF5I5EY3LZU5EIRGHNW55MWCARFEPIIPJKKYBHF5MBYEHT3VLPJIYXSITJ6RBAM; __jda=122270672.1001003686.1537348325.1545896794.1545903985.10; __jdb=122270672.1.1001003686|10.1545903985; shshshsID=b623b2c242b248c23b5ce05751697634_1_1545903985623; thor=664A4B3DDB726BF35FDFF9D648250549B1E7A67DA61ACE8C4D4152E83B4A117A95084BCCF5B088455F086AF2E45C90EB12E8380D7AAD6EE50A9761F818AF030F791B9A892B4BDE282341217C7782B3FA1529FCE71AA7363868657D5D14CE00447D1EA85C552F4AE556EF0D7911ECBDCB62F7A728A1ADA96FFCCA5CAD362C8AA4CB15264A4A80BDBEC1480F449AD91095'
        }
        html_2 = requests.get(url, headers=headers, params=params).text
        dom_2 = fromstring(html_2)
        product_id_list = dom_2.xpath('//li[@class="gl-item"]/@data-sku')
        phone_name_list1 = dom_2.xpath('//div[@class="p-name p-name-type-2"]/a/em')  # 因为em标签下不只一项，直接使用text()方法，会取到多项。
        price_list = dom_2.xpath('//div[@class="p-price"]/strong/i/text()')
        img_list = dom_2.xpath('//li[@class="gl-item"]/div[@class="gl-i-wrap"]/div[@class="p-img"]/a/img/@source-data-lazy-img')
        phone_name_list = []
        for phone_name in phone_name_list1:
            phonename = phone_name.xpath('string(.)')  # 使用关键字string(.)把em标签下所有字符串合并成一项。
            phone_name_list.append(phonename)  # 添加到list1列表返回
        phone_data = []
        for i in range(len(phone_name_list)):
            imgurl = 'http:' + img_list[i]
            phone_data.append({'name': phone_name_list[i], 'price': price_list[i], 'phone_id': product_id_list[i], 'img_url': imgurl})
        return phone_data

    def get_product_id(self):
        header = """
        :authority: club.jd.com
:method: GET
:path: /comment/productCommentSummaries.action?referenceIds=7920226,5089253,5853579,7694047,8735304,100001172674,7081550,7437788,100000773889,100000727128,7437564,7321794,8895275,100000822981,5089267,100000971366,100002332162,6735790,5089275,8790545,100000287133,100000982034,8051124,39091300529,100001790805,100001906474,100002433330,100000650837,7479810,6940276&callback=jQuery3003383&_=1546655970774
:scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
cache-control: no-cache
cookie: __jdc=122270672; __jdu=1241630742; PCSYCityID=412; shshshfpa=55b0af51-02c3-1e40-a310-1c57890f85e9-1545875426; user-key=8abc6212-d9b5-44ff-bc2c-ddd9e8be0554; ipLoc-djd=1-72-2799-0; pinId=7i7kN8FksT-lGMqtUbaimQ; pin=49817795-598178; ceshi3.com=000; _tp=5PStYdOEJwZICWIaFuxuUQ%3D%3D; _pst=49817795-598178; cn=5; mt_xid=V2_52007VwMRV11fUFsZTBpsBTQAGlNfXFNGFkgRCxliVhIFQQgGWhtVTV8DYAEVBlUKBgkdeRpdBW8fE1JBWVBLH00SXQJsAhRiX2hSahxBGFwDYwoRUG1YV1wY; unpl=V2_ZzNtbRIEQ0YgD0BTcxhbUGIGFQgSV0sXdFwWBngfVFE1ABsIclRCFX0UR1RnGFgUZwIZX0ZcQhJFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHsaWQVgARNbR1RzJXI4dmR8H1oFYgQiXHJWc1chVENUfRpUAyoDEVhCUEEUcw1FZHopXw%3d%3d; __jda=122270672.1241630742.1543824136.1546498960.1546655783.8; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_ab1bd676906d446da1930eac279ec28d|1546655782633; shshshfpb=ia%2Fipmkq%20uEmaWGI9vABqmw%3D%3D; shshshfp=850d6ace5efa78fd1bd375293fae9892; wlfstk_smdl=oyyx8u2bn6u48y20xb30kh0zfn74qtge; TrackID=1yFzo9hVXDb5sYmjz88m7mDTBOQiU9-8wSxDCsvsfozupChP6b0txJSpDBryynDnB1Hd7vBHjG2TGDGtJ4afKX-WsILItKfiNzwrXuvBaOPI; thor=9E80B4267F722B17DE5385E2D532B08A5BA85E511D0BB02FC5A68E03263DEBC93CB503E873F38980439324F13AFB698048A2E43E5429762E899F3EDA5C09434CE568260D132CF84EE6A283C4C767B51ECF6EEF3487406D2F3B5EE33FFDDA1C1EC57875A443E6EAE91912927CF1965844A0CCA6C78519208274D68ABF910F14308A631DE89546DD694A0FAFBB725E8F0C955F3434194F78BF0C61C7B0A0FC391E; 3AB9D23F7A4B3C9B=IDED2DFPH3K5BOI7I7TKDOSOEHN4R2EZHM5IT5DZOFB6SANC525KYQ3RYPWVBM6OCJJ7UB7BQU2BUDWSMNKYCJ63ZU; __jdb=122270672.7.1241630742|8.1546655783; shshshsID=d7f655406d676904e5d96bc8bcef842b_5_1546655970278
pragma: no-cache
referer: https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&suggest=1.his.0.0&wq=&pvid=3fa6cf05bc7b4ed883850597889bf9cb
user-agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
        """
        headers = ChromeHeaders2Dict(header)
        url = "https://club.jd.com/comment/productCommentSummaries.action"
        params = {
            'referenceIds': '7920226,5089253,5853579,7694047,8735304,100001172674,7081550,7437788,100000773889,100000727128,7437564,7321794,8895275,100000822981,5089267,100000971366,100002332162,6735790,5089275,8790545,100000287133,100000982034,8051124,39091300529,100001790805,100001906474,100002433330,100000650837,7479810,6940276',
            '_': '1546655970774'
        }
        comment_json = requests.get(url, headers=headers, params=params).text
        comment_dict = json.loads(comment_json)
        return comment_dict['CommentsCount']

    def save_db(self, phone_data):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS phone
        (
        id INT PRIMARY KEY AUTO_INCREMENT,
        phone_name VARCHAR (200),
        price VARCHAR (20),
        phone_id VARCHAR (50),
        img_url VARCHAR (200)
        )""")
        for i in phone_data:
            self.cursor.execute("INSERT INTO phone(phone_name, price, phone_id, img_url) VALUES (%s,%s,%s,%s)", [i['name'], i['price'], i['phone_id'], i['img_url']])

    def run_and_save(self, PAGE_AMOUNT):
        """
        运行爬虫并保存数据
        :param PAGE_AMOUNT:
        :return:
        """
        for page_num in range(PAGE_AMOUNT):
            try:
                page = page_num+1
                print(f'正在保存第{page}页前30条数据')
                phone_data = self.get_phone_1(page)
                self.save_db(phone_data)
                print(f'正在保存第{page}页后30条')
                phone_data2 = self.get_phone_2(page)
                self.save_db(phone_data2)
                time.sleep(1.25)
            except Exception as e:
                print(f'出现异常：{e}')
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    jd = Jd_spider()
    PAGE_AMOUNT = 50
    jd.run_and_save(PAGE_AMOUNT)
