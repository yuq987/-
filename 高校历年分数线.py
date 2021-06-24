# -*- coding: utf-8 -*-
import json
import re #正则表达式，文字匹配
import urllib #制订URL，获取网页数据
import requests 
import xlwt #保存到excel
from bs4 import BeautifulSoup #网页解析，获取数据
import matplotlib.pyplot as plt #画图


#所有的省份（直辖市）及对应编号Id
allprovinceId = {'北京': 11, '天津': 12, '河北': 13, '山西': 14, '内蒙古': 15,
               '辽宁': 21, '吉林': 22, '黑龙江': 23,
               '上海': 31, '江苏': 32, '浙江': 33, '安徽': 34, '福建': 35, '江西': 36, '山东': 37,
               '河南': 41, '湖北': 42, '湖南': 43, '广东': 44, '广西': 45, '海南': 46,
               '重庆': 50, '四川': 51, '贵州': 52, '云南': 53,
               '陕西': 61, '甘肃': 62, '青海': 63, '宁夏': 64, '新疆': 65}
#所有的报考类型
allexamType = ['理科','文科','综合']
 

'''排名高校排名'''
def getSchoolRanking(): 
    url = 'http://www.gaosan.com/gaokao/311315.html'
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3870.400 QQBrowser/10.8.4405.400'}
    
    request = urllib.request.Request(url, headers = head ) #请求网页信息
    html = ""
    response = urllib.request.urlopen(request) #响应网页信息
    html = response.read().decode('utf-8')
    #print(html) #测试
    
    schoolRanking = []
    soup = BeautifulSoup(html,"html.parser")
    
    i = 0 #记录次数
  
    for item in soup.find_all('tr'): #查找所有符合()里要求的字符串，形成列表
            
        school = [] #保存一个学校的信息(主要存排名和学校名称)  
        item = str(item) 
        #print(item) #测试
     
        i = i + 1
        #前面5所学校和第一行列名称的格式与后面不同，分情况讨论
        if i == 1: #第1行（列名）不要
            continue
        if i in range(2, 7): #前5所学校
            #获取学校排名
            findRanking = re.compile(r'<td>(.*)</td>')
            ranking = str(re.findall(findRanking, item))
            ranking = str(ranking[2]) 
            school.append(ranking)
            
           #获取学校名称
            findName1 = re.compile(r'<td>(.*)</td>')
            name1 = str(re.findall(findName1, item))
            #print(name1) 测试
            findName2 = re.compile(r'<td style="word-break: break-all;">(.*)</td>')
            name2 = str(re.findall(findName2, name1))
            #print(name2) #测试
            name = name2[2:6]
            school.append(name)
            #print(school) #测试
            
            schoolRanking.append(school)
            
        if i in range(7,113): #第6至第100名的学校 
        
            #获取学校排名
            findRanking = re.compile(r'<td>(.*)</td>')
            ranking = str(re.findall(findRanking, item))
            #print(ranking) #测试
            ranking = str(ranking[2:4])
            #print(ranking) #测试
            
            if ranking[1] == '<': #第6~9名的学校名次的第二位是‘<’
              ranking = ranking.replace('<','')
            school.append(ranking)
            #print(school) #测试
    
            #获取学校名称
            findName = re.compile(r'<td>(.*)</td>')
            name1 = str(re.findall(findName, item))
            name2 = str(re.findall(findName, name1))
            name = name2[2:-13]
            #print(name) #测试
            school.append(name)
            #print(school) #测试
            
            schoolRanking.append(school)
            
        if i >= 113: #第100名学校及往后 
        
            #获取学校排名
            findRanking = re.compile(r'<td>(.*)</td>')
            ranking = str(re.findall(findRanking, item))
            #print(ranking) #测试
            ranking = str(ranking[2:5])
            #print(ranking) #测试
            school.append(ranking)
                
            #获取学校名称
            findName = re.compile(r'<td>(.*)</td>')
            name1 = str(re.findall(findName, item))
            name2 = str(re.findall(findName, name1))
            name = name2[2:-13]
            #print(name) #测试
            school.append(name)
            #print(school) #测试
            
            schoolRanking.append(school) #保存这个范围内学校的名称及对应排名
    
    #print(schoolRanking) #测试
    return schoolRanking

#getSchoolRanking() #测试

'''保存学校排名'''
def saveSchoolRanking(schoolRanking):
    book = xlwt.Workbook(encoding = 'utf-8',style_compression=0) #创建workbook对象
    sheet = book.add_sheet('学校排名.xls',cell_overwrite_ok=True) #创建工作表 后面的参数表示每次更改会覆盖前面的内容
    col = ("名次","学校名称")
    for i in range(0,2):
        sheet.write(0, i, col[i]) #列名
    for i in range(0,820):
        data = schoolRanking[i]
        for j in range(0,2):
            sheet.write(i+1, j,data[j]) #数据
        
    book.save('全国高校排名.xls') #保存
    
#saveSchoolRanking(getSchoolRanking()) #保存学校及排名（共820所）
  
'''根据学校名称得到学校在该网站的编号id'''
def getSchoolId(schoolName):
    url = 'https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=&f985=&is_doublehigh=&is_dual_class=&keyword=%s&nature=&page=1&province_id=&ranktype=&request_type=1&school_type=&signsafe=&size=20&sort=view_total&type=&uri=apidata/api/gk/school/lists'%(schoolName)
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}
         #伪装成浏览器  
    response = requests.get(url, headers = head) #响应网页信息
    text = json.loads(response.text)
    
    #解析网页返回的信息，找到学校ID对应的地方
    schoolId = text['data']['item'][0]['school_id'] 
    #print(schoolId) #测试
    return schoolId

'''根据省份和报考类型得到该省2016-2019年的省控线（只得到了19年之前的）'''
def getProvinceScoreLine(provinceName, examType):
    provinceId = allprovinceId[provinceName] 
    
    science1 = [] #理科一批
    science2 = [] #理科二批
    arts1 = [] #文科一批
    arts2 = [] #文科二批
    synthesize = [] #综合类
        
    for i in range(4):
        year = 2016 + i
        
        url = 'https://api.eol.cn/gkcx/api/?page=1&province_id=%d&size=20&uri=apidata/api/gk/score/proprovince&year=%d' % (provinceId, year)
        head = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3870.400 QQBrowser/10.8.4405.400'}
             #伪装成浏览器
        response = requests.get(url, headers = head) #响应网页信息
        text = json.loads(response.text)  
        #print(text) #测试
        #解析网页返回的信息，找到文理科一、二批对应的地方
        if text['code'] != "0000":
            print(text['message']) 
            return 
        if text['data']['numFound'] == 0:
            print("抱歉！我们还没有收集到该省的省控线。")
            return 
        for i in range(text['data']['numFound']): #numFound表示item的个数
            
            #综合类
            if text['data']['item'][i]['local_type_name'] == '综合':
                temp = {'year': text['data']['item'][i]['year'],
                        'score': text['data']['item'][i]['average']}
                synthesize.append(temp)
                break
            #理科
            if text['data']['item'][i]['local_type_name'] == '理科':  #找到理科对应的
                if text['data']['item'][i]['local_batch_name'] == '本科一批' or text['data']['item'][i]['local_batch_name'] == '本科批': #找到本科一批（或者本科批）对应的
                    #一个temp保存某一报考类型某一年的省控线
                    temp = {'year': text['data']['item'][i]['year'],
                            'score': text['data']['item'][i]['average']} 
                    science1.append(temp)
                elif text['data']['item'][i]['local_batch_name'] == '本科二批':
                    temp = {'year': text['data']['item'][i]['year'],
                            'score': text['data']['item'][i]['average']}
                    science2.append(temp)
                    break
            #文科
            if text['data']['item'][i]['local_type_name'] == '文科':
                if text['data']['item'][i]['local_batch_name'] == '本科一批' or text['data']['item'][i]['local_batch_name'] == '本科批':
                    temp = {'year': text['data']['item'][i]['year'],
                            'score': text['data']['item'][i]['average']}
                    arts1.append(temp)
                elif text['data']['item'][i]['local_batch_name'] == '本科二批':
                    temp = {'year': text['data']['item'][i]['year'],
                            'score': text['data']['item'][i]['average']}
                    arts2.append(temp)
                    break
    #print(science1) #测试
        
    science1.extend(science2) #将理科二批加到一批后面，science1作为理科分数线
    #print(science1) #测试
    arts1.extend(arts2) #文科二批加到一批后面，arts作为文科分数线
    if examType == '理科':
        #print(science) #测试
        return science1
    elif examType == '文科':
        return arts1
    elif examType == '综合':
        return synthesize 

'''
#测试
for key in allprovinceId.keys():
    provinceName = key  #30个省和直辖市名称
    for item in allexamType:
        typeName = item #3种报考类型
        print(getProvinceScoreLine(provinceName, typeName))
'''
        
'''根据学校Id、学校名称、省份名称、报考类型得到该学校在该省份、该报考类型的2018-2020年的分数线（只得到了18年之后的）'''
def getSchoolLine(schoolId, schoolName, provinceName, examType):
    
    url = 'https://static-data.eol.cn/www/2.0/school/%d/info.json' % (schoolId) 
    #url = url + (new Date()).getTime().toString()
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}
         #伪装成浏览器  
    
    request = urllib.request.Request(url,headers=head)
    response = urllib.request.urlopen(request)
    html = response.read().decode("utf-8") #字符串形式
    text = eval('(' + html + ')') #转json形式
    #print(text) #测试    

    if text['code'] != "0000":
        print(text['message']) 
        return ""
    provinceId = allprovinceId[provinceName]
    scoreLine = text['data']['pro_type_min'][str(provinceId)]
    science = [] #理科
    arts = [] #文科
    synthesize = [] #综合类
    for i in range(len(scoreLine)):
        if '1' in scoreLine[i]['type']:
            temp = {'year': scoreLine[i]['year']}
            temp['score'] = float(scoreLine[i]['type']['1'])
            science.append(temp)
        if '2' in scoreLine[i]['type']:
            temp = {'year': scoreLine[i]['year']}
            temp['score'] = float(scoreLine[i]['type']['2'])
            arts.append(temp)
        if '3' in scoreLine[i]['type']:
            temp = {'year': scoreLine[i]['year']}
            temp['score'] = float(scoreLine[i]['type']['3'])
            synthesize.append(temp)

    if examType == '理科':
        #print(science) #测试
        return science
    elif examType == '文科':
        print(arts) #测试
        return arts
    elif examType == '综合':
        return synthesize 
 
'''本科一批省控线折线图'''
def drawProvinceScoreLineA(ProvinceScoreLine):
    stage1 = ProvinceScoreLine[0:4]  #本科一批
    year = []
    provinceLine = []
    for item in stage1: #每一个item都是一个字典
        year.append(item['year'])
        provinceLine.append(item['score'])
    
    plt.plot(year, provinceLine, linewidth = 3)
    
    plt.title("province score line A", fontsize = 24) #frontsize指定图表中文字的大小
    plt.xlabel("Year", fontsize = 14) #为x轴设置标题
    plt.ylabel("ProvinceScoreLine", fontsize = 14)
    
    plt.xticks(year)
    plt.tick_params(axis = 'both', labelsize = 14) #设置刻度的样式，其中指定的的实参为both表示两条都？lablesize是刻度标记的字号

    #自动保存图表
    plt.savefig('ProvinceScoreLine_A.png', bbox_inches = 'tight') 
    
    #展示图像
    #plt.show()
    
'''本科二批省控线折线图'''
def drawProvinceScoreLineB(ProvinceScoreLine):
    stage2 = ProvinceScoreLine[4:-1] #本科二批
    year = []
    provinceLine = []
    for item in stage2: #每一个item都是一个字典
        year.append(item['year'])
        provinceLine.append(item['score'])
  
    plt.plot(year, provinceLine, linewidth = 3)
    
    plt.title("province score line B", fontsize = 24) #frontsize指定图表中文字的大小
    plt.xlabel("Year", fontsize = 14) #为x轴设置标题
    plt.ylabel("ProvinceScoreLine", fontsize = 14)
    
    plt.xticks(year)
    plt.tick_params(axis = 'both', labelsize = 14) #设置刻度的样式，其中指定的的实参为both表示两条都？lablesize是刻度标记的字号

    #自动保存图表
    plt.savefig('ProvinceScoreLine_B.png', bbox_inches = 'tight') 
    
    #展示图像
    #plt.show()
    
'''学校录取分数线折线图'''
def drawSchoolScoreLine(SchoolLine):
    #直接从爬取的数据中得到年份及其分数的值，防止某些数据没有，造成画图时x和y轴数据个数不一致，无法画图
    year = []
    SchoolScoreLine = []
    for item in SchoolLine: #每一个item都是一个字典:{'year': xxxx, 'score': xxx}
        year.append(item['year'])   
        SchoolScoreLine.append(item['score']) #得到单独的只有分数值的列表
    #本来学校分数线是从2020往前的，为了方便画图，需翻转
    #SchoolScoreLine.reverse()  #这种翻转方式不行？ 
   
    plt.plot(year, SchoolScoreLine[::-1], linewidth = 3)
    
    plt.title("school score line", fontsize = 24) #frontsize指定图表中文字的大小
    plt.xlabel("Year", fontsize = 14) #为x轴设置标题
    plt.ylabel("SchoolScoreLine", fontsize = 14)
    
    plt.xticks(year)
    plt.tick_params(axis = 'both', labelsize = 14) #设置刻度的样式，其中指定的的实参为both表示两条都？lablesize是刻度标记的字号

    #自动保存图表
    plt.savefig('SchoolScoreLine.png', bbox_inches = 'tight') 
    
    #展示图像
    #plt.show()

def main():
    
    '''
    #范例
    provinceName = '湖南'
    schoolName = '中南大学'
    typeName = '理科'
    schoolId = getSchoolId(schoolName)
    '''
    
    #让用户输入高考所在省份名称、报考类型、需要查询的学校名称
    schoolName = str(input("请输入需要查询的学校全称（如：北京大学）："))
    provinceName = str(input("请输入您所在的省份（如：北京）："))
    typeName = str(input("请输入您的报考类型（如：理科）："))

    print("")
    print("稍等片刻噢~")
    
    schoolRanking = getSchoolRanking()
    
    #检查学校名、省份名、报考类型输入是否有误
    school = []
    for i in range(820):
        school.append(schoolRanking[i][1]) #得到学校的列表
        if schoolRanking[i][1] == schoolName:
            ranking = i #得到排名
    if schoolName not in school:
        print("好像没有查询到这个学校的信息~请检查输入的学校是否有误")
    if provinceName not in allprovinceId.keys():
        print("好像没有查询到这个省份的信息~请检查输入的省份是否有误")
    if typeName not in allexamType:
        print("好像没有查询到这个报考类型的信息~请检查输入的报考类型是否有误")
        
    schoolId = getSchoolId(schoolName)      
        
    ProvinceScoreLine = getProvinceScoreLine(provinceName, typeName)
    SchoolLine = getSchoolLine(schoolId, schoolName, provinceName, typeName)
    
    print("")
    print("查询结果如下：")
    print("1." + provinceName + "省控线：")
    print("  (1)" + typeName + "本科一批：", (str(ProvinceScoreLine[0:4]).lstrip('[')).rstrip(']')) #去掉前后的方括号
    print("  (2)" + typeName + "本科二批：", (str(ProvinceScoreLine[4:-1]).lstrip('[')).rstrip(']'))  
    print("2." + schoolName + "排名：", ranking) 
    print("3." + schoolName + "在" + provinceName + "的录取线：", ((str(SchoolLine[::-1])).lstrip('[')).rstrip(']')) #学校录取线是从2020往前输出的，故先翻转 
    
    print("")
    print("您想得到哪个数据的变化图？请选择数字：")
    index = input("---1:该学校录取分数线---2:该省份本科一批分数线---3:该省份本科二批分数线---")
    if index == '1':
        drawSchoolScoreLine(SchoolLine)
    elif index == '2':
        drawProvinceScoreLineA(ProvinceScoreLine)
    elif index == '3':
        drawProvinceScoreLineB(ProvinceScoreLine)

if __name__ == "__main__":          #当程序执行时
#调用函数
    main()