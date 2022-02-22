from flask import Flask 

#url lib: url 빌더
from urllib.request import Request, urlopen 
from urllib.parse import urlencode, quote_plus

#rest api 요청 lib
import requests
import pprint
import json

# pandas import
import pandas as pd
from pandas.io.json import json_normalize

app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'this is machine learning server'


# 분석 결과 
@app.route('/api/result')
def getAnalysis():

    dataFrame = getOpenApi()

    finalDataFrame = processingDataFrame(dataFrame)

    LogisticModel = doLogisticRegression(finalDataFrame)

    RegionalRepresentativeDataFrame = makeRegionalRepresentativeDataFrame()

    list = checkResult(LogisticModel,RegionalRepresentativeDataFrame)

    #TODO: checkResult에서 결과 객체 리스트로 만들것임, 이것에 쓰일 객체 만들기

    return "list to json"
    


'''
reference: https://yobbicorgi.tistory.com/32 , https://wonhwa.tistory.com/9   

info: 공공 데이터 포털에 request하여 받아온 json response를 pandas를 이용해 dataframes으로 변환합니다.
      필요한 여러개의 데이터를 받아 옵니다.

return: dataframes  ex) df1 , df2 , df3 ... dfn
'''
def getOpenApi():
    
    url = 'http://apis.data.go.kr/B552584/UlfptcaAlarmInqireSvc/getUlfptcaAlarmInfo'

    service_key = 'bAb8EJ7wcYTeQbTEM4KZ7ElEwLjrj+T1+X10tEStISwzs+/qNO+Vy/p3iTV/FIfbpWhBQJLm1eHbmQzW+40Osw=='

    queryParams = '?' + urlencode({quote_plus('ServiceKey') : service_key, 
                                   quote_plus('returnType') : 'json', 
                                   quote_plus('numOfRows') : '100', 
                                   quote_plus('pageNo') : '1', 
                                   quote_plus('year') : '2020', 
                                   })

 
    # url 불러오기
    response = requests.get(url + queryParams)

    #데이터 값 출력해보기 to String
    contents = response.text

    #json으로 변경
    json_ob = json.loads(contents)

    # response -> body -> items : 바디안에 items 리스트 추출
    body = json_ob['response']['body']['items']

    #Convert json to dataframe 
    dataframe = json_normalize(body)

    #TODO: 여러개의 데이터 프래임들을 리턴하도록 만들 예정
    return dataframe



'''
받아온 데이터 프레임들을 가공해 사용할 최종 데이터 프레임을 만듭니다.

param: dataframes
return: finalDataFrame
'''
def  processingDataFrame(dataframe):
    
    #TODO: 여러개의 데이터 프래임들을 파라미터로 받도록 만들예정
    #      그리고 이 데이터 프레임들을 요구사항에 맞게 정제할 예정
    
    #테스트 코드 : 삭제 요망
    print(dataframe)
    finalDataFrame = dataframe

    return finalDataFrame
  

'''
info: 회귀 분석 이후 해당 로지스틱 모델을 return합니다.

param: finalDataFrame

return: LogisticModel
'''
def doLogisticRegression(finalDataFrame):
    
    #TODO: 로지스틱 회귀분석 do
       

    return LogisticModel


'''
info: csv로 직접 만든 데이터를 데이터 프레임으로 가공합니다
      이 데이터는 지역별 대표 데이터 입니다.
      학습된 회귀 모델에 쓰입니다.
'''
def makeRegionalRepresentativeDataFrame():
    
    #TODO: csv -> dataframe

    return RegionalRepresentativeDataFrame


'''
info: 학습된 회귀 모델과 선별한 지역 대표 데이터를 가지고 분석한 결과를 return합니다.
      결과는 각 지역별 점수 및 확률 데이터 리스트 입니다.

param: LogisticModel,RegionalRepresentativeDataFrame
return:  지역별 점수 및 확률 데이터 리스트
'''
def fianlResult(LogisticModel,RegionalRepresentativeDataFrame):

    #TODO

    return "지역별 점수 및 확률 데이터 리스트"





# 실행 ctrl+f5
if __name__ == '__main__':
    app.run()
