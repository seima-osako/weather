# -*- coding: utf-8 -*-
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

class Get_amedas_station:
  def __init__(self):
    url = 'https://www.data.jma.go.jp/obd/stats/etrn/select/prefecture00.php?prec_no=&block_no=&year=&month=&day=&view='
    html = urllib.request.urlopen(url)
    self.soup = BeautifulSoup(html, 'html.parser')
  
  def get_area_link(self):
    elements = self.soup.find_all('area')
    self.area_list = [element['alt'] for element in elements]
    self.area_link_list = [element['href'] for element in elements]

  def get_station_link(self):
    out = pd.DataFrame(columns=['station','url','area'])
    for area, area_link in zip(self.area_list, self.area_link_list):
      url = 'https://www.data.jma.go.jp/obd/stats/etrn/select/'+ area_link
      html = urllib.request.urlopen(url)
      soup = BeautifulSoup(html, 'html.parser')
      elements = soup.find_all('area')
      station_list = [element['alt'] for element in elements]
      station_link_list = [element['href'].strip('../') for element in elements]
      df1 = pd.DataFrame(station_list,columns=['station'])
      df2 = pd.DataFrame(station_link_list,columns=['url'])
      df = pd.concat([df1, df2],axis=1).assign(area=area)
      out = pd.concat([out,df])
      print(area)
    self.out = out
  
  def data_arange(self):
    out = self.out[~self.out.duplicated()].assign(append='https://www.data.jma.go.jp/obd/stats/etrn/')
    out['amedas_url'] = out['append'] + out['url']
    out = out.loc[:,['area','station','amedas_url']]
    out.to_csv('amedas_url_list.csv',index=None, encoding='SJIS')

if __name__ == '__main__':
  amedas = Get_amedas_station()
  amedas.get_area_link()
  amedas.get_station_link()
  amedas.data_arange()