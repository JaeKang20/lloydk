import openai
import json
import dotenv
import time
import streamlit as st
from elasticsearch import Elasticsearch
from pymongo import MongoClient
import pinecone
from sentence_transformers import SentenceTransformer

#------------------------------ connection to DB----------------------------------

def connect_es():
    host = '********************
    ca_certs = '/home/******/elasticsearch-8.10.3/config/certs/http_ca.crt'
    userName = '*******'
    passWord = '******'

    client = Elasticsearch(request_timeout=600,hosts=host, ca_certs=ca_certs, basic_auth=(userName, passWord))
    return client

def connect_mongo():
    client = MongoClient(" mongodb+srv://mongo:mongo@cluster0.x2zqb.mongodb.net/?retryWrites=true&w=majority")
    db = client.lloydk
    return db

#---------------------------------Utills-------------------------------------------

def get_gpt_api():
    openai.api_key = '******'

def get_env_file(key):

    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)

    # 전체 변수 dict
    env_dict = dotenv.dotenv_values(dotenv_file)
    print(env_dict)

    value = dotenv.dotenv_values(dotenv_file)[key]
    print(key, ':', value)
    return value

#토큰 수 확인
def take_token(text_info):
    #import tiktoken #SentenceTransformer 충돌 가능성
    #tokenizer = tiktoken.get_encoding("cl100k_base") #cl100k_base: text-embedding-ada-002 model Encoding
    #token_count = len(tokenizer.encode(text_info))

    #임시
    token_count = 0
    print(f"토큰 수: {token_count}")
    return token_count

#-------------------------------search text embedding------------------------------

def get_embedding(text, model='text-embedding-ada-002'):

    response = openai.Embedding.create(
        input=text,
        model=model
    )
    embedding = response['data'][0]['embedding']

    return embedding

def text_embedding_model_ada(text_info):  # ada embedding fuction

    get_gpt_api()

    start_time = time.perf_counter()
    try:
        list_embedding_value = get_embedding(text_info)
    except Exception as e :
        #ada 입력 토큰 수 제한 8,192개
        print(e)
        print('토큰 수:', take_token(text_info))
        end_time = 10
    else: #에러 안 났을 때
        end_time = time.perf_counter()

    ada_embedding_time = end_time - start_time

    return list_embedding_value ,ada_embedding_time

def get_taaco_vector(text_info):    # taaco embedding function

    model = SentenceTransformer('KDHyun08/TAACO_STS')

    start_time = time.perf_counter()
    vector = list(model.encode(text_info))
    end_time = time.perf_counter()

    taaco_embedding_time = end_time - start_time
    vector = list(map(float, vector))

    return vector, taaco_embedding_time

#-------------------------------elastic vector search-------------------------------

def vector_search_model_ada(client, vector):
    query = {
        'field':'content_vector_ada',
        'query_vector': vector,
        'k': 5,
        'num_candidates': 10000
    }

    start_time = time.perf_counter()
    json_response = client.search(index='naver_news_ada_taaco', knn=query, source=['title', 'content'])
    end_time = time.perf_counter()

    query_time = end_time - start_time
    return json_response, query_time

def vector_search_model_taaco(client, vector):
    query = {
        'field':'content_vector_taaco',
        'query_vector': vector,
        'k': 5,
        'num_candidates': 10000
    }
    start_time = time.perf_counter()
    json_response = client.search(index='naver_news_ada_taaco', knn=query, source=['title', 'content'])
    end_time = time.perf_counter()

    query_time = end_time - start_time
    return json_response, query_time

#------------------------------------------MongoDB vector search-----------------------------------------

def query_to_mongodb_ada(client, question_vector):

    collection = client['naver-news-ada']
    start_time = time.perf_counter()
    result = collection.aggregate([
        {
        "$vectorSearch": {
            "index": "ada_index",
            "queryVector": question_vector,
            "path": "content_vector_ada",
            "numCandidates": 10000,
            "limit": 5,
            },
        "returnStoredSource": True
        }
    ])
    end_time = time.perf_counter()
    query_time = end_time - start_time
    id_list = []

    for document in result :
        id_list.append(document["id"])

    return id_list, query_time

def query_to_mongodb_taaco(client, question_vector):

    collection = client['naver-news-taaco']
    start_time = time.perf_counter()
    result = collection.aggregate([
        {
        "$vectorSearch": {
            "index": "taaco_index",
            "queryVector": question_vector,
            "path": "content_vector_ada",
            "numCandidates": 10000,
            "limit": 5,
            },
        "returnStoredSource": True
        }
    ])
    end_time = time.perf_counter()
    query_time = end_time - start_time
    id_list = []

    for document in result :
        id_list.append(document["id"])

    return id_list, query_time

#------------------------------------------pinecone vector search-----------------------------------------

def query_to_pinecone(index_name, question_vector):

    # api_key = get_env_file('PINECONE_API_KEY')
    api_key = '******'
    question_vector = list(map(float, question_vector))
    ## 초기화
    pinecone.init(
        api_key=api_key, environment="asia-northeast1-gcp"
    )
    ## 인스턴스 생성
    index = pinecone.Index(index_name)
    result = []
    start_time = time.perf_counter()
    return_json = index.query(
                    vector=question_vector,
                    top_k=5,
                    include_values=False
                    )
    end_time = time.perf_counter()
    query_time = end_time - start_time
    for doc in return_json.get('matches'):
        result.append(doc['id'])

    return result, query_time

#-------------------------------------------keyword search for other DB-----------------------------------

def url_keyword_search(client, url):
    query = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "url.keyword": url
                    }
                }
            }
        }
    }

    json_response = client.search(index='naver_news_ada_taaco', body=query, source=['title', 'content'])

    return json_response

def id_keyword_search(client, id):
    json_response = client.get(index='naver_news_ada_taaco', id=id, source=['title', 'content'])

    return json_response

#----------------------------------------------종합 검색 함수-------------------------------------------------

def elastic_vector_search(client, embedding_type, vector): # Elasticsearch vector search

    if embedding_type == "ada": # ada 벡터검색
        json_result, elastic_query_time = vector_search_model_ada(client, vector)
        result = json_result['hits']['hits']

    else : # taaco 벡터 검색
        json_result, elastic_query_time = vector_search_model_taaco(client, vector)
        result = json_result['hits']['hits']


    return result, elastic_query_time

def mongo_vector_search(client, embedding_type, vector): # MongoDB Atlas vector search

    db = connect_mongo()

    if embedding_type == "ada": # ada 벡터검색
        id_list, mongo_query_time = query_to_mongodb_ada(db, vector)
        result = []
        for id in id_list:
            result.append(id_keyword_search(client, id)['_source'])

    else : # taaco 벡터 검색
        id_list, mongo_query_time = query_to_mongodb_taaco(db, vector)
        result = []
        for id in id_list:
            result.append(id_keyword_search(client, id)['_source'])

    return result, mongo_query_time

def pinecone_vector_search(client, embedding_type, vector): # Pinecone vector search

    if embedding_type == "ada": # ada 벡터검색
        index_name = "naver-news-ada"
        id_list, pinecone_query_time = query_to_pinecone(index_name, vector)
        result = []
        for id in id_list:
            result.append(id_keyword_search(client, id)['_source'])

    else : # taaco 벡터 검색
        index_name = "naver-news-taaco"
        id_list, pinecone_query_time = query_to_pinecone(index_name, vector)
        result = []
        for id in id_list:
            result.append(id_keyword_search(client, id)['_source'])

    return result, pinecone_query_time

def one_search(embedding_type, search_text):
    result = {}
    client = connect_es()

    # 질문 벡터화
    if embedding_type == "ada":
        vector, embedding_time = text_embedding_model_ada(search_text)
    else :
        vector, embedding_time = get_taaco_vector(search_text)

    result["mongo"], result["mongo_query_time"] = '', 0

    # 각 db에 벡터로 질의
    result["embedding_time"] = embedding_time
    result["elastic"], result["elastic_query_time"] = elastic_vector_search(client, embedding_type, vector)
    # result["mongo"], result["mongo_query_time"] = mongo_vector_search(client, embedding_type, vector)
    result["pinecone"], result["pinecone_query_time"] = pinecone_vector_search(client, embedding_type, vector)

    return result

# print(one_search("taaco", "화려한 불꽃축제"))


def one_search_v2(search_text): # 6개를 한꺼번에
    result = {}
    client = connect_es()

    # 질문 벡터화
    vector_ada, embedding_time_ada = text_embedding_model_ada(search_text)
    vector_taaco, embedding_time_taaco = get_taaco_vector(search_text)

    result["mongo_ada"], result["mongo_query_time_ada"]= '', 0
    result["mongo_taaco"], result["mongo_query_time_taaco"] = '', 0

    # 각 db에 벡터로 질의
    result["embedding_time_ada"] = embedding_time_ada
    result["embedding_time_taaco"] = embedding_time_taaco
    result["elastic_ada"], result["elastic_query_time_ada"] = elastic_vector_search(client, embedding_type="ada", vector = vector_ada)
    # result["mongo_ada"], result["mongo_query_time_ada"] = mongo_vector_search(client, embedding_type="ada", vector = vector_ada)
    result["pinecone_ada"], result["pinecone_query_time_ada"] = pinecone_vector_search(client, embedding_type="ada", vector = vector_ada)
    result["elastic_taaco"], result["elastic_query_time_taaco"] = elastic_vector_search(client, embedding_type="taaco", vector = vector_taaco)
    # result["mongo_taaco"], result["mongo_query_time_taaco"] = mongo_vector_search(client, embedding_type="taaco", vector = vector_taaco)
    result["pinecone_taaco"], result["pinecone_query_time_taaco"] = pinecone_vector_search(client, embedding_type="taaco", vector = vector_taaco)

    return result

# print(one_search_v2("화려한 불꽃축제"))