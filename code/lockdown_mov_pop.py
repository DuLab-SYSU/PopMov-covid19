from __future__ import (absolute_import, division, print_function)
from collections import defaultdict
import random
import sys
import os

import pandas as pd
import numpy as np
import matplotlib.colors
from pylab import *
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon
import networkx as nx
from pathlib import Path

os.chdir('../')

root_dir = Path.cwd()
figures_dir = root_dir.joinpath('figures/example_figures')

if not figures_dir.exists():
  figures_dir.mkdir()


def Standard(alist):
  vmin = min(alist)
  vmax = max(alist)
  alist = [np.sqrt((i - vmin) / (vmax - vmin)) for i in alist]
  return alist


if __name__ == "__main__":
  fig, ax = plt.subplots(figsize=(12, 4))
  dfpop = pd.read_csv('./data/2012SHP_2010census_2016CDCPop_adm2.csv')
  dfpop['city_code'] = [int(i / 100)
                        for i in dfpop['SHP_CITY_CODE']]
  IdPop = {i: j for i, j in zip(dfpop['city_code'], dfpop['TOTAL_POP2015'])}
  IdPop[420100] = 11000000
  Idlist = list(dfpop['city_code']) + [420100]
  dfId = pd.read_csv('./data/Citycode.csv')
  IdCity = {i: j for i, j in zip(dfId['city_code'], dfId['city'])}
  Idname = {i: j for i, j in zip(dfId['city_code'], dfId['name'])}

  IdPro = {i: j for i, j in zip(dfId['city_code'], dfId['province'])}

  df = pd.read_csv('./data/20200101-20200214_out.csv')
  dl = [i for i in range(20200101, 20200132)] + \
      [i for i in range(20200201, 20200215)]
  df = df[df['date'].isin(dl)]
  df19 = pd.read_csv('./data/20190112-20190301-out.csv')
  df19['province'] = [IdPro[i] for i in df19['city_code']]
  df = df[df['from_province'].str.contains('湖北')]
  df19 = df19[df19['province'].str.contains('湖北')]
  df['only'] = [str(i) + str(j) + str(m)
                for i, j, m in zip(df['date'], df['city_code'], df['qianxi_index'])]
  df.drop_duplicates(subset=['only'], keep='first', inplace=True)

  City_DateIndex = defaultdict(dict)
  for i, j, m in zip(df['city_code'], df['date'], df['qianxi_index']):
    City_DateIndex[i].update({str(j): m})
  City_DateIndex_19 = defaultdict(dict)
  for i, j, m in zip(df19['city_code'], df19['date'], df19['qianxi_index']):
    City_DateIndex_19[i].update({str(j): m})
  Index = [str(i) for i in range(20200101, 20200132)] + [str(i)
                                                         for i in range(20200201, 20200215)]
  IndexShift = ['Jan ' + str(i)[-2:] for i in range(20200101, 20200132)] + \
      ['Feb ' + str(i)[-2:] for i in range(20200201, 20200215)]
  IndexShift = {i: j for i, j in zip(Index, IndexShift)}
  for x, y in City_DateIndex.items():
    if x == 420100:
      Value20, Value19 = [], []
      for i in Index:
        Value20.append(City_DateIndex[x][i])
        Value19.append(City_DateIndex_19[x][i])
        if City_DateIndex_19[x][i] > City_DateIndex[x][i]:
          print(i, ':19大', City_DateIndex_19[x][i], City_DateIndex[x][i])
        else:
          print(i, ':20大', City_DateIndex_19[x][i], City_DateIndex[x][i])
      Value = [i - j for i, j in zip(Value20, Value19)]
      plt.plot(Index, Value19, color='royalblue',
               linewidth=0.5, alpha=0.8, label='2019')
      plt.scatter(Index, Value19, color='royalblue', s=8)
      plt.plot(Index, Value20, color='red',
               linewidth=0.5, alpha=0.8, label='2020')
      plt.scatter(Index, Value20, color='red', s=8)

  fills1 = [str(i) for i in range(20200101, 20200103)]
  fills2 = [str(i) for i in range(20200102, 20200115)]
  fills3 = [str(i) for i in range(20200114, 20200118)]
  fills4 = [str(i) for i in range(20200117, 20200124)]
  fills5 = [str(i) for i in range(20200123, 20200132)] + [str(i)
                                                          for i in range(20200201, 20200215)]

  ax.fill_between(fills1, [City_DateIndex_19[420100][i] for i in fills1],
                  [City_DateIndex[420100][i] for i in fills1], color='royalblue', alpha=0.25)
  ax.fill_between(fills2, [City_DateIndex[420100][i] for i in fills2],
                  [City_DateIndex_19[420100][i] for i in fills2], color='red', alpha=0.25)
  ax.fill_between(fills3, [City_DateIndex_19[420100][i] for i in fills3],
                  [City_DateIndex[420100][i] for i in fills3], color='royalblue', alpha=0.25)
  ax.fill_between(fills4, [City_DateIndex[420100][i] for i in fills4],
                  [City_DateIndex_19[420100][i] for i in fills4], color='red', alpha=0.25)
  ax.fill_between(fills5, [City_DateIndex_19[420100][i] for i in fills5],
                  [City_DateIndex[420100][i] for i in fills5], color='royalblue', alpha=0.25)

  ax.fill_between(Index, [City_DateIndex_19[420100][i] if City_DateIndex[420100][i] > City_DateIndex_19[420100][i] else City_DateIndex[420100][i] for i in Index],
                  [0] * len(Index), color='lightgrey', alpha=0.25)
  font1 = {'family': 'arial', 'weight': 'normal', 'size': 8}
  ax.axvline('20200123', color='purple', ls='solid',
             linewidth=3, alpha=1, label='Lockdown')
  plt.xticks(Index, [IndexShift[i] for i in Index],
             fontproperties='arial', size=8, rotation=75)
  plt.yticks(fontproperties='arial', size=8)
  plt.grid(axis='y', linestyle='-.', c='lightgrey', alpha=0.8, linewidth=1)
  plt.legend(prop=font1, frameon=False)
  plt.ylim([0, 125000])
  plt.xlim([Index[0], Index[-1]])
  plt.ylabel(r'N$_\mathit{flow}$', fontdict={
      'family': 'arial', 'size': 10})
  plt.xlabel(r'Date', fontdict={
      'family': 'arial', 'size': 10})
  fig.tight_layout()
  plt.savefig(figures_dir / ('lockdown_pop_mov.png'))
