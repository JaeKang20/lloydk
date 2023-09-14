'''
Created on 2023. 9. 12.

@author: lloydk-jisoo
'''
import json
import sys

#파일 확인(객체 줄 바꿔서 저장)

# 1. 파일을 전체적으로 문자열로 읽기
with open('testdata/dummy_data.json', 'r', encoding='utf-8') as f: #utf-8로 읽기
    data = f.read()
    print(data[0:100])

# 2. JSON 객체를 구분하는 문자열을 찾아서 줄 바꿈 문자로 교체
data = data.replace('},{', '},\n{')

# 3. 결과 문자열을 다시 파일에 쓰기
with open('testdata/dummy_data2.json', 'w', encoding='utf-8') as f:
    f.write(data)

# 4. 각 줄 출력
with open('testdata/dummy_data2.json', 'r', encoding='utf-8') as f:
    for line in f:
        print(line)

#[객체 개수 확인]
with open('testdata/dummy_data2.json', 'r', encoding='utf-8') as f:
    #문자열을 dict타입으로 저장
    json_string = f.read()
    data = json.loads(json_string, strict=False) 
    #json.loads: JSON 형식의 문자열을 받아 해당 문자열을 파이썬 자료구조로 변환. loads는 "Load String"의 약자
    # strict=True (기본값) 인 경우, 파서는 엄격한 JSON 규칙을 따르며, JSON 문자열 내에서 허용되지 않는 특수 문자 (예: '\x00'부터 '\x1f' 까지의 제어 문자)에 대한 오류를 발생.

if isinstance(data, list): # data가 리스트인 경우
    #data가 list 타입이면(배열형식), json.loads(data) 실행 => json배열([])을 파이썬의 리스트(list)로 변환([{}, {}, ...], 각 요소 딕셔너리)
    object_count = len(data)
else: # data는 dict 타입
    # data 내에 리스트를 찾고 그 리스트의 객체 개수 계산
    object_count = sum(len(value) for value in data.values() if isinstance(value, list))
    #data.values(): data가 딕셔너리인 경우, data.values()는 딕셔너리의 모든 값들을 dict_values 타입으로 반환
    #isinstance(value, list): dict_values가 list타입이면 리스트 요소 개수(len(values))가 sum()에 하나씩 전달

print(f"The JSON file contains {object_count} objects inside arrays.")



