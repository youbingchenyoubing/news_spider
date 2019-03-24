
import os
import datetime
class write_record(object):
    def __init__(self,filename):

        self.filename = filename
    def write_log(self,log):
        
        self.__touchfile()
        body = str(datetime.datetime.now()) + ':' +str(log) + '\n'
        with open(self.filename,'a') as f:
            f.write(body)

    def __touchfile(self):
        
        if not os.path.exists(self.filename):
            file_dir = os.path.split(self.filename)[0]

            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            os.mknod(self.filename) 