# Service 계층

비즈니스 로직을 담당하는 Service 계층의 역할과 구현 방법을 알아봅니다.

## Service 계층이란?

**Service 계층:** 비즈니스 로직을 처리하는 계층으로, Controller와 Repository 사이에 위치

### 역할

1. **비즈니스 로직 구현:** 핵심 업무 규칙 처리
2. **트랜잭션 관리:** 데이터 일관성 보장
3. **도메인 객체 조작:** Entity ↔ DTO 변환
4. **외부 서비스 연동:** Feign Client, REST API 호출
5. **검증 및 예외 처리:** 비즈니스 규칙 검증

## 인터페이스와 구현 클래스

### 인터페이스 정의

```java
package com.example.demo.service;

import com.example.demo.dto.UserCreateRequest;
import com.example.demo.dto.UserResponse;
import com.example.demo.dto.UserUpdateRequest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface UserService {
    
    /**
     * 사용자 생성
     */
    UserResponse createUser(UserCreateRequest request);
    
    /**
     * 사용자 조회
     */
    UserResponse getUser(Long id);
    
    /**
     * 사용자 목록 조회
     */
    Page<UserResponse> getUsers(Pageable pageable);
    
    /**
     * 사용자 수정
     */
    UserResponse updateUser(Long id, UserUpdateRequest request);
    
    /**
     * 사용자 삭제
     */
    void deleteUser(Long id);
}
```

### 구현 클래스

```java
package com.example.demo.service;

import com.example.demo.domain.User;
import com.example.demo.dto.UserCreateRequest;
import com.example.demo.dto.UserResponse;
import com.example.demo.dto.UserUpdateRequest;
import com.example.demo.exception.EmailDuplicatedException;
import com.example.demo.exception.UserNotFoundException;
import com.example.demo.mapper.UserMapper;
import com.example.demo.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserServiceImpl implements UserService {
    
    private final UserRepository userRepository;
    private final UserMapper userMapper;
    
    @Override
    @Transactional
    public UserResponse createUser(UserCreateRequest request) {
        log.info("Creating user: {}", request.getEmail());
        
        // 1. 이메일 중복 체크
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new EmailDuplicatedException(request.getEmail());
        }
        
        // 2. DTO → Entity 변환
        User user = userMapper.toEntity(request);
        
        // 3. 저장
        User savedUser = userRepository.save(user);
        
        // 4. Entity → DTO 변환
        return userMapper.toResponse(savedUser);
    }
    
    @Override
    public UserResponse getUser(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id));
        
        return userMapper.toResponse(user);
    }
    
    @Override
    public Page<UserResponse> getUsers(Pageable pageable) {
        return userRepository.findAll(pageable)
                .map(userMapper::toResponse);
    }
    
    @Override
    @Transactional
    public UserResponse updateUser(Long id, UserUpdateRequest request) {
        log.info("Updating user: {}", id);
        
        // 1. 사용자 조회
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id));
        
        // 2. 엔티티 수정
        user.update(request.getName(), request.getEmail());
        
        // 3. 변경 감지로 자동 저장 (Dirty Checking)
        return userMapper.toResponse(user);
    }
    
    @Override
    @Transactional
    public void deleteUser(Long id) {
        log.info("Deleting user: {}", id);
        
        if (!userRepository.existsById(id)) {
            throw new UserNotFoundException(id);
        }
        
        userRepository.deleteById(id);
    }
}
```

## @Transactional

### 트랜잭션이란?

**트랜잭션:** 데이터베이스의 상태를 변경하는 작업의 논리적 단위

**ACID 특성:**
- **A**tomicity (원자성): 전부 성공 또는 전부 실패
- **C**onsistency (일관성): 데이터 무결성 유지
- **I**solation (격리성): 동시 실행되는 트랜잭션 간 독립성
- **D**urability (지속성): 완료된 트랜잭션의 영구 보존

### 기본 사용법

```java
@Service
@Transactional(readOnly = true)  // 클래스 레벨: 모든 메서드에 적용
public class UserServiceImpl implements UserService {
    
    @Transactional  // 읽기/쓰기 트랜잭션
    public UserResponse createUser(UserCreateRequest request) {
        // DB 변경 작업
    }
    
    // readOnly = true (클래스 레벨에서 상속)
    public UserResponse getUser(Long id) {
        // 조회만 수행
    }
}
```

### readOnly 속성

```java
// ✅ 조회 전용: readOnly = true
@Transactional(readOnly = true)
public UserResponse getUser(Long id) {
    // 성능 최적화: flush 생략, 더티 체킹 안 함
    return userRepository.findById(id)
            .map(userMapper::toResponse)
            .orElseThrow(() -> new UserNotFoundException(id));
}

// ✅ 데이터 변경: readOnly = false (기본값)
@Transactional
public UserResponse createUser(UserCreateRequest request) {
    User user = userMapper.toEntity(request);
    User savedUser = userRepository.save(user);
    return userMapper.toResponse(savedUser);
}
```

### 트랜잭션 전파 (Propagation)

```java
@Service
public class OrderService {
    
    // REQUIRED (기본값): 기존 트랜잭션 사용, 없으면 새로 생성
    @Transactional(propagation = Propagation.REQUIRED)
    public void createOrder() {
        // 트랜잭션 내에서 실행
    }
    
    // REQUIRES_NEW: 항상 새로운 트랜잭션 생성
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void createPayment() {
        // 독립적인 트랜잭션
    }
    
    // SUPPORTS: 트랜잭션이 있으면 사용, 없어도 실행
    @Transactional(propagation = Propagation.SUPPORTS)
    public void logEvent() {
        // 트랜잭션 선택적
    }
}
```

### 격리 수준 (Isolation)

```java
// READ_COMMITTED (일반적인 설정)
@Transactional(isolation = Isolation.READ_COMMITTED)
public UserResponse getUser(Long id) {
    // 커밋된 데이터만 읽기
}

// REPEATABLE_READ (MySQL InnoDB 기본값)
@Transactional(isolation = Isolation.REPEATABLE_READ)
public void transfer(Long from, Long to, BigDecimal amount) {
    // 트랜잭션 내에서 같은 데이터 반복 읽기 보장
}
```

### 롤백 규칙

```java
@Service
public class OrderService {
    
    // 기본: RuntimeException과 Error만 롤백
    @Transactional
    public void createOrder() throws Exception {
        // RuntimeException → 롤백
        // Exception (체크 예외) → 롤백 안 함
    }
    
    // 체크 예외도 롤백
    @Transactional(rollbackFor = Exception.class)
    public void createOrder() throws Exception {
        // 모든 Exception에서 롤백
    }
    
    // 특정 예외는 롤백 안 함
    @Transactional(noRollbackFor = IgnorableException.class)
    public void createOrder() {
        // IgnorableException은 롤백 안 함
    }
}
```

## 비즈니스 로직 구현

### 1. 생성 (Create)

```java
@Transactional
public UserResponse createUser(UserCreateRequest request) {
    // 1. 유효성 검증
    validateUser(request);
    
    // 2. 중복 체크
    if (userRepository.existsByEmail(request.getEmail())) {
        throw new EmailDuplicatedException(request.getEmail());
    }
    
    // 3. 비밀번호 암호화
    String encodedPassword = passwordEncoder.encode(request.getPassword());
    
    // 4. 엔티티 생성
    User user = User.builder()
            .name(request.getName())
            .email(request.getEmail())
            .password(encodedPassword)
            .status(UserStatus.ACTIVE)
            .build();
    
    // 5. 저장
    User savedUser = userRepository.save(user);
    
    // 6. 이벤트 발행 (선택)
    eventPublisher.publishEvent(new UserCreatedEvent(savedUser.getId()));
    
    // 7. 응답 DTO 변환
    return userMapper.toResponse(savedUser);
}
```

### 2. 조회 (Read)

```java
@Transactional(readOnly = true)
public UserResponse getUser(Long id) {
    User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    
    return userMapper.toResponse(user);
}

@Transactional(readOnly = true)
public Page<UserResponse> getUsers(UserSearchCondition condition, Pageable pageable) {
    // 동적 쿼리로 검색
    return userRepository.search(condition, pageable)
            .map(userMapper::toResponse);
}
```

### 3. 수정 (Update)

```java
@Transactional
public UserResponse updateUser(Long id, UserUpdateRequest request) {
    // 1. 엔티티 조회
    User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    
    // 2. 권한 체크 (선택)
    validateUpdatePermission(user);
    
    // 3. 엔티티 수정 (Dirty Checking)
    user.update(request.getName(), request.getEmail());
    
    // 4. 변경 감지로 자동 UPDATE 쿼리 실행
    return userMapper.toResponse(user);
}
```

### 4. 삭제 (Delete)

```java
@Transactional
public void deleteUser(Long id) {
    // 1. 존재 확인
    User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    
    // 2. 삭제 가능 여부 확인
    if (user.hasActiveOrders()) {
        throw new BusinessException(ErrorCode.USER_HAS_ACTIVE_ORDERS);
    }
    
    // 3. 삭제 (Hard Delete)
    userRepository.delete(user);
    
    // 또는 논리 삭제 (Soft Delete)
    // user.markAsDeleted();
}
```

## 복잡한 비즈니스 로직

### 주문 생성 예제

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class OrderServiceImpl implements OrderService {
    
    private final OrderRepository orderRepository;
    private final UserRepository userRepository;
    private final ProductRepository productRepository;
    private final PaymentService paymentService;
    
    @Transactional
    public OrderResponse createOrder(OrderCreateRequest request) {
        // 1. 사용자 조회
        User user = userRepository.findById(request.getUserId())
                .orElseThrow(() -> new UserNotFoundException(request.getUserId()));
        
        // 2. 주문 항목 처리
        List<OrderItem> orderItems = new ArrayList<>();
        BigDecimal totalAmount = BigDecimal.ZERO;
        
        for (OrderItemRequest itemRequest : request.getItems()) {
            // 상품 조회
            Product product = productRepository.findById(itemRequest.getProductId())
                    .orElseThrow(() -> new ProductNotFoundException(itemRequest.getProductId()));
            
            // 재고 확인
            if (product.getStock() < itemRequest.getQuantity()) {
                throw new InsufficientStockException(
                        product.getName(), 
                        itemRequest.getQuantity(), 
                        product.getStock()
                );
            }
            
            // 재고 차감
            product.decreaseStock(itemRequest.getQuantity());
            
            // 주문 항목 생성
            OrderItem orderItem = OrderItem.builder()
                    .product(product)
                    .quantity(itemRequest.getQuantity())
                    .price(product.getPrice())
                    .build();
            
            orderItems.add(orderItem);
            totalAmount = totalAmount.add(
                    product.getPrice().multiply(BigDecimal.valueOf(itemRequest.getQuantity()))
            );
        }
        
        // 3. 주문 생성
        Order order = Order.builder()
                .user(user)
                .orderItems(orderItems)
                .totalAmount(totalAmount)
                .status(OrderStatus.PENDING)
                .build();
        
        Order savedOrder = orderRepository.save(order);
        
        // 4. 결제 처리 (외부 서비스)
        try {
            paymentService.processPayment(savedOrder.getId(), totalAmount);
            order.confirm();
        } catch (PaymentException e) {
            order.cancel();
            throw new BusinessException(ErrorCode.PAYMENT_FAILED, e);
        }
        
        return OrderMapper.toResponse(savedOrder);
    }
}
```

## Service 간 호출

### 같은 서비스 내 메서드 호출

```java
@Service
@Transactional(readOnly = true)
public class UserService {
    
    @Transactional
    public void createUser(UserCreateRequest request) {
        // ...
        sendWelcomeEmail(savedUser);  // ❌ 트랜잭션 전파 안 됨
    }
    
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void sendWelcomeEmail(User user) {
        // 독립적인 트랜잭션으로 실행되지 않음!
    }
}
```

**해결책: 다른 서비스로 분리**

```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final EmailService emailService;
    
    @Transactional
    public void createUser(UserCreateRequest request) {
        // ...
        emailService.sendWelcomeEmail(savedUser);  // ✅ 올바른 전파
    }
}

@Service
public class EmailService {
    
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void sendWelcomeEmail(User user) {
        // 독립적인 트랜잭션
    }
}
```

### Service 간 의존성

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class OrderService {
    
    private final OrderRepository orderRepository;
    private final UserService userService;
    private final ProductService productService;
    private final PaymentService paymentService;
    
    @Transactional
    public OrderResponse createOrder(OrderCreateRequest request) {
        // 다른 서비스 호출
        UserResponse user = userService.getUser(request.getUserId());
        ProductResponse product = productService.getProduct(request.getProductId());
        
        // 비즈니스 로직...
        
        // 결제 처리
        paymentService.processPayment(order.getId(), order.getTotalAmount());
        
        return OrderResponse.from(order);
    }
}
```

## 예외 처리

### Service에서의 예외 처리

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserServiceImpl implements UserService {
    
    @Transactional
    public UserResponse createUser(UserCreateRequest request) {
        // 비즈니스 규칙 검증
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new EmailDuplicatedException(request.getEmail());
        }
        
        try {
            User user = userMapper.toEntity(request);
            User savedUser = userRepository.save(user);
            return userMapper.toResponse(savedUser);
        } catch (DataIntegrityViolationException e) {
            // DB 제약 조건 위반
            throw new BusinessException(ErrorCode.DATA_INTEGRITY_VIOLATION, e);
        }
    }
    
    @Transactional
    public void updateUser(Long id, UserUpdateRequest request) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id));
        
        // 비즈니스 규칙 검증
        if (!user.canUpdate()) {
            throw new BusinessException(ErrorCode.USER_CANNOT_UPDATE);
        }
        
        user.update(request.getName(), request.getEmail());
    }
}
```

## 테스트

### Service 단위 테스트

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @Mock
    private UserMapper userMapper;
    
    @InjectMocks
    private UserServiceImpl userService;
    
    @Test
    void createUser_Success() {
        // given
        UserCreateRequest request = new UserCreateRequest();
        request.setName("홍길동");
        request.setEmail("hong@example.com");
        
        User user = new User(null, "홍길동", "hong@example.com");
        User savedUser = new User(1L, "홍길동", "hong@example.com");
        UserResponse expected = new UserResponse(1L, "홍길동", "hong@example.com");
        
        given(userRepository.existsByEmail(request.getEmail())).willReturn(false);
        given(userMapper.toEntity(request)).willReturn(user);
        given(userRepository.save(user)).willReturn(savedUser);
        given(userMapper.toResponse(savedUser)).willReturn(expected);
        
        // when
        UserResponse actual = userService.createUser(request);
        
        // then
        assertThat(actual).isEqualTo(expected);
        verify(userRepository).save(user);
    }
    
    @Test
    void createUser_EmailDuplicated_ThrowException() {
        // given
        UserCreateRequest request = new UserCreateRequest();
        request.setEmail("hong@example.com");
        
        given(userRepository.existsByEmail(request.getEmail())).willReturn(true);
        
        // when & then
        assertThatThrownBy(() -> userService.createUser(request))
                .isInstanceOf(EmailDuplicatedException.class);
    }
}
```

### Service 통합 테스트

```java
@SpringBootTest
@Transactional
class UserServiceIntegrationTest {
    
    @Autowired
    private UserService userService;
    
    @Autowired
    private UserRepository userRepository;
    
    @Test
    void createAndGetUser() {
        // given
        UserCreateRequest request = new UserCreateRequest();
        request.setName("홍길동");
        request.setEmail("hong@example.com");
        
        // when
        UserResponse created = userService.createUser(request);
        UserResponse found = userService.getUser(created.getId());
        
        // then
        assertThat(found.getName()).isEqualTo("홍길동");
        assertThat(found.getEmail()).isEqualTo("hong@example.com");
    }
}
```

## 실전 팁

### 1. 인터페이스 사용 여부

```java
// ✅ 좋은 예: 여러 구현체가 있을 때
public interface PaymentService {
    // ...
}

@Service
public class CreditCardPaymentService implements PaymentService {
    // ...
}

@Service
public class MobilePaymentService implements PaymentService {
    // ...
}

// ✅ 구현체가 하나일 때는 인터페이스 생략 가능
@Service
public class UserService {
    // 인터페이스 없이 바로 구현
}
```

### 2. @Transactional 위치

```java
// ✅ 좋은 예: 클래스 레벨 + 메서드 레벨
@Service
@Transactional(readOnly = true)  // 기본값: 읽기 전용
public class UserService {
    
    @Transactional  // 쓰기 작업만 오버라이드
    public void createUser() {
        // ...
    }
}
```

### 3. 비즈니스 로직 위치

```java
// ✅ 좋은 예: 도메인 객체에 비즈니스 로직
@Entity
public class Order {
    
    public void cancel() {
        if (this.status == OrderStatus.SHIPPED) {
            throw new BusinessException(ErrorCode.ORDER_ALREADY_SHIPPED);
        }
        this.status = OrderStatus.CANCELLED;
    }
}

@Service
public class OrderService {
    
    @Transactional
    public void cancelOrder(Long orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException(orderId));
        
        order.cancel();  // 도메인 객체의 메서드 호출
    }
}
```

## 다음 단계

Service 계층을 배웠습니다. 이제 Repository 계층을 알아봅시다.

👉 [다음: Repository 계층](08-repository.md)

## 참고 자료

- [Spring Transaction Management](https://docs.spring.io/spring-framework/reference/data-access/transaction.html)
- [@Transactional](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/annotation/Transactional.html)
