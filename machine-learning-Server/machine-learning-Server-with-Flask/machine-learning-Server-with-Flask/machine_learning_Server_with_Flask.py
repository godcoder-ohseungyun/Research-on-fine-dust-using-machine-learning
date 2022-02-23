from flask import Flask 


# 사용자 정의 모듈: 모듈로 부터 클래스 가져옴: 임포트 방식 알아둘것
from UrlBuilder import UrlBuilder

#
from DFBuilder import DFBuilder


from Item import Item
import json

app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'this is machine learning server'


# 분석 결과 
@app.route('/api/result')
def getAnalysis():

    finalDataFrame = getOpenApi()

    LogisticModel = doLogisticRegression(finalDataFrame)

    #RegionalRepresentativeDataFrame =  DFBuilder().csvToDataFrame(csv)

    resultList = fianlResult(LogisticModel,RegionalRepresentativeDataFrame)
    
    #TODO: object list -> JSON 변환작업
    jsonResult = json.dumps([Item.__dict__ for Item in resultList],ensure_ascii=False)

    return jsonResult
    



def getOpenApi():
    
    url1,url2 = UrlBuilder().buildRequsetUrls()

    finalDataFrame  = DFBuilder().buildDataFrame(url1,url2)

    return  finalDataFrame



def doLogisticRegression(finalDataFrame):
    
    #TODO: 로지스틱 회귀분석 do

    return '학습완료된 모델 자체'



def fianlResult(LogisticModel,RegionalRepresentativeDataFrame):

    #TODO: 구현해야함 지금은 테스트코드임
    testList = list()
    testList.append(Item("서울","송파",28,10))
    testList.append(Item("서울","동작",70,6))

    return testList





# 실행 ctrl+f5
if __name__ == '__main__':
    app.run()
    
