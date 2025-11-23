# Configuration

Spring Boot의 다양한 설정 방법을 알아봅니다.

## @Configuration

### Configuration 클래스

```java
@Configuration
public class AppConfig {
    
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
    
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
    
    @Bean
    public ObjectMapper objectMapper() {
        ObjectMapper mapper = new ObjectMapper();
        mapper.registerModule(new JavaTimeModule());
        mapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
        return mapper;
    }
}
```

### @Bean

```java
@Configuration
public class DatabaseConfig {
    
    // 기본 빈
    @Bean
    public DataSource dataSource() {
        return DataSourceBuilder.create()
                .url("jdbc:mysql://localhost:3306/mydb")
                .username("root")
                .password("password")
                .build();
    }
    
    // 빈 이름 지정
    @Bean(name = "customDataSource")
    public DataSource customDataSource() {
        // ...
    }
    
    // 초기화/소멸 메서드
    @Bean(initMethod = "init", destroyMethod = "cleanup")
    public MyService myService() {
        return new MyService();
    }
}
```

## application.yml

### 기본 구조

```yaml
# 서버 설정
server:
  port: 8080
  servlet:
    context-path: /api
    encoding:
      charset: UTF-8
      enabled: true
      force: true

# 애플리케이션 설정
spring:
  application:
    name: my-application
  
  # 데이터소스
  datasource:
    url: jdbc:mysql://localhost:3306/mydb
    username: root
    password: password
    driver-class-name: com.mysql.cj.jdbc.Driver
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      connection-timeout: 30000
  
  # JPA
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
    properties:
      hibernate:
        dialect: org.hibernate.dialect.MySQL8Dialect
        format_sql: true
        use_sql_comments: true
  
  # Jackson
  jackson:
    serialization:
      write-dates-as-timestamps: false
    time-zone: Asia/Seoul
    default-property-inclusion: non_null

# 로깅
logging:
  level:
    root: INFO
    com.example: DEBUG
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} - %msg%n"
  file:
    name: logs/application.log
```

### 프로파일별 설정

```yaml
# application.yml (공통)
spring:
  application:
    name: my-application
  
  jpa:
    hibernate:
      ddl-auto: validate

---
# application-local.yml (로컬)
spring:
  config:
    activate:
      on-profile: local
  
  datasource:
    url: jdbc:h2:mem:testdb
    username: sa
    password:
  
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true
  
  h2:
    console:
      enabled: true

logging:
  level:
    com.example: DEBUG

---
# application-dev.yml (개발)
spring:
  config:
    activate:
      on-profile: dev
  
  datasource:
    url: jdbc:mysql://dev-server:3306/mydb
    username: dev_user
    password: ${DB_PASSWORD}
  
  jpa:
    show-sql: true

logging:
  level:
    com.example: DEBUG

---
# application-prod.yml (운영)
spring:
  config:
    activate:
      on-profile: prod
  
  datasource:
    url: jdbc:mysql://prod-server:3306/mydb
    username: prod_user
    password: ${DB_PASSWORD}
  
  jpa:
    show-sql: false

logging:
  level:
    root: WARN
    com.example: INFO
```

## @ConfigurationProperties

### Properties 클래스

```java
@ConfigurationProperties(prefix = "app")
@Validated
@Getter
@Setter
public class AppProperties {
    
    @NotBlank
    private String name;
    
    @NotBlank
    private String version;
    
    private Security security = new Security();
    private Database database = new Database();
    
    @Getter
    @Setter
    public static class Security {
        @NotBlank
        private String jwtSecret;
        
        @Min(3600000)
        private long jwtExpiration;
        
        private List<String> allowedOrigins = new ArrayList<>();
    }
    
    @Getter
    @Setter
    public static class Database {
        @Min(1)
        private int maxPoolSize = 10;
        
        @Min(0)
        private int minIdle = 5;
        
        @Min(1000)
        private long connectionTimeout = 30000;
    }
}
```

### application.yml

```yaml
app:
  name: My Application
  version: 1.0.0
  security:
    jwt-secret: ${JWT_SECRET}
    jwt-expiration: 86400000
    allowed-origins:
      - http://localhost:3000
      - https://example.com
  database:
    max-pool-size: 20
    min-idle: 10
    connection-timeout: 30000
```

### 활성화

```java
@SpringBootApplication
@EnableConfigurationProperties(AppProperties.class)
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### 사용

```java
@Service
@RequiredArgsConstructor
public class MyService {
    
    private final AppProperties appProperties;
    
    public void printConfig() {
        log.info("App Name: {}", appProperties.getName());
        log.info("JWT Secret: {}", appProperties.getSecurity().getJwtSecret());
        log.info("Max Pool Size: {}", appProperties.getDatabase().getMaxPoolSize());
    }
}
```

## @Value

### 기본 사용

```java
@Component
public class AppConfig {
    
    @Value("${app.name}")
    private String appName;
    
    @Value("${app.version:1.0.0}")  // 기본값
    private String version;
    
    @Value("${server.port}")
    private int port;
    
    @Value("${app.enabled:true}")
    private boolean enabled;
    
    @Value("${app.allowed-origins}")
    private List<String> allowedOrigins;
    
    // SpEL (Spring Expression Language)
    @Value("#{systemProperties['user.home']}")
    private String userHome;
    
    @Value("#{T(java.lang.Math).random() * 100}")
    private double randomNumber;
}
```

## 환경 변수

### 환경 변수 사용

```yaml
spring:
  datasource:
    url: ${DATABASE_URL:jdbc:mysql://localhost:3306/mydb}
    username: ${DATABASE_USERNAME:root}
    password: ${DATABASE_PASSWORD}

jwt:
  secret: ${JWT_SECRET}
  expiration: ${JWT_EXPIRATION:86400000}
```

### 시스템 속성

```bash
# 실행 시 설정
java -jar app.jar --spring.profiles.active=prod --server.port=8081

# 환경 변수
export DATABASE_URL=jdbc:mysql://prod-server:3306/mydb
export DATABASE_USERNAME=prod_user
export DATABASE_PASSWORD=secret
java -jar app.jar
```

## 프로파일

### 프로파일 활성화

```yaml
# application.yml
spring:
  profiles:
    active: local
```

```bash
# 실행 시 설정
java -jar app.jar --spring.profiles.active=prod

# 환경 변수
export SPRING_PROFILES_ACTIVE=prod
java -jar app.jar

# IDE 설정 (IntelliJ)
Run > Edit Configurations > Active profiles: prod
```

### 프로파일별 Bean

```java
@Configuration
public class DataSourceConfig {
    
    @Bean
    @Profile("local")
    public DataSource localDataSource() {
        return DataSourceBuilder.create()
                .url("jdbc:h2:mem:testdb")
                .build();
    }
    
    @Bean
    @Profile("dev")
    public DataSource devDataSource() {
        return DataSourceBuilder.create()
                .url("jdbc:mysql://dev-server:3306/mydb")
                .build();
    }
    
    @Bean
    @Profile("prod")
    public DataSource prodDataSource() {
        return DataSourceBuilder.create()
                .url("jdbc:mysql://prod-server:3306/mydb")
                .build();
    }
}
```

### @Profile 활용

```java
@Component
@Profile("!prod")  // prod가 아닐 때
public class DebugComponent {
    // 개발 환경에서만 활성화
}

@Component
@Profile({"dev", "staging"})  // dev 또는 staging일 때
public class TestComponent {
    // 테스트 환경에서 활성화
}
```

## 외부 설정 파일

### 커스텀 설정 파일

```java
@Configuration
@PropertySource("classpath:custom.properties")
public class CustomConfig {
    
    @Value("${custom.property}")
    private String customProperty;
}
```

### YAML 파일 로드

```java
@Configuration
@PropertySource(value = "classpath:custom.yml", factory = YamlPropertySourceFactory.class)
public class CustomYamlConfig {
    // ...
}

public class YamlPropertySourceFactory implements PropertySourceFactory {
    
    @Override
    public PropertySource<?> createPropertySource(String name, EncodedResource resource) {
        YamlPropertiesFactoryBean factory = new YamlPropertiesFactoryBean();
        factory.setResources(resource.getResource());
        Properties properties = factory.getObject();
        
        return new PropertiesPropertySource(
            resource.getResource().getFilename(),
            properties
        );
    }
}
```

## Conditional Configuration

### @Conditional

```java
@Configuration
public class ConditionalConfig {
    
    @Bean
    @ConditionalOnProperty(name = "feature.enabled", havingValue = "true")
    public FeatureService featureService() {
        return new FeatureService();
    }
    
    @Bean
    @ConditionalOnMissingBean
    public DefaultService defaultService() {
        return new DefaultService();
    }
    
    @Bean
    @ConditionalOnClass(name = "com.example.SomeClass")
    public SomeService someService() {
        return new SomeService();
    }
}
```

## 실전 예제

### 다중 환경 설정

```yaml
# application.yml
spring:
  application:
    name: my-app
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:local}

app:
  name: My Application
  version: 1.0.0

---
# Local
spring:
  config:
    activate:
      on-profile: local

  datasource:
    url: jdbc:h2:mem:testdb
    username: sa
    password:
  
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true

app:
  api:
    url: http://localhost:8081
  security:
    enabled: false

---
# Development
spring:
  config:
    activate:
      on-profile: dev

  datasource:
    url: jdbc:mysql://dev-db:3306/mydb
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
  
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: true

app:
  api:
    url: https://dev-api.example.com
  security:
    enabled: true
    jwt-secret: ${JWT_SECRET}

---
# Production
spring:
  config:
    activate:
      on-profile: prod

  datasource:
    url: jdbc:mysql://prod-db:3306/mydb
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 20
      minimum-idle: 10
  
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
    properties:
      hibernate:
        jdbc:
          batch_size: 50

app:
  api:
    url: https://api.example.com
  security:
    enabled: true
    jwt-secret: ${JWT_SECRET}

logging:
  level:
    root: WARN
    com.example: INFO
```

## 실전 팁

### 1. 민감 정보 관리

```yaml
# application.yml - 절대 커밋하지 않음
spring:
  datasource:
    password: ${DB_PASSWORD}

jwt:
  secret: ${JWT_SECRET}
```

```bash
# .env 파일 (Git에서 제외)
DB_PASSWORD=secret
JWT_SECRET=my-secret-key
```

### 2. 설정 검증

```java
@ConfigurationProperties(prefix = "app")
@Validated
public class AppProperties {
    
    @NotBlank(message = "앱 이름은 필수입니다")
    private String name;
    
    @Min(value = 1024, message = "포트는 1024 이상이어야 합니다")
    private int port;
    
    @Email(message = "올바른 이메일 형식이 아닙니다")
    private String adminEmail;
}
```

### 3. 프로파일 그룹

```yaml
spring:
  profiles:
    group:
      local: [common, local-db, local-cache]
      dev: [common, dev-db, dev-cache]
      prod: [common, prod-db, prod-cache]
```

### 4. 설정 암호화 (Jasypt)

```xml
<dependency>
    <groupId>com.github.ulisesbocchio</groupId>
    <artifactId>jasypt-spring-boot-starter</artifactId>
    <version>3.0.5</version>
</dependency>
```

```yaml
spring:
  datasource:
    password: ENC(encrypted_password)

jasypt:
  encryptor:
    password: ${JASYPT_PASSWORD}
```

## 다음 단계

Configuration을 배웠습니다. 이제 Interceptor를 알아봅시다.

👉 [다음: Interceptor](22-interceptor.md)

## 참고 자료

- [Spring Boot Configuration](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.external-config)
- [Configuration Properties](https://docs.spring.io/spring-boot/docs/current/reference/html/configuration-metadata.html)
- [Profiles](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.profiles)
