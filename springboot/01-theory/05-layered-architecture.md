# 계층형 아키텍처 개요

엔터프라이즈 애플리케이션의 표준 아키텍처 패턴인 계층형 아키텍처를 알아봅니다.

## 계층형 아키텍처란?

애플리케이션을 역할과 책임에 따라 여러 계층(Layer)으로 분리하는 설계 패턴입니다.

### 핵심 원칙

1. **관심사의 분리 (Separation of Concerns)**
   - 각 계층은 명확한 책임을 가짐
   - 계층 간 결합도 최소화

2. **단방향 의존성**
   - 상위 계층이 하위 계층을 의존
   - 하위 계층은 상위 계층을 알지 못함

3. **계층 간 명확한 인터페이스**
   - 정의된 방법으로만 통신
   - 구현 세부사항 은닉

## Spring Boot 계층 구조

```
┌─────────────────────────────────────┐
│   Presentation Layer (표현 계층)    │
│   - Controller                      │
│   - RestController                  │
│   - Request/Response DTO            │
└─────────────┬───────────────────────┘
              │ HTTP Request/Response
              ↓
┌─────────────────────────────────────┐
│   Business Layer (비즈니스 계층)    │
│   - Service (Interface)             │
│   - ServiceImpl (Implementation)    │
│   - Business Logic                  │
│   - Transaction Management          │
└─────────────┬───────────────────────┘
              │ Domain Objects
              ↓
┌─────────────────────────────────────┐
│   Persistence Layer (영속 계층)     │
│   - Repository                      │
│   - Entity                          │
│   - Data Access Logic               │
└─────────────┬───────────────────────┘
              │ SQL/Query
              ↓
┌─────────────────────────────────────┐
│   Database (데이터베이스)           │
└─────────────────────────────────────┘
```

### 추가 계층

```
┌─────────────────────────────────────┐
│   Common/Utility Layer (공통 계층)  │
│   - Exception Handler               │
│   - Interceptor                     │
│   - AOP                             │
│   - Config                          │
│   - Util                            │
└─────────────────────────────────────┘
```

## 각 계층의 역할

### 1. Presentation Layer (표현 계층)

**책임:**
- HTTP 요청 수신 및 응답 반환
- 요청 데이터 검증
- DTO 변환
- 예외를 사용자 친화적 메시지로 변환

**구성 요소:**
```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    private final UserService userService;
    
    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
        // 1. 요청 수신
        // 2. Service 호출
        // 3. DTO 변환
        // 4. 응답 반환
    }
}
```

**담당하지 않는 것:**
- ❌ 비즈니스 로직
- ❌ 데이터베이스 접근
- ❌ 트랜잭션 관리

### 2. Business Layer (비즈니스 계층)

**책임:**
- 비즈니스 로직 구현
- 트랜잭션 관리
- 권한 검증
- 데이터 가공 및 변환

**구성 요소:**
```java
// 인터페이스
public interface UserService {
    UserResponse createUser(UserCreateRequest request);
    UserResponse getUser(Long id);
}

// 구현체
@Service
@Transactional
public class UserServiceImpl implements UserService {
    private final UserRepository userRepository;
    private final UserMapper userMapper;
    
    @Override
    public UserResponse createUser(UserCreateRequest request) {
        // 1. 비즈니스 규칙 검증
        // 2. Entity 생성
        // 3. Repository 호출
        // 4. DTO 변환
        // 5. 응답 반환
    }
}
```

**담당하지 않는 것:**
- ❌ HTTP 요청/응답 처리
- ❌ SQL 쿼리 작성
- ❌ UI 관련 로직

### 3. Persistence Layer (영속 계층)

**책임:**
- 데이터베이스 CRUD 작업
- 쿼리 실행
- 엔티티 관리

**구성 요소:**
```java
// Repository (JPA)
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    List<User> findByStatus(UserStatus status);
}

// Entity
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    private String email;
}
```

**담당하지 않는 것:**
- ❌ 비즈니스 로직
- ❌ 데이터 검증 (비즈니스 규칙)
- ❌ DTO 변환

## 패키지 구조

### 계층별 패키지 구조 (권장)

```
com.example.demo
├── controller/              # Presentation Layer
│   ├── api/
│   │   └── v1/
│   │       ├── UserController.java
│   │       └── OrderController.java
│   └── advice/
│       └── GlobalExceptionHandler.java
│
├── service/                 # Business Layer (Interface)
│   ├── UserService.java
│   └── OrderService.java
│
├── service/impl/            # Business Layer (Implementation)
│   ├── UserServiceImpl.java
│   └── OrderServiceImpl.java
│
├── repository/              # Persistence Layer
│   ├── jpa/
│   │   ├── UserRepository.java
│   │   └── OrderRepository.java
│   └── mybatis/
│       ├── UserMapper.java
│       └── OrderMapper.java
│
├── domain/                  # Domain Model (Entity)
│   ├── User.java
│   └── Order.java
│
├── dto/                     # Data Transfer Object
│   ├── request/
│   │   ├── UserCreateRequest.java
│   │   └── UserUpdateRequest.java
│   └── response/
│       ├── UserResponse.java
│       └── OrderResponse.java
│
├── mapper/                  # Object Mapper (MapStruct)
│   ├── UserMapper.java
│   └── OrderMapper.java
│
├── config/                  # Configuration
│   ├── WebConfig.java
│   ├── JpaConfig.java
│   └── SecurityConfig.java
│
├── exception/               # Exception
│   ├── BusinessException.java
│   ├── ErrorCode.java
│   └── GlobalExceptionHandler.java
│
├── common/                  # Common Utilities
│   ├── response/
│   │   └── ApiResponse.java
│   └── constants/
│       └── Constants.java
│
└── DemoApplication.java     # Main Class
```

### 기능별 패키지 구조 (선택사항)

```
com.example.demo
├── user/                    # User 기능
│   ├── controller/
│   ├── service/
│   ├── repository/
│   ├── domain/
│   └── dto/
│
├── order/                   # Order 기능
│   ├── controller/
│   ├── service/
│   ├── repository/
│   ├── domain/
│   └── dto/
│
└── common/                  # 공통
    ├── config/
    ├── exception/
    └── util/
```

## 데이터 흐름

### 요청 처리 흐름

```
1. Client → HTTP Request
   ↓
2. Controller (Presentation Layer)
   - 요청 수신
   - DTO 검증
   - Request DTO → Service 전달
   ↓
3. Service (Business Layer)
   - 비즈니스 로직 수행
   - Request DTO → Entity 변환
   - Repository 호출
   ↓
4. Repository (Persistence Layer)
   - 데이터베이스 작업
   - Entity 반환
   ↓
5. Service (Business Layer)
   - Entity → Response DTO 변환
   - 추가 비즈니스 로직
   - Response DTO 반환
   ↓
6. Controller (Presentation Layer)
   - Response DTO → HTTP Response
   - 상태 코드 설정
   ↓
7. Client ← HTTP Response
```

### 코드 예시

```java
// 1. Controller: HTTP 요청 수신
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    private final UserService userService;
    
    @PostMapping
    public ResponseEntity<UserResponse> createUser(
            @Valid @RequestBody UserCreateRequest request) {
        UserResponse response = userService.createUser(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
}

// 2. Service: 비즈니스 로직
@Service
@Transactional
public class UserServiceImpl implements UserService {
    private final UserRepository userRepository;
    private final UserMapper userMapper;
    
    @Override
    public UserResponse createUser(UserCreateRequest request) {
        // 중복 체크 (비즈니스 규칙)
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new BusinessException(ErrorCode.USER_EMAIL_DUPLICATED);
        }
        
        // DTO → Entity 변환
        User user = userMapper.toEntity(request);
        
        // 데이터베이스 저장
        User savedUser = userRepository.save(user);
        
        // Entity → Response DTO 변환
        return userMapper.toResponse(savedUser);
    }
}

// 3. Repository: 데이터 접근
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    boolean existsByEmail(String email);
}
```

## 계층 간 통신

### DTO 사용

계층 간 데이터 전달 시 DTO를 사용합니다.

```java
// Request DTO (Client → Controller → Service)
public class UserCreateRequest {
    @NotBlank(message = "이름은 필수입니다")
    private String name;
    
    @Email(message = "올바른 이메일 형식이 아닙니다")
    private String email;
}

// Response DTO (Service → Controller → Client)
public class UserResponse {
    private Long id;
    private String name;
    private String email;
    private LocalDateTime createdAt;
}

// Entity (Service ↔ Repository)
@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
    private String email;
    private LocalDateTime createdAt;
}
```

### 왜 DTO를 사용하나?

1. **정보 은닉**
   - Entity의 내부 구조를 숨김
   - 클라이언트에 필요한 정보만 노출

2. **검증**
   - 계층별로 다른 검증 규칙 적용
   - Controller에서 입력 검증

3. **유연성**
   - Entity 변경이 API에 영향 주지 않음
   - 여러 Entity를 조합한 DTO 생성 가능

4. **성능**
   - 필요한 데이터만 전송
   - 지연 로딩 문제 방지

## 트랜잭션 관리

### Service 계층에서 관리

```java
@Service
@Transactional  // 클래스 레벨: 모든 메서드에 적용
public class OrderServiceImpl implements OrderService {
    
    @Transactional(readOnly = true)  // 조회 메서드: 성능 최적화
    public OrderResponse getOrder(Long id) {
        // ...
    }
    
    @Transactional  // 쓰기 메서드: 트랜잭션 필요
    public OrderResponse createOrder(OrderCreateRequest request) {
        // 여러 Repository 호출이 하나의 트랜잭션으로 묶임
        Order order = orderRepository.save(/* ... */);
        orderItemRepository.saveAll(/* ... */);
        return orderMapper.toResponse(order);
    }
}
```

### 트랜잭션 전파

```java
@Service
public class OrderServiceImpl implements OrderService {
    private final PaymentService paymentService;
    
    @Transactional
    public void processOrder(Long orderId) {
        // Order 처리
        Order order = orderRepository.findById(orderId).orElseThrow();
        order.process();
        
        // Payment 처리 (같은 트랜잭션)
        paymentService.processPayment(order);
        
        // 하나라도 실패하면 전체 롤백
    }
}
```

## 의존성 주입

### 생성자 주입 (권장)

```java
@RestController
@RequiredArgsConstructor  // Lombok: final 필드 생성자 자동 생성
public class UserController {
    private final UserService userService;
    
    // 생성자 주입 (Lombok이 자동 생성)
    // public UserController(UserService userService) {
    //     this.userService = userService;
    // }
}
```

### 왜 생성자 주입인가?

1. **불변성**: final 키워드 사용 가능
2. **테스트**: Mock 객체 주입 용이
3. **순환 참조**: 컴파일 타임에 감지
4. **명확성**: 필수 의존성이 명확

## 계층형 아키텍처의 장점

### ✅ 유지보수성
- 변경 영향 범위 최소화
- 계층별 독립적 수정 가능

### ✅ 테스트 용이성
- 계층별 단위 테스트 가능
- Mock 객체 사용 쉬움

### ✅ 재사용성
- Service 로직을 다른 Controller에서 재사용
- Repository를 다른 Service에서 재사용

### ✅ 확장성
- 새로운 기능 추가 시 기존 코드 영향 최소
- 계층별 독립적 확장

## 계층형 아키텍처의 단점

### ⚠️ 복잡도 증가
- 간단한 CRUD도 여러 계층 필요
- 보일러플레이트 코드 증가

### ⚠️ 성능 오버헤드
- 계층 간 데이터 변환 비용
- 메서드 호출 스택 깊어짐

### ⚠️ 과도한 추상화
- 작은 프로젝트에는 과한 구조
- 학습 곡선 존재

## 대안 아키텍처

### 헥사고날 아키텍처 (포트와 어댑터)
- 도메인 중심 설계
- 외부 시스템과의 독립성 강조

### 클린 아키텍처
- 의존성 규칙 강조
- 도메인 로직의 순수성 유지

### CQRS (Command Query Responsibility Segregation)
- 읽기와 쓰기 모델 분리
- 복잡한 도메인에 적합

## 실전 팁

### 1. 계층 경계 명확히

```java
// ❌ 나쁜 예: Controller에서 Repository 직접 접근
@RestController
public class UserController {
    private final UserRepository userRepository;  // 계층 위반!
}

// ✅ 좋은 예: Service를 통해 접근
@RestController
public class UserController {
    private final UserService userService;  // 올바른 계층 구조
}
```

### 2. 비즈니스 로직은 Service에

```java
// ❌ 나쁜 예: Controller에 비즈니스 로직
@PostMapping
public ResponseEntity<?> createUser(@RequestBody UserCreateRequest request) {
    if (userRepository.existsByEmail(request.getEmail())) {  // 비즈니스 로직!
        throw new BusinessException("중복된 이메일");
    }
    // ...
}

// ✅ 좋은 예: Service에 비즈니스 로직
@PostMapping
public ResponseEntity<?> createUser(@RequestBody UserCreateRequest request) {
    return ResponseEntity.ok(userService.createUser(request));
}
```

### 3. Entity를 직접 노출하지 않기

```java
// ❌ 나쁜 예: Entity 직접 반환
@GetMapping("/{id}")
public ResponseEntity<User> getUser(@PathVariable Long id) {
    return ResponseEntity.ok(userRepository.findById(id).orElseThrow());
}

// ✅ 좋은 예: DTO 반환
@GetMapping("/{id}")
public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
    return ResponseEntity.ok(userService.getUser(id));
}
```

## 다음 단계

계층형 아키텍처의 전체 구조를 이해했습니다. 이제 각 계층을 상세히 알아봅시다.

👉 [다음: Controller 레이어](06-controller.md)

## 참고 자료

- [Spring Framework Reference - Web MVC](https://docs.spring.io/spring-framework/reference/web/webmvc.html)
- [Martin Fowler - Patterns of Enterprise Application Architecture](https://martinfowler.com/eaaCatalog/)
- [DDD (Domain-Driven Design)](https://www.domainlanguage.com/ddd/)
