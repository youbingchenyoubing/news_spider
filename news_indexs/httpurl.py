#coding=utf8
import urllib2
import json
import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='elasticseach.log',
    filemode='a')

def http_put(URL, data):
    try:
        jdata = json.dumps(data)                  # 对数据进行JSON格式化编码
        headers = {  
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            "Content-Type":"application/json"
        }
        request = urllib2.Request(URL, jdata, headers)
        #request.add_header("Content-Type", "application/json")
        request.get_method = lambda:'PUT'           # 设置HTTP的访问方式
        request = urllib2.urlopen(request)
        return request.read()
    except BaseException, e:
        logging.error("URL=" + URL+" data=" + data)
        logging.error(e)
        return None

def http_post(URL, data):
    try:
        jdata = json.dumps(data)             # 对数据进行JSON格式化编码
        req = urllib2.Request(URL, jdata)       # 生成页面请求的完整数据
        request.add_header('Content-Type', 'application/json')
        request.get_method = lambda:'POST'           # 设置HTTP的访问方式
        response = urllib2.urlopen(req)       # 发送页面请求
        return response.read()   
    except BaseException, e:
        logging.error("URL=" + URL+" data=" + data) 
        logging.error(e)
        return None

def http_get(URL):
    try:
        response = urllib2.urlopen(URL)         #调用urllib2向服务器发送get请求
        return response.read() 
    except BaseException, e:
        logging.error("URL=" + URL)
        logging.error(e)
        return None
        


def http_delete(URL, data):
    try:
        if data:
            jdata = json.dumps(data)
            request = urllib2.Request(URL, jdata)
        else:
            request = urllib2.Request(URL)
        request.add_header('Content-Type', 'application/json')
        request.get_method = lambda:'DELETE'        # 设置HTTP的访问方式
        request = urllib2.urlopen(request)
        return request.read()
    except BaseException, e:
        logging.error("URL=" + URL + " data=" + str(data))
        logging.error(e)
        return None


#print http_put("http://localhost:9200/test/test/2", {"name":"zjl", "age":"28"})
#print "-------"
#print http_delete("http://localhost:9200/test/test/1", None)
#print "-------"
print http_get("http://localhost:9200/test/test/_search")

