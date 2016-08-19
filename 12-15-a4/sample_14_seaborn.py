#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import seaborn
import pandas

# フォントの指定
seaborn.set(font='FreeSans')

# ラベルの例
label_list = ['07:11:35', '07:11:45', '07:11:55', '07:12:05', '07:12:15', '07:12:25']

# データフレームの作成
data_frame = pandas.DataFrame(
    {'created_datetime': ['2016-07-22 07:11:35', '2016-07-22 07:11:45', '2016-07-22 07:11:55',
                          '2016-07-22 07:12:05', '2016-07-22 07:12:15', '2016-07-22 07:12:25'],
     'hPa': [950.084019730771, 965.113327645037, 970.115821262263, 960.148246742742, 960.089009240076,
             955.089009240076]},
    columns=['created_datetime', 'hPa'])

# pointplot()によるグラフの作成
ax = seaborn.pointplot(x='created_datetime', y='hPa', data=data_frame, markers=[''])

# x軸ラベル指定
ax.set_xticklabels(label_list)

# PNGファイルに保存
seaborn.plt.savefig('air_pressure.png')
