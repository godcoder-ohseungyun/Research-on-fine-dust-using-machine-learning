# machine-learning-Server API Document

---

###  EndPoint

~~~
 http://127.0.0.1:5000/api
~~~

<br>

### APIs

~~~
[GET] http://127.0.0.1:5000/api/result
~~~

+ 지역별 미세먼지 점수 및 전망을 응답합니다.

~~~JSON
EX)
[{	
    "City": "seoul"
    "District": "songpa"
    "Pollution factor score": 73  --지역내 공해시설수 등의 공해 요인 종합 점수 100점 만점
    "prospect": -1.5     --확률을 의미 [상승 or 하양]
},
{
    ...
},..
]
~~~

+ 매핑 메서드

### **getAnalysis()**

~~~python
@app.route('/api/result')
def getAnalysis():
	# 최종 데이터 프레임
    finalDataFrame = getOpenApi()
	
    # 로지스틱 회귀 학습
    LogisticModel = doLogisticRegression(finalDataFrame)
    
    # 수동 데이터 프레임
    RegionalRepresentativeDataFrame =  DFBuilder().csvToDataFrame(csv)
    
    #최종 결과: 객체 리스트 형태
    resultList = fianlResult(LogisticModel,RegionalRepresentativeDataFrame)
    
    #TODO: object list -> JSON 변환작업
    jsonResult = json.dumps([Item.__dict__ for Item in resultList], ensure_ascii=False)

    return jsonResult
~~~

> **reference**
>
> + 한글이 유니코드로 저장되는 현상 해결
> + 객체 타입 json으로 변환하기
> + 객체 리스트 타입 json으로 변환하기
>
> [Python) json.dumps() 이용시 한글이 유니코드로 저장되는 현상 해결 :: Developer Calssess (tistory.com)](https://calssess.tistory.com/98)
>
> [List of objects to JSON with Python - Stack Overflow](https://stackoverflow.com/questions/26033239/list-of-objects-to-json-with-python)
>
> [How to Convert Python Class Object to JSON? - Python Examples](https://pythonexamples.org/convert-python-class-object-to-json/)

<br>

<br>

# Server internal logic Document

---

<br>

## mainServer logic 

+ request & response 작업을 수행합니다.
+ 내부 로직들을 호출해서 응답데이터를 생성합니다.

<br>

### **getOpenApi()**

> **reference:** https://yobbicorgi.tistory.com/32 , https://wonhwa.tistory.com/9   
>
> 
>
> **info:** 공공 데이터 포털에 request하여 받아온 json response를 정재하여 요구사항에 맞도록 정제합니다.
>
> 
>
> **Dependency:** DFBuilder class , UrlBuilder class
>
> 
>
> **return:** finalDataFrame
>
> 
>
> ### 'Dependency Class Info'
>
> ---
>
> **DFBuilder class** 
>
> + 회귀분석에 사용할 dataFrame 작업을 수행하는 클래스
>
> ~~~python
> '''
> info: 파라미터로 입력받은 url들을 convertToDataFrame , getFinalDataFrame 를 사용하여 변환 및 정제하여 최종 데이터 프레임을 반환합니다.
> 
> param: urls
> 
> return: finalDataFrame
> '''
> def buildDataFrame(self, url1,url2 .. n):
> 
> 
> '''
> info: 파라미터로 넘겨받은 url로 요청을 보내 받아온 json 데이터를 dataFrame으로 변환합니다.
> 
> param: url
> 
> return: dataFrame
> '''
> def convertToDataFrame(self, url):    
> 
> 
> '''
> info: 파라미터로 받아온 데이터 프레임들을 가공해 사용할 최종 데이터 프레임을 만듭니다.
> 
> param: dataframes
> 
> return: finalDataFrame
> '''
> def  getFinalDataFrame(self, dataframe1,dataframe2 ... n):
> 
> 
> '''
> info: csv로 직접 만든 데이터를 데이터 프레임으로 가공합니다
> '''
> def csvToDataFrame(csv):
> ~~~
>
> ---
>
>  **UrlBuilder class**
>
> + 회귀 분석에 사용할 모든 데이터의 OpenAPI request url생성을 작업하는 클래스
>
> ~~~python
> '''
> info: 회귀 분석에 사용할 모든 데이터의 OpenAPI request url을 생성합니다.
> 
> return: urls
> '''
> def buildRequsetUrls(self):
> ~~~

<br>



### doLogisticRegression(finalDataFrame)

> **info:** finalDataFrame을 가지고 회귀 분석 수행 후 해당 로지스틱 학습모델을 return합니다.
>
> 
>
> **param:** finalDataFrame
>
> 
>
> **return:** LogisticModel



<br>

### **fianlResult(LogisticModel, DataFrame)**

> **info:** 학습된 회귀 모델과 선별한 지역 대표 데이터를 가지고 분석한 결과를 return합니다.
>       결과는 각 지역별 결과표 리스트 입니다.
>
> 
>
> **Dependency:** Item class
>
> 
>
> **param:** LogisticModel, RegionalRepresentativeDataFrame
>
> 
>
> **return:**  City, District , Pollution factor score , prospect 를 가진 객체 리스트



















