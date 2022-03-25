from flask import Flask 
from flask import Response


from DFBuilder import DFBuilder

from Item import Item
import json

app = Flask(__name__)

#테스트 용 컨트롤러임-------------------------------------------------------
@app.route('/test')
def test():

    testList = list()
    testList.append(Item("서울","송파",28,10))
    testList.append(Item("서울","동작",70,6))
    
    #TODO: object list -> JSON 변환작업
    jsonResult = json.dumps([Item.__dict__ for Item in testList],ensure_ascii=False) #testList -> resultList

    response = Response(response=jsonResult, status=200, mimetype="application/json; charset=utf-8")

    return response
#---------------------------------------------------------------------------





@app.route('/')
def hello_world():
    return 'this is machine learning server'


# 분석 결과 
@app.route('/api/result')
def getAnalysis():

    finalDataFrame = getFinalDataFrame()

    LogisticModel = doLogisticRegression(finalDataFrame)

    RegionalRepresentativeDataFrame =  DFBuilder().csvToDataFrame(csv)

    resultList = fianlResult(LogisticModel,RegionalRepresentativeDataFrame)
    
    #TODO: object list -> JSON 변환작업
    jsonResult = json.dumps([Item.__dict__ for Item in resultList],ensure_ascii=False) 
    
    response = Response(response=jsonResult, status=200, mimetype="application/json; charset=utf-8")

    return response
    

'''
url + df builder 합칠꺼임 이구간 변화할 예정
'''
def getFinalDataFrame():
    
    df = DFBuilder()
    
    return  df.makeFinalDataFrame()



def doLogisticRegression(finalDataFrame):
    
    #TODO: 로지스틱 회귀분석 do

    return '학습완료된 모델 자체'



def finalResult(LogisticModel,RegionalRepresentativeDataFrame):

    #TODO: 구현해야함 지금은 테스트코드임
    testList = list()
    testList.append(Item("서울","송파",28,10))
    testList.append(Item("서울","동작",70,6))

    return testList





# 실행 ctrl+f5
if __name__ == '__main__':
    app.run()
    
