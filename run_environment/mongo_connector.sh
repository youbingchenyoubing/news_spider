#!/bin/bash

ntpdate time.nist.gov
#ip_host=127.0.0.1
cmd="rs.initiate();rs.conf();rs.status();"
/usr/local/mongodb/bin/mongo --port 27017 --eval $cmd
cd /usr/local/elasticsearch-5.2.2/bin
bash ./elasticsearch -d
if [ $? -eq 0 ];then
    mongo-connector --auto-commit-interval=0 -m 127.0.0.1:27017 -t 127.0.0.1:9200 -d elastic2_doc_manager -n news_spider_db.articles_testN -e article_discuss 
    if [ $? -eq 0 ];then
        #mongo-connector --auto-commit-interval=0 -m 127.0.0.1:27017 -t 127.0.0.1:9200 -d elastic2_doc_manager -n news_spider_db.articles_testP -e article_discuss
        # if [ $? -eq 0 ];then
        #     echo "sucesss"
        # else
        #     echo "mongo-connector collection error 2"
        #     exit 1
        # fi
        echo "mongo-connector run success"
    else
        echo "mongo-connector collection error"
        exit 1
    fi
else
    echo "elasticsearch error"
    exit 1
fi
 
