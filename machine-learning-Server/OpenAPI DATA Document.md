

### Make finalDataFrame using  OpenAP's json response

----

**데이터 제공포털 open api**를 통해  얻은 json respone 들을 파싱해서 dataFrame들로 변환후 

해당 dataFrame들을 필요에 맞게 병합 및 가공해서 **머신러닝에 활용될 finalDataFrame**으로 만든다.



**[절차]**

+ **http request to api server**
+ **Convert received response to dataframe** (data format is json)
+ **Repeat the above process until enough data frames are gathered.**
+ **Merge and Manufacture clusters of data frames to make a final data frame**



**[데이터 제공 포털]**

+ [KOSIS](https://kosis.kr/openapi/index/index.jsp)
+ [공공데이터포털](https://www.data.go.kr/)







### 받을 데이터의 형태

---

+ 횡단면 자료로 객체 리스트를 받아 dataFrame으로 가공할것이다.

+ 횡단면이기 때문에 시점당 한개의 dataFrame이 만들어진다.

  > **예를들어 2019~2020 시군구별 흡연율 데이터프레임을 만들것이라면 총 2개의 데이터 프레임이 만들어진다.**
  >
  > 
  >
  > 2019년도 데이터프레임
  >
  > |  시군구별  | 조율 (%) | 조율표준오차 (%) | 응답자수 (명) | 표준화율 (%) | 표준화율표준오차 (%) |
  > | :--------: | -------- | ---------------- | ------------- | ------------ | -------------------- |
  > | 서울특별시 | 16.7     | 0.3              | 22928         | 17.8         | 0.3                  |
  > | 부산광역시 | 17.7     | 0.4              | 14510         | 19           | 0.4                  |
  >
  > 2020년도 데이터프레임
  >
  > |  시군구별  | 조율 (%) | 조율표준오차 (%) | 응답자수 (명) | 표준화율 (%) | 표준화율표준오차 (%) |
  > | :--------: | -------- | ---------------- | ------------- | ------------ | -------------------- |
  > | 서울특별시 | 16.7     | 0.3              | 22928         | 17.8         | 0.3                  |
  > | 부산광역시 | 17.7     | 0.4              | 14510         | 19           | 0.4                  |









# 요청 및 변환 자동화 모듈 설계 계획

---

+ **주제당 2012~2022 까지 데이터를 수집할예정이다.**

  > <u>주제당 10개의 url과 dataFrame이 생성된다.</u> (횡단면 자료이기때문에 시점당 한개씩 생성됨)





+ **20개의 주제가 존재함으로 200개의 요청 url과 dataFrame이 생성될것이다.**

+ **<u>중복코드를 최대한 줄이고 추후 관리가 편하도록 설계해야한다.</u>**

  > 인증키 만료
  >
  > 주제변경에 따른 url 재설계
  >
  > 등등 
  >
  > **변동가능성이 높기때문**







**How?**

### <u>동적코딩기술을 이용</u>

자바에서 사용했던 **자바 리플렉션(java Reflection)**처럼 **동적으로** 클래스,변수,메서드 등에 접근해 결과를 만들어내도록 **설계하면** **중복제거**와 **유지 보수** 두 마리 토끼를 모두 잡을수있다.



### <u>요청 url 패턴분석</u>

요청 url들의 패턴을 분석해 **동적인 부분과 정적인 부분을 구분**해 url encoding 시 동적 코딩기술이 적용될 부분을 파악한다.

~~~http
https://kosis.kr/openapi/statisticsData.do?method=getList
&apiKey=ZDYyOTEwNjM2OTJmMGM2MDk3ODlkODE1ZmFkMmI5Yjk=
&format=json 
&jsonVD=Y
&userStatsId=vt0602/117/DT_H_SM/2/1/20220314130922
&prdSe=Y
&startPrdDe=2018&endPrdDe=2018
~~~

> + **apiKey:** 인증키 부분
> + **startPrdDe , endPrdDe:** 조회기간 부분(최대 1년임 ,  2017~2018 불가   2018~2018 가능)
> + **나머지:** 주제별로 가지는 부분(자료 ID,페이지 수 등등)





**apiKey 와 나머지 부분은 정적 queryparam**

+ apiKey는 인증기간 만료때만 갱신해주면됨



**startPrdDe , endPrdDe 은 동적 queryparam**

+ 기간별로 1개씩 데이터프레임을 받을것임으로 이부분만 동적으로 바꿔가면서 요청 보내면 됨



### <u>변수명 규칙 결정</u>

+ 아 멀티쓰래딩 마렵다
+ 가이드 20페이지
+ 소계단위로 받아지도록 해야함 > level별 2로 선택

~~~
[주제]
[필요속성]
[약자코드]
[주기]
[고정코드]
~~~

---

~~~
[공장현황및면적]
[면적]
[SOF]
[201502 ~ 202101] (반기 01 02)
[&format=json&jsonVD=Y&userStatsId=vt0602/399/TX_399020016/2/1/20220318151356&prdSe=H]
~~~

~~~
[녹지면적]
[계-면적]
[GA]
[2012 ~ 2020] 
[&format=json&jsonVD=Y&userStatsId=vt0602/460/TX_315_2009_H1037/2/1/20220318151611&prdSe=Y]
~~~

~~~
[녹지율]
[녹지지역-면적]
[GR]
[2012 ~ 2020]
[&format=json&jsonVD=Y&userStatsId=vt0602/101/DT_1YL202105E/2/1/20220318152644&prdSe=Y]
~~~

~~~
[도시지역인구현황]
[전체인구]
[PR]
[2012~2020]
[&format=json&jsonVD=Y&userStatsId=vt0602/460/TX_315_2009_H1001/2/1/20220318152808&prdSe=Y]
~~~

~~~
[면적_크기]
[합계]
[AS]
[2012~2020]
[&format=json&jsonVD=Y&userStatsId=vt0602/460/TX_315_2009_H1002/2/1/20220318152935&prdSe=Y]
~~~

~~~
[자동차주행거리]
[합계+승용차+승합차+화물차]
[CM]
[2012~2020]
[&format=json&jsonVD=Y&userStatsId=vt0602/426/DT_426001_N004/2/1/20220318153302&prdSe=Y]
~~~

~~~asciiarmor

[하천_면적]  //추후작업예정
[]
[10년미만,10년이상 합칠수 있으면 합치고 못합치면 10년미만-계, 10년이상-계]

~~~

~~~
[현재흡연율]
[조율]
[SM]
[2012~2019]
[&format=json&jsonVD=Y&userStatsId=vt0602/117/DT_H_SM/2/1/20220318153811&prdSe=Y]
~~~

~~~
[강수량]
[RR]
[2012~2021]
[&format=json&jsonVD=Y&userStatsId=vt0602/101/DT_1YL9901/2/1/20220318154444&prdSe=Y]
~~~

~~~
[유동인구]
[총전입 총전출 순이동]
[FP]
[2012~2021]
[&format=json&jsonVD=Y&userStatsId=vt0602/101/DT_1B26001_A01/2/1/20220318154916&prdSe=Y]
~~~

~~~
[폐기물처리시설매립시설]
[매립량(면적) 매립량(톤)]
[2012~2019]
[TLF]
[&format=json&jsonVD=Y&userStatsId=vt0602/106/DT_106N_99_3300027/2/1/20220318155252&prdSe=Y]
~~~

~~~
[폐기물처리시설현황]
[처리량]
[2012~2019]
[PTR]
[&format=json&jsonVD=Y&userStatsId=vt0602/106/DT_106T_009432/2/1/20220318155650&prdSe=Y]
~~~

~~~
[이산화탄소대기오염도]
[CO2]
[201201~202012] (월단위: 2021 존재는 하는데 아직 4월까지만 있어서 제외함)
[&format=json&jsonVD=Y&userStatsId=vt0602/106/DT_106N_03_0200044/2/1/20220318160001&prdSe=M]
~~~

~~~
[농장수및마리수]
[한육우:마리수]
[COW]
[201401~202104] (분기 4분기순 01 02 03 04)
[&format=json&jsonVD=Y&userStatsId=vt0602/101/DT_1EO200/2/1/20220318160410&prdSe=Q]
~~~

~~~
[폐수유기물질방류량]
[폐수발생량, 폐수방류량, 유기물질부하량]
[WW]
[2012~2019]
[&format=json&jsonVD=Y&userStatsId=vt0602/106/DT_106N_01_0100069/2/1/20220318160929&prdSe=Y]
~~~

~~~
[논밭별경지면적]
[계]
[F]
[2012~2021]
[&format=json&jsonVD=Y&userStatsId=vt0602/101/DT_1EB002/2/1/20220318161216&prdSe=Y]
~~~

~~~
[미세먼지 연평균 (시/군/구)]

~~~





### 응답 자료의 종류

---

### response data form

~~~
자료의 종류를 구분하는 것은 매우 기초적인 것이지만, 분석 대상과 방법을 설정함에 있어서 가장 중요한 부분이니 반드시 숙지하고 있어야 합니다.
~~~

<u>아래 두 양식중 원하는 자료 양식을 선택해야한다.</u>

+ **시계열:** 하나의 변수를 여러 시점으로 반환   ex) 변수 A의 2019 ,2020 , 2021 데이터
+ **횡단면:** 하나의 시점에 여러개의 변수를 반환  ex) 2019시점의 변수 A,B,C,D 데이터

[[통계학\] 횡단면, 시계열, 패널 자료 개념 정리 – 모두의매뉴얼 (triki.net)](http://triki.net/study/3343)





### 횡단면 자료

~~~
[대상] - 서울,부산 
[기간] - 최근 3년자료 
[형식] - 횡단면
[변수(속성)] - 조율,표준오차,응답자수,표준화율,표준화율표준오차
~~~



+ 하나의 시점에 모든 자료를 반환함을 볼수있다.

| 활용자료명 | URL 상세 정보                                                | 조회구분 | URL보기/결과값보기 |
| :--------: | ------------------------------------------------------------ | -------- | ------------------ |
|    횡단    | 조율／조율표준오차／응답자수／표준화율 ＊ 서울특별시／부산광역시 | 횡단면   |                    |



**응답**

+ 응답 결과는 아래와 같다.
+ 서울시 모든 변수의 값 다 나오고 부산시 모든 변수의 값 나옴

|  시군구별  | 조율 (%) | 조율표준오차 (%) | 응답자수 (명) | 표준화율 (%) | 표준화율표준오차 (%) |
| :--------: | -------- | ---------------- | ------------- | ------------ | -------------------- |
| 서울특별시 | 16.7     | 0.3              | 22928         | 17.8         | 0.3                  |
| 부산광역시 | 17.7     | 0.4              | 14510         | 19           | 0.4                  |

~~~json
[
    {
        "TBL_NM": "시·군·구별 현재흡연율",
        "PRD_DE": "2019", //모두 2019 시점
        "TBL_ID": "DT_H_SM",
        "ITM_NM": "조율", //변수1
        "ITM_NM_ENG": "Crude Death Rate",
        "ITM_ID": "CR",
        "UNIT_NM": "%",
        "ORG_ID": "117",
        "UNIT_NM_ENG": "%",
        "C1_OBJ_NM": "시군구별",
        "C1_OBJ_NM_ENG": "Classification of Region of Regional Community'S Health Survey",
        "DT": "16.7",
        "PRD_SE": "A",
        "C1": "001",
        "C1_NM": "서울특별시", //대상1
        "C1_NM_ENG": "Seoul"
    },
    {
        "TBL_NM": "시·군·구별 현재흡연율",
        "PRD_DE": "2019",
        "TBL_ID": "DT_H_SM",
        "ITM_NM": "조율표준오차", //변수2
        "ITM_NM_ENG": "Standard Error",
        "ITM_ID": "CR_SE",
        "ORG_ID": "117",
        "C1_OBJ_NM": "시군구별",
        "C1_OBJ_NM_ENG": "Classification of Region of Regional Community'S Health Survey",
        "DT": "0.3",
        "PRD_SE": "A",
        "C1": "001",
        "C1_NM": "서울특별시",
        "C1_NM_ENG": "Seoul"
    },
    {
        "TBL_NM": "시·군·구별 현재흡연율",
        "PRD_DE": "2019",
        "TBL_ID": "DT_H_SM",
        "ITM_NM": "응답자수", //변수3
        "ITM_NM_ENG": "N",
        "ITM_ID": "N",
        "UNIT_NM": "명",
        "ORG_ID": "117",
        "UNIT_NM_ENG": "Person",
        "C1_OBJ_NM": "시군구별",
        "C1_OBJ_NM_ENG": "Classification of Region of Regional Community'S Health Survey",
        "DT": "22928",
        "PRD_SE": "A",
        "C1": "001",
        "C1_NM": "서울특별시",
        "C1_NM_ENG": "Seoul"
    },
    {
        "TBL_NM": "시·군·구별 현재흡연율",
        "PRD_DE": "2019",
        "TBL_ID": "DT_H_SM",
        "ITM_NM": "표준화율", //변수4
        "ITM_NM_ENG": "Standardized Rate",
        "ITM_ID": "SR",
        "UNIT_NM": "%",
        "ORG_ID": "117",
        "UNIT_NM_ENG": "%",
        "C1_OBJ_NM": "시군구별",
        "C1_OBJ_NM_ENG": "Classification of Region of Regional Community'S Health Survey",
        "DT": "17.8",
        "PRD_SE": "A",
        "C1": "001",
        "C1_NM": "서울특별시",
        "C1_NM_ENG": "Seoul"
    },
    {
        "TBL_NM": "시·군·구별 현재흡연율",
        "PRD_DE": "2019",
        "TBL_ID": "DT_H_SM",
        "ITM_NM": "표준화율표준오차", //변수5
        "ITM_NM_ENG": "Standard Error",
        "ITM_ID": "SR_SE",
        "ORG_ID": "117",
        "C1_OBJ_NM": "시군구별",
        "C1_OBJ_NM_ENG": "Classification of Region of Regional Community'S Health Survey",
        "DT": "0.3",
        "PRD_SE": "A",
        "C1": "001",
        "C1_NM": "서울특별시",
        "C1_NM_ENG": "Seoul"
    },
    {
        "TBL_NM": "시·군·구별 현재흡연율",
        "PRD_DE": "2019",
        "TBL_ID": "DT_H_SM",
        "ITM_NM": "조율",
        "ITM_NM_ENG": "Crude Death Rate",
        "ITM_ID": "CR",
        "UNIT_NM": "%",
        "ORG_ID": "117",
        "UNIT_NM_ENG": "%",
        "C1_OBJ_NM": "시군구별",
        "C1_OBJ_NM_ENG": "Classification of Region of Regional Community'S Health Survey",
        "DT": "17.7",
        "PRD_SE": "A",
        "C1": "002",
        "C1_NM": "부산광역시", //대상2
        "C1_NM_ENG": "Busan"
    },
    {
        "TBL_NM": "시·군·구별 현재흡연율",
        "PRD_DE": "2019",
        "TBL_ID": "DT_H_SM",
        "ITM_NM": "조율표준오차",
        "ITM_NM_ENG": "Standard Error",
        "ITM_ID": "CR_SE",
        "ORG_ID": "117",
        "C1_OBJ_NM": "시군구별",
        "C1_OBJ_NM_ENG": "Classification of Region of Regional Community'S Health Survey",
        "DT": "0.4",
        "PRD_SE": "A",
        "C1": "002",
        "C1_NM": "부산광역시",
        "C1_NM_ENG": "Busan"
    },
    {
        "TBL_NM": "시·군·구별 현재흡연율",
        "PRD_DE": "2019",
        "TBL_ID": "DT_H_SM",
        "ITM_NM": "응답자수",
        "ITM_NM_ENG": "N",
        "ITM_ID": "N",
        "UNIT_NM": "명",
        "ORG_ID": "117",
        "UNIT_NM_ENG": "Person",
        "C1_OBJ_NM": "시군구별",
        "C1_OBJ_NM_ENG": "Classification of Region of Regional Community'S Health Survey",
        "DT": "14510",
        "PRD_SE": "A",
        "C1": "002",
        "C1_NM": "부산광역시",
        "C1_NM_ENG": "Busan"
    },
    {
        "TBL_NM": "시·군·구별 현재흡연율",
        "PRD_DE": "2019",
        "TBL_ID": "DT_H_SM",
        "ITM_NM": "표준화율",
        "ITM_NM_ENG": "Standardized Rate",
        "ITM_ID": "SR",
        "UNIT_NM": "%",
        "ORG_ID": "117",
        "UNIT_NM_ENG": "%",
        "C1_OBJ_NM": "시군구별",
        "C1_OBJ_NM_ENG": "Classification of Region of Regional Community'S Health Survey",
        "DT": "19",
        "PRD_SE": "A",
        "C1": "002",
        "C1_NM": "부산광역시",
        "C1_NM_ENG": "Busan"
    },
    {
        "TBL_NM": "시·군·구별 현재흡연율",
        "PRD_DE": "2019",
        "TBL_ID": "DT_H_SM",
        "ITM_NM": "표준화율표준오차",
        "ITM_NM_ENG": "Standard Error",
        "ITM_ID": "SR_SE",
        "ORG_ID": "117",
        "C1_OBJ_NM": "시군구별",
        "C1_OBJ_NM_ENG": "Classification of Region of Regional Community'S Health Survey",
        "DT": "0.4",
        "PRD_SE": "A",
        "C1": "002",
        "C1_NM": "부산광역시",
        "C1_NM_ENG": "Busan"
    }
]
~~~

> 객체 리스트 반환







### 시계열 자료

~~~
[대상] - 서울,부산 
[기간] - 최근 3년자료 
[형식] - 시계열 
[변수(속성)] - 조율,표준오차,응답자수,표준화율,표준화율표준오차
~~~



+ 각 `변수(속성) * 대상` 마다 요청이 생성되는 것을 확인할수있다.

| 활용자료명 | URL 상세 정보                  | 조회구분 | URL보기/결과값보기 |
| :--------: | ------------------------------ | -------- | ------------------ |
|  시계열_1  | 조율 ＊ 서울특별시             | 시계열   |                    |
|  시계열_2  | 조율 ＊ 부산광역시             | 시계열   |                    |
|  시계열_3  | 조율표준오차 ＊ 서울특별시     | 시계열   |                    |
|  시계열_4  | 조율표준오차 ＊ 부산광역시     | 시계열   |                    |
|  시계열_5  | 응답자수 ＊ 서울특별시         | 시계열   |                    |
|  시계열_6  | 응답자수 ＊ 부산광역시         | 시계열   |                    |
|  시계열_7  | 표준화율 ＊ 서울특별시         | 시계열   |                    |
|  시계열_8  | 표준화율 ＊ 부산광역시         | 시계열   |                    |
|  시계열_9  | 표준화율표준오차 ＊ 서울특별시 | 시계열   |                    |
| 시계열_10  | 표준화율표준오차 ＊ 부산광역시 | 시계열   |                    |



**응답**

+ 첫번째 요청 `  조율 ＊ 서울특별시` 만 확인해보면 아래와 같은 응답이 온다.

|  시군구별  | 항목     | 2017 | 2018 | 2019 |
| :--------: | -------- | ---- | ---- | ---- |
| 서울특별시 | 조율 (%) | 18.8 | 18.6 | 16.7 |

~~~json
[
    {
        "TBL_NM": "시·군·구별 현재흡연율",
        "PRD_DE": "2017", //시점1
        "TBL_ID": "DT_H_SM",
        "ITM_NM": "조율", //변수
        "ITM_NM_ENG": "Crude Death Rate",
        "ITM_ID": "CR",
        "UNIT_NM": "%",
        "ORG_ID": "117",
        "UNIT_NM_ENG": "%",
        "C1_OBJ_NM": "시군구별",
        "C1_OBJ_NM_ENG": "Classification of Region of Regional Community'S Health Survey",
        "DT": "18.8", //값
        "PRD_SE": "A",
        "C1": "001",
        "C1_NM": "서울특별시", //대상
        "C1_NM_ENG": "Seoul"
    },
    {
        "TBL_NM": "시·군·구별 현재흡연율",
        "PRD_DE": "2018", //시점2
        "TBL_ID": "DT_H_SM",
        "ITM_NM": "조율",  //변수
        "ITM_NM_ENG": "Crude Death Rate",
        "ITM_ID": "CR",
        "UNIT_NM": "%",
        "ORG_ID": "117",
        "UNIT_NM_ENG": "%",
        "C1_OBJ_NM": "시군구별",
        "C1_OBJ_NM_ENG": "Classification of Region of Regional Community'S Health Survey",
        "DT": "18.6", //값
        "PRD_SE": "A",
        "C1": "001",
        "C1_NM": "서울특별시", //대상
        "C1_NM_ENG": "Seoul"
    },
    {
        "TBL_NM": "시·군·구별 현재흡연율",
        "PRD_DE": "2019", //시점3
        "TBL_ID": "DT_H_SM",
        "ITM_NM": "조율",  //변수
        "ITM_NM_ENG": "Crude Death Rate",
        "ITM_ID": "CR",
        "UNIT_NM": "%",
        "ORG_ID": "117",
        "UNIT_NM_ENG": "%",
        "C1_OBJ_NM": "시군구별",
        "C1_OBJ_NM_ENG": "Classification of Region of Regional Community'S Health Survey",
        "DT": "16.7", //값
        "PRD_SE": "A",
        "C1": "001",
        "C1_NM": "서울특별시", //대상
        "C1_NM_ENG": "Seoul"
    }
]
~~~

> 객체 리스트 반환





## Parsing

---

+ Kosis는 모든 응답을 객체 리스트로 반환한다.

~~~json
[
{},
{},
{},
...
{}
]
~~~





