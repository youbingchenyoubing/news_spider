# -*- coding: utf-8 -*-
import jieba
from word2Vec import Word2Vector
import property as propertyUtil

import sys 
import os
reload(sys) 
import re
sys.setdefaultencoding('utf-8')

Path = os.path.abspath(os.path.dirname(__file__))
class DataUtils(object):
    def __init__(self, word2VecPath = None, stopWordPath = None, load = True):
        file_path = Path + '/conf/system.properties'
        self.props = propertyUtil.parse(file_path)
        if word2VecPath is None:
            self.word2VecPath = self.props.get("EMBEDDING_PATH")
        if stopWordPath is None:
            self.stopWordPath =  self.props.get("STOPWORDS_PATH")
        self.stopWords = self._getStopWords()

        if load:
            #print word2VecPath
            self.word2Vec = Word2Vector(word2VecPath)

    def _getStopWords(self):
        result = []
        stopWordsFile = open(Path + '/' + self.stopWordPath, "r")
        for line in stopWordsFile:
            result.append(line.strip())
        return result
        
    def remove_stopWords(self, words):
        newWords = []
        for word in words:
            if word not in self.stopWords:
                newWords.append(word)
        return newWords


    def cutText_for_hash(self, rawData):
        rawData = rawData.replace('\r', '')
        rawData = rawData.replace('\n', '')
        rawData = rawData.replace('\t', '')
        rawData = rawData.replace(' ', '')
        words = jieba.cut(rawData)
        words = self.remove_stopWords(words)
        return words

    def cutText(self, rawData):
        '''
      
        '''
        words = jieba.cut(rawData)
        #words = " ".join(words).encode("UTF-8")
        words = " ".join(words)
        return words

    def words_to_index(self, rawData):
        '''
        
        '''
        rawData = rawData.replace('\r', '')
        rawData = rawData.replace('\n', '')
        rawData = rawData.replace('\t', '')
        words = self.cutText(rawData)
        words = words.split(' ')
        words = self.remove_stopWords(words)
        #print words
        result = self.word2Vec.batch_index(words)
        return result

    def loadWordsWeightsMap(self):
        wordsNumFile = open(self.props.get("WORDS_NUM_MAP_PATH"), 'r')
        wordsNumMap = {}
        for line in wordsNumFile:
            item = line.split(" ")
            wordsNumMap[item[0]] = int(item[1])
        wordsNumFile.close()

        wordsWeightsMap = {}
        for (key, value) in wordsNumMap.items():
            if wordsNumMap[key] == 0:
                wordsNumMap[key] = 1000000
            wordsWeightsMap[key] = self.weight_fn(wordsNumMap[key])

        #wordsWeightMap['UNK'] = 0.00001
        return wordsWeightsMap
    
    def weight_fn(self, x):
        return 1.0 / x
   


class PreTrainDataBuild(object):
    '''
    '''
    def __init__(self, dataSetPath, dataLabelPath):
        self.dataSetPath = dataSetPath
        self.dataLabelPath = dataLabelPath
        self.dataUtil = DataUtils( Path +"/data/word2Vec.bin")
        pass


    def addTrainData(self, data_path, isPos = True):
        data = open(data_path, "r")
        content = ""
        for line in data:
            content += line
        data.close()
        result = self.dataUtil.words_to_index(content)
        line = ""
        for index in result:
            line += str(index) + " "

        dataSet = open(self.dataSetPath, "a")
        dataLabel = open(self.dataLabelPath, "a")
        dataSet.write(str(line) + "\n")
        if isPos:
            dataLabel.write(str(1) + "\n")
        else:
            dataLabel.write(str(0) + "\n")
        dataSet.close()
        dataLabel.close()

    def batchAddTrainData(self, path, isPos = True):  
        filelist =  os.listdir(path)
        for filename in filelist:
            filepath = os.path.join(path, filename) 
            print filepath
            self.addTrainData(filepath, isPos)



def preTrainData():
    preTrainData = PreTrainDataBuild(Path + "/data/dataSet.txt", Path + "/data/dataLabel.txt")
    preTrainData.batchAddTrainData(Path + "/data/news/shehui", True)
    preTrainData.batchAddTrainData(Path + "/data/news/jiaoyu", False)
    preTrainData.batchAddTrainData(Path + "/data/news/keji", False)



