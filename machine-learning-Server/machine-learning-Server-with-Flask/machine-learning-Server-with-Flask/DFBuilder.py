# pandas import
import pandas as pd
from pandas.io.json import json_normalize

#rest api 요청 lib
import requests
import pprint
import json


class DFBuilder:

        
        def jsonToDataFrame(self, url):    
            # url 불러오기
            response = requests.get(url)

            #데이터 값 to String
            contents = response.text

            #json으로 변경
            json_ob = json.loads(contents)

            # response -> body -> items : 바디안에 items 리스트 추출
            body = json_ob['response']['body']['items']

            #Convert json to dataframe 
            dataframe = json_normalize(body)

            return dataframe


       
        def  getFinalDataFrame(self, dataframe1,dataframe2):
    
            #파이널 데이터 프레임 가공작업

            return 'finalDataFrame'
    
    
        
        def buildDataFrame(self, url1,url2):

            #converting..
            testDF= self.jsonToDataFrame(url2)

            alertStatusDF= self.jsonToDataFrame(url2)
   
            finalDataFrame = self.getFinalDataFrame(testDF,alertStatusDF)
        
            return finalDataFrame



        def csvToDataFrame(csv):

            #read csv and return dataframe

            return 'csv'