## Elasticsearch란?

- Elastic 사의 Elasticsearch 제품을 칭한다.

다루는 모든 데이터는 텍스트로 존재해야 한다.(정형화/비정형화와는 상관 없다.)

### 클러스터란?
역색인을 사용하는데

기본적으로 노드가 3개 존재한다. (하나는 empty하지만 원본 데이터가 죽을 때 사용됨)

부하가 생길 때마다 스케일 아웃합니다. 1개(Y) > 3개(G) (스케일 업 x)

분산 저장할수 있음

G,Y,R
G: 데이터의 원본과 백업본이 존재\
Y: 원본만 존재\
R: 원본, 백업본 모두 없는 상태

레플리카는 백업을 빠르게 하기 위해
샤딩은 검색을 빠르게 하기 위해

## Task_설치해보기!

| Window(powershell로 설치 gitbash x) | zip      |
|----------------------------------|----------|
| Linux                            | tar, rpm | 

6,7,8버전 (7,8,6순으로 하기를 추천)

8 마지막 버전 보안 설정이 생겨서 에러가 많이 생김

7점 (마지막버전, 중반버전) 6점 중반 버전

ES -> kibana(비츠는 매트릭 비츠, 로그 스테시 설치(로그 확인해보기))

[참고링크](https://docs.google.com/document/d/1Dz_TR1NGn4f1mpoP2JU2j6N5EdZeND8J5xfnpGUGKtA/edit)

[참고링크2](https://velog.io/@yje876/ElasticSearch-CentOS7-ELK-Stack-%EC%84%A4%EC%B9%98)

    
## 01. Java설치
[자바설치참고 링크](https://studying-penguin.tistory.com/2)

02. home설정


    which javac
    /bin/javac
    [root@localhost ~]# readlink -f /bin/javac
    /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.382.b05-1.el7_9.x86_64/bin/javac
    이거를 JAVA_HOME 설정 하고 싶어


> export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.382.b05-1.el7_9.x86_64

## 03. ElasticSearch 설치
 [ElasticSearch설치참고 링크]()

wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.5.2-linux-x86_64.tar.gz

tar -xzf elasticsearch-7.5.2-linux-x86_64.tar.gz

