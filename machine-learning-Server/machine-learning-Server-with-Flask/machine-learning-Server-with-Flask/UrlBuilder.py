#url lib: url 빌더
from urllib.request import Request, urlopen 
from urllib.parse import urlencode, quote_plus


class UrlBuilder:

    def buildRequsetUrls(self):

        #공공데이터 포털 API
        dataUrl = 'http://apis.data.go.kr/B552584/UlfptcaAlarmInqireSvc/getUlfptcaAlarmInfo'

        dataService_key = 'bAb8EJ7wcYTeQbTEM4KZ7ElEwLjrj+T1+X10tEStISwzs+/qNO+Vy/p3iTV/FIfbpWhBQJLm1eHbmQzW+40Osw=='

        dataQueryParams = '?' + urlencode({quote_plus('dataService_key') : service_key, 
                                       quote_plus('returnType') : 'json', 
                                       quote_plus('numOfRows') : '100', 
                                       quote_plus('pageNo') : '1', 
                                       quote_plus('year') : '2020', 
                                       })

        '''
        https://www.data.go.kr/data/15073885/openapi.do
        
        미세먼지 경보 현황 조회 api url
        '''
        alertStatusUrl = dataUrl + dataQueryParams




        #KOSIS 포털 API
        kosisUrl = 'https://kosis.kr/openapi/statisticsList.do?method=getList'

        kosisService_key = 'ZDYyOTEwNjM2OTJmMGM2MDk3ODlkODE1ZmFkMmI5Yjk='

        kosisQueryParams = '&' + urlencode({quote_plus('kosisService_key') : service_key, 
                                       quote_plus('format') : 'json', 
                                       quote_plus('numOfRows') : '100', 
                                       quote_plus('pageNo') : '1', 
                                       quote_plus('year') : '2020', 
                                       })

        #추가 예정임, 아래는 테스트 url
        defaultUrl = url

        return defaultUrl, alertStatusUrl