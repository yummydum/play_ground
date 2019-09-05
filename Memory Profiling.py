# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # 空間計算量

from memory_profiler import memory_usage

# ## プロセスのメモリ使用量を計測
# プロセスの現在のメモリ使用状況を取得．
#
# procにはプロセスIDを指定する（-1を指定すると自分自身のプロセスIDが使用される）
#

memory_usage(proc=-1)

# .1秒ごとにメモリの使用状況を記録する（interval=.1）
#
# 計測時間は１秒（timeout=1）

memory_usage(proc=-1, interval=.1, timeout=1)

# ## モジュール/関数のメモリ使用量を行ごとに計測
#
# コマンドラインから実行するかjupyter magic commandを使用するかmemory_usage()を使うかの３択．
#
# memory_usage()は大体上と同じなのでドキュメント見てください．

# ### コマンドラインから実行

# +
# Sample code on current directory

sample_code = """

@profile
def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a
if __name__ == "__main__":
    my_func()
"""

with open("mem_prof_example.py",mode="w") as f:
    f.write(sample_code)


# -

# #### メモリ使用量を行ごとに計測
# デコレータ@profileをつけておけば，以下のように実行するだけで良い．
# オーバーヘッドはまぁまぁある．

# ! python -m memory_profiler mem_prof_example.py

# #### メモリ使用量を行ごとに計測してプロット
# ```
# mprof run <executable>
# mprof plot
# ```
# を実行するだけで良い．
# ちゃんと関数の内容通りの挙動をしていることを確認する．

# ! mprof run mem_prof_example.py
# ! mprof plot -o "memory_profile_result.png"
# 画像はGUIで見てください

# ### jupyter magic commandから実行
#
# 上記でやったことをjupyter magic commandで簡単に出来る．
# プロファイリングという行為自体がアドホックなものなので，jupyterかHydrogen上で必要に応じてmagic commandを使って計測するのが良い気がしている．

# %load_ext memory_profiler

def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a


# %memit my_func()

# 別のファイルからimportしか関数にしか使えない！
from mem_prof_example import my_func
# %mprun -f my_func()

# ## オブジェクトのメモリを計測

# ### pymplerを使おう
#
# sys.getsizeof()というbuilt-in methodがあるが，こいつはrecursiveにオブジェクトのメモリを測ってくれない．
# これに対してpymplerはrecursiveにメモリの使用量を測ってくれるので良いやつなんだ．

from pympler.asizeof import asizeof

obj = [1,2,3,4]
asizeof(obj)

# ### numpyとpandasのメモリ使用量を測って，肌感を身に着けよう
#
# 実際に計測してみて，行列やデータフレームのメモリ使用量を感じよう
# 以下に色々とプロットしてみました．
# 縦軸はMB単位で，横軸は計測対象ごとにセッティングが異なっているのでちゃんと読んで理解して下さい．
#
# * 巨大な行列を扱う際には注意が必要 (次元に対して空間計算量は$n^2$ということをちゃんと意識しよう)
# * pandasは大体numpyの2倍くらいメモリを使っている？
#
# などと分かる．
# 他にも色々試してみよう！
#

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# +
# numpy 1d array
x = np.linspace(1,10**4,1000)
mem_list = []
for n in x:
    mem_list.append(asizeof(np.zeros(int(n))) / (2**20))
fig,ax = plt.subplots()

ax.plot(x,mem_list)

# +
# numpy 2d array
x = np.linspace(1,10**4,100)
mem_list = []
for n in x:
    mem_list.append(asizeof(np.zeros(shape=(int(n),int(n)))) / (2**20))
fig,ax = plt.subplots()

ax.plot(x,mem_list)
# -

# 縦長 data frame
x = np.linspace(1,10**4,100)
mem_list = []
for n in x:
    measure_this = pd.DataFrame(np.zeros(shape=(int(n),10)))
    mem_list.append(asizeof(measure_this) / (2**20))
fig,ax = plt.subplots()
ax.plot(x,mem_list)

# pandas 巨大 data frame (重い！数分待つかも)
x = np.linspace(1,10**3,100)
mem_list = []
for n in x:
    measure_this = pd.DataFrame(np.zeros(shape=(int(n),int(n))))
    mem_list.append(asizeof(measure_this) / (2**20))
fig,ax = plt.subplots()
ax.plot(x,mem_list)

# ### ベストプラクティス
# * プロセスのメモリ使用量をまるっとプロファイルして大体ピークがどれくらいなのかとかメモリがどう時間発展するのかとか見る
# * コーディング中も%memitとかasizeof()とか使ってちょくちょく確認する
# * インタプリタが大体50~60Mとかなので，でかいデータフレームとかが使用量を支配してる．そこだけasizeof()で見れば良いのかも．
# * ゆーてmemory_usage()とasizeof()でloggerに出力していくのが便利な気もする...


# ## References
#
# https://github.com/pythonprofilers/memory_profiler
#

# # 時間計算量

# ## line_profilerをコマンドラインから
# 実はline_profilerはmemory_profilerと同じデコレータを使っている．
# 先程と同じコードに対して以下を実行すれば良い．

# ! kernprof -l -v mem_prof_example.py
