#!/usr/bin/env python
# coding: utf-8

'''
导出数据'''
from __future__ import unicode_literals

import math
from urllib import quote
from datetime import datetime, date, timedelta

import xlwt
import gevent
import requests
from gevent import monkey
from gevent.pool import Pool
monkey.patch_all()  # noqa

import config
from mail import mail_multipart

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) '
      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 '
      'Safari/537.36')

category2param = {
    0: 'NETWORK_DRAMA',
    1: 'NETWORK_MOVIE',
    2: 'NETWORK_VARIETY',
    3: 'TV_DRAMA',
    4: 'ANIME',
}

category2sheet_name = {
    0: u'网络剧',
    1: u'网络大电影',
    2: u'网络综艺',
    3: u'电视剧',
    4: u'网络动漫',
}


class HttpClient(object):

    def __init__(self, tries=5):
        assert 1 <= tries < 10
        self.session = requests.Session()
        self.tries = tries

    def fetch(self, url, method='GET', data=None, **options):
        req = requests.Request(
            method,
            url,
            data=data,
            headers=options.get('headers'),
            cookies=options.get('cookies'))
        req = self.session.prepare_request(req)
        req.headers['Date'] = datetime.now().strftime(
            '%a, %d %b %Y %H:%M:%S GMT')
        req.headers['User-Agent'] = UA
        for i in range(self.tries):
            try:
                resp = self.session.send(req)
            except:
                gevent.sleep(0.5)
                continue
            if resp:
                break
        else:
            raise StandardError(u'网络请求失败.')
        return resp


def export_data(date):
    xls_name = u'%s 影视统计分析表.xls' % str(date)
    workbook = xlwt.Workbook(encoding='utf-8')
    pool = Pool(5)
    for i in range(5):
        pool.spawn(process_items, workbook, date, i)
    pool.join()
    workbook.save(xls_name)
    return xls_name


def standardizing(play_count_text):
    last_idx = 0
    play_count = 0.0
    if u'亿' in play_count_text:
        idx = play_count_text.index(u'亿')
        play_count = \
            play_count + float(play_count_text[:idx]) * 10000
        last_idx = idx + 1
    if u'万' in play_count_text:
        idx = play_count_text.index(u'万')
        play_count = \
            play_count + float(play_count_text[last_idx:idx])
    return int(play_count)


def process_items(workbook, date, category):
    assert 0 <= category <= 4
    param = category2param[category]
    sheet_name = category2sheet_name[category]
    client = HttpClient()
    api_url = 'http://d.guduomedia.com/m/show/billboard?type=0&category=%s&date=%s' % (param, date)  # noqa
    items = client.fetch(api_url).json()
    if not isinstance(items, list):
        raise StandardError(u'数据未更新')
    sheet = workbook.add_sheet(sheet_name)
    headers = [
        u'排名', u'剧名', u'平台', u'播放量（万）',
        u'累计播放量（万）', u'上线天数', u'名次变动',
    ]
    for i, header in enumerate(headers):
        sheet.write(0, i, header)
    for i, item in enumerate(items, 1):
        name = item['name']
        detail_url = 'http://d.guduomedia.com/m/show/few_play_count/%s' \
            % quote(name.encode('utf-8'))
        detail_info = client.fetch(detail_url)
        play_count = detail_info.json()['total_play_count']
        increase_count = int(item['increaseCount'])
        rise, rise_text = int(item['rise']), ''
        if rise >= 3:
            rise_text = u'上升%d' % rise
        elif rise <= -3:
            rise_text = u'下降%d' % abs(rise)
        sheet.write(i, 0, str(i))
        sheet.write(i, 1, name)
        sheet.write(i, 2, item['platformName'])
        sheet.write(i, 3, int(math.ceil(increase_count/10000.0)))
        sheet.write(i, 4, str(standardizing(play_count)))
        sheet.write(i, 5, item['days'])
        sheet.write(i, 6, rise_text)

if __name__ == '__main__':
    yesterday = date.today() - timedelta(days=2)
    xls_name = export_data(yesterday)
    mail = dict()
    mail['to'] = config.RECEIPTS
    mail['attach'] = xls_name
    mail['subject'] = u'影视剧分析统计邮件'
    mail_multipart(mail)
