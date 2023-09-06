    Systemctl 명령어를 통해 리눅스를 킬때마다 zookeeper, kafka를 사용하는 법


리눅스에서 시스템을 부팅할 때마다 ZooKeeper와 Kafka를 자동으로 실행하려면 `systemctl`을 사용하여 서비스 유닛을 생성해야 합니다. 이것은 시스템 부팅 시에 자동으로 시작되도록 구성할 수 있습니다.

다음은 시스템 부팅 시에 ZooKeeper와 Kafka를 자동으로 시작하는 방법입니다. 아래의 단계를 따라 실행하세요.

1. **ZooKeeper 서비스 유닛 설정**:

   먼저, ZooKeeper를 위한 서비스 유닛을 작성합니다. 서비스 유닛 파일은 보통 `/etc/systemd/system/` 디렉토리에 저장됩니다.

   ```bash
   sudo vi /etc/systemd/system/zookeeper.service
   ```

   그리고 아래와 같이 파일 내용을 작성합니다. 파일 이름은 `zookeeper.service`로 저장되어야 합니다.

   ```plaintext
   [Unit]
   Description=ZooKeeper Service
   After=network.target
   
   [Service]
   ExecStart=/path/to/zookeeper/bin/zkServer.sh start
   ExecStop=/path/to/zookeeper/bin/zkServer.sh stop
   User=zookeeper-user
   Group=zookeeper-group
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

   위 설정에서 `/path/to/zookeeper`를 실제 ZooKeeper 설치 경로로 바꿔주어야 합니다. 또한 `zookeeper-user`와 `zookeeper-group`을 실제로 사용하고 있는 유저와 그룹으로 변경해야 합니다.

2. **Kafka 서비스 유닛 설정**:

   다음으로, Kafka를 위한 서비스 유닛을 생성합니다. ZooKeeper 서비스 유닛을 만드는 것과 유사한 방식으로 진행합니다.

   ```bash
   sudo nano /etc/systemd/system/kafka.service
   ```

   그리고 아래와 같이 파일 내용을 작성합니다. 파일 이름은 `kafka.service`로 저장되어야 합니다.

   ```plaintext
   [Unit]
   Description=Apache Kafka Service
   After=zookeeper.service network.target
   
   [Service]
   ExecStart=/path/to/kafka/bin/kafka-server-start.sh /path/to/kafka/config/server.properties
   ExecStop=/path/to/kafka/bin/kafka-server-stop.sh
   User=kafka-user
   Group=kafka-group
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

   마찬가지로 `/path/to/kafka`를 실제 Kafka 설치 경로로 바꾸고, `kafka-user`와 `kafka-group`을 실제 유저와 그룹으로 변경해야 합니다.

3. **시스템 서비스 다시 읽기 및 시작**:

   설정 파일을 작성한 후, 시스템 서비스를 다시 읽고 시작해야 합니다.

   ```bash
   sudo systemctl daemon-reload
   ```

4. **시스템 부팅 시 자동 시작 설정**:

   이제 서비스를 시스템 부팅 시에 자동으로 시작하도록 설정할 수 있습니다.

   ```bash
   sudo systemctl enable zookeeper.service
   sudo systemctl enable kafka.service
   ```

   이제 시스템을 재부팅하면 ZooKeeper와 Kafka 서비스가 자동으로 시작됩니다.

이제 시스템을 재부팅하면 ZooKeeper와 Kafka가 자동으로 시작됩니다. 필요한 경우 서비스 이름, 사용자 및 그룹, 경로 등을 실제 환경에 맞게 수정하십시오.ㅇ