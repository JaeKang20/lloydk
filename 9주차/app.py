import streamlit as st
from vector_search import elastic_vector_search, mongo_vector_search, pinecone_vector_searh

#검색 결과를 화면에 표시
#Elasticsearch, MongoDB, Pinecone의 결과 형식에 따라 결과를 추출하고 제목과 내용을 출력합니다.
def display_results(json_search_result):

    for search_result in json_search_result :
        content=''; title=''

        #print(type(json_search_result))
        # 검색 결과가 딕셔너리인지 확인
        if isinstance(search_result, dict):
            #{'_index': 'naver_news_ada_taaco', '_id': '_2yENosBQ3ADMC_7tZ8-', '_score': 0.6944564,
            # '_source': {'title': '[속보] 대법 "구글, 이용자 정보 제공내역 공개해야"', 'content': 'ⓒ연합뉴스'}}
            # 딕셔너리인 경우, 제목과 내용을 추출합니다
            try :
                content=search_result['_source']['content']
                title=search_result['_source']['title']
            except: #실패시 몽고db
                content=search_result['content']
                title=search_result['title']
        # 만약 검색 결과가 리스트인 경우, 리스트를 반복하며 처리합니다
        if isinstance(search_result, list):
            for jj in search_result :
                content=jj['_source']['content']
                title=jj['_source']['title']

        else : #결과 에러 문자열 반환
            st.write(f"###### {title}")
            st.error('json_search_result')
            return


        st.write(f"###### {title}")
        st.markdown(f'<div style="background-color: #f4f4f4; padding: 10px;">{content}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    #time ---------------------------
    # response_time = json_search_result.get('took', 0)
    # response_time_str = f"Response Time: {response_time} ms"
    # st.subheader(response_time_str)


def set_columns_response(elasticsearch_results, mongodb_results, pinecone_results):

    # Streamlit에 3개의 컬럼을 생성
    columns = st.columns(3)

    responses = {
        "Elasticsearch": ("#### Elasticsearch", elasticsearch_results),
        "MongoDB": ("#### MongoDB", mongodb_results),
        "Pinecone": ("#### Pinecone", pinecone_results)
    }

    for i, selected_type in enumerate(responses):
        with columns[i]:
            st.markdown(responses[selected_type][0])
            display_results(responses[selected_type][1])


# Streamlit 앱의 메인 부분
def main():
    #st.title("로이드케이-7기")
    st.title("Vector search compare")

    query = st.text_input("검색어 입력",'요즘 북한의 도발 정세는?')

    # Add a selection for embedding type (ADA or Taaco)
    embedding_type = st.radio("Embedding 선택", ("ADA", "Taaco"))

    if st.button("검색하기"):
        with st.spinner('검색 중...'):
            # 검색 실행 및 결과 반환
            elasticsearch_results = elastic_vector_search(embedding_type, query)
            mongodb_results = mongo_vector_search(embedding_type, query)
            pinecone_results = pinecone_vector_searh(embedding_type, query)

        # 결과 표시
        set_columns_response(elasticsearch_results, mongodb_results, pinecone_results)

if __name__ == "__main__":
    main()









