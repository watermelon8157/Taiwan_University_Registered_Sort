
# coding: utf-8
#建立資料庫連線方式
# In[1]:

#http://www.runoob.com/python3/python3-mysql.html
#此 Cell 一定要執行成功，且設定自己的學號以及密碼，之後才能work!
#import pymysql as mysql #載入 pymysql
import pandas as pd #載入 pandas
#pUser = '#你的帳號#';pPasswd='#密碼#';pDb= '#資料庫名稱#'
pUser = 'root';pPasswd='1234';pDb='py_106_tmu' #設定對應變數帳號密碼
pHost ='localhost'


# In[2]:

class DBA(object):
    #///pType資料來源
    def __init__(self,pType):
        self.lastError = '';
        self.isFromMySQL = False
        self.Data = pd.DataFrame()
        self.type = pType
        if self.type == '使用MySQL資料庫':
            self.isFromMySQL = True
            sql ='SELECT * FROM university_105'
            cols = ['學年度','學校類別','設立別','學校代碼','學校名稱','日間','學制別','科系代碼','科系名稱','學生總計','新生註冊率','一年級人數','縣市名稱','體系別']
            self.Data = self.getDataFrame(sql,cols)
        else:
            self.Data = pd.read_excel('105ENROLL_ALL.xlsx')
     #取得資料
    def getData(self):
        return self.Data
    #取得錯誤訊息
    def getLastError(self):
        pStr = self.lastError
        return pStr
    #資料庫連線
    def DB_connect(self):
        self.lastError = ''
        return mysql.connect(host='127.0.0.1',user=pUser,passwd=pPasswd,db=pDb,charset='utf8',use_unicode=True)
    #取得資料
    #////取得資料
    #///  pSQL 取得資料SQL語法
    #/// pCols 取得欄位
    def getDataFrame(self,pSQL,pCols):
        result = pd.DataFrame(columns=pCols)
        #import mysql.connector
        ##連接資料庫
        db = None
        try:
            db = self.DB_connect()
            cursor = db.cursor()
            # 执行SQL语句
            cursor.execute(pSQL)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                pList =[];
                for i in range(len(pCols)):
                    pList.append(row[i])
                result.loc[len(result)] = pList
            cursor.close()
        except:
            self.lastError = '資料庫連線失敗!'
        # 关闭数据库连接
        if db != None:
            db.close()
        return result


# In[ ]:



