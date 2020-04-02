# -*- coding: utf-8 -*-
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

#東京 2019/1/1の10分値を取得
yyyy = '2019'
mm = '01'
dd = '01'
url = f'https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=44&block_no=47662&year={yyyy}&month={mm}&day={dd}&view=p1'
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
element = soup.find_all('tr', attrs={'class':'mtx', 'style':'text-align:right;'})
out = [list(map(lambda x: x.text, ele)) for ele in element]

df = pd.DataFrame(data=out, columns=['時分','現地気圧','海面気圧','降水量','気温','相対湿度','平均風速','平均風向','最大瞬間風速','最大瞬間風向','日照時間'])
df.to_csv('tokyo_2019-01-01.csv', index=None,encoding='SJIS')
print(df)
