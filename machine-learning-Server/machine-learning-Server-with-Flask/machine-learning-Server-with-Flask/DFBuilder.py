# pandas import
from asyncio.windows_events import NULL
from numpy import False_
import pandas as pd
from pandas import json_normalize

# rest api 요청 lib
import requests
import pprint
import json


# url lib: url 빌더
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus


# 기간생성기
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
    # kosis api default server default
    kosisUrl = 'https://kosis.kr/openapi/statisticsData.do?method=getList'

    # 인증키: 추후 갱신 필요
    kosisService_key = 'ZDYyOTEwNjM2OTJmMGM2MDk3ODlkODE1ZmFkMmI5Yjk='

    # 주제 리스트: 수집할 모든 데이터 주제를 유지합니다. (약자사용: 약자문서 확인)
    topics = ['SOF', 'GA', 'GR', 'PR', 'AS', 'CM', 'SM',
              'RR', 'FP', 'TLF', 'PTR', 'CO2', 'COW', 'WW', 'F']

    # 시훈 추가 : 2012 ~ 2021
    yearmade = ['2012', '2013', '2014', '2015',
                '2016', '2017', '2018', '2019', '2020', '2021']
    # 시훈 추가 : WW를 위하여
    wwcity = ['서울특별시', '서울특별시', '부산광역시', '부산광역시', '대구광역시', '대구광역시', '인천광역시', '인천광역시', '광주광역시', '광주광역시', '대전광역시', '대전광역시', '울산광역시', '울산광역시', '세종특별자치시', '세종특별자치시',
              '경기도', '경기도', '강원도', '강원도', '충청북도', '충청북도', '충청남도', '충청남도', '전라북도', '전라북도', '전라남도', '전라남도', '경상북도', '경상북도', '경상남도', '경상남도', '제주특별자치도', '제주특별자치도']

    # 시훈 추가 : 시도를 남기기 위하여
    cities = ['전국', '요소', '서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시', '세종특별자치시',
              '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도']

    # 주제별: 수집기간,고정URL: 주제별로 수집할 기간, 고정url부분을 유지합니다. (자세한사항 문서확인)
    cm = CycleMaker()

    SOF = [cm.getCycle(
        "semi_annual"), '&format=json&jsonVD=Y&userStatsId=vt0602/399/TX_399020016/2/1/20220318151356&prdSe=H']
    GA = [cm.getCycle(
        "annual"), '&format=json&jsonVD=Y&userStatsId=vt0602/460/TX_315_2009_H1037/2/1/20220318151611&prdSe=Y']
    GR = [cm.getCycle(
        "annual"), '&format=json&jsonVD=Y&userStatsId=vt0602/101/DT_1YL202105E/2/1/20220318152644&prdSe=Y']
    PR = [cm.getCycle(
        "annual"), '&format=json&jsonVD=Y&userStatsId=vt0602/460/TX_315_2009_H1001/2/1/20220318152808&prdSe=Y']
    AS = [cm.getCycle(
        "annual"), '&format=json&jsonVD=Y&userStatsId=vt0602/460/TX_315_2009_H1002/2/1/20220318152935&prdSe=Y']
    CM = [cm.getCycle(
        "annual"), '&format=json&jsonVD=Y&userStatsId=vt0602/426/DT_426001_N004/2/1/20220318153302&prdSe=Y']
    SM = [cm.getCycle(
        "annual"), '&format=json&jsonVD=Y&userStatsId=vt0602/117/DT_H_SM/2/1/20220318153811&prdSe=Y']
    RR = [cm.getCycle(
        "annual"), '&format=json&jsonVD=Y&userStatsId=vt0602/101/DT_1YL9901/2/1/20220318154444&prdSe=Y']
    FP = [cm.getCycle(
        "annual"), '&format=json&jsonVD=Y&userStatsId=vt0602/101/DT_1B26001_A01/2/1/20220318154916&prdSe=Y']
    TLF = [cm.getCycle(
        "annual"), '&format=json&jsonVD=Y&userStatsId=vt0602/106/DT_106N_99_3300027/2/1/20220318155252&prdSe=Y']
    PTR = [cm.getCycle(
        "annual"), '&format=json&jsonVD=Y&userStatsId=vt0602/106/DT_106T_009432/2/1/20220318155650&prdSe=Y']
    CO2 = [cm.getCycle(
        "monthly"), '&format=json&jsonVD=Y&userStatsId=vt0602/106/DT_106N_03_0200044/2/1/20220318160001&prdSe=M']
    COW = [cm.getCycle(
        "quarterly"), '&format=json&jsonVD=Y&userStatsId=vt0602/101/DT_1EO200/2/1/20220318160410&prdSe=Q']
    WW = [cm.getCycle(
        "annual"), '&format=json&jsonVD=Y&userStatsId=vt0602/106/DT_106N_01_0100069/2/1/20220318160929&prdSe=Y']
    F = [cm.getCycle(
        "annual"), '&format=json&jsonVD=Y&userStatsId=vt0602/101/DT_1EB002/2/1/20220318161216&prdSe=Y']

    '''
        -api 자동 요청 모듈- (동적코드 사용)
        주어진 주제와 수집기간으로 api server로 자동 요청을 보내 받은 json response를 dataFrame으로 converting 이후 global 변수로 선언합니다.
        '''

    def makeResponseToDF(self, topic, yearList, staicPram):

        for year in yearList:
            kosisDataQueryParams = '&' + urlencode({quote_plus('apiKey'): DFBuilder.kosisService_key,
                                                    quote_plus('startPrdDe'): year,
                                                    quote_plus('endPrdDe'): year,
                                                    }) + staicPram

            url = DFBuilder.kosisUrl+kosisDataQueryParams

            response = requests.get(url)

            # 데이터 값 to String
            contents = response.text

            # json으로 변경
            json_ob = json.loads(contents)

            # Convert json to dataframe
            # 공공 포털은 ITEMS를 꺼내야하는데 이건 이미 객체 리스트만 넘어옴
            dataframe = json_normalize(json_ob)

            # globals()['{}_DF_{}'.format(topic,year)] = dataframe #동적코드1

            dataframe.to_csv("{}{}/{}_DF_{}.csv".format(FileMaker.root,
                             topic, topic, year), index=False, encoding="utf-8-sig")

    '''
        -makeDF 실행 모듈-
        모든 주제에 대하여 makeDF를 수행해서 데이터 프레임들을 전역으로 생성합니다.
        '''

    def requestAPI(self):

        fm = FileMaker()

        for topic in DFBuilder.topics:

            fm.createDirectory(topic)

            self.makeResponseToDF(topic, eval(f"DFBuilder.{topic}[0]"), eval(
                f"DFBuilder.{topic}[1]"))  # 동적코드2
            time.sleep(1)

    def readCacheStorage(self):
        for topic in DFBuilder.topics:
            years = eval(f"DFBuilder.{topic}[0]")
            for year in years:
                globals()['{}_DF_{}'.format(topic, year)] = pd.read_csv(
                    "{}{}/{}_DF_{}.csv".format(FileMaker.root, topic, topic, year))

        print("모든 DataFrame 불러오기 완료")

    '''
        -최종데이터프레임 생성 모듈-
        전역으로 선언되어있는 데이터프레임들을 활용해 최종 데이터 프레임을 반환합니다.
        이 최종 데이터 프레임은 회귀분석에 사용됩니다.
        '''

    def readDataFrames(self, renew):

        # 데이터프레임 자동 생성기 호출
        if(renew == True):
            print("api 서버로부터 갱신 데이터 호출중(시간이 걸릴수있습니다. 2분)")
            self.requestAPI()
            self.readCacheStorage()

        else:
            self.readCacheStorage()

    def makeFinalDataFrame(self):

        # dataFrames 전역생성
        self.readDataFrames(False)  # True로 바꾸면 api로부터 데이터 호출후 전역생성
        # for key, value in globals().items():
        #     print(key, value)
        '''
            정제작업
            '''
        for topic in DFBuilder.topics:
            df1 = pd.DataFrame()
            years = eval(f"DFBuilder.{topic}[0]")
            # print(topic)
            for year in years:
                # print(year)
                dftemp = globals()['{}_DF_{}'.format(topic, year)]
                if len(dftemp) > 4:
                    dftemp = dftemp[['C1_NM', 'DT']]
                    dftemp = dftemp.rename(columns={'C1_NM': '지역', 'DT': year})
                    # print(dftemp)
                    if df1.empty:
                        if topic == 'WW':
                            tempnum = 0
                            for i in range(0, len(dftemp)):
                                if dftemp.loc[i, '지역'] == '계':
                                    dftemp.loc[i,
                                               '지역'] = DFBuilder.wwcity[tempnum]
                                    tempnum += 1
                        df1 = pd.concat([df1, dftemp])
                        df1 = df1.drop_duplicates('지역', keep='first')
                        # print(df1)
                    else:
                        if topic == 'WW':
                            tempnum = 0
                            for i in range(0, len(dftemp)):
                                if dftemp.loc[i, '지역'] == '계':
                                    dftemp.loc[i,
                                               '지역'] = DFBuilder.wwcity[tempnum]
                                    tempnum += 1
                        dftemp = dftemp.drop_duplicates('지역', keep='first')
                        df1 = df1.drop_duplicates('지역', keep='first')
                        df1 = pd.merge(left=df1, right=dftemp,
                                       how="left", on="지역", sort=False)
                        # print(df1)
                else:
                    pass
                    # print("!!!!!")

            if topic == 'CO2' or topic == 'PTR' or topic == 'RR' or topic == 'SOF' or topic == 'TLF':
                df1.loc[0, '지역'] = '전국'

            if topic == 'CO2' or topic == 'F' or topic == 'PTR' or topic == 'TLF':
                # Why won't the code under work?????            -------------------------
                # df1.loc['서울', '지역'] = '서울특별시'
                for i in range(0, len(df1)):
                    if df1.loc[i, '지역'] == '서울' or df1.loc[i, '지역'] == '세종':
                        df1.loc[i, '지역'] = '서울특별시'
                    elif df1.loc[i, '지역'] == '부산' or df1.loc[i, '지역'] == '대구' or df1.loc[i, '지역'] == '인천' or df1.loc[i, '지역'] == '광주' or df1.loc[i, '지역'] == '대전' or df1.loc[i, '지역'] == '울산':
                        df1.loc[i, '지역'] = df1.loc[i, '지역']+'광역시'
                    elif df1.loc[i, '지역'] == '경기' or df1.loc[i, '지역'] == '강원':
                        df1.loc[i, '지역'] = df1.loc[i, '지역']+'도'
                    elif df1.loc[i, '지역'] == '충북':
                        df1.loc[i, '지역'] = '충청북도'
                    elif df1.loc[i, '지역'] == '충남':
                        df1.loc[i, '지역'] = '충청남도'
                    elif df1.loc[i, '지역'] == '전북':
                        df1.loc[i, '지역'] = '전라북도'
                    elif df1.loc[i, '지역'] == '전남':
                        df1.loc[i, '지역'] = '전라남도'
                    elif df1.loc[i, '지역'] == '경북':
                        df1.loc[i, '지역'] = '경상북도'
                    elif df1.loc[i, '지역'] == '경남':
                        df1.loc[i, '지역'] = '경상남도'
                    elif df1.loc[i, '지역'] == '제주':
                        df1.loc[i, '지역'] = '제주특별자치도'

            if topic == 'F':
                df1 = df1.drop([4, 7, 10, 13, 17])

            # temporary until I find a way to make an average of these data
            elif topic == 'CO2' or topic == 'COW' or topic == 'SOF':
                for year in years:
                    if year in df1:
                        if (year % 20) != 1:
                            df1 = df1.drop(columns=[year])
                for col in df1.columns:
                    if str(type(col)) == "<class 'int'>":
                        df1 = df1.rename(columns={col: int(col/100)})

            else:
                pass
                # Make a File using the code beneath

            df1.to_csv("{}{}/{}_DF_all.csv".format(FileMaker.root,
                                                   topic, topic), index=False, encoding="utf-8-sig")

        # Adding all Data into One DataFile
        df1 = pd.DataFrame()
        for topic in DFBuilder.topics:

            # dftemp = globals()['{}_DF_{}'.format(topic, 'all')]
            dftemp = pd.read_csv(
                "{}{}/{}_DF_{}.csv".format(FileMaker.root, topic, topic, 'all'))
            # print(dftemp)
            # print(type(topic))
            # print(len(dftemp.columns))

            dfempty = pd.DataFrame(index=range(
                0, 1), columns=dftemp.columns, data=topic)
            dfempty.loc[0, '지역'] = '요소'
            # print('\n\n\n')
            dftemp = pd.concat([dfempty, dftemp])
            # print(dftemp)
            if df1.empty:

                df1 = pd.concat([df1, dftemp])
                df1 = df1.drop_duplicates('지역', keep='first')
                # print(df1)
            else:
                dftemp = dftemp.drop_duplicates('지역', keep='first')
                df1 = df1.drop_duplicates('지역', keep='first')
                df1 = pd.merge(left=df1, right=dftemp,
                               how="left", on="지역", sort=False)
                # print(df1)

        for col in df1.columns:
            if len(col) > 5:
                df1 = df1.rename(columns={col: col[0:4]})
            # print(type(col))
            # print(col)
        # print("\n\n\n\n\n\n")
        # print(df1.values)
        dropnum = 0
        for val in df1.values:
            if val[0] not in DFBuilder.cities:
                print(val[0], '\n')
                df1 = df1.drop([dropnum])
                # dropnum -= 1
            dropnum += 1
        # print("\n\n\n\n\n\n")

        df1.to_csv("{}/DF_all.csv".format(FileMaker.root),
                   index=False, encoding="utf-8-sig")
        print("All Finisihed")

        '''정제작업'''

        return 'FinaldataFrame'


# testCode

t = DFBuilder()

t.makeFinalDataFrame()
