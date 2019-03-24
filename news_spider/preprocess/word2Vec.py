# -*- coding: utf-8 -*-
import numpy as np
import word2vec
import property as propertyUtil
import os
Path = os.path.abspath(os.path.dirname(__file__))
class Word2Vector(object):
    def __init__(self, embeddings_path = None):
        file_path = Path + '/conf/system.properties'
        self.props = propertyUtil.parse(file_path)
        if embeddings_path is None:
            embeddings_path = self.props.get("EMBEDDING_PATH")
        model = word2vec.load(Path + '/' + embeddings_path)
        self.model = model
	self.embeddings = model.vectors.tolist()
	self.vocab = model.vocab.tolist()
        self.wordsMap = self._build(self.vocab)

    def _build(self, vocab):
    	wordsMap = {}
    	for i, word in zip(xrange(len(vocab)), vocab):
    	    wordsMap[word] = i
        wordsMap['UNK']  = len(vocab)
        UNK = np.zeros(len(self.embeddings[0]))
        self.embeddings.append(UNK)
        return wordsMap


    def index(self, word):
    	if word in self.wordsMap:
    	    return self.wordsMap[word]
    	else:
            return self.wordsMap['UNK']
    
    def batch_index(self, words):
        result = [] 
        for word in words:
            result.append(self.index(word))
        return result

    def lookup(self, index):
    	return self.embeddings[index]








    
	
