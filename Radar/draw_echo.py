# -*- coding: utf-8 -*-¥
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

#↓ルックアップテーブル作成
def lookup_table(start1, end1, step1, start2, end2, step2):
    keys = []
    values = []
    for i in np.arange(start1, end1, step1):
        i = str(round(i, 2))
        keys.append(i)
    for j in np.arange(start2, end2, step2):
        j = round(j, 2)
        values.append(j)
    d = dict(zip(keys, values))
    return d


class Radar_echo:
    def __init__(self):
        f = open("Z__C_RJTD_20141216000000_RDR_JMAGPV_Ggis1km_Prr10lv_ANAL_.bin", mode="rb") #切り出したデータを読み込んでから配列変換
        echo = np.fromfile(f, dtype="float32",sep="").reshape(3360,2560)
        #とりあえず0,0.1,260のデータ代表値を降水強度へ変換
        echo = np.where(echo < 0, 0, echo)
        echo = np.where(echo == 0.1, 0.1, echo)
        self.echo = np.where(echo == 260, 256, echo)

    def lut_to_echo(self):
        d1 = lookup_table(0.25, 2.05, 0.1,0.2, 2.0, 0.1)
        d2 = lookup_table(2.13, 5.13, 0.25, 2.0, 4.95, 0.25)
        d3 = lookup_table(5.25, 10.25, 0.5, 5.0, 10.0, 0.5)
        d4 = lookup_table(10.5, 180.5, 1.0, 10, 180, 1.0)
        d5 = lookup_table(181, 257, 2.0, 180, 256, 2.0)

        d1.update(d2)
        d1.update(d3)
        d1.update(d4)
        d1.update(d5)
        #ルックアップテーブルをもとに降水強度へ変換
        for k, v in d1.items():
            self.echo = np.where(self.echo == float(k), v, self.echo)
    
    def draw(self):
        #東西・南北のグリッドを作成
        lon = np.round(np.linspace(118, 150, 2560), 4)
        lat = np.round(np.linspace(20, 48, 3360)[::-1], 4)
        X, Y = np.meshgrid(lon,lat)

        fig = plt.figure(dpi=100)
        levels = [0.5, 1, 3, 5, 8, 10]
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
        im = plt.contourf(X,Y, self.echo, levels, cmap=cmap, extend='both')
        cb = m.colorbar(im, "right", size="2.5%")
        cb.set_label('mm/hr')
        plt.title("Radar Echo Intensity 9:00JST 16DEC2014")
        plt.savefig('echo_201412160900.jpeg', dpi=100)

if __name__ == '__main__':
    echo = Radar_echo()
    echo.lut_to_echo()
    echo.draw()