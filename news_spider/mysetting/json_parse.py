# -*- coding: utf-8 -*-
#coding=utf-8   
import json
import logging
# 加载json文件类
class JsonLoad(object):

#读取配置文件
	def __init__(self,filePath):

		if filePath == '':
			filePath = "json_setting.json"
		with open(filePath,'r') as f:

			self.data = json.load(f)
#改变配置文件
	def changejson(self,filePath):

		if filePath == '':
			filePath = "json_setting.json"
		
		with open(filePath,'w') as f:

			json.dump(self.data,f)

	def getdata(self):

		return self.data

	def getlist(self):
		user_agent_list = []
		for json_key in self.data:
			user_agent_list.extend(self.data[json_key])

		return user_agent_list




