
# coding: utf-8

# In[34]:

#http://www.runoob.com/python3/python3-mysql.html
#此 Cell 一定要執行成功，且設定自己的學號以及密碼，之後才能work!
import pymysql as mysql #載入 pymysql
import pandas as pd #載入 pandas
#pUser = '#你的帳號#';pPasswd='#密碼#';pDb= '#資料庫名稱#'
pUser = 'root';pPasswd='1234';pDb='py_106_tmu' #設定對應變數帳號密碼
pHost ='localhost'

class DBA(object):
    #///pType資料來源
    def __init__(self,pType):
        self.lastError = '';
        self.isFromMySQL = False
        self.Data = pd.DataFrame()
        self.type = pType
        if self.type == '使用MySQL資料庫':
            self.Data = pd.read_excel('105ENROLL_ALL.xlsx')
            #self.isFromMySQL = True
            #sql ='SELECT * FROM university_105'
            #cols = ['學年度','學校類別','設立別','學校代碼','學校名稱','日間','學制別','科系代碼','科系名稱','學生總計','新生註冊率','一年級人數','縣市名稱','體系別']
            #self.Data = self.getDataFrame(sql,cols)
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
        return mysql.connect(host=pHost,user=pUser,passwd=pPasswd,db=pDb,charset='utf8',use_unicode=True)
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


# In[35]:

#http://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html
#載入套件
from ipywidgets import *#網頁互動
#widgets 元素 #HBox 橫軸 #VBox 縱軸 #Layout 畫布
from IPython.core.display import display, HTML #輸出顯示
from functools import partial #互動程式用 #http://blog.blackwhite.tw/2013/02/python-functoolspartial.html
#from DBA import * #資料庫連線設定
import datetime
import time
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei'] #將預設字體改用SimHei字體
import matplotlib.pyplot as plt


# In[36]:

# RadioButtons
tiawanCity = ['30 臺北市','01 新北市','03 桃園市','06 臺中市','11 臺南市','12 高雄市']
chartChk = widgets.RadioButtons(options=['各科系大學系所註冊率(10名)','臺灣六都大學系所註冊率'])
chartChk_data = widgets.RadioButtons(options=['倒數幾名註冊率(註冊率)','前幾名註冊率(新生人數)'])
chartChk_school = widgets.RadioButtons(options=['公立','私立'])
#定義按鈕
buttonSchool = widgets.Button(description='搜尋學校名稱')
buttonDept = widgets.Button(description='搜尋科系名稱')
buttoncity = widgets.Button(description='搜尋縣市')
button0 = widgets.Button(description='設定資料取得方式')
button1 = widgets.Button(description='查詢報表' )
button2 = widgets.Button(description='產生圖表' )
#定義下拉式選單
schooldp = widgets.Dropdown(options=['一般大學', '技專校院'],disabled=False,layout=Layout(width='150px'))
school_name = widgets.Dropdown(options=['請選擇'])
dept_name = widgets.Dropdown(options=['請選擇'])
city = widgets.Dropdown(options=['請選擇'])
#chartDp = widgets.RadioButtons(options=['折線圖'])
chartDp = widgets.RadioButtons(options=['註冊率及新生人數'])
#產生畫面及按鈕功能
cols = ['學年度','學校類別','設立別','學校代碼','學校名稱','日間','學制別','科系代碼','科系名稱','學生總計','新生註冊率','一年級人數','縣市名稱','體系別']
class General_functions(object):
    #####建構子(設定畫面)
    def __init__(self):
        #//判斷是否已經設定資料了
        self.chartDF = None
        self.isSetData = False;self.DBA = None
        self.HTML0 = widgets.HTML(value="查詢大學新生入取率:")
        #///查詢項目
        self.Label1 = widgets.Label(value="查詢方式:")
        self.dpd1 = widgets.Dropdown(options=['使用CSV檔案', '使用MySQL資料庫'],disabled=False,layout=Layout(width='150px'))
        #self.dpd1 = widgets.Dropdown(options=['使用CSV檔案'],disabled=False,layout=Layout(width='150px'))
        #///學年度
        self.Label2 = widgets.Label(value="學年度:")
        self.sYear = widgets.Dropdown(options=['請選擇'] ,disabled=False,layout=Layout(width='100px'))
        self.Label2_1 = widgets.Label(value="至:")
        self.eYear = widgets.Dropdown(options=['請選擇'] ,disabled=False,layout=Layout(width='100px'))  
        #///學校類別
        self.Label3 = widgets.Label(value="學校類別:")
         #///設立別
        self.Label4 = widgets.Label(value="設立別:")
        self.school_type1 = widgets.Checkbox(value=True,description='日間部(學制)',disabled=True)
        #///學制別
        self.Label5 = widgets.Label(value="學制別:")
        self.school_class = widgets.Checkbox(value=True,description='學士班(含四技)',disabled=True)
        self.Label6 = widgets.Label(value="學校名稱:")
        self.Labelsc = widgets.Label(value="快速搜尋:")
        self.school_name_txt = widgets.Text(layout=Layout(width='180px'))
        
        self.LabelDept = widgets.Label(value="科系名稱:")
        self.LabeldeptSearch = widgets.Label(value="快速搜尋:")
        self.dept_name_txt = widgets.Text(layout=Layout(width='180px'))
        
        self.LabelCity = widgets.Label(value="縣市:")
        self.LabelCitySearch = widgets.Label(value="快速搜尋:")
        self.City_txt = widgets.Text(layout=Layout(width='180px'))
        #///系統訊息
        self.Label7 = widgets.Label(value="系統訊息:")
        self.Valid = widgets.Valid(value=False,description='產生介面...',layout=Layout(width='600px'))
        #///產生結果
        self.html = widgets.HTML(value="")
        #///圖表選擇
        self.Label9 = widgets.Label(value="選擇圖表:",layout=Layout(width='180px'))
        self.Label9_1 = widgets.Label(value="選擇資料類型:",layout=Layout(width='180px'))
        self.Label9_2 = widgets.Label(value="選擇資料資料範圍:",layout=Layout(width='180px'))
        self.chartHtml = widgets.HTML(value="")
    #///錯誤訊息
    def isValid(self, pMsg=''):
        if pMsg != '':
            self.Valid.description = pMsg
        else:
            self.Valid.description = '程式錯誤，請洽資訊人員!'
        self.Valid.value =False
     #///當按鈕按下去的時候要做的事情
    def on_button0_clicked(self, button):
        button.disabled = True
        self.isValid('資料載入中....')
        self.DBA = DBA(self.dpd1.value)
        if self.DBA.getLastError() != '':
            self.isValid(self.DBA.getLastError())
        else:
            self.Valid.description = '資料設定成功!'
            self.Valid.value =True
            self.isSetData = True
            self.setDropDownList()
        button.disabled = False
    def getTableHTML(self, a):
        pStr = '<div style=" width: 100%;height: 500px;overflow: scroll;"><table class="table table-striped table-hover">' 
        pStr += '<tr class="info">' 
        for i in cols:
            pStr += '<th>' +str(i)+'</th>'
        pStr += '</tr>'
        for i in a.values:
            pStr += '<tr>' 
            for j in i:
                pStr += '<td>' +str(j)+'</td>' 
            pStr += '</tr>'
        pStr += '</table></div>'  
        return pStr
    #Year
    def setDropDownListYear(self,pList):
        pList.append('請選擇');pList.reverse()
        self.sYear.options = pList;self.sYear.value =self.sYear.options[1]
        self.eYear.options = pList;self.eYear.value =self.eYear.options[1]
    def setDropDownListSchool_name(self,pList):
        pList.append('請選擇');pList.reverse()
        school_name.options = pList
    def setDropDownListCity(self,pList):
        pList = sorted(pList, key=lambda x: x[0:2]);pList.reverse()
        pList.append('請選擇');pList.reverse()
        city.options = pList
    def setDropDownListDept_name(self,pList):
        pList.append('請選擇');pList.reverse()
        dept_name.options = pList
    #設定下拉式選單
    def setDropDownList(self):
        self.setDropDownListCity(list(set([str(x) for x in set(list(self.DBA.getData()['縣市名稱'])) if str(x) != 'nan'])))
        self.setDropDownListYear(list(set([str(int(x)) for x in set(list(self.DBA.getData()['學年度'])) if str(x) != 'nan'])))
        self.setDropDownListSchool_name(list(set([str(x) for x in set(list(self.DBA.getData()['學校名稱'])) if str(x) != 'nan'])))
        self.setDropDownListDept_name( [str(x) for x in set(list(self.DBA.getData()['科系名稱'])) if str(x) != 'nan'])
    #///當按鈕按下去的時候要做的事情
    def on_button1_clicked(self, button):
        if self.isSetData:
            self.html.value = self.getTableHTML(self.getReport())
        else:
            self.isValid('請先設定資料!')
     #///當按鈕按下去的時候要做的事情
    def on_buttoncity_clicked(self, button):
        if self.isSetData:
            button.disabled = True
            if len(self.City_txt.value) > 0:
                pcity = set(list(self.DBA.getData()['縣市名稱']))
                pcity_name = [x for x in pcity if self.City_txt.value in str(x)]
                if len(pcity_name) > 0:
                    city.options = pcity_name
                else:
                    self.isValid('查無"'+self.City_txt.value + '"縣市關鍵字!')
            else:
                self.setDropDownListCity(list(set([str(x) for x in set(list(self.DBA.getData()['縣市名稱'])) if str(x) != 'nan'])))
            button.disabled = False
        else:
            self.isValid('請先設定資料!')
    #///當按鈕按下去的時候要做的事情
    def on_button2_clicked(self, button):
        if self.isSetData:
            fileName = self.getChart()
            self.html.value = '<img src="'+fileName+'" alt="no image!" width="900" height="600">' + '</br>'+ self.getTableHTML(self.chartDF)
        else:
            self.isValid('請先設定資料!')
    #///當按鈕按下去的時候要做的事情
    def on_buttonSchool_clicked(self, button):
        if self.isSetData:
            button.disabled = True
            if len(self.school_name_txt.value) > 0:
                if schooldp.value == '一般大學':
                    pTemp = set(list(self.DBA.getData().loc[self.DBA.getData()['學校類別']=='一般']['學校名稱']))
                elif schooldp.value == '技專校院':
                    pTemp = set(list(self.DBA.getData().loc[self.DBA.getData()['學校類別']=='技職']['學校名稱']))
                else:
                    pTemp = set(list(self.DBA.getData()['學校名稱']))
                pSchool_name = [x for x in pTemp if self.school_name_txt.value in str(x)]
                if len(pSchool_name) > 0:
                    school_name.options = pSchool_name
                else:
                    self.isValid('查無"'+self.school_name_txt.value + '"學校關鍵字!')
            else:
                self.setDropDownListSchool_name(list(set([str(x) for x in set(list(self.DBA.getData()['學校名稱'])) if str(x) != 'nan'])))
            button.disabled = False
        else:
            self.isValid('請先設定資料!')
    #///當按鈕按下去的時候要做的事情
    def on_buttonDept_clicked(self, button):
        if self.isSetData:
            button.disabled = True
            if len(self.dept_name_txt.value) > 0:
                if school_name.value != '請選擇':
                    pTemp = set(list(self.DBA.getData().loc[self.DBA.getData()['學校名稱']==school_name.value]['科系名稱']))
                else:
                    pTemp = set(list(self.DBA.getData()['科系名稱']))
                pDept_name = [x for x in pTemp if self.dept_name_txt.value in str(x)]
                if len(pDept_name) > 0:
                    dept_name.options = pDept_name
                else:
                    self.isValid('查無"'+self.dept_name_txt.value + '"科系關鍵字!')
            else:
                self.setDropDownListDept_name( [str(x) for x in set(list(self.DBA.getData()['科系名稱'])) if str(x) != 'nan'])
            button.disabled = False
        else:
            self.isValid('請先設定資料!')
    #///當按鈕按下去的時候要做的事情
    def on_schooldp_change(self,dp):
        if self.isSetData:
            if dp['type'] == 'change' and dp['name'] == 'value':
                dp.disabled = True
                pTemp = self.DBA.getData().loc[self.DBA.getData()['學校類別'] == '一般']
                
                if dp['new'] == '一般大學':
                     pTemp = self.DBA.getData().loc[self.DBA.getData()['學校類別'] == '一般']
                if dp['new'] == '技專校院':
                     pTemp = self.DBA.getData().loc[self.DBA.getData()['學校類別'] == '技職']
                if city.value != '請選擇':
                    pTemp = pTemp.loc[self.DBA.getData()['縣市名稱'] == city.value ]
                self.setDropDownListSchool_name(list(set(pTemp['學校名稱'])))
                self.setDropDownListDept_name(list(set(pTemp['科系名稱'])))
                self.setDropDownListCity(list(set(pTemp['縣市名稱'])))
                dp.disabled = False
        else:
            self.isValid('請先設定資料!')
     #///當按鈕按下去的時候要做的事情
    def on_city_change(self,dp):
        if self.isSetData:
            if dp['type'] == 'change' and dp['name'] == 'value':
                dp.disabled = True
                if schooldp.value == '一般大學':
                    self.setDropDownListSchool_name(list(set(self.DBA.getData().loc[(self.DBA.getData()['縣市名稱'] == dp['new']) & (self.DBA.getData()['學校類別'] == '一般')]['學校名稱'])))
                elif schooldp.value == '技專校院':
                    self.setDropDownListSchool_name(list(set(self.DBA.getData().loc[(self.DBA.getData()['縣市名稱'] == dp['new']) & (self.DBA.getData()['學校類別'] == '技職')]['學校名稱'])))
     
                dp.disabled = False
        else:
            self.isValid('請先設定資料!')
     #///當按鈕按下去的時候要做的事情
    def on_school_name_change(self,dp):
        if self.isSetData:
            if dp['type'] == 'change' and dp['name'] == 'value':
                dp.disabled = True
                self.setDropDownListDept_name(list(set(self.DBA.getData().loc[self.DBA.getData()['學校名稱'] ==  dp['new']]['科系名稱'])))
                dp.disabled = False
        else:
            self.isValid('請先設定資料!')
    #產生報表
    def getReport(self):
        pTemp = self.DBA.getData()
        if schooldp.value != '請選擇':
            if schooldp.value == '一般大學':
                 pTemp = pTemp.loc[self.DBA.getData()['學校類別'] == '一般']
            elif schooldp.value == '技專校院':
                 pTemp = pTemp.loc[self.DBA.getData()['學校類別'] == '技職']
        if school_name.value != '請選擇':   
            pTemp = pTemp.loc[self.DBA.getData()['學校名稱'] ==school_name.value]
        if dept_name.value != '請選擇':   
            pTemp = pTemp.loc[self.DBA.getData()['科系名稱'] ==dept_name.value]
        if city.value != '請選擇':   
            pTemp = pTemp.loc[self.DBA.getData()['縣市名稱'] ==city.value]
        return pTemp
    #產生chart
    def getChart(self):
        plt.cla()
        pDf = self.getReport()
        pDf = pDf.loc[pDf['設立別'] == chartChk_school.value]
        pngName = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.png'
        fig, ax1 = plt.subplots()
        if chartChk.value == '臺灣六都大學系所註冊率':
            pDf = self.getChartCity(chartChk.value,pDf)
            plt.xlabel("縣市名稱")
            plt.xticks(range(len(pDf)),list(pDf['縣市名稱']))
        else:
            pDf = self.getChartDept(chartChk.value,pDf)
            plt.xlabel("科系名稱")
            plt.xticks(range(len(pDf)),list(pDf['科系名稱']))
        
        self.chartDF = pDf
        yLay = list(pDf['一年級人數'])
        y2Lay = list(pDf['新生註冊率'])
        
        ax1.bar(range(len(pDf)),yLay, 0.35)
        ax1.set_ylabel('一年級人數', color='b')
        ax1.tick_params('y', colors='b')

        ax2 = ax1.twinx()
        ax2.plot(y2Lay,'r--o',color="red")
        ax2.set_ylabel('新生註冊率', color='r')
        ax2.tick_params('y', colors='r')

        plt.grid( color='#95a5a6',linestyle='--', linewidth=1 ,axis='y',alpha=0.4)
        pTitle = ''
        if city.value != '請選擇':
            pTitle += city.value + ' '
        if school_name.value != '請選擇':
            pTitle += school_name.value + ' '
        else:
            pTitle += chartChk_school.value + schooldp.value + '  '
        if dept_name.value != '請選擇':
            pTitle += dept_name.value + ' '
        pTitle += '\n'+ chartChk.value + ' ' + chartChk_data.value
        plt.title(pTitle)
        fig.tight_layout()
        plt.savefig(pngName, dpi=300)
        return pngName
    #六都資料
    def getChartCity(self,pVal,pDf):
        pTemp = pd.DataFrame(columns=list(pDf.columns))
        for i in tiawanCity:
            if len(pDf.loc[pDf['縣市名稱'] == i]) >0:
                pList =  pDf.loc[pDf['縣市名稱'] == i]
                #print(pList.sort_values(by='一年級人數', ascending=0).iloc[0].tolist())
                if chartChk_data.value == '前幾名註冊率(新生人數)':
                    pTemp.loc[len(pTemp)] = pList.sort_values(by=['新生註冊率','一年級人數'], ascending=[0,0]).iloc[0].tolist()
                else:
                    pTemp.loc[len(pTemp)] = pList.sort_values(by='新生註冊率', ascending=1).iloc[0].tolist()
        return pTemp
    #科別資料
    def getChartDept(self,pVal,pDf):
        #print(pList.sort_values(by='一年級人數', ascending=0).iloc[0].tolist())
        if chartChk_data.value == '前幾名註冊率(新生人數)':
            pTemp = pDf.sort_values(by=['新生註冊率','一年級人數'], ascending=[0,0])
        else:
            pTemp = pDf.sort_values(by='新生註冊率', ascending=1)
        return pTemp.head(10)
    #///將顯示畫面印出
    def draw_board(self):
        #設定互動動作
        buttonSchool.on_click(partial(self.on_buttonSchool_clicked))
        buttonDept.on_click(partial(self.on_buttonDept_clicked))
        button0.on_click(partial(self.on_button0_clicked))
        button1.on_click(partial(self.on_button1_clicked))
        button2.on_click(partial(self.on_button2_clicked))
        #chartChk_school
        buttoncity.on_click(partial(self.on_buttoncity_clicked))
        self.Accordion =  widgets.Accordion(children=[button1,VBox([HBox([self.Label9,chartChk_data]),
                                                                    HBox([self.Label9_1,chartChk]),
                                                                     HBox([widgets.Label(value="選擇設立別:",layout=Layout(width='180px')),chartChk_school]),
                                                                    HBox([self.Label9_2,chartDp,button2]),
                                                                    self.chartHtml])])
        self.Accordion.set_title(0, '產生報表(dataFrame)')
        self.Accordion.set_title(1, '產生圖表(Chart)')
        schooldp.observe(partial(self.on_schooldp_change))
        school_name.observe(partial(self.on_school_name_change))
        city.observe(partial(self.on_city_change))
        #將顯示畫面印出......
        HTML(display( VBox([self.HTML0,
                            HBox([self.Label7,self.Valid]),
                            HBox([self.Label1,self.dpd1,button0]),
                           HBox([self.Label2,self.sYear,self.Label2_1,self.eYear]),
                           HBox([self.Label3,schooldp]),
                           HBox([self.Label4,self.school_type1,self.Label5,self.school_class]),
                           HBox([self.LabelCity,city,self.LabelCitySearch,self.City_txt,buttoncity]),
                           HBox([self.Label6,school_name,self.Labelsc,self.school_name_txt,buttonSchool]),
                           HBox([self.LabelDept,dept_name,self.LabeldeptSearch,self.dept_name_txt,buttonDept]),
                            
                           self.Accordion,self.html])))
        self.Valid.value = True
        self.Valid.description = "產生查詢介面完成!"


# In[37]:

#GF = General_functions() #建立物件
#GF.draw_board()#產生互動畫面


# In[38]:

GF = General_functions() #建立物件
GF.draw_board()#產生互動畫面


# In[ ]:



