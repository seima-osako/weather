# -*- coding: utf-8 -*-¥
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap


class Radar_etop:
    def __init__(self):
        f = open("Z__C_RJTD_20141216000000_RDR_JMAGPV_Gll2p5km_Phhlv_ANAL_.bin", mode="rb") #切り出したデータを読み込んでから配列変換
        etop = np.fromfile(f, dtype="float32",sep="").reshape(1120,1024)
        etop = np.where(etop < 0, 0, etop)
        etop = np.where(etop == 1, 1, etop)
        self.etop = np.where(etop == 15, 14, etop)

    def lut_to_etop(self):
        keys = []
        values = []
        for i in np.arange(3.0, 15.0, 2.0):
            i = round(i, 1)
            keys.append(i)
        for j in np.arange(2.0, 16.0, 2.0):
            j = round(j,1)
            values.append(j)
        d = dict(zip(keys, values))
        for k, v in d.items():
            self.etop = np.where(self.etop == k, v, self.etop)
    
    def draw(self):
        #東西・南北のグリッドを作成
        lon = np.round(np.linspace(118, 150, 1024), 5)
        lat = np.round(np.linspace(20, 48, 1120)[::-1], 3)
        X, Y = np.meshgrid(lon,lat)

        fig = plt.figure(dpi=100)
        interval = list(np.arange(2, 10, 2))
        cmap = plt.get_cmap('jet')
        cmap.set_under("w")
        cmap.set_over("firebrick")

        #Basemapによる描画
        m = Basemap(projection="cyl", resolution="i", llcrnrlat=20,urcrnrlat=50, llcrnrlon=120, urcrnrlon=150)
        m.drawcoastlines(color='black')
        m.drawmeridians(np.arange(0, 360, 5), labels=[True, False, False, True],linewidth=0.0)
        m.drawparallels(np.arange(-90, 90, 5), labels=[True, False, True, False],linewidth=0.0)
        fname1 = 'gadm/gadm36_JPN_1'
        m.readshapefile(fname1,'prefectual_bound1', color='k', linewidth=.8)
        im = plt.contourf(X,Y, self.etop, interval, cmap=cmap, extend='both')
        cb = m.colorbar(im, "right", size="2.5%")
        cb.set_label('km')
        plt.title("Radar Echo Height 9:00JST 16DEC2014")
        plt.savefig('etop_201412160900.jpeg', dpi=100)

if __name__ == '__main__':
    etop = Radar_etop()
    etop.lut_to_etop()
    etop.draw()