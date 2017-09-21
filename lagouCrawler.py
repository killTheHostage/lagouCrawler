#!/usr/bin/python
# #coding:utf-8

import requests
import time
import urllib
import re

class crawler_lagou:


    def get_json(self, url,cookies, page):
        global lagou_data
        data = {'first': 'true', 'pn': page, 'kd': ''}
        html = requests.post(url, data,headers = self.header,cookies = cookies)
        json = html.json()
        now_page = json['content']['pageNo']
        global counts
        if(now_page == page):
            if(json['success']):
                list_con = json['content']['positionResult']['result']
                for work in list_con:
                    counts += 1
                    salary_re = '(.*?)k-(.*?)k'
                    salary_t = re.findall(salary_re,work['salary'].lower())
                    if(salary_t == []):
                        salary = '0'
                    else:
                        salary = str(int(salary_t[0][0]) * 1000) + ',' + str(int(salary_t[0][1]) * 1000)
                    workYear_re = '\\d+'
                    workYear_t = re.findall(workYear_re,work['workYear'])
                    if workYear_t == []:
                        workYear_t.append('0')
                    workYear = ','.join(workYear_t)
                    lagou_data.writelines(work['createTime'] + '\t' + work['positionName'] + '\t' + workYear + '\t' + work['education'] + '\t' + salary + '\t' + work['city'] + '\t' + work['companyFullName'] + '\t' + work['secondType'] + '\n')
            else:
                print(json['msg'])
            return True
        return False

    def get_cookies(self):
        print("now is getting cookies,please wait")
        c = requests.cookies.RequestsCookieJar()
        c1 = requests.get('https://www.lagou.com/jobs/list_ios?labelWords=&fromSearch=true&suginput=',headers = header)
        c2 = requests.get('http://a.lagou.com/collect?v=1&_-v=j31&a=1891258726&t=pageview&_s=1&dl=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%3Fcity%3D%25E5%2585%25A8%25E5%259B%25BD%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D&ul=zh-cn&de=UTF-8&dt=%E6%89%BE%E5%B7%A5%E4%BD%9C-%E4%BA%92%E8%81%94%E7%BD%91%E6%8B%9B%E8%81%98%E6%B1%82%E8%81%8C%E7%BD%91-%E6%8B%89%E5%8B%BE%E7%BD%91&sd=24-bit&sr=1920x1080&vp=1251x789&je=0&_u=MEAAAAQBK~&jid=1821275559&cid=974360180.1503408423&tid=UA-41268416-1&_r=1&z=117414640',headers = header)
        c.set('user_trace_token', c1.cookies['user_trace_token'], path='/', domain='www.lagou.com')
        c.set('LGUID', c2.cookies['LGUID'], path='/', domain='.lagou.com')
        c.set('JSESSIONID', c1.cookies['JSESSIONID'], path='/', domain='.lagou.com')
        return c

    def get_all_city(self):
        print("now is getting city list,please wait")
        city_html = requests.get(self.city_url, None, headers = self.header).text
        xpath_str = "//ul[@class='city_list']/li/a/text()"
        city_dom_tree = etree.HTML(city_html)
        city_set = city_dom_tree.xpath(xpath_str)
        return city_set

    def make_url(self, city, job):
        return self.basic_url + '&hy=' + job + '&city=' + city

    def main_control(self):
        global lagou_data
        global counts
        city_set = self.get_all_city()
        cookies = self.get_cookies()
        for i in range(121,161):
            city = city_set[i]
            info_page = 1
            for job in self.job_set:
                time.sleep(2)
                search_url = self.make_url(city,job)
                while(self.get_json(search_url,cookies,info_page)):
                    print("city is " + city + " jobLabel is " + job + " page is on " + str(info_page))
                    print('---------------------------------------------------------')
                    info_page += 1
                    lagou_data.flush()
                info_page = 1
                time.sleep(1)
            print("city " + city + " end,now data count is " + str(counts) + ' columns is ' + str(i))
            print('---------------------------------------------------------')
        lagou_data.close()
        return

    def __init__(self):
        self.main_control()
