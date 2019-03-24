# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    article_url = scrapy.Field()  #文章的链接

    article_source = scrapy.Field() #文章来自哪个网站

    article_title = scrapy.Field() #文章的标题

    article_source_from = scrapy.Field() #来源哪个新闻社


    article_content = scrapy.Field() #文章内容

    article_publish_time = scrapy.Field() # 文章发布时间

    #article_preprocess_function_Name = 


    preprocess_class = scrapy.Field() #文章预处理的类名，不同的文章预处理的方式不一样

    #processed_content = scrapy.Field() # 处理完的内容

    #processed_title = scrapy.Field() #预处理完的标题

    #article_label = scrapy.Field() #文章分类的类别

    article_discuss = scrapy.Field() #文章评论

    article_discuss_number = scrapy.Field() # 文章评论数

    article_attend_number = scrapy.Field() # 文章参与人数（阅读量）

    #article_read_number = scrapy.Field() # 
    
    #simhash = scrapy.Field() # 存储文章的hashid,主要这个是用来计算覆盖率

    #is_repeate = scrapy.Field() # 文章的最大重复率，大于80%就默认是重复多的

    #article_max_correlation_id = scrapy.Field() # 最大相似文章的ID

    #article_label_state = scrapy.Field() #文章类标状态 0 表示分类器预测，1表示学生挑选，2表示老师审核通过
    pass
