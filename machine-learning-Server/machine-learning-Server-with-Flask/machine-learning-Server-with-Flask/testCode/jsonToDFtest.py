
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


from DFBuilder import DFBuilder



dff = DFBuilder()

dff.getFinalDataFrame()









#이런식으로 다른곳 전역변수를 불러올수있음
import autoVtest as a
print(a.smt_1)