### mongodb 启动
```shell 
docker run -p 127.0.0.1:27017:27017 -v /home/wwg/mogo_db/db:/data/db -d mongo:3.6
```
### web启动
```shell
cd  /home/wwg/news_spider/news_spider/news_web
sh run.sh & 
```
### es
```shell
chown -R 1000:1000 /home/wwg/data_es/elasticsearch/

docker run -d --privileged=true --name elasticsearch -e "discovery.type=single-node" -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -v /home/wwg/news_spider/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml -v /home/wwg/data_es/elasticsearch/:/usr/share/elasticsearch/data/:rw elasticsearch:6.4.0
https://www.elastic.co/guide/en/elasticsearch/reference/6.4/docker.html
curl http://localhost:9200/news_spider_db/articles_testN/_search
curl http://localhost:9200/news_spider_db/articles_testP/_search
```

### keras 
```
sudo pip install numpy
sudo pip install keras==1.1.2
sudo pip install h5py
sudo pip install Cython
sudo pip install word2vec
```
