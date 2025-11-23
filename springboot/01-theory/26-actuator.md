# Actuator

Spring Boot Actuator를 사용하여 애플리케이션을 모니터링하고 관리하는 방법을 알아봅니다.

## Actuator란?

**Actuator:** Spring Boot 애플리케이션의 상태와 메트릭을 모니터링하는 도구

### 주요 기능

- ✅ 헬스 체크
- ✅ 메트릭 수집
- ✅ 환경 설정 확인
- ✅ 로깅 레벨 변경
- ✅ HTTP 추적
- ✅ 스레드 덤프

## 의존성 추가

### Maven

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

### Gradle

```gradle
implementation 'org.springframework.boot:spring-boot-starter-actuator'
```

## 기본 설정

### application.yml

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus  # 노출할 엔드포인트
        # include: "*"  # 모든 엔드포인트 노출 (개발 환경)
      base-path: /actuator  # 기본 경로
  
  endpoint:
    health:
      show-details: always  # 상세 정보 표시
      show-components: always
    shutdown:
      enabled: true  # 애플리케이션 종료 엔드포인트
  
  server:
    port: 9090  # Actuator 전용 포트 (선택)
  
  metrics:
    tags:
      application: ${spring.application.name}
```

## 주요 엔드포인트

### Health Check

```
GET /actuator/health
```

**응답:**
```json
{
  "status": "UP",
  "components": {
    "db": {
      "status": "UP",
      "details": {
        "database": "MySQL",
        "validationQuery": "isValid()"
      }
    },
    "diskSpace": {
      "status": "UP",
      "details": {
        "total": 499963174912,
        "free": 123456789012,
        "threshold": 10485760,
        "exists": true
      }
    }
  }
}
```

### Info

```
GET /actuator/info
```

```yaml
# application.yml
info:
  app:
    name: My Application
    version: 1.0.0
    description: Spring Boot Application
```

**응답:**
```json
{
  "app": {
    "name": "My Application",
    "version": "1.0.0",
    "description": "Spring Boot Application"
  }
}
```

### Metrics

```
GET /actuator/metrics
```

**응답:**
```json
{
  "names": [
    "jvm.memory.used",
    "jvm.gc.pause",
    "http.server.requests",
    "logback.events",
    "system.cpu.usage"
  ]
}
```

**특정 메트릭 조회:**
```
GET /actuator/metrics/http.server.requests
```

```json
{
  "name": "http.server.requests",
  "measurements": [
    {
      "statistic": "COUNT",
      "value": 150
    },
    {
      "statistic": "TOTAL_TIME",
      "value": 1.5
    }
  ]
}
```

### Loggers

```
GET /actuator/loggers
GET /actuator/loggers/com.example.service.UserService
```

**로그 레벨 변경:**
```
POST /actuator/loggers/com.example.service.UserService
Content-Type: application/json

{
  "configuredLevel": "DEBUG"
}
```

### Environment

```
GET /actuator/env
GET /actuator/env/server.port
```

## 커스텀 Health Indicator

### 데이터베이스 Health

```java
@Component
public class DatabaseHealthIndicator implements HealthIndicator {
    
    @Autowired
    private DataSource dataSource;
    
    @Override
    public Health health() {
        try (Connection connection = dataSource.getConnection()) {
            if (connection.isValid(1000)) {
                return Health.up()
                        .withDetail("database", "MySQL")
                        .withDetail("validationQuery", "isValid()")
                        .build();
            } else {
                return Health.down()
                        .withDetail("error", "Connection validation failed")
                        .build();
            }
        } catch (Exception e) {
            return Health.down()
                    .withDetail("error", e.getMessage())
                    .build();
        }
    }
}
```

### 외부 API Health

```java
@Component
@RequiredArgsConstructor
public class ExternalApiHealthIndicator implements HealthIndicator {
    
    private final RestTemplate restTemplate;
    private static final String API_URL = "https://api.example.com/health";
    
    @Override
    public Health health() {
        try {
            ResponseEntity<String> response = restTemplate.getForEntity(API_URL, String.class);
            
            if (response.getStatusCode().is2xxSuccessful()) {
                return Health.up()
                        .withDetail("api", API_URL)
                        .withDetail("status", response.getStatusCode())
                        .build();
            } else {
                return Health.down()
                        .withDetail("api", API_URL)
                        .withDetail("status", response.getStatusCode())
                        .build();
            }
        } catch (Exception e) {
            return Health.down()
                    .withDetail("api", API_URL)
                    .withDetail("error", e.getMessage())
                    .build();
        }
    }
}
```

### 디스크 공간 Health

```java
@Component
public class DiskSpaceHealthIndicator implements HealthIndicator {
    
    private static final long THRESHOLD = 10 * 1024 * 1024 * 1024L;  // 10GB
    
    @Override
    public Health health() {
        File file = new File("/");
        long freeSpace = file.getFreeSpace();
        
        if (freeSpace > THRESHOLD) {
            return Health.up()
                    .withDetail("free", freeSpace)
                    .withDetail("threshold", THRESHOLD)
                    .build();
        } else {
            return Health.down()
                    .withDetail("free", freeSpace)
                    .withDetail("threshold", THRESHOLD)
                    .withDetail("warning", "Low disk space")
                    .build();
        }
    }
}
```

## 커스텀 Metrics

### Counter (카운터)

```java
@Service
@RequiredArgsConstructor
public class UserService {
    
    private final MeterRegistry meterRegistry;
    private final UserRepository userRepository;
    
    public UserResponse createUser(UserCreateRequest request) {
        // 사용자 생성 로직
        User user = userRepository.save(User.from(request));
        
        // 메트릭 카운트 증가
        meterRegistry.counter("users.created").increment();
        
        return UserResponse.from(user);
    }
}
```

### Gauge (게이지)

```java
@Component
@RequiredArgsConstructor
public class UserMetrics {
    
    private final UserRepository userRepository;
    private final MeterRegistry meterRegistry;
    
    @PostConstruct
    public void initMetrics() {
        // 활성 사용자 수 게이지
        Gauge.builder("users.active.count", userRepository, repo -> 
                repo.countByStatus(UserStatus.ACTIVE))
                .description("Number of active users")
                .register(meterRegistry);
    }
}
```

### Timer (타이머)

```java
@Service
@RequiredArgsConstructor
public class OrderService {
    
    private final MeterRegistry meterRegistry;
    
    public OrderResponse createOrder(OrderCreateRequest request) {
        Timer.Sample sample = Timer.start(meterRegistry);
        
        try {
            // 주문 생성 로직
            Order order = processOrder(request);
            return OrderResponse.from(order);
        } finally {
            sample.stop(meterRegistry.timer("order.creation.time"));
        }
    }
}
```

### @Timed 어노테이션

```java
@Service
public class UserService {
    
    @Timed(value = "user.service.getUser", description = "Time taken to get user")
    public UserResponse getUser(Long id) {
        // 메서드 실행 시간 자동 측정
        return userRepository.findById(id)
                .map(UserResponse::from)
                .orElseThrow(() -> new UserNotFoundException(id));
    }
}

// TimedAspect 설정 필요
@Configuration
public class MetricsConfig {
    
    @Bean
    public TimedAspect timedAspect(MeterRegistry registry) {
        return new TimedAspect(registry);
    }
}
```

## Info Contributor

### Git 정보

```xml
<!-- Maven -->
<build>
    <plugins>
        <plugin>
            <groupId>pl.project13.maven</groupId>
            <artifactId>git-commit-id-plugin</artifactId>
        </plugin>
    </plugins>
</build>
```

```yaml
management:
  info:
    git:
      mode: full  # simple 또는 full
```

**응답:**
```json
{
  "git": {
    "branch": "main",
    "commit": {
      "id": "abc123",
      "time": "2025-11-22T10:30:00Z"
    }
  }
}
```

### 커스텀 Info

```java
@Component
public class CustomInfoContributor implements InfoContributor {
    
    @Override
    public void contribute(Info.Builder builder) {
        builder.withDetail("custom", Map.of(
            "key1", "value1",
            "key2", "value2"
        ));
    }
}
```

## Prometheus 통합

### 의존성 추가

```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

### 설정

```yaml
management:
  endpoints:
    web:
      exposure:
        include: prometheus
  
  metrics:
    export:
      prometheus:
        enabled: true
```

**메트릭 확인:**
```
GET /actuator/prometheus
```

**Prometheus 설정:**
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'spring-boot'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['localhost:8080']
```

## 보안 설정

### Basic Auth

```yaml
spring:
  security:
    user:
      name: admin
      password: secret

management:
  endpoints:
    web:
      exposure:
        include: "*"
```

### 커스텀 보안

```java
@Configuration
public class ActuatorSecurityConfig {
    
    @Bean
    public SecurityFilterChain actuatorSecurityFilterChain(HttpSecurity http) throws Exception {
        http
            .securityMatcher("/actuator/**")
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health").permitAll()
                .requestMatchers("/actuator/info").permitAll()
                .requestMatchers("/actuator/**").hasRole("ADMIN")
            )
            .httpBasic(Customizer.withDefaults());
        
        return http.build();
    }
}
```

## HTTP Trace

```yaml
management:
  endpoints:
    web:
      exposure:
        include: httptrace
  
  trace:
    http:
      enabled: true
```

```java
@Bean
public HttpTraceRepository httpTraceRepository() {
    return new InMemoryHttpTraceRepository();
}
```

## 실전 예제

### 완전한 모니터링 설정

```yaml
# application-prod.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
      base-path: /actuator
  
  endpoint:
    health:
      show-details: when-authorized
      roles: ADMIN
  
  server:
    port: 9090  # 별도 포트
  
  metrics:
    tags:
      application: ${spring.application.name}
      environment: ${spring.profiles.active}
    export:
      prometheus:
        enabled: true

# 헬스 체크 상세 설정
  health:
    defaults:
      enabled: true
    db:
      enabled: true
    diskspace:
      enabled: true
      threshold: 10GB
```

### 커스텀 메트릭 예제

```java
@Component
@RequiredArgsConstructor
public class ApplicationMetrics {
    
    private final MeterRegistry meterRegistry;
    
    @PostConstruct
    public void init() {
        // 요청 성공/실패 카운터
        Counter.builder("api.requests")
                .tag("result", "success")
                .description("Successful API requests")
                .register(meterRegistry);
        
        Counter.builder("api.requests")
                .tag("result", "failure")
                .description("Failed API requests")
                .register(meterRegistry);
    }
    
    public void recordSuccess() {
        meterRegistry.counter("api.requests", "result", "success").increment();
    }
    
    public void recordFailure() {
        meterRegistry.counter("api.requests", "result", "failure").increment();
    }
}
```

## 실전 팁

### 1. 프로덕션 엔드포인트 제한

```yaml
# application-prod.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus  # 필요한 것만
        exclude: env,beans,mappings  # 민감한 정보 제외
```

### 2. 커스텀 Health 그룹

```yaml
management:
  endpoint:
    health:
      group:
        liveness:
          include: ping
        readiness:
          include: db,redis
```

**사용:**
```
GET /actuator/health/liveness
GET /actuator/health/readiness
```

### 3. 조건부 Actuator

```yaml
management:
  endpoints:
    enabled-by-default: false
  endpoint:
    health:
      enabled: true
    info:
      enabled: true
```

### 4. CORS 설정

```yaml
management:
  endpoints:
    web:
      cors:
        allowed-origins: "https://monitoring.example.com"
        allowed-methods: GET
```

## 다음 단계

Actuator를 배웠습니다. 이제 배포를 알아봅시다.

👉 [다음: 배포](27-deployment.md)

## 참고 자료

- [Spring Boot Actuator](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html)
- [Micrometer](https://micrometer.io/)
- [Prometheus](https://prometheus.io/)
