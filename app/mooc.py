from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup  #executable_path为chromedriver.exe的解压安装目录，需要与chrome浏览器同一文件夹下
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# url='https://www.icourse163.org/course/BIT-268001'   #爬取Python语言程序设计为例
def parse_detail(url,sheetname):
    driver = webdriver.Chrome(executable_path=r"D:\chromedriver\chromedriver.exe")
    driver.get(url)
    cont=driver.page_source             #获得初始页面代码，接下来进行简单的解析
    # soup=BeautifulSoup(cont,'html.parser')
    # #print(soup)
    WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located((By.ID, 'review-tag-button')))
    ele=driver.find_element_by_id("review-tag-button")  #模仿浏览器就行点击查看课程评价的功能

    ele.click()


    xyy=driver.find_element_by_class_name("ux-pager_btn__next")#翻页功能，类名不能有空格，有空格可取后边的部分

    connt=driver.page_source
    soup=BeautifulSoup(connt,'html.parser')
    #print(soup)
            #n页的总评论
    content=soup.find_all('div',{'class':'ux-mooc-comment-course-comment_comment-list_item_body_content'})#包含全部评论项目的总表标签
    #print(content)
    acontent = []
    for ctt in content:       #第一页评论的爬取
        scontent=[]
        aspan=ctt.find_all('span') #刚获得一页中的content中每一项评论还有少量标签
        for span in aspan:
            scontent.append(span.string)#只要span标签里边的评论内容
        acontent.append(scontent) #将一页中的一条评论加到总评论列表里，知道该页加完

    # print(acontent)
    # print(len(acontent))
    for i in range(20): #翻页 286-0+1次，也就是287次，第一页打开就是，上边读完第一页了
        xyy.click()
        connt = driver.page_source
        soup = BeautifulSoup(connt,'html.parser')
        content = soup.find_all('div',{'class': 'ux-mooc-comment-course-comment_comment-list_item_body_content'})  # 包含全部评论项目的总表标签
        for ctt in content:
            scontent = []
            aspan = ctt.find_all('span')
            for span in aspan:
                scontent.append(span.string)
            acontent.append(scontent)
        df = pd.DataFrame(acontent)
        df.to_excel('%s.xlsx'%sheetname,index=False)


    driver.close()

data=pd.read_csv(r'url.txt',)
# acontent = []

for x ,y in zip(data.name,data.url):
    parse_detail(y,x)




