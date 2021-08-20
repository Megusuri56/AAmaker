# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 20:29:05 2021

@author: 85355
"""

import cv2 as cv
import numpy as np
from math import sqrt
from collections import Counter

'''第一部分：图片读取'''

origin = cv.imread('C:\\Users\\85355\\Desktop\\222.jpeg',1)
gray = cv.cvtColor(origin,cv.COLOR_BGR2GRAY)
#cv.imshow('aaa',gray)
'''第二部分：轮廓绘制'''
ret,thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
width = 222
thresh = cv.resize(thresh,(width,int(gray.shape[0]/gray.shape[1]*width)),cv.INTER_AREA)
cv.imwrite('C:\\Users\\85355\\Desktop\\aaa.png',thresh)

mid = []
step = 3
for i in range(0,thresh.shape[0],step):
    for j in range(0,thresh.shape[1],step):
        cell = []
        for k in range(step):
            for n in range(step):
                if i+k < thresh.shape[0] and j+n < thresh.shape[1]:
                    cell.append(thresh[i+k][j+n])
                else:
                    cell.append(255)
        mid.append(cell)
maxm = np.amax(np.asarray(mid))
minm = np.amin(np.asarray(mid))
midnp = []
for row in mid:
    l = []
    for x in row:
        l.append((float(x)-minm)/(maxm-minm))
    midnp.append(l)
midnp = np.asarray(midnp)

pixel = [
         ' | ','一',' / ',
         ' \\ ',' ` ',' · ',
         ' . ','__',' ( ',
         ' ) ','█','   ',
         '◤  ','  ◥','  ◢',
         '◣  ','十','口',
         '| |','▉ ',' ▉'
        ]

'''samples = [
          [1,0,0,1,0,0,1,0,0],
          [0,1,0,0,1,0,0,1,0],
          [0,0,1,0,0,1,0,0,1],
          
          [0,0,0,1,1,1,0,0,0],
          [0,0,1,0,1,0,1,0,0],
          [1,0,0,0,1,0,0,0,1],
          
          [0,1,0,0,0,0,0,0,0],
          [0,0,0,0,1,0,0,0,0],
          [0,0,0,0,0,0,0,1,0],
          
          [0,0,0,0,0,0,1,1,1],
          [0,1,0,1,0,0,0,1,0],
          [0,0,1,0,1,0,0,0,1],
          
          [1,0,0,0,1,0,1,0,0],
          [0,1,0,0,0,1,0,1,0],
          [1,1,1,1,1,1,1,1,1],
          
          [0,0,0,0,0,0,0,0,0]
         ]'''
samples = [
           [0,1,1,0,1,1,0,1,1],
           [1,0,1,1,0,1,1,0,1],
           [1,1,0,1,1,0,1,1,0],
          
           [1,1,1,0,0,0,1,1,1],
           [1,1,0,1,0,1,0,1,1],
           [0,1,1,1,0,1,1,1,0],
          
           [1,0,1,1,1,1,1,1,1],
           [1,1,1,1,0,1,1,1,1],
           [1,1,1,1,1,1,1,0,1],
          ######################
           [1,1,1,1,1,1,0,0,0],
           [1,0,1,0,1,1,1,0,1],
           [1,1,0,1,0,1,1,1,0],
          
           [0,1,1,1,0,1,0,1,1],
           [1,0,1,1,1,0,1,0,1],
           [0,0,0,0,0,0,0,0,0],
          
           [1,1,1,1,1,1,1,1,1],#[0,0,0,0,0,1,0,1,1],
           [0,0,1,0,1,1,1,1,1],#[0,0,0,1,0,0,1,1,0],
           [1,0,0,1,1,0,1,1,1],
          ######################
           [1,1,1,1,1,0,1,0,0],
           [1,1,1,0,1,1,0,0,1],
           [1,0,1,0,1,1,1,1,1],
           
           [1,1,1,1,1,0,1,0,1],
           [1,0,1,1,1,0,1,1,1],
           [1,1,1,0,1,1,1,0,1],
           
           [0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0],
           [0,0,1,0,0,0,0,0,0],
          #####################
           [0,0,0,0,0,0,1,0,0],
           [1,0,1,0,0,0,1,0,1],
           [0,0,0,0,1,0,0,0,0],
           
           [0,1,0,0,1,0,0,1,0],
           [0,0,1,0,0,1,0,0,1],
           [1,0,0,1,0,0,1,0,0]
          ]

SP = [0,0,0,
      1,2,3,
      4,5,6,
      
      7,8,8,
      9,9,10,
      11,12,13,
      
      14,15,2,
      2,3,3,
      10,10,10,
      
      10,16,17,
      18,19,20
      ]

string1 = ''
i = 1
for cell in midnp:
    distances = [ sqrt(np.sum((sample-cell)**2)) for sample in samples ]

    nearest = np.argsort(distances)	#将点用索引排序
    k = 3	
    topK_y = [ SP[i] for i in nearest[:k] ]	

    votes = Counter(topK_y)	#统计票数 这里结果为 Counter({1: 5, 0: 1})
    string1 += pixel[ votes.most_common(1)[0][0] ]
    i += 1
    if i == ( width / step ) :
        string1 += '\n'
        i = 0

'''第三部分：色彩填充(暂时不用）'''
width = 100
gray1 = cv.resize(gray,(2*width,int(gray.shape[0]/gray.shape[1]*width)),cv.INTER_AREA)

color = list('靇我区一　　')
#color = list('█▒#%=-  ')
lenc = len(color)-1
maxc = np.amax(gray1)
minc = np.amin(gray1)

string = ''
for row in gray1:
    for x in row:
        string += color[int((x-minc)/(maxc-minc)*(lenc))]
    string += '\n'

with open('C:\\Users\\85355\\Desktop\\result.txt','wb') as f:
    f.write(string1.encode('UTF-8'))