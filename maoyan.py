import re
import requests
import csv
import os
import time



class MaoYan():
    def __init__(self):
        self.url = "http://maoyan.com/board/4"
        self.fieldnames = ['index','title', 'actor','time','score']
        self.file = 0
        
    def file_del(self):
        files = os.listdir(os.getcwd())   #列出目录下的文件
        for file in files:
            suffix = file.split('.')[-1]
            if suffix == 'csv':
                os.remove(file)
                print(file,"文件已经被删除")

    #"思路：先创建文件，然后返回文件操作对象， 或者创建全局操作对象"
    def file_cre(self):
        self.file = open('my.csv','a', newline='')
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        self.writer.writeheader()


    def url_cre(self):
        for i in range(10):
            url_start = "http://maoyan.com/board/4?offset="
            url = url_start + str(i*10)
            yield url

            
    def html_get(self):
        for url in self.url_cre():
            r = requests.get(url)
            html = r.text
            yield html
        
            
    def html_parse(self):
        
        for html in self.html_get():
            p2 = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?class="name".*?><a.*?>(.*?)</a>.*?"star".*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
            items = re.findall(p2,html)
            for item in items:
                info = {
                    'index':item[0],
                    'title':item[1],
                    'actor':item[2].strip().split('：')[-1],
                    'time':item[3].split('：')[-1],
                    'score':item[4]+item[5],
                }
                print(info)
                #self.save_to_csv(info)

                

    def save_to_csv(self,info):
        global writer
        if self.writer.writerow(info):
            print("保存成功")
            


    def file_close(self):
        self.file.close()   #关闭文件
        
        


    def main(self):
        #self.file_del()      #首先进行文件删除
        #self.file_cre()      #创建文件
        self.html_parse()    #解析并存储
        #self.file_close()    #关闭文件
           

if __name__ == "__main__":
    s_time = time.time()
    app = MaoYan()
    app.main()
    e_time = time.time()
    print("总耗时:", e_time-s_time)
