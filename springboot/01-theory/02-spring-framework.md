# Spring Framework 기초

Spring Boot를 이해하기 위해 먼저 Spring Framework의 핵심 개념을 알아봅니다.

## Spring Framework란?

**Spring Framework:** 자바 엔터프라이즈 애플리케이션 개발을 위한 경량 프레임워크

### 주요 특징

1. **경량 컨테이너:** 객체의 생명주기 관리
2. **IoC (Inversion of Control):** 제어의 역전
3. **DI (Dependency Injection):** 의존성 주입
4. **AOP (Aspect-Oriented Programming):** 관점 지향 프로그래밍
5. **PSA (Portable Service Abstraction):** 이식 가능한 서비스 추상화

## IoC (Inversion of Control)

**제어의 역전:** 객체의 생성과 생명주기 관리를 개발자가 아닌 프레임워크가 담당

### 전통적인 방식

```java
// ❌ 개발자가 직접 객체 생성 및 관리
public class UserService {
    private UserRepository userRepository = new UserRepositoryImpl();
    
    public User getUser(Long id) {
        return userRepository.findById(id);
    }
}
```

**문제점:**
- ❌ 강한 결합 (tight coupling)
- ❌ 테스트 어려움
- ❌ 구현체 변경 시 코드 수정 필요

### IoC 방식

```java
// ✅ Spring이 객체를 생성하고 주입
@Service
public class UserService {
    private final UserRepository userRepository;
    
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    public User getUser(Long id) {
        return userRepository.findById(id);
    }
}
```

**장점:**
- ✅ 느슨한 결합 (loose coupling)
- ✅ 테스트 용이
- ✅ 유연한 구현체 교체

## DI (Dependency Injection)

**의존성 주입:** 객체 간의 의존 관계를 외부에서 주입하는 디자인 패턴

### 의존성이란?

```java
// UserService는 UserRepository에 의존
public class UserService {
    private UserRepository userRepository;  // 의존성
    
    // UserRepository 없이는 UserService가 동작할 수 없음
    public User getUser(Long id) {
        return userRepository.findById(id);
    }
}
```

### DI의 3가지 방식

#### 1. 생성자 주입 (Constructor Injection) - 권장 ✅

```java
@Service
public class UserService {
    private final UserRepository userRepository;
    
    // 생성자를 통한 주입
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}

// Lombok 사용 시
@Service
@RequiredArgsConstructor  // final 필드에 대한 생성자 자동 생성
public class UserService {
    private final UserRepository userRepository;
}
```

**장점:**
- ✅ 불변성 보장 (final 사용 가능)
- ✅ 순환 참조 방지
- ✅ 테스트 용이
- ✅ 필수 의존성 명시

#### 2. 세터 주입 (Setter Injection)

```java
@Service
public class UserService {
    private UserRepository userRepository;
    
    // Setter를 통한 주입
    @Autowired
    public void setUserRepository(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}
```

**단점:**
- ❌ 불변성 보장 안 됨
- ❌ 선택적 의존성에만 사용

#### 3. 필드 주입 (Field Injection) - 비권장 ❌

```java
@Service
public class UserService {
    @Autowired  // 필드에 직접 주입
    private UserRepository userRepository;
}
```

**단점:**
- ❌ 불변성 보장 안 됨
- ❌ 순환 참조 감지 어려움
- ❌ 테스트 어려움
- ❌ DI 컨테이너 없이는 사용 불가

### DI 방식 비교

| 방식 | 불변성 | 순환참조 감지 | 테스트 용이성 | 권장도 |
|------|--------|--------------|--------------|--------|
| 생성자 주입 | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| 세터 주입 | ❌ | ❌ | ✅ | ⭐⭐ |
| 필드 주입 | ❌ | ❌ | ❌ | ⭐ |

## Bean

**Bean:** Spring IoC 컨테이너가 관리하는 객체

### Bean 등록 방법

#### 1. 컴포넌트 스캔 (Component Scan)

```java
// @Component 또는 파생 어노테이션
@Component
public class MyComponent {
    // ...
}

@Service
public class UserService {
    // ...
}

@Repository
public class UserRepository {
    // ...
}

@Controller
public class UserController {
    // ...
}

@RestController
public class UserRestController {
    // ...
}
```

**Spring Boot는 기본적으로 `@SpringBootApplication`이 있는 패키지부터 하위 패키지를 스캔합니다.**

```java
@SpringBootApplication  // 여기가 스캔 시작점
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

#### 2. Java Config (@Configuration + @Bean)

```java
@Configuration
public class AppConfig {
    
    @Bean
    public UserService userService() {
        return new UserService(userRepository());
    }
    
    @Bean
    public UserRepository userRepository() {
        return new UserRepositoryImpl();
    }
}
```

**언제 사용?**
- 외부 라이브러리 객체를 Bean으로 등록할 때
- 복잡한 초기화 로직이 필요할 때
- 조건부로 Bean을 생성할 때

### Bean 스코프

```java
@Component
@Scope("singleton")  // 기본값
public class SingletonBean {
    // 애플리케이션 전체에서 하나의 인스턴스만 존재
}

@Component
@Scope("prototype")
public class PrototypeBean {
    // 요청할 때마다 새로운 인스턴스 생성
}

@Component
@Scope("request")
public class RequestBean {
    // HTTP 요청마다 새로운 인스턴스 생성 (웹 애플리케이션만)
}

@Component
@Scope("session")
public class SessionBean {
    // HTTP 세션마다 새로운 인스턴스 생성 (웹 애플리케이션만)
}
```

### Bean 스코프 종류

| 스코프 | 설명 | 사용 시기 |
|--------|------|----------|
| `singleton` | 하나의 인스턴스만 생성 (기본값) | 대부분의 경우 |
| `prototype` | 요청마다 새 인스턴스 생성 | 상태를 가진 Bean |
| `request` | HTTP 요청마다 생성 | 웹 요청 정보 저장 |
| `session` | HTTP 세션마다 생성 | 사용자 세션 정보 |
| `application` | ServletContext마다 생성 | 애플리케이션 전역 |

## ApplicationContext

**ApplicationContext:** Spring IoC 컨테이너의 핵심 인터페이스

### 주요 기능

1. **Bean 관리:** Bean의 생성, 초기화, 소멸 관리
2. **의존성 주입:** Bean 간의 의존 관계 설정
3. **이벤트 발행:** 애플리케이션 이벤트 처리
4. **국제화:** 메시지 다국어 처리
5. **리소스 로딩:** 파일, 클래스패스 리소스 접근

### ApplicationContext 계층

```
ApplicationContext (인터페이스)
├── WebApplicationContext (웹 애플리케이션용)
│   └── AnnotationConfigServletWebServerApplicationContext (Spring Boot 기본)
└── AnnotationConfigApplicationContext (일반 애플리케이션용)
```

### ApplicationContext 사용

```java
@Service
@RequiredArgsConstructor
public class MyService {
    
    private final ApplicationContext context;
    
    public void printAllBeans() {
        String[] beanNames = context.getBeanDefinitionNames();
        for (String beanName : beanNames) {
            System.out.println(beanName);
        }
    }
    
    public Object getBean(String beanName) {
        return context.getBean(beanName);
    }
    
    public <T> T getBean(Class<T> clazz) {
        return context.getBean(clazz);
    }
}
```

## Bean 생명주기

### 생명주기 순서

```
1. Bean 인스턴스 생성
   ↓
2. 의존성 주입
   ↓
3. @PostConstruct 실행 (초기화)
   ↓
4. Bean 사용
   ↓
5. @PreDestroy 실행 (소멸)
```

### 생명주기 콜백

```java
@Component
public class MyBean {
    
    // 1. 생성자
    public MyBean() {
        System.out.println("1. Constructor called");
    }
    
    // 2. 초기화 콜백
    @PostConstruct
    public void init() {
        System.out.println("2. @PostConstruct called");
        // 초기화 작업 (DB 연결, 캐시 로딩 등)
    }
    
    // 3. 소멸 콜백
    @PreDestroy
    public void destroy() {
        System.out.println("3. @PreDestroy called");
        // 정리 작업 (연결 해제, 리소스 반환 등)
    }
}
```

### InitializingBean, DisposableBean 인터페이스

```java
@Component
public class MyBean implements InitializingBean, DisposableBean {
    
    @Override
    public void afterPropertiesSet() throws Exception {
        // 초기화 로직
        System.out.println("InitializingBean.afterPropertiesSet()");
    }
    
    @Override
    public void destroy() throws Exception {
        // 소멸 로직
        System.out.println("DisposableBean.destroy()");
    }
}
```

**권장:** `@PostConstruct`, `@PreDestroy` 사용 (표준 자바 어노테이션)

## 자동 주입과 수동 주입

### 자동 주입 (@Autowired)

```java
@Service
public class UserService {
    private final UserRepository userRepository;
    
    // @Autowired는 생성자가 하나일 때 생략 가능
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}
```

### 같은 타입의 Bean이 여러 개일 때

#### 1. @Primary 사용

```java
@Repository
@Primary  // 우선순위 지정
public class MysqlUserRepository implements UserRepository {
    // ...
}

@Repository
public class MongoUserRepository implements UserRepository {
    // ...
}
```

#### 2. @Qualifier 사용

```java
@Service
public class UserService {
    private final UserRepository userRepository;
    
    public UserService(@Qualifier("mysqlUserRepository") UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}
```

#### 3. 필드명으로 매칭

```java
@Service
public class UserService {
    private final UserRepository mysqlUserRepository;
    
    // 파라미터명과 Bean 이름이 일치하면 자동 매칭
    public UserService(UserRepository mysqlUserRepository) {
        this.mysqlUserRepository = mysqlUserRepository;
    }
}
```

#### 4. List로 모두 주입

```java
@Service
public class UserService {
    private final List<UserRepository> repositories;
    
    // 모든 UserRepository 구현체를 주입받음
    public UserService(List<UserRepository> repositories) {
        this.repositories = repositories;
    }
}
```

## 조건부 Bean 등록

### @Conditional 어노테이션

```java
@Configuration
public class DatabaseConfig {
    
    @Bean
    @ConditionalOnProperty(name = "database.type", havingValue = "mysql")
    public DataSource mysqlDataSource() {
        // MySQL DataSource 설정
        return new MysqlDataSource();
    }
    
    @Bean
    @ConditionalOnProperty(name = "database.type", havingValue = "postgresql")
    public DataSource postgresqlDataSource() {
        // PostgreSQL DataSource 설정
        return new PostgresqlDataSource();
    }
}
```

### 자주 사용하는 @Conditional 어노테이션

| 어노테이션 | 설명 |
|-----------|------|
| `@ConditionalOnClass` | 특정 클래스가 클래스패스에 있을 때 |
| `@ConditionalOnMissingClass` | 특정 클래스가 없을 때 |
| `@ConditionalOnBean` | 특정 Bean이 등록되어 있을 때 |
| `@ConditionalOnMissingBean` | 특정 Bean이 없을 때 |
| `@ConditionalOnProperty` | 특정 프로퍼티가 있을 때 |
| `@ConditionalOnWebApplication` | 웹 애플리케이션일 때 |

## @SpringBootApplication 분석

```java
@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

### @SpringBootApplication의 구성

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@SpringBootConfiguration      // = @Configuration
@EnableAutoConfiguration      // 자동 설정 활성화
@ComponentScan                // 컴포넌트 스캔
public @interface SpringBootApplication {
    // ...
}
```

#### 1. @SpringBootConfiguration

```java
// @Configuration과 동일
@Configuration
public class AppConfig {
    @Bean
    public MyBean myBean() {
        return new MyBean();
    }
}
```

#### 2. @EnableAutoConfiguration

```java
// Spring Boot의 자동 설정 활성화
// META-INF/spring.factories의 설정 클래스들을 자동으로 로드
@EnableAutoConfiguration
```

#### 3. @ComponentScan

```java
// 현재 패키지와 하위 패키지를 스캔
@ComponentScan(basePackages = "com.example.demo")
```

## 실습 예제

### 1. 간단한 DI 예제

```java
// Repository
public interface UserRepository {
    User findById(Long id);
}

@Repository
public class UserRepositoryImpl implements UserRepository {
    @Override
    public User findById(Long id) {
        // DB 조회 로직
        return new User(id, "홍길동", "hong@example.com");
    }
}

// Service
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    
    public User getUser(Long id) {
        return userRepository.findById(id);
    }
}

// Controller
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;
    
    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.getUser(id);
    }
}
```

### 2. @Configuration 예제

```java
@Configuration
public class AppConfig {
    
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
    
    @Bean
    public ObjectMapper objectMapper() {
        ObjectMapper mapper = new ObjectMapper();
        mapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
        mapper.registerModule(new JavaTimeModule());
        return mapper;
    }
}
```

### 3. 생명주기 콜백 예제

```java
@Component
@Slf4j
public class CacheManager {
    
    private Map<String, Object> cache = new ConcurrentHashMap<>();
    
    @PostConstruct
    public void init() {
        log.info("Initializing cache...");
        // 캐시 초기 데이터 로드
        cache.put("config", loadConfig());
    }
    
    @PreDestroy
    public void cleanup() {
        log.info("Cleaning up cache...");
        cache.clear();
    }
    
    private Object loadConfig() {
        // 설정 로드
        return new HashMap<>();
    }
}
```

## 정리

### Spring Framework 핵심 개념

1. **IoC/DI:** 객체 생성과 의존성 관리를 프레임워크가 담당
2. **Bean:** Spring 컨테이너가 관리하는 객체
3. **ApplicationContext:** Bean을 관리하는 IoC 컨테이너
4. **생성자 주입:** 가장 권장되는 의존성 주입 방식

### 실전 권장사항

- ✅ 생성자 주입 사용 (+ Lombok의 `@RequiredArgsConstructor`)
- ✅ 인터페이스 기반 설계
- ✅ Bean 스코프는 기본 singleton 사용
- ✅ `@PostConstruct`, `@PreDestroy`로 생명주기 관리
- ❌ 필드 주입 지양
- ❌ 순환 참조 주의

## 다음 단계

Spring Framework의 기초를 배웠습니다. 이제 빌드 도구를 알아봅시다.

👉 [다음: 빌드 도구 (Maven/Gradle)](03-build-tools.md)

## 참고 자료

- [Spring Framework Documentation](https://docs.spring.io/spring-framework/reference/)
- [Spring Core](https://docs.spring.io/spring-framework/reference/core.html)
- [Dependency Injection](https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html)
