import pandas as pd
import numpy as np
from collections import defaultdict
import random
import sys
import os 

from pylab import *
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib import pylab
from matplotlib.collections import LineCollection
from matplotlib import colors
import networkx as nx
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import matplotlib.colors
from pathlib import Path

os.chdir('../')
root_dir = Path.cwd()
sys.path.append(str(root_dir / ('packages/Basemap/lib/mpl_toolkits')))
figures_dir = root_dir.joinpath('example_figure/figures')
if not figures_dir.exists():
  figures_dir.mkdir()
from basemap import Basemap


CityShift_A = {'拉萨': '拉萨市', '合肥': '合肥市', '红河州': '红河哈尼族彝族自治州', '滁州': '滁州市',
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
               '淮北': '淮北市', '大理州': '大理白族自治州', '陵水': '陵水黎族自治县', '兴安盟乌兰浩特市': '兴安盟'}

CityShift_B = {'重庆市': '重庆', '那曲市': '那曲地区', '衡阳市': '衡陽市', '海东市': '海东地区', '日喀则市': '日喀则地区',
               '山南市': '山南地区', '张家界市': '張家界市', '上海市': '上海', '运城市': '运城县', '昌都市': '昌都地区',
               '益阳市': '益陽市', '林芝市': '林芝地区', '铜仁市': '铜仁地区', '邵阳市': '邵陽市', '哈密市': '哈密地区',
               '北京市': '北京', '滨州市': '滨州', '怀化市': '懷化市', '天津市': '天津',
               '吐鲁番市': '吐鲁番地区', '娄底市': '婁底市', '长沙市': '長沙市', '巴音郭楞蒙古自治州': '巴音郭愣蒙古自治州',
               '岳阳市': '岳陽市', '毕节市': '毕节地区', '襄阳市': '襄樊市', '': '', '': '', '': '',
               }

if __name__ == "__main__":

  dfId = pd.read_csv('./data/Citycode.csv')
  dfId['city'] = [CityShift_B[i] if i in CityShift_B else i for i in dfId['city']]
  dfprot = pd.read_csv('./data/LocDownProt_3day.csv')
  dfprot['city_code'] = ['CN' + str(i) for i in dfprot['city_code']]
  IDCity = {'CN' + str(i): j for i, j in zip(dfId['city_code'], dfId['city'])}
  CityID = {i: 'CN' + str(j) for i, j in zip(dfId['city'], dfId['city_code'])}
  IDname = {'CN' + str(i): j for i, j in zip(dfId['city_code'], dfId['name'])}
  IDPro = {'CN' + str(i): j for i, j in zip(dfId['city_code'], dfId['province'])}
  dfprot['City'] = [IDCity[i] for i in dfprot['city_code']]
  dfprot['Weight'] = dfprot['prot']
  dfprot = dfprot[dfprot['Weight']>0]
  Mycity = list(dfId['city'])
  df = pd.read_csv('./data/20200112-20200201.csv', index_col=0)
  df.rename(index=CityShift_A, inplace=True)
  df.rename(index=CityShift_B, inplace=True)
  CityCase = {i: j for i, j in zip(dfprot['City'], dfprot['Weight'])}

  CityCase['武汉市'] = 1
  IdCase = {CityID[i]: j for i, j in CityCase.items() if i in CityID}


  # Figure
  fig = plt.figure()

  map = Basemap(llcrnrlon=70, llcrnrlat=10, urcrnrlon=138, urcrnrlat=55,
                projection='mill', resolution='l', area_thresh=10000)

  # map
  map.drawmapboundary(fill_color='white')
  map.readshapefile('./data/gadm36_CHN_shp/China',
                    'prov', drawbounds=False)
  map.readshapefile('./data/gadm36_CHN_shp/gadm36_CHN_2',
                    'states', drawbounds=False)
  map.readshapefile('./data/gadm36_CHN_shp/gadm36_TWN_0',
                    'taiwan', drawbounds=False)
  map.readshapefile('./data/gadm36_CHN_shp/china_nine_dotted_line',
                    'nSea', drawbounds=False)

  # Position
  df_pos = pd.read_csv('./data/WuhanNodesTotal.csv')
  Pos_dict = {}
  Longitude, Latitude = map(
      np.array(df_pos['Longitude']), np.array(df_pos['Latitude']))
  for x, y, z in zip(df_pos['Id'], Longitude, Latitude):
    Pos_dict[x] = np.array([y, z])


  ax = plt.gca()
  cmap = plt.cm.YlGnBu
  colors = {}
  statenames = []
  for shapedict in map.states_info:
    statename = shapedict['NL_NAME_2']
    p = statename.split('|')
    if len(p) > 1:
      s = p[1]
    else:
      s = p[0]
    statenames.append(s)
  Mapcity = (set(statenames))
  vmax = 1
  vmin = 0
  for city in Mapcity:
    if city in CityCase:
      colors[city] = cmap(np.sqrt((CityCase[city] - vmin) / (vmax - vmin)))[:3]
    else:
      colors[city] = cmap(0.01)
  colors['台湾'] = cmap(np.sqrt((CityCase['花莲县'] - vmin) / (vmax - vmin)))[:3]

  patches = []
  for nshape, seg in enumerate(map.prov):
    if colors[statenames[nshape]] == cmap(0.01):
      color = 'lightgrey'
    else:
      color = rgb2hex(colors[statenames[nshape]])
    poly = Polygon(seg, facecolor='lightgrey', edgecolor='lightgrey')
    ax.add_patch(poly)
  for nshape, seg in enumerate(map.states):
    if colors[statenames[nshape]] == cmap(0.01):
      color = 'lightgrey'
    else:
      color = rgb2hex(colors[statenames[nshape]])
    poly = Polygon(seg, facecolor=color, edgecolor=color)
    patches.append(poly)
    ax.add_patch(poly)
  for nshape, seg in enumerate(map.taiwan):
    colors['福州市'] = colors['台湾']

    if colors[statenames[nshape]] == cmap(0.01):
      color = 'lightgrey'
    else:
      color = rgb2hex(colors[statenames[nshape]])
    poly = Polygon(seg, facecolor=color, edgecolor=color)
    ax.add_patch(poly)

  for nshape, seg in enumerate(map.nSea):
    if colors[statenames[nshape]] == cmap(0.01):
      color = 'lightgrey'
    else:
      color = rgb2hex(colors[statenames[nshape]])
    poly = Polygon(seg, facecolor='lightgrey', edgecolor='lightgrey')
    ax.add_patch(poly)


  colors1 = [i[1] for i in colors.values()]
  colorVotes = plt.cm.YlGnBu
  p = PatchCollection(patches, cmap=colorVotes)
  p.set_array(np.array(colors1))
  cb = plt.colorbar(p, shrink=0.25, fraction=0.06,
                    pad=0.04, drawedges=False, aspect=5)
  font = {'family': 'arial', 'size': 8,
          }
  cb.outline.set_linewidth(0)
  cb.set_ticks(np.linspace(10, 20, 2))

  G2 = nx.Graph()
  G2.add_node('CN420100')
  nx.draw(
      G2, pos={'CN420100': Pos_dict['CN420100']}, node_color='red', node_size=0)


  left, bottom, width, height = 0.18, 0.15, 0.10, 0.22
  ax1 = fig.add_axes([left, bottom, width, height])
  map = Basemap(llcrnrlon=105, llcrnrlat=0, urcrnrlon=125, urcrnrlat=25,
                projection='mill', resolution='l', area_thresh=10000, ax=ax1)
  map.drawmapboundary(fill_color='white')
  map.readshapefile('./data/gadm36_CHN_shp/gadm36_CHN_2',
                    'states', drawbounds=False, ax=ax1)
  map.readshapefile('./data/gadm36_CHN_shp/China',
                    'nSea2', drawbounds=True, ax=ax1)
  map.readshapefile('./data/gadm36_CHN_shp/gadm36_TWN_0',
                    'taiwan', drawbounds=True, ax=ax1)

  for nshape, seg in enumerate(map.taiwan):
    colors['福州市'] = colors['台湾']

    color = rgb2hex(colors[statenames[nshape]])
    poly = Polygon(seg, facecolor=color, edgecolor='lightgrey')
    ax1.add_patch(poly)
  for nshape, seg in enumerate(map.nSea2):
    color = rgb2hex(colors[statenames[nshape]])

    poly = Polygon(seg, facecolor=color, edgecolor='lightgrey', alpha=0.6)
    ax1.add_patch(poly)

  for nshape, seg in enumerate(map.states):
    color = rgb2hex(colors[statenames[nshape]])
    poly = Polygon(seg, facecolor='lightgrey', edgecolor=color)
    ax1.add_patch(poly)
  ax1.set_xticks([])
  ax1.set_yticks([])
  ax.scatter(Pos_dict['CN420100'][0] , Pos_dict['CN420100'][1],s = 50,color = 'red',alpha =1,zorder = 2)

  ax.set_xlabel('Longitude', fontdict={'size': 11, 'family': 'arial'})
  ax.set_ylabel('Latitude', fontdict={'size': 11, 'family': 'arial'})
  plt.show()
  plt.savefig(figures_dir / ('pretect_map_3day_earlier.png'))
