import math
import os
import time
from collections import defaultdict
from collections import OrderedDict

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import statsmodels
from scipy import stats
from statsmodels.formula.api import ols
from pathlib import Path

os.chdir('../')
root_dir = Path.cwd()
figures_dir = root_dir.joinpath('./figures')

if not figures_dir.exists():
  figures_dir.mkdir()


def polyfit(x, y, degree):
  results = {}
  coeffs = np.polyfit(x, y, degree)
  results['polynomial'] = coeffs.tolist()
  p = np.poly1d(coeffs)
  yhat = p(x)
  ybar = np.sum(y) / len(y)
  ssreg = np.sum((yhat - ybar)**2)
  sstot = np.sum((y - ybar)**2)
  results['determination'] = ssreg / sstot
  return results


def DrawPlot(Index, Value, out_fig):
  x_mean = np.mean(Index)
  y_mean = np.mean(Value)
  data = pd.DataFrame({'x': Index, 'y': Value})
  model = ols('y~x', data).fit()
  p_test = float(model.pvalues['x'])
  R2 = (polyfit(Index, Value, 1)['determination'])
  m1 = 0
  m2 = 0
  for x_i, y_i in zip(Index, Value):
    m1 += (x_i - x_mean) * (y_i - y_mean)
    m2 += (x_i - x_mean)**2

  a = m1 / m2
  b = y_mean - a * x_mean
  plt.text(0, 450, r'$\mathit{R}$' + r'$^2$=%.2f,' % (R2) +
           r'$\mathit{p}$' + r'<%.2f1' % (p_test), size=8, fontdict={'family': 'arial'})
  y_line = a * np.array(Index) + b

  n = 0
  for i, j in zip(Index, Value):
    if j > 300:
      size = 200
      plt.scatter(i, j, s=size, color='lightgreen',
                  edgecolor='black', alpha=0.4, label=str(300))
    elif j > 100:
      size = 100
      plt.scatter(i, j, s=size, color='lightgreen',
                  edgecolor='black', alpha=0.4, label=str(100))
    elif j > 50:
      size = 50
      plt.scatter(i, j, s=size, color='lightgreen',
                  edgecolor='black', alpha=0.4, label=str(50))
    else:
      size = 10
      plt.scatter(i, j, s=size, color='lightgreen',
                  edgecolor='black', alpha=0.4, label=str(10))
    n += 1
    if n <= 17:
      plt.text(i, j - 20, Cityname[flowCity[i]].title(), size=6,
               ha='center', fontdict={'family': 'arial'})
  plt.plot(Index, y_line, color='black', alpha=0.7)
  plt.xlabel(r'N$_\mathit{inflow}$', fontdict={
      'family': 'arial', 'size': 10})
  plt.ylabel(r'N$_\mathit{cases}$', fontdict={
      'family': 'arial', 'size': 10})
  plt.yticks(fontproperties='arial', size=8)
  plt.xticks(fontproperties='arial', size=8)

  handles, labels = plt.gca().get_legend_handles_labels()
  by_label = OrderedDict(zip(labels, handles))
  legend = plt.legend(by_label.values(), by_label.keys(), loc=4, prop={
      'family': 'arial', 'size': 8}, frameon=False, title='Number of cases')
  legend.get_title().set_fontsize(fontsize=8)
  plt.grid(axis='x', linestyle='-', c='lightgrey', alpha=0.6, linewidth=1)
  plt.grid(axis='y', linestyle='-', c='lightgrey', alpha=0.6, linewidth=1)
  plt.savefig(figures_dir / (out_fig), dpi=300)
  plt.close()
  # plt.show()


if __name__ == "__main__":

  CityShift = {'拉萨': '拉萨市', '合肥': '合肥市', '红河州': '红河哈尼族彝族自治州', '滁州': '滁州市',
               '德宏州': '德宏傣族景颇族自治州', '黔南州': '黔南布依族苗族自治州',
               '甘孜州': '甘孜藏族自治州', '湘西自治州': '湘西土家族苗族自治州', '亳州': '亳州市',
               '昌江县': '昌江黎族自治县', '六盘水': '六盘水市', '甘南州': '甘南藏族自治州',
               '台湾': '花莲县', '六安': '六安市', '宿州': '宿州市', '恩施州': '恩施土家族苗族自治州',
               '秦皇岛': '秦皇岛市', '淮南': '淮南市',
               '伊犁州': '伊犁哈萨克自治州', '临夏州': '临夏回族自治州', '乐东县': '乐东黎族自治县',
               '黔东南州': '黔东南苗族侗族自治州', '兵团第八师石河子市': '石河子市', '阜阳': '阜阳市',
               '铜陵': '铜陵市', '蚌埠': '蚌埠市', '黔西南州': '黔西南布依族苗族自治州', '安庆': '安庆市',
               '阿坝州': '阿坝藏族羌族自治州', '马鞍山': '马鞍山市',
               '黄山': '黄山市', '延边州': '延边朝鲜族自治州', '芜湖': '芜湖市', '琼中县': '琼中黎族苗族自治县',
               '西双版纳州': '西双版纳傣族自治州', '凉山州': '凉山彝族自治州', '宣城': '宣城市', '池州': '池州市',
               '淮北': '淮北市', '大理州': '大理白族自治州'}

  dfId = pd.read_csv('./data/Citycode.csv')
  Cityname = {i: j for i, j in zip(dfId['city'], dfId['name'])}
  CityPro = {i: j for i, j in zip(dfId['city'], dfId['province'])}

  df_flow = pd.read_csv('./data/Corr_wuhan_20200117-20200123.csv')
  df_case = pd.read_csv('./data/city_20200124-20200130.csv', index_col=0)
  df_case.rename(index=CityShift, inplace=True)

  citys_1 = ['荆门市', '黄石市', '咸宁市', '宜昌市', '孝感市', '随州市', '恩施土家族苗族自治州',
             '潜江市', '仙桃市', '天门市', '神农架林区', '荆州市', '鄂州市', '黄冈市', '襄阳市', '十堰市']
  citys_2 = []

  cities = list(df_case.index)

  dropcitys = list(set(cities) - set(citys_1))
  df_case_1 = df_case.drop(dropcitys, axis=0)
  flow = {i: j for i, j in zip(df_flow['to_city'], df_flow['flow'])}
  case = {i: j for i, j in zip(list(df_case_1.index), df_case_1['case'])}
  flowCity = {i: j for i, j in zip(df_flow['flow'], df_flow['to_city'])}
  Index = []
  Value = []
  Adict = defaultdict(dict)
  for i in case.keys():
    if i in flow and case[i] >= 1:
      Adict['case'].update({i: case[i]})
      Adict['flow'].update({i: flow[i]})
      Index.append(flow[i])
      Value.append(case[i])
  DrawPlot(Index, Value, 'qianxi_case_correlation_InHubei.png')

  df_case_2 = df_case.drop(citys_1, axis=0)
  flow = {i: j for i, j in zip(df_flow['to_city'], df_flow['flow'])}
  case = {i: j for i, j in zip(list(df_case_2.index), df_case_2['case'])}
  flowCity = {i: j for i, j in zip(df_flow['flow'], df_flow['to_city'])}
  Index = []
  Value = []
  Adict = defaultdict(dict)
  for i in case.keys():
    if i in flow and case[i] >= 1:
      Adict['case'].update({i: case[i]})
      Adict['flow'].update({i: flow[i]})
      Index.append(flow[i])
      Value.append(case[i])
  DrawPlot(Index, Value, 'qianxi_case_correlation_OutHubei.png')
