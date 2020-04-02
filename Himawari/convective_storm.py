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

class Himawari:
  def __init__(self):
    band03 = (np.fromfile("201910120600.ext.01.fld.geoss",dtype='>u2').reshape(6000,4,6000,4).mean(-1).mean(1)+0.5).astype('u2')
    band05 = np.fromfile("201910120600.sir.01.fld.geoss", dtype='>u2').reshape(6000, 6000)
    band07 = np.fromfile("201910120600.tir.05.fld.geoss", dtype='>u2').reshape(6000, 6000)
    band08 = np.fromfile("201910120600.tir.06.fld.geoss", dtype='>u2').reshape(6000, 6000)
    band10 = np.fromfile("201910120600.tir.08.fld.geoss", dtype='>u2').reshape(6000, 6000)
    band13 = np.fromfile("201910120600.tir.01.fld.geoss", dtype='>u2').reshape(6000, 6000)

    #欠損値置換
    band03 = np.where(band03 > 2047, 2047, band03)
    band05 = np.where(band05 > 2047, 2047, band05)
    band07 = np.where(band07 > 16350, 16350, band07)
    band08 = np.where(band08 > 2000, 2000, band08)
    band10 = np.where(band10 > 4050, 4050, band10)
    band13 = np.where(band13 > 4050, 4050, band13)

    #日本領域にトレミング
    band03 = np.loadtxt('./count2tbb/ext.01',usecols=(1,))[band03][500:1500, 2000:3250]
    band05 = np.loadtxt('./count2tbb/sir.01',usecols=(1,))[band05][500:1500, 2000:3250]
    band07 = np.loadtxt('./count2tbb/tir.05',usecols=(1,))[band07][500:1500, 2000:3250]
    band08 = np.loadtxt('./count2tbb/tir.06',usecols=(1,))[band08][500:1500, 2000:3250]
    band10 = np.loadtxt('./count2tbb/tir.08',usecols=(1,))[band10][500:1500, 2000:3250]
    band13 = np.loadtxt('./count2tbb/tir.01', usecols=(1,))[band13][500:1500, 2000:3250]

    R = band08 - band10
    G = band07 - band13
    B = band05 - band03

    #階調域の限定
    self.R = R.clip(-35, 5)
    self.G = G.clip(-5, 60)
    self.B = B.clip(-70, 25)

  def rgb_synthesis(self):
    R = np.power(normalization(self.R), 1.0)
    G = np.power(normalization(self.G), 1.0/0.5)
    B = np.power(normalization(self.B), 1.0)
    self.rgb = np.dstack((R, G, B))

  def draw(self):
    fig = plt.figure(dpi=100)
    fname1 = 'gadm/gadm36_JPN_1'
    m = Basemap(projection="cyl", resolution="i", llcrnrlat=30, urcrnrlat=50, llcrnrlon=125, urcrnrlon=150, area_thresh=100, fix_aspect=True)
    m.imshow(self.rgb, origin="upper")
    m.drawcoastlines(color='k')
    m.drawmeridians(np.arange(0, 360, 10), labels=[True, False, False, True], linewidth=0)
    m.drawparallels(np.arange(-90, 90, 10), labels=[ True,False, True, False],linewidth=0)
    m.readshapefile(fname1, 'prefectural_bound1', color='k', linewidth=.8) #県境
    plt.title("Day convective storm RGB 20191012 15:00JST")
    plt.savefig('convective_storm_201910121500.jpeg', dpi=100)


if __name__ == '__main__':
  h = Himawari()
  h.rgb_synthesis()
  h.draw()