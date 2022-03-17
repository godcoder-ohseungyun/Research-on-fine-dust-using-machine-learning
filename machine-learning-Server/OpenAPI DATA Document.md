

### Make finalDataFrame using  OpenAP's json response

---

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





### 모듈화

---

+ **주제당 2012~2022 까지 데이터를 수집할예정이다.**

  > <u>주제당 10개의 url과 dataFrame이 생성된다.</u> (횡단면 자료이기때문에 시점당 한개씩 생성됨)





+ **20개의 주제가 존재함으로 200개의 요청 url과 dataFrame이 생성될것이다.**

+ **기능을 쪼개 모듈화해 중복코드를 최대한 줄이고 추후 관리가 편하도록 설계해야한다.**

  > 인증키 만료
  >
  > 주제변경에 따른 url 재설계
  >
  > 등등 
  >
  > **변동가능성이 높기때문**





### **설계 계획**























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





