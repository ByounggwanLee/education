# 외부 API 통합

외부 API를 안전하고 효율적으로 통합하는 방법을 알아봅니다.

## RestTemplate vs WebClient

### RestTemplate (동기)

```java
@Service
@RequiredArgsConstructor
public class RestTemplateService {
    
    private final RestTemplate restTemplate;
    
    public UserResponse getUser(Long id) {
        String url = "https://api.example.com/users/" + id;
        return restTemplate.getForObject(url, UserResponse.class);
    }
}
```

### WebClient (비동기)

```java
@Service
@RequiredArgsConstructor
public class WebClientService {
    
    private final WebClient webClient;
    
    public Mono<UserResponse> getUser(Long id) {
        return webClient.get()
                .uri("/users/{id}", id)
                .retrieve()
                .bodyToMono(UserResponse.class);
    }
}
```

## RestTemplate 설정

### Bean 등록

```java
@Configuration
public class RestTemplateConfig {
    
    @Bean
    public RestTemplate restTemplate() {
        RestTemplate restTemplate = new RestTemplate();
        
        // 타임아웃 설정
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(5000);
        factory.setReadTimeout(5000);
        restTemplate.setRequestFactory(factory);
        
        // 에러 핸들러
        restTemplate.setErrorHandler(new RestTemplateErrorHandler());
        
        // 인터셉터
        restTemplate.setInterceptors(List.of(new RestTemplateInterceptor()));
        
        return restTemplate;
    }
}
```

### 기본 사용법

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class ExternalApiService {
    
    private final RestTemplate restTemplate;
    private static final String BASE_URL = "https://api.example.com";
    
    // GET 요청
    public UserResponse getUser(Long id) {
        String url = BASE_URL + "/users/" + id;
        return restTemplate.getForObject(url, UserResponse.class);
    }
    
    // GET with ResponseEntity
    public ResponseEntity<UserResponse> getUserWithStatus(Long id) {
        String url = BASE_URL + "/users/{id}";
        return restTemplate.getForEntity(url, UserResponse.class, id);
    }
    
    // POST 요청
    public UserResponse createUser(UserCreateRequest request) {
        String url = BASE_URL + "/users";
        return restTemplate.postForObject(url, request, UserResponse.class);
    }
    
    // PUT 요청
    public void updateUser(Long id, UserUpdateRequest request) {
        String url = BASE_URL + "/users/{id}";
        restTemplate.put(url, request, id);
    }
    
    // DELETE 요청
    public void deleteUser(Long id) {
        String url = BASE_URL + "/users/{id}";
        restTemplate.delete(url, id);
    }
    
    // exchange (모든 HTTP 메서드)
    public UserResponse exchangeExample(Long id) {
        String url = BASE_URL + "/users/{id}";
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.setBearerAuth("token");
        
        HttpEntity<Void> entity = new HttpEntity<>(headers);
        
        ResponseEntity<UserResponse> response = restTemplate.exchange(
            url,
            HttpMethod.GET,
            entity,
            UserResponse.class,
            id
        );
        
        return response.getBody();
    }
}
```

### 쿼리 파라미터

```java
public List<UserResponse> searchUsers(String name, Integer age) {
    String url = BASE_URL + "/users/search?name={name}&age={age}";
    
    Map<String, Object> params = new HashMap<>();
    params.put("name", name);
    params.put("age", age);
    
    ResponseEntity<UserResponse[]> response = restTemplate.getForEntity(
        url,
        UserResponse[].class,
        params
    );
    
    return Arrays.asList(response.getBody());
}

// UriComponentsBuilder 사용
public List<UserResponse> searchUsersWithBuilder(String name, Integer age) {
    UriComponents uri = UriComponentsBuilder
            .fromHttpUrl(BASE_URL + "/users/search")
            .queryParam("name", name)
            .queryParam("age", age)
            .build();
    
    ResponseEntity<UserResponse[]> response = restTemplate.getForEntity(
        uri.toUriString(),
        UserResponse[].class
    );
    
    return Arrays.asList(response.getBody());
}
```

## WebClient 설정

### 의존성 추가

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
```

### Bean 등록

```java
@Configuration
public class WebClientConfig {
    
    @Bean
    public WebClient webClient() {
        return WebClient.builder()
                .baseUrl("https://api.example.com")
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .defaultHeader(HttpHeaders.USER_AGENT, "My-Service")
                .filter(ExchangeFilterFunction.ofRequestProcessor(clientRequest -> {
                    log.info("Request: {} {}", clientRequest.method(), clientRequest.url());
                    return Mono.just(clientRequest);
                }))
                .filter(ExchangeFilterFunction.ofResponseProcessor(clientResponse -> {
                    log.info("Response status: {}", clientResponse.statusCode());
                    return Mono.just(clientResponse);
                }))
                .build();
    }
}
```

### 기본 사용법

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class WebClientService {
    
    private final WebClient webClient;
    
    // GET 요청 (비동기)
    public Mono<UserResponse> getUser(Long id) {
        return webClient.get()
                .uri("/users/{id}", id)
                .retrieve()
                .bodyToMono(UserResponse.class);
    }
    
    // GET 요청 (동기)
    public UserResponse getUserSync(Long id) {
        return webClient.get()
                .uri("/users/{id}", id)
                .retrieve()
                .bodyToMono(UserResponse.class)
                .block();  // 블로킹
    }
    
    // POST 요청
    public Mono<UserResponse> createUser(UserCreateRequest request) {
        return webClient.post()
                .uri("/users")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(UserResponse.class);
    }
    
    // PUT 요청
    public Mono<UserResponse> updateUser(Long id, UserUpdateRequest request) {
        return webClient.put()
                .uri("/users/{id}", id)
                .bodyValue(request)
                .retrieve()
                .bodyToMono(UserResponse.class);
    }
    
    // DELETE 요청
    public Mono<Void> deleteUser(Long id) {
        return webClient.delete()
                .uri("/users/{id}", id)
                .retrieve()
                .bodyToMono(Void.class);
    }
    
    // 리스트 조회
    public Flux<UserResponse> getUsers() {
        return webClient.get()
                .uri("/users")
                .retrieve()
                .bodyToFlux(UserResponse.class);
    }
}
```

## 에러 처리

### RestTemplate ErrorHandler

```java
@Slf4j
public class RestTemplateErrorHandler implements ResponseErrorHandler {
    
    @Override
    public boolean hasError(ClientHttpResponse response) throws IOException {
        return response.getStatusCode().isError();
    }
    
    @Override
    public void handleError(ClientHttpResponse response) throws IOException {
        HttpStatus status = (HttpStatus) response.getStatusCode();
        String body = StreamUtils.copyToString(response.getBody(), StandardCharsets.UTF_8);
        
        log.error("External API error - Status: {}, Body: {}", status, body);
        
        switch (status) {
            case BAD_REQUEST:
                throw new ExternalApiBadRequestException(body);
            case UNAUTHORIZED:
                throw new ExternalApiUnauthorizedException();
            case NOT_FOUND:
                throw new ExternalApiNotFoundException();
            case INTERNAL_SERVER_ERROR:
                throw new ExternalApiServerException(body);
            default:
                throw new ExternalApiException("Unknown error: " + status);
        }
    }
}
```

### WebClient 에러 처리

```java
@Service
public class WebClientService {
    
    public Mono<UserResponse> getUser(Long id) {
        return webClient.get()
                .uri("/users/{id}", id)
                .retrieve()
                .onStatus(HttpStatus::is4xxClientError, response -> {
                    return response.bodyToMono(String.class)
                            .flatMap(body -> {
                                log.error("Client error: {}", body);
                                return Mono.error(new ExternalApiClientException(body));
                            });
                })
                .onStatus(HttpStatus::is5xxServerError, response -> {
                    return Mono.error(new ExternalApiServerException());
                })
                .bodyToMono(UserResponse.class)
                .doOnError(error -> log.error("Error calling external API", error));
    }
}
```

## 인터셉터

### RestTemplate Interceptor

```java
@Slf4j
public class RestTemplateInterceptor implements ClientHttpRequestInterceptor {
    
    @Override
    public ClientHttpResponse intercept(
            HttpRequest request,
            byte[] body,
            ClientHttpRequestExecution execution) throws IOException {
        
        // 요청 로깅
        log.info("Request URI: {}", request.getURI());
        log.info("Request Method: {}", request.getMethod());
        log.info("Request Headers: {}", request.getHeaders());
        
        // 요청 시간 측정
        long startTime = System.currentTimeMillis();
        
        // 실제 요청 실행
        ClientHttpResponse response = execution.execute(request, body);
        
        // 응답 시간 측정
        long duration = System.currentTimeMillis() - startTime;
        
        // 응답 로깅
        log.info("Response Status: {}", response.getStatusCode());
        log.info("Response Time: {}ms", duration);
        
        return response;
    }
}
```

### JWT 토큰 자동 추가

```java
@Component
@RequiredArgsConstructor
public class JwtTokenInterceptor implements ClientHttpRequestInterceptor {
    
    private final TokenProvider tokenProvider;
    
    @Override
    public ClientHttpResponse intercept(
            HttpRequest request,
            byte[] body,
            ClientHttpRequestExecution execution) throws IOException {
        
        // JWT 토큰 추가
        String token = tokenProvider.generateToken();
        request.getHeaders().setBearerAuth(token);
        
        return execution.execute(request, body);
    }
}
```

## 재시도

### RestTemplate with Retry

```java
@Configuration
public class RestTemplateRetryConfig {
    
    @Bean
    public RestTemplate restTemplateWithRetry() {
        RestTemplate restTemplate = new RestTemplate();
        
        // 재시도 정책
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory() {
            @Override
            protected void prepareConnection(HttpURLConnection connection, String httpMethod) throws IOException {
                super.prepareConnection(connection, httpMethod);
                // 재시도 설정
            }
        };
        
        restTemplate.setRequestFactory(factory);
        return restTemplate;
    }
}

// Spring Retry 사용
@Service
public class RetryableService {
    
    @Retryable(
        value = {ExternalApiException.class},
        maxAttempts = 3,
        backoff = @Backoff(delay = 1000, multiplier = 2)
    )
    public UserResponse getUser(Long id) {
        return restTemplate.getForObject("/users/{id}", UserResponse.class, id);
    }
}
```

### WebClient with Retry

```java
public Mono<UserResponse> getUserWithRetry(Long id) {
    return webClient.get()
            .uri("/users/{id}", id)
            .retrieve()
            .bodyToMono(UserResponse.class)
            .retryWhen(Retry.backoff(3, Duration.ofSeconds(1))
                    .filter(throwable -> throwable instanceof WebClientException)
                    .onRetryExhaustedThrow((retryBackoffSpec, retrySignal) -> {
                        throw new ExternalApiException("최대 재시도 횟수 초과");
                    }));
}
```

## 타임아웃

### RestTemplate 타임아웃

```java
@Bean
public RestTemplate restTemplate() {
    SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
    factory.setConnectTimeout(5000);  // 연결 타임아웃: 5초
    factory.setReadTimeout(10000);    // 읽기 타임아웃: 10초
    
    return new RestTemplate(factory);
}
```

### WebClient 타임아웃

```java
@Bean
public WebClient webClient() {
    HttpClient httpClient = HttpClient.create()
            .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 5000)
            .responseTimeout(Duration.ofSeconds(10))
            .doOnConnected(conn -> 
                conn.addHandlerLast(new ReadTimeoutHandler(10))
                    .addHandlerLast(new WriteTimeoutHandler(10)));
    
    return WebClient.builder()
            .clientConnector(new ReactorClientHttpConnector(httpClient))
            .build();
}
```

## 캐싱

### Spring Cache 적용

```java
@Service
@EnableCaching
public class CachedExternalApiService {
    
    @Cacheable(value = "users", key = "#id", unless = "#result == null")
    public UserResponse getUser(Long id) {
        return restTemplate.getForObject("/users/{id}", UserResponse.class, id);
    }
    
    @CacheEvict(value = "users", key = "#id")
    public UserResponse updateUser(Long id, UserUpdateRequest request) {
        return restTemplate.patchForObject("/users/{id}", request, UserResponse.class, id);
    }
    
    @CacheEvict(value = "users", allEntries = true)
    public void clearCache() {
        // 전체 캐시 삭제
    }
}
```

## Circuit Breaker

### Resilience4j 설정

```xml
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-spring-boot2</artifactId>
    <version>2.1.0</version>
</dependency>
```

```yaml
resilience4j:
  circuitbreaker:
    instances:
      externalApi:
        registerHealthIndicator: true
        slidingWindowSize: 10
        permittedNumberOfCallsInHalfOpenState: 3
        slidingWindowType: COUNT_BASED
        minimumNumberOfCalls: 5
        waitDurationInOpenState: 10s
        failureRateThreshold: 50
        eventConsumerBufferSize: 10
```

### 사용

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class CircuitBreakerService {
    
    private final RestTemplate restTemplate;
    private final CircuitBreakerRegistry circuitBreakerRegistry;
    
    public UserResponse getUser(Long id) {
        CircuitBreaker circuitBreaker = circuitBreakerRegistry.circuitBreaker("externalApi");
        
        return circuitBreaker.executeSupplier(() -> {
            try {
                return restTemplate.getForObject("/users/{id}", UserResponse.class, id);
            } catch (Exception e) {
                log.error("External API call failed", e);
                throw new ExternalApiException(e);
            }
        });
    }
    
    // Annotation 방식
    @CircuitBreaker(name = "externalApi", fallbackMethod = "getUserFallback")
    public UserResponse getUserWithAnnotation(Long id) {
        return restTemplate.getForObject("/users/{id}", UserResponse.class, id);
    }
    
    private UserResponse getUserFallback(Long id, Exception e) {
        log.error("Circuit breaker fallback for user: {}", id, e);
        return UserResponse.builder()
                .id(id)
                .name("Unknown")
                .build();
    }
}
```

## 실전 팁

### 1. Base URL 환경별 관리

```yaml
# application.yml
external-api:
  base-url: ${EXTERNAL_API_URL:https://api.example.com}
  timeout:
    connect: 5000
    read: 10000

# application-local.yml
external-api:
  base-url: http://localhost:8081

# application-prod.yml
external-api:
  base-url: https://api.production.com
```

### 2. API Key 관리

```java
@Configuration
public class ExternalApiConfig {
    
    @Value("${external-api.api-key}")
    private String apiKey;
    
    @Bean
    public RestTemplate restTemplate() {
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.setInterceptors(List.of(new ClientHttpRequestInterceptor() {
            @Override
            public ClientHttpResponse intercept(
                    HttpRequest request,
                    byte[] body,
                    ClientHttpRequestExecution execution) throws IOException {
                request.getHeaders().set("X-API-Key", apiKey);
                return execution.execute(request, body);
            }
        }));
        return restTemplate;
    }
}
```

### 3. 응답 로깅

```java
@Aspect
@Component
@Slf4j
public class ExternalApiLoggingAspect {
    
    @Around("@annotation(ExternalApiCall)")
    public Object logExternalApiCall(ProceedingJoinPoint joinPoint) throws Throwable {
        long startTime = System.currentTimeMillis();
        
        try {
            Object result = joinPoint.proceed();
            long duration = System.currentTimeMillis() - startTime;
            
            log.info("External API call successful - Method: {}, Duration: {}ms",
                joinPoint.getSignature().getName(), duration);
            
            return result;
        } catch (Exception e) {
            long duration = System.currentTimeMillis() - startTime;
            
            log.error("External API call failed - Method: {}, Duration: {}ms",
                joinPoint.getSignature().getName(), duration, e);
            
            throw e;
        }
    }
}
```

### 4. 모의 서버 (테스트)

```java
@SpringBootTest
@AutoConfigureMockRestServiceServer
class ExternalApiServiceTest {
    
    @Autowired
    private MockRestServiceServer mockServer;
    
    @Autowired
    private ExternalApiService service;
    
    @Test
    void getUserTest() {
        // Mock 응답 설정
        mockServer.expect(requestTo("/users/1"))
                .andExpect(method(HttpMethod.GET))
                .andRespond(withSuccess(
                    "{\"id\":1,\"name\":\"홍길동\"}",
                    MediaType.APPLICATION_JSON));
        
        // 테스트
        UserResponse user = service.getUser(1L);
        
        assertThat(user.getId()).isEqualTo(1L);
        assertThat(user.getName()).isEqualTo("홍길동");
        
        mockServer.verify();
    }
}
```

## 다음 단계

외부 API 통합을 배웠습니다. 이제 보안을 알아봅시다.

👉 [다음: Spring Security](19-spring-security.md)

## 참고 자료

- [RestTemplate Guide](https://docs.spring.io/spring-framework/docs/current/reference/html/integration.html#rest-client-access)
- [WebClient Documentation](https://docs.spring.io/spring-framework/docs/current/reference/html/web-reactive.html#webflux-client)
- [Resilience4j](https://resilience4j.readme.io/)
