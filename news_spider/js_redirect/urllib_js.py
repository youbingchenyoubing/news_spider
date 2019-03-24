# -*- coding: utf-8 -*-
#coding=utf-8


import re

class verify_js_redirect(object):

    def verify_location_replace(self,text):

        try:
            p = re.compile('location\.replace\(\"(.*?)\"\)')

            real_url = p.search(text).group(1)

            return real_url
        except BaseException,error:
            print error
            return None