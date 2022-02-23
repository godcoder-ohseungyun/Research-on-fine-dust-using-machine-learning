from flask import Flask 


# 사용자 정의 모듈: 모듈로 부터 클래스 가져옴: 임포트 방식 알아둘것
from UrlBuilder import UrlBuilder

#
from DFBuilder import DFBuilder

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

    result = fianlResult(LogisticModel,RegionalRepresentativeDataFrame)


    #TODO: result -> JSON 변환작업

    return "list to json"
    



def getOpenApi():
    
    url1,url2 = UrlBuilder().buildRequsetUrls()

    finalDataFrame  = DFBuilder().buildDataFrame(url1,url2)

    return  finalDataFrame



def doLogisticRegression(finalDataFrame):
    
    #TODO: 로지스틱 회귀분석 do

    return '학습완료된 모델 자체'



def fianlResult(LogisticModel,RegionalRepresentativeDataFrame):

    #TODO

    return "최종 결과"





# 실행 ctrl+f5
if __name__ == '__main__':
    app.run()
    
