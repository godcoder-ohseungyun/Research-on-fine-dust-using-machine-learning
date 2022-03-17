
# pandas import
import pandas as pd
from pandas.io.json import json_normalize

#rest api 요청 lib
import requests
import pprint
import json

url = 'https://kosis.kr/openapi/statisticsData.do?method=getList&apiKey=ZDYyOTEwNjM2OTJmMGM2MDk3ODlkODE1ZmFkMmI5Yjk=&format=json&jsonVD=Y&userStatsId=vt0602/117/DT_H_SM/2/1/20220314130922&prdSe=Y&startPrdDe=2015&endPrdDe=2017'

response = requests.get(url)

#데이터 값 to String
contents = response.text

#json으로 변경
json_ob = json.loads(contents)



#print(json_ob)

#Convert json to dataframe 
dataframe = json_normalize(json_ob) #공공 포털은 ITEMS를 꺼내야하는데 이건 이미 객체 리스트만 넘어옴

print(dataframe)




#자동 변수 생성기
'''
이부분은 조금 힘들것같다. global()[] 모듈을 이용하면 반복문을 통해 만들수있지만,
우리 데이터는 10~22까지 균일하게 있는게 아니라 누락되는 부분도 존재하기 때문에
주제별로 리스트를 만들어서 뒤에 넘버를 돌려야할것같다

-데이터 프래임 변수이름도 마찮가지...


아니면 별도로 요청주제 별로 리스트 만들어서 해당 부분으로 숫자 넣기
ex) 19 20 21만 있다면
list = 19 20 21

for(int i : list){
    local()[smt_{}, i]
}


smt_19     20   21 생성될꺼임

https://velog.io/@paori/python-%EB%8F%99%EC%A0%81-%EB%B3%80%EC%88%98-%EC%9E%90%EB%8F%99-%EB%B3%80%EC%88%98-%EC%83%9D%EC%84%B1
'''



#요청 url규칙
'''
말단 파라미터 &startPrdDe=2019&endPrdDe=2019 로 몇년도인지 결정됨
https://kosis.kr/openapi/devGuide/devGuide_0201List.jsp

- end와 start 시점은 동일함.
다르게 해도 시작시점에서 종료됨  설계자체가 그렇게 되어있는듯함

'''
