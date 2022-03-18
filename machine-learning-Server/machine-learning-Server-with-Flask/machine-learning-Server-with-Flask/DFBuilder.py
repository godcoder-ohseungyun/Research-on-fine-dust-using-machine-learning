# pandas import
import pandas as pd
from pandas.io.json import json_normalize

#rest api 요청 lib
import requests
import pprint
import json


#url lib: url 빌더
from urllib.request import Request, urlopen 
from urllib.parse import urlencode, quote_plus




'''
이 클래스는 api 자동요청 및 df 자동생성후 정제 과정을 거쳐 최종 데이터 프레임을 출력합니다.
- 자동생성된 데이터프레임들은 전역변수로 관리됩니다.
'''
class DFBuilder:

        
        '''
        -자동화 모듈에 사용될 맴버변수-
        동적코드를 활용해 맴버변수에 따라 생성결과를 제어할수있습니다.
        이 목록을 수정하는것 만으로 자동화 모듈을 제어할수있습니다.
        '''
        #kosis api default server default
        kosisUrl = 'https://kosis.kr/openapi/statisticsData.do?method=getList'

        #인증키: 추후 갱신 필요
        kosisService_key = 'ZDYyOTEwNjM2OTJmMGM2MDk3ODlkODE1ZmFkMmI5Yjk='

        #주제 리스트: 수집할 모든 데이터 주제를 유지합니다. (약자사용: 약자문서 확인)
        topics = ['SOF','GA','CM']

        #주제별: 수집기간,고정URL: 주제별로 수집할 기간, 고정url부분을 유지합니다. (자세한사항 문서확인)
        
        
        SOF = [[202101],'&format=json&jsonVD=Y&userStatsId=vt0602/399/TX_399020016/2/1/20220318151356&prdSe=H'] 
        GA = [[2012,2013,2014,2015],'&format=json&jsonVD=Y&userStatsId=vt0602/460/TX_315_2009_H1037/2/1/20220318151611&prdSe=Y']
        CM = [[2012],'&format=json&jsonVD=Y&userStatsId=vt0602/426/DT_426001_N004/2/1/20220318153302&prdSe=Y']
        
        '''
        -api 자동 요청 모듈- (동적코드 사용)
        주어진 주제와 수집기간으로 api server로 자동 요청을 보내 받은 json response를 dataFrame으로 converting 이후 global 변수로 선언합니다.
        '''
        def makeDF(self,topic,yearList,staicPram):

    

            for year in yearList:
                kosisDataQueryParams = '&' + urlencode({quote_plus('apiKey') : DFBuilder.kosisService_key,                                         
                                            quote_plus('startPrdDe') : year,
                                            quote_plus('endPrdDe') : year,
                                            }) + staicPram
    
                url =  DFBuilder.kosisUrl+kosisDataQueryParams

    
                response = requests.get(url)

                #데이터 값 to String
                contents = response.text

                #json으로 변경
                json_ob = json.loads(contents)



                #print(json_ob)

                #Convert json to dataframe 
                dataframe = json_normalize(json_ob) #공공 포털은 ITEMS를 꺼내야하는데 이건 이미 객체 리스트만 넘어옴

                #print(dataframe)

                globals()['{}_DF_{}'.format(topic,year)] = dataframe #동적코드1


        '''
        -makeDF 실행 모듈-
        모든 주제에 대하여 makeDF를 수행해서 데이터 프레임들을 전역으로 생성합니다.
        '''
        def getDataFrames(self):

            for topic in DFBuilder.topics:
                self.makeDF(topic,eval(f"DFBuilder.{topic}[0]"),eval(f"DFBuilder.{topic}[1]"))  #동적코드2

            
            
        '''
        -최종데이터프레임 생성 모듈-
        전역으로 선언되어있는 데이터프레임들을 활용해 최종 데이터 프레임을 반환합니다.
        이 최종 데이터 프레임은 회귀분석에 사용됩니다.
        '''
        def getFinalDataFrame(self):

            #데이터프레임 자동 생성기 호출
            self.getDataFrames()

            print(SOF_DF_202101,GA_DF_2012,GA_DF_2013,GA_DF_2014,GA_DF_2015,CM_DF_2012)
            #SMT_DF_2017, SMT_DF_2018, SMT_DF_2019 이런식으로 데이터프레임 접근해서 사용하면됨

            return 'finalDataFrame'


dff = DFBuilder()

dff.getFinalDataFrame()


        

       