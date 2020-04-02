# -*- coding: utf-8 -*-
import gzip
from struct import unpack
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap


class GSMaP:
    def __init__(self):
        filename = "gsmap_gauge.20141217.0000.v7.0001.0.dat.gz" 
        i = 0
        rain = [0]*3600*1200
        with gzip.open(filename, "rb") as f:
            while True:
                data = f.read(4)
                if len(data) < 4:
                    break
                rain[i] = unpack("<f", data)[0]
                i = i+1
        
        hprecipRateGC = np.reshape(rain, (1200, 3600)) #読み込んだ降水量データを1200×3600の配列に変換
        hprecipRateGC = np.where(hprecipRateGC < 0, 0, hprecipRateGC) #欠損値があれば0に置換
        a = hprecipRateGC[:, 0:1801][:, ::-1]
        b = hprecipRateGC[:, 1801:3601][:, ::-1]
        self.hprecipRateGC = np.concatenate([a, b],1)

    def make_grid(self):
        # meshgrid関数で、データに一致する格子状の座標を生成。
        lo = [5+10*i for i in range(0, 1800)[::-1]] 
        lo.extend([-17995+10*i for i in range(0, 1800)[::-1]])

        Lo = 0.01*np.array(lo)
        la = [5995-10*i for i in range(0, 600)]
        la.extend([-5-10*i for i in range(0, 600)])
        La = 0.01*np.array(la)
        self.Lon, self.Lat = np.meshgrid(Lo, La)

    def draw(self):
        fig = plt.figure(dpi=100)
        levels = [0.1, 0.5, 1, 3, 5, 8, 10]
        cmap = plt.get_cmap('jet')
        cmap.set_under("w")
        cmap.set_over("firebrick")

        m = Basemap(projection="cyl", resolution="i", llcrnrlat=20,urcrnrlat=50, llcrnrlon=120, urcrnrlon=150)
        m.drawcoastlines(color='black')
        m.drawmeridians(np.arange(0, 360, 5), labels=[True, False, False, True],linewidth=0.0)
        m.drawparallels(np.arange(-90, 90, 5), labels=[True, False, True, False],linewidth=0.0)
        fname1 = 'gadm/gadm36_JPN_1'
        m.readshapefile(fname1,'prefectual_bound1', color='k', linewidth=.8)
        im = plt.contourf(self.Lon, self.Lat, self.hprecipRateGC, levels, cmap=cmap, extend='both')
        cb = m.colorbar(im, "right", size="2.5%")
        cb.set_label('mm/hr')
        plt.title("GSMaP  9:00JST 17DEC2014")
        plt.savefig('gsmap_201412170900.jpeg', dpi=100)

if __name__ == '__main__':
    g = GSMaP()
    g.make_grid()
    g.draw()