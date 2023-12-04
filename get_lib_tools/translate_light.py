import requests
import re
import json
from cases import cases_dict
from cases import really_big_cases
from cases import matreshka
from cases import k2
from cases import k12
from time import perf_counter


beta_staging = "adolgov.xstaging.tv"
beta_stable = "beta.tradingview.com"

def request_translate_light(beta,version, source):
    url = f"https://{beta}/pine-facade/translate_light?user_name=Batut&v={version}" #mbakholdin.xstaging.tv
    headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "multipart/form-data; boundary=---------------------------106017837933037236722733296263"
    }
    data1 = f"-----------------------------106017837933037236722733296263\r\nContent-Disposition: form-data; name=\"source\"\r\n\r\n{source}\r\n\r\n-----------------------------106017837933037236722733296263--\r\n"
    response = requests.post(url, headers = headers, data=data1)
    return response

#case 3812,3813

def perf_counters(beta,version,case):
    start = perf_counter()
    for key,value in case.items():
        responce = request_translate_light(beta,version,value)
        assert responce.status_code == 200, f'status code = {responce.status_code}\n with case = {key}\n responce = {responce.json()}'
    stop = perf_counter()

    print(f"beta = {beta} version = {version}\nestimated {stop - start}\n")

def case_import(case):
    result_dict = {}
    for key,value in case.items():
        result_dict[key] = [request_translate_light(beta_staging,3,value).json(),request_translate_light(beta_staging,2,value).json()]

    with open("v3_result.json","w+") as v1:
        for key,value in result_dict.items(): 
            v1.write(f"case = {key}\n{json.dumps(value[0], sort_keys=True, indent=4)}\n\n")
    with open("v2_result.json","w+") as v2:
        for key,value in result_dict.items(): 
            v2.write(f"case = {key}\n{json.dumps(value[1], sort_keys=True, indent=4)}\n\n")

# version = ["1","2"]
# version = ["3","2"]
# betas = {beta_stable:version,beta_stable:version}
# cases = [cases_dict,really_big_cases,matreshka]
# n = 0
# while n <=3:
#     print(f'circle {n}: ') 
#     for k,v in betas.items():
#         for i in v:
#             perf_counters(k,i,k12)
#     n+=1

case_import(cases_dict)  

