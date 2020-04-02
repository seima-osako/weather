# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap


#最小値0、最大値1にする数量正規化メソッド
def normalization(x):
    x_min = x.min()
    x_max = x.max()
    x_norm = (x - x_min) / (x_max - x_min)
    return x_norm   #正規化した配列を返す

#階調反転メソッド
def reverse(color, min, max):
  for x in color[:]:
    y = ((0-1)/(max-min))*x + (max/(max-min))
    color = np.where(color == x, y, color)
  return color

class Himawari:
  def __init__(self):
    #必要なバンドの読み込み
    band08 = np.fromfile("201910120600.tir.06.fld.geoss", dtype='>u2').reshape(6000, 6000)
    band10 = np.fromfile("201910120600.tir.08.fld.geoss", dtype='>u2').reshape(6000, 6000)
    band12 = np.fromfile("201910120600.tir.10.fld.geoss", dtype='>u2').reshape(6000, 6000)
    band13 = np.fromfile("201910120600.tir.01.fld.geoss", dtype='>u2').reshape(6000, 6000)

    #欠損値置換
    band08 = np.where(band08 > 2000, 2000, band08)
    band10 = np.where(band10 > 4050, 4050, band10)
    band12 = np.where(band12 > 4050, 4050, band12)
    band13 = np.where(band13 > 4050, 4050, band13)

    #ルックアップテーブル参照
    #日本領域にトレミング(50→30, l25→150)
    band08 = np.loadtxt('count2tbb/tir.06',usecols=(1,))[band08][500:1500, 2000:3250]
    band10 = np.loadtxt('count2tbb/tir.08',usecols=(1,))[band10][500:1500, 2000:3250]
    band12 = np.loadtxt('count2tbb/tir.10',usecols=(1,))[band12][500:1500, 2000:3250]
    band13 = np.loadtxt('count2tbb/tir.01', usecols=(1,))[band13][500:1500, 2000:3250]

    #差分をとって階調域の限定
    self.R = (band08 - band10).clip(-25, 0)
    self.G = (band12 - band13).clip(-40, 5)
    self.B = band08.clip(208, 243)

  def rgb_synthesis(self):
    R = normalization(self.R)
    G = normalization(self.G)
    B = reverse(self.B, 208, 243)
    
    rgb = np.dstack((R, G, B))
    self.rgb = np.power(rgb, 1.0)

  def draw(self):
    fig = plt.figure(dpi=100)
    fname1 = 'gadm/gadm36_JPN_1'
    m = Basemap(projection="cyl", resolution="i", llcrnrlat=30, urcrnrlat=50, llcrnrlon=125, urcrnrlon=150, area_thresh=100, fix_aspect=True)
    m.imshow(self.rgb, origin="upper")
    m.drawcoastlines(color='k')
    m.drawmeridians(np.arange(0, 360, 10), labels=[True, False, False, True], linewidth=0)
    m.drawparallels(np.arange(-90, 90, 10), labels=[ True,False, True, False],linewidth=0)
    m.readshapefile(fname1, 'prefectural_bound1', color='k', linewidth=.8) #県境
    plt.title("Airmass RGB 20191012 15:00JST")
    plt.savefig('airmass_201910121500.jpeg', dpi=100)


if __name__ == '__main__':
  h = Himawari()
  h.rgb_synthesis()
  h.draw()