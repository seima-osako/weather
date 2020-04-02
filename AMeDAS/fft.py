# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fftn, ifftn, fftfreq

class FFT:
  def __init__(self):
    df = pd.read_csv('東京都_東京_20190401-20190731_10min.csv', encoding='SJIS').replace(['--','×'],-99)
    df['気温'] = df['気温'].astype(float)
    y = df['気温'].replace(-99, (df['気温'] > -99).mean()).values
    y = (y - np.mean(y)) * np.hamming(len(y))
    '''
    サンプリング周波数 fs → 1秒間にサンプリングされるデータ数 第二引数にはd=1.0/fs
    今回のサンプリング周波数は10分間隔データなので1/600
    '''
    self.z = np.fft.fft(y)
    self.freq = fftfreq(len(y), d=1.0/(1/600))


  def plot(self, n_samples):
    fig, axes = plt.subplots(figsize=(8, 4), ncols=2, sharey=True)
    ax = axes[0]
    ax.plot(self.freq[1:int(n_samples/2)], abs(self.z[1:int(n_samples/2)]))
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_ylabel('Power')
    ax.set_xlabel('周波数（Hz）')
    ax = axes[1]
    ax.plot((1 / self.freq[1:int(n_samples / 2)])/(60*60), abs(self.z[1:int(n_samples / 2)]))
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlabel('周期（時間）')
    plt.show()
  
  def periodic_characteristics(self, n_samples):
    fft_pow_df = pd.DataFrame([(1 / self.freq[1:int(n_samples / 2)])/(60*60), np.log10(abs(self.z[1:int(n_samples / 2)]))], index=['周期（時間）', 'log10_power']).T
    fft_pow_df = fft_pow_df.sort_values('log10_power', ascending=False).head(10).reset_index()
    print(fft_pow_df.loc[:, ['周期（時間）', 'log10_power']])

if __name__ == '__main__':
  fft = FFT()
  fft.periodic_characteristics(512)
  fft.plot(512)