# -*- coding: utf-8 -*-
import math
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap


class MSM_vertical_distribution:
  def __init__(self, t,lat_id):
    self.nc_p = netCDF4.Dataset('20141217_P.nc', 'r')
    self.nc_s = netCDF4.Dataset('20141217_S.nc', 'r')
    #['time']['p']['lat']['lon']
    self.sp = self.nc_s['sp'][t][:][:][::2,::2] /100
    temp = self.nc_p['temp'][t][:][:][:]
    rh = self.nc_p['rh'][t][:][:][:]
    u = self.nc_p['u'][t][:][:][:]
    v = self.nc_p['v'][t][:][:][:]
    uv = np.sqrt(u*u+v*v)

    self.temp = temp[:,lat_id,:]
    self.rh = rh[:,lat_id,:]
    self.u = u[:,lat_id,:]
    self.v = v[:,lat_id,:]
    self.uv = uv[:,lat_id,:]

  def vertical_p(self):
    self.p = np.zeros((0,241))
    for x in [1000,975,950,925,900,850,800,700,600,500,400,300,250,200,150,100]:
      out = np.full((1,241),x)
      self.p = np.vstack((self.p,out))
  
  def physical_quantity_calculation(self):
    es=6.112*np.exp(17.67*(self.temp-273.15)/(self.temp-29.65))
    e=self.rh/100*es
    x=0.622*e/(self.p-e)
    self.thetae = self.temp+2.8*x #相当温位
    
    self.q=0.622*1000*e/(self.p-0.378*e) #比湿
    
    self.wspd = np.sqrt(self.u * self.u + self.v * self.v) #風速
    wdir = np.rad2deg(np.arctan2(self.u,self.v))+180
    self.wdir = np.round(wdir,0) #風向

    self.qu = self.q * self.u #水蒸気フラックス(東西成分)
    self.qv = self.q * self.v #水蒸気フラックス(南北成分)
    self.quv = np.sqrt(self.qu * self.qu + self.qv * self.qv) #水蒸気フラックス
    
  def maskout(self):
    self.mask_p = np.zeros((0,253,241))
    for hpa in [1000,975,950,925,900,850,800,700,600,500,400,300,250,200,150,100]:
      mask_hpa = (self.sp - hpa).reshape(1,253,241)
      self.mask_p = np.vstack((self.mask_p,mask_hpa))
      

  def draw(self, lat_id, type):
    X, Y = np.meshgrid(self.nc_p['lon'][:], self.nc_p['p'][:])
    fig = plt.figure(dpi=100)
    
    if type=='temp':
      im = plt.contourf(X, Y, self.temp-273.15, cmap=cm.jet)
      cmap2=cm.Greys
      cmap2.set_over('w', alpha=0)
      im2 = plt.contourf(X, Y, self.mask_p[:,lat_id,:],cmap=cmap2,vmin=-100000,vmax=0)
      plt.gca().invert_yaxis()
      plt.colorbar(im)
      plt.title("lat=35.6 気温の鉛直分布\n9:00JST 17DEC2014")
      plt.savefig(f'{type}_20141217_v.jpeg', dpi=100)
    
    elif type=='thetae':
      im = plt.contourf(X, Y, self.thetae, cmap=cm.jet)
      cmap2=cm.Greys
      cmap2.set_over('w', alpha=0)
      im2 = plt.contourf(X, Y, self.mask_p[:,lat_id,:],cmap=cmap2,vmin=-100000,vmax=0)
      plt.gca().invert_yaxis()
      plt.ylim(1000,300)
      plt.colorbar(im)
      plt.title("lat=35.6 相当温位の鉛直分布\n9:00JST 17DEC2014")
      plt.savefig(f'{type}_20141217_v.jpeg', dpi=100)

    elif type=='quv':
      im = plt.contourf(X, Y, self.q , cmap=cm.Blues)
      cmap2=cm.Greys
      cmap2.set_over('w', alpha=0)
      Q = plt.quiver(X[:, ::8],Y[:, ::8], self.qu[:, ::8], self.qv[:, ::8], color='g', width=0.005)
      im2 = plt.contourf(X, Y, self.mask_p[:,lat_id,:],cmap=cmap2,vmin=-100000,vmax=0)
      plt.gca().invert_yaxis()
      plt.ylim(1000,300)
      plt.colorbar(im)
      plt.title("lat=35.6 水蒸気フラックスおよび比湿の鉛直分布\n9:00JST 17DEC2014")
      plt.savefig(f'{type}_20141217_v.jpeg', dpi=100)

if __name__ == '__main__':
  vmsm = MSM_vertical_distribution(0,120)
  vmsm.vertical_p()
  vmsm.physical_quantity_calculation()
  vmsm.maskout()
  type = input('temp or thetae or quv???')
  vmsm.draw(120, type)