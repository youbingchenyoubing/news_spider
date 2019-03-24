# -*- coding: utf-8 -*-
#coding=utf-8
import os
import sys

#sys.path.append('..')
#from news_mongodb.db_connection import MongoDBConnection
from  preprocess.preProcessItem import BasePreProcessItem
try:
    import cPickle as pickle
except:
    import pickle
'''
def InitMongoDB(filename):
    if os.path.exists(filename):
        return
    print "初始化mongoDB连接"
    mongodb_obj = MongoDBConnection()

    with open(filename,'w') as f:
        pickle.dump(mongodb_obj,f)'''


def InitSimHash(filename):

    if os.path.exists(filename):
        return
    print "初始化...."

    simhash = BasePreProcessItem()

    with open(filename,'w') as f:

        pickle.dump(simhash,f)


