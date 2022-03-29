# pandas import
import pandas as pd
from pandas import json_normalize

#rest api 요청 lib
import requests
import pprint
import json


#url lib: url 빌더
from urllib.request import Request, urlopen 
from urllib.parse import urlencode, quote_plus



#기간생성기
from cycleMaker import CycleMaker
from fileMaker import FileMaker


import time

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
        topics = ['SOF','GA','GR','PR','AS','CM','SM','RR','FP','TLF','PTR','CO2','COW','WW','F']

        #주제별: 수집기간,고정URL: 주제별로 수집할 기간, 고정url부분을 유지합니다. (자세한사항 문서확인)
        cm = CycleMaker()
        
        SOF = [cm.getCycle("semi_annual"),'&format=json&jsonVD=Y&userStatsId=vt0602/399/TX_399020016/2/1/20220318151356&prdSe=H'] 
        GA = [cm.getCycle("annual"),'&format=json&jsonVD=Y&userStatsId=vt0602/460/TX_315_2009_H1037/2/1/20220318151611&prdSe=Y']
        GR = [cm.getCycle("annual"),'&format=json&jsonVD=Y&userStatsId=vt0602/101/DT_1YL202105E/2/1/20220318152644&prdSe=Y']
        PR = [cm.getCycle("annual"),'&format=json&jsonVD=Y&userStatsId=vt0602/460/TX_315_2009_H1001/2/1/20220318152808&prdSe=Y']
        AS = [cm.getCycle("annual"),'&format=json&jsonVD=Y&userStatsId=vt0602/460/TX_315_2009_H1002/2/1/20220318152935&prdSe=Y']
        CM = [cm.getCycle("annual"),'&format=json&jsonVD=Y&userStatsId=vt0602/426/DT_426001_N004/2/1/20220318153302&prdSe=Y']
        SM = [cm.getCycle("annual"),'&format=json&jsonVD=Y&userStatsId=vt0602/117/DT_H_SM/2/1/20220318153811&prdSe=Y']
        RR = [cm.getCycle("annual"),'&format=json&jsonVD=Y&userStatsId=vt0602/101/DT_1YL9901/2/1/20220318154444&prdSe=Y']
        FP = [cm.getCycle("annual"),'&format=json&jsonVD=Y&userStatsId=vt0602/101/DT_1B26001_A01/2/1/20220318154916&prdSe=Y']
        TLF = [cm.getCycle("annual"),'&format=json&jsonVD=Y&userStatsId=vt0602/106/DT_106N_99_3300027/2/1/20220318155252&prdSe=Y']
        PTR = [cm.getCycle("annual"),'&format=json&jsonVD=Y&userStatsId=vt0602/106/DT_106T_009432/2/1/20220318155650&prdSe=Y']
        CO2 = [cm.getCycle("monthly"),'&format=json&jsonVD=Y&userStatsId=vt0602/106/DT_106N_03_0200044/2/1/20220318160001&prdSe=M']
        COW = [cm.getCycle("quarterly"),'&format=json&jsonVD=Y&userStatsId=vt0602/101/DT_1EO200/2/1/20220318160410&prdSe=Q']
        WW = [cm.getCycle("annual"),'&format=json&jsonVD=Y&userStatsId=vt0602/106/DT_106N_01_0100069/2/1/20220318160929&prdSe=Y']
        F=[cm.getCycle("annual"),'&format=json&jsonVD=Y&userStatsId=vt0602/101/DT_1EB002/2/1/20220318161216&prdSe=Y']
        

        

        
        '''
        -api 자동 요청 모듈- (동적코드 사용)
        주어진 주제와 수집기간으로 api server로 자동 요청을 보내 받은 json response를 dataFrame으로 converting 이후 global 변수로 선언합니다.
        '''
        def makeResponseToDF(self,topic,yearList,staicPram):

    

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


                #Convert json to dataframe 
                dataframe = json_normalize(json_ob) #공공 포털은 ITEMS를 꺼내야하는데 이건 이미 객체 리스트만 넘어옴

                
                #globals()['{}_DF_{}'.format(topic,year)] = dataframe #동적코드1

                dataframe.to_csv("{}{}/{}_DF_{}.csv".format(FileMaker.root,topic,topic,year),index=False, encoding="utf-8-sig")


      
        def requestAPI(self):
            
            fm = FileMaker()

            for topic in DFBuilder.topics:

                fm.createDirectory(topic)

                self.makeResponseToDF(topic,eval(f"DFBuilder.{topic}[0]"),eval(f"DFBuilder.{topic}[1]"))  #동적코드2
                time.sleep(1)

            

        def readCacheStorage(self):
            for topic in DFBuilder.topics:
                years =  eval(f"DFBuilder.{topic}[0]")
                for year in years:
                    globals()['{}_DF_{}'.format(topic,year)] =  pd.read_csv("{}{}/{}_DF_{}.csv".format(FileMaker.root,topic,topic,year))
           
            print("모든 DataFrame 불러오기 완료")
                                                                           

      
        def readDataFrames(self,renew):

            
            #데이터프레임 자동 생성기 호출            
            if(renew == True):
                print("api 서버로부터 갱신 데이터 호출중(시간이 걸릴수있습니다. 2분)")
                self.requestAPI()
                self.readCacheStorage()

            else:
                self.readCacheStorage()

           
   


        def makeFinalDataFrame(self):

            #dataFrames 전역생성
            self.readDataFrames(False)  #True로 바꾸면 api로부터 데이터 호출후 전역생성

            print(globals())

            '''
            정제작업
            '''


            return 'FinaldataFrame'



#testCode


t = DFBuilder()

t.makeFinalDataFrame()


        

       