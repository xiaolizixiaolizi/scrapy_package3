# -*- coding: utf-8 -*-
import os
import  pandas as pd
import  re
def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)

file_list=[]

listdir(r'E:\pachong\scrapy_package3\app\info',file_list)

file_list.remove(r'E:\pachong\scrapy_package3\app\info\合并.py')



li = []
for i in file_list:
    name=''.join(re.findall(r'[\u4e00-\u9fa5]',i))  #匹配中文
    df=pd.read_excel(i)
    df['name']=name
    order=['name',0] #改变列的顺序
    df=df[order]
    li.append(df)

writer = pd.ExcelWriter(r'E:\pachong\scrapy_package3\app\info\output.xlsx')
pd.concat(li).to_excel(writer, 'Sheet1', index=False)

writer.save()
