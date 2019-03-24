# -*- coding: utf-8 -*-
import sys
import os
reload(sys)
import re
sys.setdefaultencoding('utf-8')
# pairPath = os.path.abspath(os.path.dirname(__file__))
# sys.path.append(pairPath)
 from simhash import Simhash
from dataUtil import DataUtils
#from filter_noise import cx_extractor_Python #调用过滤标签 scrpit等信息
from goose import Goose
from goose.text import StopWordsChinese
def singleton(cls):
    instance = {}

    def wrapper(*args,**kwargs):
        if cls not in instance:

            instance[cls] = cls(*args,**kwargs)
        return instance[cls]

    return wrapper
@singleton
class BasePreProcessItem(object):
    def __init__(self, word2VecPath =None):
        self.dataUtil = DataUtils(word2VecPath)
        #self.extractor = cx_extractor_Python()
        self.extractor_goose = Goose({'stopwords_class': StopWordsChinese})
    def preProcessData(self, data):
        a = self.extractor_goose.extract(raw_html=data['article_content'])
        article_content = a.cleaned_text
        #article_content = self.extractor.filter_tags(data['article_content'])
        #article_content= self.extractor.getText(article_content)
        #article_content = self._remove_htmlTags(self.__remove_scripts(data['article_content']))
        #print article_content
        data['processed_content'] = self.dataUtil.words_to_index(article_content)

        article_title = self._remove_htmlTags(data['article_title'])
        data['processed_title'] = self.dataUtil.words_to_index(article_title)
        processed_content = self.dataUtil.cutText_for_hash(article_content)
        data['simhash'] =Simhash(processed_content).value


    def preProcessConent(self,data):

        # if data['flag'] == 3: #单纯的视频，不更新向量和哈希值
        #     return
        # article_content = None
        # if data['flag'] == 1: #article_xpath 能提取出内容来
        #     article_content = data['article_content']
        # else:
        #     article_content = data['video_info']
        #article_content = self.extractor.filter_tags(data['article_content'])
        #article_content= self.extractor.getText(article_content)
        #article_content = self._remove_htmlTags(self.__remove_scripts(data['article_content']))
        #print "content:",article_content
        a = self.extractor_goose.extract(raw_html=data['article_content'])
        article_content = a.cleaned_text
        data['processed_content'] = self.dataUtil.words_to_index(article_content)
        processed_content = self.dataUtil.cutText_for_hash(article_content)
        data['simhash'] =Simhash(processed_content).value

    def _remove_htmlTags(self, html):
        # tag
        tag_re = re.compile(r'<[^>]+>',re.S)
        result = tag_re.sub('', html)

        ## space
        space_re = re.compile(r'&[^>]+;', re.S)
        result = space_re.sub('', result)
        return result
    def __remove_scripts(self,html):

        script_re = re.compile(r'<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I|re.S|re.M)

        result = script_re.sub('',html)
        return result
    
    def similarity(self, arg1_simhash, arg2_simhash, f = 64):
        x = (arg1_simhash ^ arg2_simhash) & ((1 << f) - 1)
        ans = 0
        while x:
            ans += 1
            x &= x - 1

        sim_rate = (f - ans) / f
        if sim_rate > 0.85:
            return 1;
        else:
            return 0; 
        



# #preTrainData()
# bpp = BasePreProcessItem()
# #data={'article_content':u"各位朋友，大家早上好！我是张小龙","article_title":u"张小龙首次全面阐述小程序，定档1月9日上线" }

# data=dict({})

# with open('data.txt') as file_object:

#     data['article_content'] = file_object.read()

# bpp.preProcessData(data)
#print data['simhash']
#print data['processed_content']
#print data['processed_title']
