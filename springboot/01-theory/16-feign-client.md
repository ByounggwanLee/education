# Feign Client

Spring Cloud OpenFeign을 사용하여 선언적 HTTP 클라이언트를 구현하는 방법을 알아봅니다.

## Feign이란?

**Feign:** Netflix에서 개발한 선언적 웹 서비스 클라이언트

### 장점

- ✅ 간결한 코드 (인터페이스만 작성)
- ✅ RestTemplate 대체
- ✅ Spring MVC 어노테이션 지원
- ✅ 로드 밸런싱 통합
- ✅ 에러 처리 자동화

### RestTemplate vs Feign

```java
// RestTemplate (복잡)
@Service
@RequiredArgsConstructor
public class UserService {
    private final RestTemplate restTemplate;
    
    public UserResponse getUser(Long id) {
        String url = "http://user-service/api/v1/users/" + id;
        return restTemplate.getForObject(url, UserResponse.class);
    }
}

// Feign (간결)
@FeignClient(name = "user-service")
public interface UserClient {
    
    @GetMapping("/api/v1/users/{id}")
    UserResponse getUser(@PathVariable Long id);
}
```

## 의존성 추가

### Maven

```xml
<!-- Spring Cloud 버전 관리 -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>2023.0.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <!-- Feign Client -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-openfeign</artifactId>
    </dependency>
    
    <!-- Load Balancer (선택) -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-loadbalancer</artifactId>
    </dependency>
</dependencies>
```

### Gradle

```gradle
ext {
    set('springCloudVersion', "2023.0.0")
}

dependencies {
    implementation 'org.springframework.cloud:spring-cloud-starter-openfeign'
    implementation 'org.springframework.cloud:spring-cloud-starter-loadbalancer'
}

dependencyManagement {
    imports {
        mavenBom "org.springframework.cloud:spring-cloud-dependencies:${springCloudVersion}"
    }
}
```

## 기본 설정

### Application 클래스

```java
@EnableFeignClients  // Feign 활성화
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### application.yml

```yaml
spring:
  cloud:
    openfeign:
      client:
        config:
          default:
            connectTimeout: 5000      # 연결 타임아웃 (ms)
            readTimeout: 5000         # 읽기 타임아웃 (ms)
            loggerLevel: FULL         # 로그 레벨
```

## Feign Client 작성

### 기본 클라이언트

```java
@FeignClient(name = "user-service", url = "http://localhost:8081")
public interface UserClient {
    
    // GET 요청
    @GetMapping("/api/v1/users/{id}")
    UserResponse getUser(@PathVariable Long id);
    
    // 목록 조회
    @GetMapping("/api/v1/users")
    List<UserResponse> getUsers();
    
    // POST 요청
    @PostMapping("/api/v1/users")
    UserResponse createUser(@RequestBody UserCreateRequest request);
    
    // PUT 요청
    @PutMapping("/api/v1/users/{id}")
    UserResponse updateUser(@PathVariable Long id, @RequestBody UserUpdateRequest request);
    
    // DELETE 요청
    @DeleteMapping("/api/v1/users/{id}")
    void deleteUser(@PathVariable Long id);
}
```

### 쿼리 파라미터

```java
@FeignClient(name = "user-service")
public interface UserClient {
    
    // 단일 파라미터
    @GetMapping("/api/v1/users/search")
    List<UserResponse> searchUsers(@RequestParam String name);
    
    // 다중 파라미터
    @GetMapping("/api/v1/users/search")
    List<UserResponse> searchUsers(
            @RequestParam(required = false) String name,
            @RequestParam(required = false) String email,
            @RequestParam(required = false) UserStatus status
    );
    
    // Map으로 전달
    @GetMapping("/api/v1/users/search")
    List<UserResponse> searchUsers(@SpringQueryMap UserSearchCondition condition);
}
```

### 헤더 추가

```java
@FeignClient(name = "user-service")
public interface UserClient {
    
    // 고정 헤더
    @GetMapping(value = "/api/v1/users/{id}", 
                headers = "X-API-Version=1")
    UserResponse getUser(@PathVariable Long id);
    
    // 동적 헤더
    @GetMapping("/api/v1/users/{id}")
    UserResponse getUser(
            @PathVariable Long id,
            @RequestHeader("Authorization") String token
    );
    
    // 여러 헤더
    @GetMapping("/api/v1/users/{id}")
    UserResponse getUser(
            @PathVariable Long id,
            @RequestHeader Map<String, String> headers
    );
}
```

## 설정 커스터마이징

### Client별 설정

```java
@FeignClient(
    name = "user-service",
    url = "${user-service.url}",
    configuration = UserClientConfig.class
)
public interface UserClient {
    // ...
}
```

### Configuration 클래스

```java
@Configuration
public class UserClientConfig {
    
    // 로거 설정
    @Bean
    Logger.Level feignLoggerLevel() {
        return Logger.Level.FULL;
    }
    
    // 에러 디코더
    @Bean
    public ErrorDecoder errorDecoder() {
        return new CustomErrorDecoder();
    }
    
    // 요청 인터셉터
    @Bean
    public RequestInterceptor requestInterceptor() {
        return template -> {
            template.header("X-Custom-Header", "value");
        };
    }
    
    // 재시도 정책
    @Bean
    public Retryer retryer() {
        return new Retryer.Default(100, 1000, 3);  // 최대 3회 재시도
    }
}
```

## 에러 처리

### ErrorDecoder 구현

```java
@Slf4j
public class CustomErrorDecoder implements ErrorDecoder {
    
    private final ErrorDecoder defaultDecoder = new Default();
    
    @Override
    public Exception decode(String methodKey, Response response) {
        log.error("Feign error - method: {}, status: {}", methodKey, response.status());
        
        switch (response.status()) {
            case 400:
                return new BadRequestException("잘못된 요청입니다");
            case 401:
                return new UnauthorizedException("인증이 필요합니다");
            case 404:
                return new NotFoundException("리소스를 찾을 수 없습니다");
            case 500:
                return new InternalServerErrorException("서버 오류가 발생했습니다");
            default:
                return defaultDecoder.decode(methodKey, response);
        }
    }
}
```

### FallbackFactory

```java
@FeignClient(
    name = "user-service",
    fallbackFactory = UserClientFallbackFactory.class
)
public interface UserClient {
    @GetMapping("/api/v1/users/{id}")
    UserResponse getUser(@PathVariable Long id);
}

@Component
@Slf4j
public class UserClientFallbackFactory implements FallbackFactory<UserClient> {
    
    @Override
    public UserClient create(Throwable cause) {
        return new UserClient() {
            @Override
            public UserResponse getUser(Long id) {
                log.error("Failed to get user: {}", id, cause);
                // 기본값 반환
                return UserResponse.builder()
                        .id(id)
                        .name("Unknown")
                        .build();
            }
        };
    }
}
```

## 인터셉터

### JWT 토큰 자동 추가

```java
@Component
public class FeignClientInterceptor implements RequestInterceptor {
    
    @Override
    public void apply(RequestTemplate template) {
        // 현재 요청에서 토큰 가져오기
        ServletRequestAttributes attributes = 
            (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        
        if (attributes != null) {
            HttpServletRequest request = attributes.getRequest();
            String token = request.getHeader("Authorization");
            
            if (token != null) {
                template.header("Authorization", token);
            }
        }
    }
}
```

### 설정 적용

```yaml
spring:
  cloud:
    openfeign:
      client:
        config:
          default:
            request-interceptors:
              - com.example.config.FeignClientInterceptor
```

## 로드 밸런싱

### 서비스 디스커버리 (Eureka)

```java
@FeignClient(name = "user-service")  // URL 없이 서비스명만
public interface UserClient {
    @GetMapping("/api/v1/users/{id}")
    UserResponse getUser(@PathVariable Long id);
}
```

### 직접 URL 목록 지정

```yaml
user-service:
  ribbon:
    listOfServers: localhost:8081,localhost:8082,localhost:8083
```

## 파일 업로드

### MultipartFile 전송

```java
@FeignClient(name = "file-service")
public interface FileClient {
    
    @PostMapping(value = "/api/v1/files", 
                 consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    FileResponse uploadFile(@RequestPart("file") MultipartFile file,
                           @RequestPart("metadata") FileMetadata metadata);
}
```

### Configuration

```java
@Bean
public Encoder feignFormEncoder() {
    return new SpringFormEncoder(new SpringEncoder(messageConverters()));
}
```

## 실전 예제

### User Service Client

```java
@FeignClient(
    name = "user-service",
    url = "${user-service.url}",
    configuration = UserClientConfig.class,
    fallbackFactory = UserClientFallbackFactory.class
)
public interface UserClient {
    
    @GetMapping("/api/v1/users/{id}")
    UserResponse getUser(@PathVariable Long id);
    
    @GetMapping("/api/v1/users")
    Page<UserResponse> getUsers(@SpringQueryMap Pageable pageable);
    
    @PostMapping("/api/v1/users")
    UserResponse createUser(@RequestBody UserCreateRequest request);
    
    @PutMapping("/api/v1/users/{id}")
    UserResponse updateUser(@PathVariable Long id, 
                           @RequestBody UserUpdateRequest request);
    
    @DeleteMapping("/api/v1/users/{id}")
    void deleteUser(@PathVariable Long id);
}
```

### Service에서 사용

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class OrderService {
    
    private final UserClient userClient;
    private final OrderRepository orderRepository;
    
    public OrderResponse createOrder(OrderCreateRequest request) {
        // Feign Client로 사용자 정보 조회
        UserResponse user = userClient.getUser(request.getUserId());
        log.info("Retrieved user: {}", user.getName());
        
        // 주문 생성
        Order order = Order.builder()
                .userId(user.getId())
                .userName(user.getName())
                .items(request.getItems())
                .build();
        
        Order savedOrder = orderRepository.save(order);
        return OrderResponse.from(savedOrder);
    }
}
```

## 로깅

### 로그 레벨 설정

```yaml
logging:
  level:
    com.example.client: DEBUG  # Feign Client 로그
    
spring:
  cloud:
    openfeign:
      client:
        config:
          user-service:
            loggerLevel: FULL  # NONE, BASIC, HEADERS, FULL
```

### 로그 출력

```
2025-11-22 10:30:00 DEBUG [user-service#getUser] ---> GET http://localhost:8081/api/v1/users/1 HTTP/1.1
2025-11-22 10:30:00 DEBUG [user-service#getUser] Authorization: Bearer eyJhbGc...
2025-11-22 10:30:00 DEBUG [user-service#getUser] ---> END HTTP (0-byte body)
2025-11-22 10:30:00 DEBUG [user-service#getUser] <--- HTTP/1.1 200 (45ms)
2025-11-22 10:30:00 DEBUG [user-service#getUser] content-type: application/json
2025-11-22 10:30:00 DEBUG [user-service#getUser] {"id":1,"name":"홍길동","email":"hong@example.com"}
2025-11-22 10:30:00 DEBUG [user-service#getUser] <--- END HTTP (65-byte body)
```

## 타임아웃

### 전역 설정

```yaml
spring:
  cloud:
    openfeign:
      client:
        config:
          default:
            connectTimeout: 5000
            readTimeout: 10000
```

### Client별 설정

```yaml
spring:
  cloud:
    openfeign:
      client:
        config:
          user-service:
            connectTimeout: 3000
            readTimeout: 5000
          order-service:
            connectTimeout: 5000
            readTimeout: 10000
```

## 재시도

### Retryer 설정

```java
@Bean
public Retryer retryer() {
    return new Retryer.Default(
        100,   // 시작 간격 (ms)
        1000,  // 최대 간격 (ms)
        3      // 최대 재시도 횟수
    );
}
```

### 재시도 비활성화

```java
@Bean
public Retryer retryer() {
    return Retryer.NEVER_RETRY;
}
```

## 테스트

### MockServer 사용

```java
@SpringBootTest
@AutoConfigureMockMvc
class UserClientTest {
    
    @Autowired
    private UserClient userClient;
    
    private MockWebServer mockServer;
    
    @BeforeEach
    void setUp() throws IOException {
        mockServer = new MockWebServer();
        mockServer.start();
    }
    
    @AfterEach
    void tearDown() throws IOException {
        mockServer.shutdown();
    }
    
    @Test
    void getUserTest() {
        // Mock 응답 설정
        mockServer.enqueue(new MockResponse()
                .setResponseCode(200)
                .setBody("{\"id\":1,\"name\":\"홍길동\"}")
                .addHeader("Content-Type", "application/json"));
        
        // 테스트
        UserResponse user = userClient.getUser(1L);
        
        assertThat(user.getId()).isEqualTo(1L);
        assertThat(user.getName()).isEqualTo("홍길동");
    }
}
```

## 실전 팁

### 1. 공통 Configuration

```java
@Configuration
public class FeignCommonConfig {
    
    @Bean
    public RequestInterceptor requestInterceptor() {
        return template -> {
            template.header("User-Agent", "My-Service");
            template.header("Accept", "application/json");
        };
    }
    
    @Bean
    public ErrorDecoder errorDecoder() {
        return new CustomErrorDecoder();
    }
    
    @Bean
    public Logger.Level feignLoggerLevel() {
        return Logger.Level.BASIC;
    }
}
```

### 2. 예외 처리

```java
@Slf4j
@Service
@RequiredArgsConstructor
public class UserService {
    
    private final UserClient userClient;
    
    public UserResponse getUser(Long id) {
        try {
            return userClient.getUser(id);
        } catch (FeignException.NotFound e) {
            log.warn("User not found: {}", id);
            throw new UserNotFoundException(id);
        } catch (FeignException e) {
            log.error("Feign error", e);
            throw new ExternalServiceException("사용자 서비스 오류");
        }
    }
}
```

### 3. 응답 캐싱

```java
@Configuration
@EnableCaching
public class CacheConfig {
    
    @Bean
    public CacheManager cacheManager() {
        return new ConcurrentMapCacheManager("users");
    }
}

@Service
public class UserService {
    
    @Cacheable(value = "users", key = "#id")
    public UserResponse getUser(Long id) {
        return userClient.getUser(id);
    }
}
```

### 4. Circuit Breaker (Resilience4j)

```java
@CircuitBreaker(name = "user-service", fallbackMethod = "getUserFallback")
public UserResponse getUser(Long id) {
    return userClient.getUser(id);
}

private UserResponse getUserFallback(Long id, Exception e) {
    log.error("Circuit breaker fallback for user: {}", id, e);
    return UserResponse.builder()
            .id(id)
            .name("Unknown")
            .build();
}
```

## 다음 단계

Feign Client를 배웠습니다. 이제 Kafka를 알아봅시다.

👉 [다음: Kafka](17-kafka.md)

## 참고 자료

- [Spring Cloud OpenFeign](https://spring.io/projects/spring-cloud-openfeign)
- [Feign GitHub](https://github.com/OpenFeign/feign)
- [Netflix Feign](https://netflixtechblog.com/introducing-feign-declarative-rest-client-8e9d0e2e8e0d)
