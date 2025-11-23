# Kafka

Apache Kafka와 Spring Kafka를 사용하여 메시지 기반 비동기 통신을 구현하는 방법을 알아봅니다.

## Kafka란?

**Apache Kafka:** 분산 스트리밍 플랫폼

### 주요 개념

- **Producer:** 메시지를 발행하는 애플리케이션
- **Consumer:** 메시지를 구독하는 애플리케이션
- **Topic:** 메시지가 저장되는 카테고리
- **Partition:** Topic의 물리적 분할
- **Broker:** Kafka 서버
- **Consumer Group:** 여러 Consumer의 논리적 그룹

### 장점

- ✅ 높은 처리량 (초당 수백만 메시지)
- ✅ 확장성 (수평 확장 가능)
- ✅ 내구성 (디스크 저장)
- ✅ 순서 보장 (파티션 내)
- ✅ 실시간 처리

## 의존성 추가

### Maven

```xml
<dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
</dependency>

<!-- JSON 직렬화 -->
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
</dependency>
```

### Gradle

```gradle
implementation 'org.springframework.kafka:spring-kafka'
implementation 'com.fasterxml.jackson.core:jackson-databind'
```

## Kafka 설치

### Docker Compose

```yaml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"
  
  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

**실행:**
```bash
docker-compose up -d
```

## 기본 설정

### application.yml

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    
    # Producer 설정
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
      acks: all  # 모든 복제본 확인
      retries: 3
      properties:
        enable.idempotence: true  # 멱등성 보장
    
    # Consumer 설정
    consumer:
      group-id: my-group
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
      auto-offset-reset: earliest  # 처음부터 읽기
      enable-auto-commit: false   # 수동 커밋
      properties:
        spring.json.trusted.packages: "*"
    
    # Listener 설정
    listener:
      ack-mode: manual  # 수동 ACK
```

## Producer (생성자)

### KafkaTemplate 사용

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class UserEventProducer {
    
    private final KafkaTemplate<String, UserEvent> kafkaTemplate;
    
    private static final String TOPIC = "user-events";
    
    // 메시지 전송
    public void sendUserCreatedEvent(User user) {
        UserEvent event = UserEvent.builder()
                .eventType("USER_CREATED")
                .userId(user.getId())
                .userName(user.getName())
                .email(user.getEmail())
                .timestamp(LocalDateTime.now())
                .build();
        
        kafkaTemplate.send(TOPIC, user.getId().toString(), event);
        log.info("Sent user created event: {}", event);
    }
    
    // 콜백 사용
    public void sendUserUpdatedEvent(User user) {
        UserEvent event = UserEvent.builder()
                .eventType("USER_UPDATED")
                .userId(user.getId())
                .userName(user.getName())
                .email(user.getEmail())
                .timestamp(LocalDateTime.now())
                .build();
        
        CompletableFuture<SendResult<String, UserEvent>> future = 
            kafkaTemplate.send(TOPIC, user.getId().toString(), event);
        
        future.whenComplete((result, ex) -> {
            if (ex == null) {
                log.info("Sent message=[{}] with offset=[{}]", 
                    event, result.getRecordMetadata().offset());
            } else {
                log.error("Unable to send message=[{}]", event, ex);
            }
        });
    }
    
    // 파티션 지정
    public void sendToPartition(User user, int partition) {
        UserEvent event = UserEvent.from(user);
        kafkaTemplate.send(TOPIC, partition, user.getId().toString(), event);
    }
}
```

### Event DTO

```java
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserEvent {
    private String eventType;
    private Long userId;
    private String userName;
    private String email;
    private LocalDateTime timestamp;
    
    public static UserEvent from(User user) {
        return UserEvent.builder()
                .userId(user.getId())
                .userName(user.getName())
                .email(user.getEmail())
                .timestamp(LocalDateTime.now())
                .build();
    }
}
```

## Consumer (소비자)

### @KafkaListener

```java
@Component
@Slf4j
public class UserEventConsumer {
    
    // 기본 리스너
    @KafkaListener(topics = "user-events", groupId = "user-group")
    public void consume(UserEvent event) {
        log.info("Consumed event: {}", event);
        // 이벤트 처리 로직
    }
    
    // 메타데이터 함께 받기
    @KafkaListener(topics = "user-events", groupId = "user-group")
    public void consumeWithMetadata(
            @Payload UserEvent event,
            @Header(KafkaHeaders.RECEIVED_TOPIC) String topic,
            @Header(KafkaHeaders.RECEIVED_PARTITION) int partition,
            @Header(KafkaHeaders.OFFSET) long offset) {
        
        log.info("Received message from topic: {}, partition: {}, offset: {}", 
            topic, partition, offset);
        log.info("Event: {}", event);
    }
    
    // 수동 ACK
    @KafkaListener(topics = "user-events", groupId = "user-group")
    public void consumeManualAck(UserEvent event, Acknowledgment ack) {
        try {
            log.info("Processing event: {}", event);
            // 이벤트 처리
            processEvent(event);
            // 처리 성공 시 ACK
            ack.acknowledge();
        } catch (Exception e) {
            log.error("Failed to process event", e);
            // 실패 시 재시도 또는 DLQ로 전송
        }
    }
    
    private void processEvent(UserEvent event) {
        // 실제 처리 로직
    }
}
```

### 여러 Topic 구독

```java
@Component
@Slf4j
public class MultiTopicConsumer {
    
    @KafkaListener(topics = {"user-events", "order-events"}, groupId = "multi-group")
    public void consume(ConsumerRecord<String, String> record) {
        log.info("Topic: {}, Key: {}, Value: {}", 
            record.topic(), record.key(), record.value());
    }
}
```

## Configuration

### Producer Config

```java
@Configuration
public class KafkaProducerConfig {
    
    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;
    
    @Bean
    public ProducerFactory<String, UserEvent> producerFactory() {
        Map<String, Object> config = new HashMap<>();
        config.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        config.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        config.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, JsonSerializer.class);
        config.put(ProducerConfig.ACKS_CONFIG, "all");
        config.put(ProducerConfig.RETRIES_CONFIG, 3);
        config.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
        
        return new DefaultKafkaProducerFactory<>(config);
    }
    
    @Bean
    public KafkaTemplate<String, UserEvent> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }
}
```

### Consumer Config

```java
@Configuration
public class KafkaConsumerConfig {
    
    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;
    
    @Bean
    public ConsumerFactory<String, UserEvent> consumerFactory() {
        Map<String, Object> config = new HashMap<>();
        config.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        config.put(ConsumerConfig.GROUP_ID_CONFIG, "user-group");
        config.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        config.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, JsonDeserializer.class);
        config.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        config.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);
        config.put(JsonDeserializer.TRUSTED_PACKAGES, "*");
        
        return new DefaultKafkaConsumerFactory<>(
            config,
            new StringDeserializer(),
            new JsonDeserializer<>(UserEvent.class, false)
        );
    }
    
    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, UserEvent> kafkaListenerContainerFactory() {
        ConcurrentKafkaListenerContainerFactory<String, UserEvent> factory = 
            new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory());
        factory.getContainerProperties().setAckMode(ContainerProperties.AckMode.MANUAL);
        return factory;
    }
}
```

## 에러 처리

### ErrorHandler 설정

```java
@Configuration
public class KafkaErrorHandlingConfig {
    
    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, UserEvent> kafkaListenerContainerFactory(
            ConsumerFactory<String, UserEvent> consumerFactory) {
        
        ConcurrentKafkaListenerContainerFactory<String, UserEvent> factory = 
            new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory);
        
        // 에러 핸들러 설정
        factory.setCommonErrorHandler(new DefaultErrorHandler(
            new DeadLetterPublishingRecoverer(kafkaTemplate(),
                (record, ex) -> new TopicPartition("user-events-dlt", record.partition())),
            new FixedBackOff(1000L, 3)  // 1초 간격으로 3회 재시도
        ));
        
        return factory;
    }
    
    @Bean
    public KafkaTemplate<String, UserEvent> kafkaTemplate() {
        // Producer 설정
        return new KafkaTemplate<>(producerFactory());
    }
}
```

### Dead Letter Topic

```java
@Component
@Slf4j
public class DeadLetterTopicConsumer {
    
    @KafkaListener(topics = "user-events-dlt", groupId = "dlt-group")
    public void consumeDeadLetter(
            ConsumerRecord<String, UserEvent> record,
            @Header(KafkaHeaders.EXCEPTION_MESSAGE) String exceptionMessage) {
        
        log.error("Dead letter received - Key: {}, Value: {}, Error: {}", 
            record.key(), record.value(), exceptionMessage);
        
        // 실패한 메시지 저장 또는 알림
    }
}
```

## 실전 예제

### 사용자 서비스

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class UserService {
    
    private final UserRepository userRepository;
    private final UserEventProducer eventProducer;
    
    @Transactional
    public UserResponse createUser(UserCreateRequest request) {
        // 사용자 생성
        User user = User.create(request);
        User savedUser = userRepository.save(user);
        
        // 이벤트 발행
        eventProducer.sendUserCreatedEvent(savedUser);
        
        return UserResponse.from(savedUser);
    }
    
    @Transactional
    public UserResponse updateUser(Long id, UserUpdateRequest request) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id));
        
        user.update(request);
        
        // 이벤트 발행
        eventProducer.sendUserUpdatedEvent(user);
        
        return UserResponse.from(user);
    }
}
```

### 이메일 서비스 (Consumer)

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class EmailEventConsumer {
    
    private final EmailService emailService;
    
    @KafkaListener(topics = "user-events", groupId = "email-group")
    public void handleUserEvent(UserEvent event, Acknowledgment ack) {
        try {
            log.info("Processing user event: {}", event);
            
            switch (event.getEventType()) {
                case "USER_CREATED":
                    emailService.sendWelcomeEmail(event.getEmail(), event.getUserName());
                    break;
                case "USER_UPDATED":
                    emailService.sendProfileUpdateEmail(event.getEmail());
                    break;
                case "USER_DELETED":
                    emailService.sendGoodbyeEmail(event.getEmail());
                    break;
            }
            
            ack.acknowledge();
            log.info("Email sent successfully for event: {}", event.getEventType());
            
        } catch (Exception e) {
            log.error("Failed to send email for event: {}", event, e);
            // 실패 시 재시도 또는 DLQ로 전송
        }
    }
}
```

## 트랜잭션

### 트랜잭션 설정

```yaml
spring:
  kafka:
    producer:
      transaction-id-prefix: tx-
      acks: all
```

### 트랜잭션 사용

```java
@Service
@RequiredArgsConstructor
public class TransactionalProducer {
    
    private final KafkaTemplate<String, UserEvent> kafkaTemplate;
    
    public void sendInTransaction(List<UserEvent> events) {
        kafkaTemplate.executeInTransaction(operations -> {
            events.forEach(event -> 
                operations.send("user-events", event.getUserId().toString(), event)
            );
            return true;
        });
    }
}
```

## 배치 처리

### Batch Listener

```java
@Component
@Slf4j
public class BatchConsumer {
    
    @KafkaListener(topics = "user-events", groupId = "batch-group")
    public void consumeBatch(List<UserEvent> events) {
        log.info("Received {} events", events.size());
        
        // 배치 처리
        events.forEach(event -> {
            log.info("Processing event: {}", event);
        });
    }
}
```

### 배치 설정

```yaml
spring:
  kafka:
    consumer:
      max-poll-records: 100  # 한 번에 가져올 최대 레코드 수
    listener:
      type: batch  # 배치 모드
```

## 모니터링

### Actuator 설정

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,metrics,prometheus
  metrics:
    tags:
      application: ${spring.application.name}
```

### 메트릭 확인

```
# Producer 메트릭
kafka.producer.record-send-total
kafka.producer.record-error-total

# Consumer 메트릭
kafka.consumer.records-consumed-total
kafka.consumer.fetch-manager-records-lag
```

## 테스트

### EmbeddedKafka 사용

```java
@SpringBootTest
@EmbeddedKafka(
    partitions = 1,
    topics = {"user-events"},
    brokerProperties = {
        "listeners=PLAINTEXT://localhost:9093",
        "port=9093"
    }
)
class UserEventProducerTest {
    
    @Autowired
    private UserEventProducer producer;
    
    @Autowired
    private KafkaTemplate<String, UserEvent> kafkaTemplate;
    
    @Test
    void sendUserCreatedEventTest() {
        // Given
        User user = User.builder()
                .id(1L)
                .name("홍길동")
                .email("hong@example.com")
                .build();
        
        // When
        producer.sendUserCreatedEvent(user);
        
        // Then
        // Consumer에서 메시지 수신 확인
    }
}
```

## 실전 팁

### 1. 멱등성 보장

```yaml
spring:
  kafka:
    producer:
      enable-idempotence: true  # 중복 방지
      acks: all
      retries: 3
```

### 2. 순서 보장

```java
// 같은 파티션으로 전송
String key = userId.toString();  // 동일한 키는 같은 파티션
kafkaTemplate.send(TOPIC, key, event);
```

### 3. 커밋 전략

```yaml
spring:
  kafka:
    consumer:
      enable-auto-commit: false  # 수동 커밋
    listener:
      ack-mode: manual  # 처리 후 ACK
```

### 4. Consumer Lag 모니터링

```java
@Component
@Slf4j
public class KafkaHealthIndicator implements HealthIndicator {
    
    @Autowired
    private KafkaListenerEndpointRegistry registry;
    
    @Override
    public Health health() {
        // Consumer lag 확인
        // lag이 크면 DOWN 반환
        return Health.up().build();
    }
}
```

### 5. 재시도 정책

```java
@Configuration
public class KafkaErrorConfig {
    
    @Bean
    public DefaultErrorHandler errorHandler() {
        // 지수 백오프: 1초, 2초, 4초
        ExponentialBackOff backOff = new ExponentialBackOff(1000, 2);
        backOff.setMaxElapsedTime(10000);  // 최대 10초
        
        return new DefaultErrorHandler(backOff);
    }
}
```

## 다음 단계

Kafka를 배웠습니다. 이제 외부 API 통합을 알아봅시다.

👉 [다음: 외부 API 통합](18-external-api.md)

## 참고 자료

- [Apache Kafka](https://kafka.apache.org/)
- [Spring for Apache Kafka](https://spring.io/projects/spring-kafka)
- [Kafka Documentation](https://kafka.apache.org/documentation/)
