from collections import defaultdict
import random
import sys
import os
from pathlib import Path

import pandas as pd
import numpy as np

os.chdir('../')
root_dir = Path.cwd()
sys.path.append(str(root_dir / ('packages/Basemap/lib/mpl_toolkits')))
data_dir = root_dir.joinpath('data')
if not data_dir.exists():
  data_dir.mkdir()


def RiskShift():
  df = pd.read_csv('./Data/Qianxi/risk_current_V1.csv')
  dfId = pd.read_csv('./Data/Citycode.csv')
  CityName = {i: j for i, j in zip(dfId['city'], dfId['name'])}
  df['name'] = [CityName[i] for i in df['city']]
  df['infectious2'] = [round(i) for i in df['infectious']]
  df.to_csv(data_dir / ('risk_current_V1.csv'),
            index=False, encoding='utf-8-sig')


def RiskShift(a, b, x):
  y = a * x + b
  return y


def RiskShift2(x):
  a = 21.20764796
  b = 3.09399548
  y = (x - b) / a
  return y


def RiskShift3(x):
  a = 21.20764796
  b = 3.09399548
  y = a * x + b
  return y


def ProtShift(x, y):
  return (y - x) / y


if __name__ == "__main__":
  file = open('./data/bootstrap_para_100', 'r')
  df = pd.read_csv('./data/LocDownProt_7day.csv')

  df['risk'] = [RiskShift2(i) for i in df['Infectious1']]
  CityRisk = {i: j for i, j in zip(df['city'], df['risk'])}
  CityPred = {i: j for i, j in zip(df['city'], df['Infectious1'])}
  CityReal = {i: j for i, j in zip(df['city'], df['Infectious2'])}
  para_lst = []
  for line in file:
    if line.split() != ['10.0', '0.0']:
      line = line.split()
      para_lst.append((float(line[0]), float(line[1])))

  Result = defaultdict(list)
  for i, j in zip(df['city'], df['risk']):

    for x in para_lst:
      Result[i].append(RiskShift(x[0], x[1], j))

  City_Interval = {}
  City_protrate = {}
  City_derisk_Interval = {}
  for x, y in Result.items():
    SE = np.std(y) / np.sqrt(len(y))
    y.sort()
    real = CityReal[x]
    City_Interval[x] = str(RiskShift3(CityRisk[x])) + \
        str((round(y[24]), round(y[974])))
    City_derisk_Interval[x] = str(round(CityReal[x] - RiskShift3(CityRisk[x]))) + str(
        (round(CityReal[x] - y[974]), round(CityReal[x] - y[24])))

    City_protrate[x] = str(round(ProtShift(CityPred[x], real), 2)) + str((round(
        ProtShift(y[974], real), 2), round(ProtShift(y[24], real), 2)))

  df['derisk_interval'] = [City_derisk_Interval[i] for i in df['city']]

  print(df)

  df.to_csv('./Data/Qianxi/LocDownProt_7day.csv',
            index=False, encoding='utf-8-sig')
