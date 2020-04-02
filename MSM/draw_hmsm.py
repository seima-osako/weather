# -*- coding: utf-8 -*-
import math
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

class MSM_horizontal_distribution:
  def __init__(self, t,p_id):
    self.nc_p = netCDF4.Dataset('20141217_P.nc', 'r')
    self.nc_s = netCDF4.Dataset('20141217_S.nc', 'r')
    #['time']['p']['lat']['lon']
    self.temp = self.nc_p['temp'][t][p_id][:][:]
    self.sp = self.nc_s['sp'][t][:][:][::2,::2] /100
    self.rh = self.nc_p['rh'][t][p_id][:][:]
    self.u = self.nc_p['u'][t][p_id][:][:]
    self.v = self.nc_p['v'][t][p_id][:][:]

  def physical_quantity_calculation(self, p):
    es=6.112*np.exp(17.67*(self.temp-273.15)/(self.temp-29.65))
    e=self.rh/100*es
    x=0.622*e/(p-e)
    self.thetae = self.temp+2.8*x #相当温位
    
    self.q=0.622*1000*e/(p-0.378*e) #比湿
    
    self.wspd = np.sqrt(self.u * self.u + self.v * self.v) #風速
    wdir = np.rad2deg(np.arctan2(self.u,self.v))+180
    self.wdir = np.round(wdir,0) #風向

    self.qu = self.q * self.u #水蒸気フラックス(東西成分)
    self.qv = self.q * self.v #水蒸気フラックス(南北成分)
    self.quv = np.sqrt(self.qu * self.qu + self.qv * self.qv) #水蒸気フラックス
    
    self.mask_s = self.sp - p #マスクアウトするグリッド

  def draw(self, p, type):
    X, Y = np.meshgrid(self.nc_p['lon'][:], self.nc_p['lat'][:])
    fig = plt.figure(dpi=100)
    m = Basemap(projection="cyl", resolution="i", llcrnrlat=30,urcrnrlat=47, llcrnrlon=130, urcrnrlon=150)
    m.drawcoastlines(color='black')
    m.drawmeridians(np.arange(0, 360, 5), labels=[True, False, False, True],linewidth=0.0)
    m.drawparallels(np.arange(-90, 90, 5), labels=[True, False, True, False],linewidth=0.0)
    fname1 = 'gadm/gadm36_JPN_1'
    m.readshapefile(fname1,'prefectual_bound1', color='k', linewidth=.8)
    
    if type=='temp':
      im = plt.contourf(X, Y, self.temp-273.15, cmap=cm.jet)
      cmap2=cm.gray
      cmap2.set_over('w', alpha=0)
      im2 = plt.contourf(X, Y, self.mask_s,cmap=cmap2,vmin=-100000,vmax=0)
      plt.title(f"{p}hPaの気温\n9:00JST 17DEC2014")
      cb = m.colorbar(im)
      plt.savefig(f'{type}_20141217_h.jpeg', dpi=100)
    
    elif type=='thetae':
      im = plt.contourf(X, Y, self.thetae, cmap=cm.jet)
      cmap2=cm.gray
      cmap2.set_over('w', alpha=0)
      im2 = plt.contourf(X, Y, self.mask_s,cmap=cmap2,vmin=-100000,vmax=0)
      plt.title(f"{p}hPaの相当温位\n9:00JST 17DEC2014")
      cb = m.colorbar(im)
      plt.savefig(f'{type}_20141217_h.jpeg', dpi=100)

    elif type=='quv':
      im = plt.contourf(X, Y, self.q , cmap=cm.Blues)
      cmap2=cm.Greys
      cmap2.set_over('w', alpha=0)
      Q = plt.quiver(X[::12, ::12],Y[::12, ::12], self.qu[::12, ::12], self.qv[::12, ::12], color='g', width=0.003)
      im2 = plt.contourf(X, Y, self.mask_s,cmap=cmap2,vmin=-100000,vmax=0)
      plt.title(f"{p}hPaの水蒸気フラックスおよび比湿\n9:00JST 17DEC2014")
      cb = m.colorbar(im)
      plt.savefig(f'{type}_20141217_h.jpeg', dpi=100)

if __name__ == '__main__':
  hmsm = MSM_horizontal_distribution(0,5)
  hmsm.physical_quantity_calculation(850)
  type = input('temp or thetae or quv???')
  hmsm.draw(850, type)