import math
import os
import time
import re
from collections import defaultdict
import multiprocessing as mp
from pathlib import Path

import glob
import requests
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
from urllib import request
from urllib import error


os.chdir('../')
root_dir = Path.cwd()
data_dir = root_dir.joinpath('data')
result_dir = root_dir.joinpath('result')
if not result_dir.exists():
  result_dir.mkdir()

if not data_dir.exists():
  data_dir.mkdir()


def getHTMLText(url):
  headers = {
      "User-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
  try:
    r = request.urlopen(url).read().decode("utf-8")
    r = r.encode("utf-8").decode("unicode_escape")
    return r
  except:
    return '产生异常'


def getQianxiIndex(url, date, n):
  if n == 1:
    html = getHTMLText(url)
    pat = '"list":({.*?})'
    Idxinfo = eval(re.compile(pat).findall((html))[0])
    return float(Idxinfo[date])
  elif n == 2:

    try:
      html = getHTMLText(url)
      pat = '"list":({.*?})'
      Idxinfo = eval(re.compile(pat).findall((html))[0])
      return float(Idxinfo[date])
    except:
      return ""


def getQianxiValue(cityid, date, drt):

  urlQx = 'http://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id=' + cityid + \
      '&type=move_' + drt + '&date=' + date + '&callback=jsonp_1611660576001_3225993'

  try:
    n = 1
    urlIdx = 'http://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id=' + \
        cityid + '&type=move_' + drt + '&callback=jsonp_1611660574799_4280213'
    qianxiIdx = getQianxiIndex(urlIdx, date, n)
  except:
    n = 2
    urlIdx = 'http://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id=' + \
        cityid + '&type=move_' + drt + '&callback=jsonp_1611660574799_4280213'
    qianxiIdx = getQianxiIndex(urlIdx, date, n)
  html = getHTMLText(urlQx)
  # print(html)
  Drt = {'in': '迁入', 'out': '迁出'}
  try:
    pat = '{"city_name":"(.*?)","province_name":"(.*?)","value":(.*?)}'
    cityinfo = re.compile(pat).findall(html)
    if drt == 'out':
      info_dict = {'date': [date] * len(cityinfo),
                   'city_code': [cityid] * len(cityinfo),
                   'from_city': [IdProCity[int(cityid)][1]] * len(cityinfo),
                   'from_province': [IdProCity[int(cityid)][0]] * len(cityinfo),
                   'to_city': [i[0] for i in cityinfo],
                   'to_province': [i[1] for i in cityinfo],
                   'percent': [float(i[2]) for i in cityinfo],
                   'index': [float(qianxiIdx) * 10000] * len(cityinfo)}
    elif drt == 'in':
      if len(cityinfo) > 0:
        info_dict = {'date': [date] * len(cityinfo),
                     'city_code': [cityid] * len(cityinfo),
                     'tar_city': [IdProCity[int(cityid)][1]] * len(cityinfo),
                     'tar_province': [IdProCity[int(cityid)][0]] * len(cityinfo),
                     'origin_city': [i[0] for i in cityinfo],
                     'origin_province': [i[1] for i in cityinfo],
                     'percent': [float(i[2]) for i in cityinfo],
                     'index': [float(qianxiIdx) * 10000] * len(cityinfo)}
    df = pd.DataFrame(info_dict)
    itertime = time.time()
    print('————— 爬取地区(%s):%s,日期:%s,累计耗时:%s,已进行%s' %
          (Drt[drt], IdProCity[int(cityid)][1], date, str(itertime - starttime), str(cityidList.index(cityid) + 1) + '/' + str(len(cityidList))))
    return df
  except:
    itertime = time.time()
    Errorfile = './QxData/Error/' + date + '_' + drt
    print('***异常*** 爬取地区(%s):%s,日期:%s,累计耗时:%s,已进行%s' %
          (Drt[drt], IdProCity[int(cityid)][1], date, str(itertime - starttime), str(cityidList.index(cityid) + 1) + '/' + str(len(cityidList))))
    with open(Errorfile, 'a') as f:
      f.write(IdProCity[int(cityid)][1] + '\n')


def getCityDict(file):
  df = pd.read_csv(file)
  IdProCity = {i: (j, k) for i, j, k in zip(
      df['city_code'], df['province'], df['city'])}
  cityidList = [str(i) for i in list(df['city_code'])]
  return IdProCity, cityidList


if __name__ == "__main__":
  IdProCity, cityidList = getCityDict('./data/Citycode.csv')
  dateList = [str(i.date()).replace('-', '') for i in pd.date_range(
      start='2020-01-10', end='2020-03-15 ', freq='D')]
  print(dateList)
  directions = ['out', 'in']
  starttime = time.time()
  pool = mp.Pool(processes=2)
  for drt in directions:
    dflist = []
    for date in dateList:
      lst = pool.starmap(
          getQianxiValue, [(cityid, date, drt) for cityid in cityidList])
      for i in lst:
        dflist.append(i)
    try:

      df = pd.concat(dflist)
      outfile = dateList[0] + '_' + dateList[-1] + '_' + drt + '.csv'
      df.to_csv(data_dir / (outfile), index=False, encoding='utf-8-sig')
    except:
      print("存在异常")

  pool.close()
  pool.join()
