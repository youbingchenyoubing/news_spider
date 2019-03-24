# -*- coding: utf-8 -*-
import time
from dataUtil import DataUtils
from simhash import Simhash

if __name__ == '__main__':
    start = time.time()
    dataUtil = DataUtils(load = False)
    rawData = str(open('1.txt','r').read())
    rawData = dataUtil.cutText_for_hash(rawData)
    #rawData = dataUtil.remove_stopWords(rawData)


    
    hash1 =Simhash(rawData)
    rawData = str(open('2.txt','r').read())
   
    rawData = dataUtil.cutText_for_hash(rawData)
    #rawData = dataUtil.remove_stopWords(rawData)
    hash2 = Simhash(rawData)
    print "*********************************"
    print '%f%% percent similarity on hash' %(100*(hash1.similarity(hash2)))
    print hash1.distance(hash2),"bits differ out of", hash2.f
    print "*********************************"
    end = time.time()
    time = end - start
    print '运行时间:' + str(time)

