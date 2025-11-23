# 커스텀 예외 설계

비즈니스 로직에 맞는 커스텀 예외를 설계하고 활용하는 방법을 알아봅니다.

## 커스텀 예외의 필요성

### 표준 예외의 한계

```java
// ❌ 나쁜 예: 표준 예외 사용
public User getUser(Long id) {
    return userRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("User not found"));
}
```

**문제점:**
- ❌ 예외 처리가 어려움 (모든 RuntimeException을 잡아야 함)
- ❌ 에러 코드가 없음
- ❌ HTTP 상태 코드 매핑 어려움
- ❌ 비즈니스 의미를 담지 못함

### 커스텀 예외의 장점

```java
// ✅ 좋은 예: 커스텀 예외 사용
public User getUser(Long id) {
    return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
}
```

**장점:**
- ✅ 명확한 예외 처리
- ✅ 에러 코드 포함
- ✅ HTTP 상태 코드 자동 매핑
- ✅ 비즈니스 의미 명확

## BusinessException 설계

### 기본 BusinessException

```java
package com.example.demo.exception;

import lombok.Getter;

@Getter
public class BusinessException extends RuntimeException {
    
    private final ErrorCode errorCode;
    private final Object[] args;  // 메시지 파라미터
    
    public BusinessException(ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
        this.args = null;
    }
    
    public BusinessException(ErrorCode errorCode, Object... args) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
        this.args = args;
    }
    
    public BusinessException(ErrorCode errorCode, Throwable cause) {
        super(errorCode.getMessage(), cause);
        this.errorCode = errorCode;
        this.args = null;
    }
    
    public BusinessException(ErrorCode errorCode, Throwable cause, Object... args) {
        super(errorCode.getMessage(), cause);
        this.errorCode = errorCode;
        this.args = args;
    }
}
```

## ErrorCode enum

### 체계적인 ErrorCode 설계

```java
package com.example.demo.exception;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;

@Getter
@RequiredArgsConstructor
public enum ErrorCode {
    
    // ===== User =====
    USER_NOT_FOUND("USER001", "사용자를 찾을 수 없습니다", HttpStatus.NOT_FOUND),
    USER_ALREADY_EXISTS("USER002", "이미 존재하는 사용자입니다", HttpStatus.CONFLICT),
    EMAIL_DUPLICATED("USER003", "이미 사용 중인 이메일입니다", HttpStatus.CONFLICT),
    INVALID_PASSWORD("USER004", "비밀번호가 올바르지 않습니다", HttpStatus.BAD_REQUEST),
    USER_DISABLED("USER005", "비활성화된 사용자입니다", HttpStatus.FORBIDDEN),
    
    // ===== Order =====
    ORDER_NOT_FOUND("ORDER001", "주문을 찾을 수 없습니다", HttpStatus.NOT_FOUND),
    ORDER_ALREADY_CANCELLED("ORDER002", "이미 취소된 주문입니다", HttpStatus.BAD_REQUEST),
    ORDER_CANNOT_CANCEL("ORDER003", "취소할 수 없는 주문입니다", HttpStatus.BAD_REQUEST),
    INSUFFICIENT_STOCK("ORDER004", "재고가 부족합니다", HttpStatus.BAD_REQUEST),
    
    // ===== Payment =====
    PAYMENT_FAILED("PAY001", "결제에 실패했습니다", HttpStatus.BAD_REQUEST),
    PAYMENT_CANCELLED("PAY002", "결제가 취소되었습니다", HttpStatus.BAD_REQUEST),
    INVALID_PAYMENT_AMOUNT("PAY003", "결제 금액이 올바르지 않습니다", HttpStatus.BAD_REQUEST),
    
    // ===== Authentication =====
    UNAUTHORIZED("AUTH001", "인증이 필요합니다", HttpStatus.UNAUTHORIZED),
    ACCESS_DENIED("AUTH002", "접근 권한이 없습니다", HttpStatus.FORBIDDEN),
    INVALID_TOKEN("AUTH003", "유효하지 않은 토큰입니다", HttpStatus.UNAUTHORIZED),
    TOKEN_EXPIRED("AUTH004", "토큰이 만료되었습니다", HttpStatus.UNAUTHORIZED),
    
    // ===== Validation =====
    INVALID_INPUT_VALUE("VALID001", "입력값이 올바르지 않습니다", HttpStatus.BAD_REQUEST),
    MISSING_PARAMETER("VALID002", "필수 파라미터가 누락되었습니다", HttpStatus.BAD_REQUEST),
    TYPE_MISMATCH("VALID003", "타입이 올바르지 않습니다", HttpStatus.BAD_REQUEST),
    
    // ===== Common =====
    INTERNAL_SERVER_ERROR("COMMON001", "서버 내부 오류가 발생했습니다", HttpStatus.INTERNAL_SERVER_ERROR),
    METHOD_NOT_ALLOWED("COMMON002", "허용되지 않는 메서드입니다", HttpStatus.METHOD_NOT_ALLOWED),
    NOT_FOUND("COMMON003", "요청한 리소스를 찾을 수 없습니다", HttpStatus.NOT_FOUND),
    BAD_REQUEST("COMMON004", "잘못된 요청입니다", HttpStatus.BAD_REQUEST);
    
    private final String code;
    private final String message;
    private final HttpStatus status;
}
```

### ErrorCode 네이밍 규칙

```
{도메인}{일련번호}
- USER001, USER002, ...
- ORDER001, ORDER002, ...
- PAY001, PAY002, ...
```

## 도메인별 커스텀 예외

### 1. UserNotFoundException

```java
package com.example.demo.exception;

public class UserNotFoundException extends BusinessException {
    
    public UserNotFoundException() {
        super(ErrorCode.USER_NOT_FOUND);
    }
    
    public UserNotFoundException(Long userId) {
        super(ErrorCode.USER_NOT_FOUND, userId);
    }
    
    public UserNotFoundException(String email) {
        super(ErrorCode.USER_NOT_FOUND, email);
    }
}
```

**사용:**
```java
throw new UserNotFoundException(userId);
```

### 2. EmailDuplicatedException

```java
package com.example.demo.exception;

public class EmailDuplicatedException extends BusinessException {
    
    public EmailDuplicatedException(String email) {
        super(ErrorCode.EMAIL_DUPLICATED, email);
    }
}
```

**사용:**
```java
if (userRepository.existsByEmail(email)) {
    throw new EmailDuplicatedException(email);
}
```

### 3. InvalidPasswordException

```java
package com.example.demo.exception;

public class InvalidPasswordException extends BusinessException {
    
    public InvalidPasswordException() {
        super(ErrorCode.INVALID_PASSWORD);
    }
}
```

**사용:**
```java
if (!passwordEncoder.matches(rawPassword, encodedPassword)) {
    throw new InvalidPasswordException();
}
```

### 4. OrderNotFoundException

```java
package com.example.demo.exception;

public class OrderNotFoundException extends BusinessException {
    
    public OrderNotFoundException(Long orderId) {
        super(ErrorCode.ORDER_NOT_FOUND, orderId);
    }
}
```

### 5. InsufficientStockException

```java
package com.example.demo.exception;

public class InsufficientStockException extends BusinessException {
    
    public InsufficientStockException(String productName, int requested, int available) {
        super(ErrorCode.INSUFFICIENT_STOCK, productName, requested, available);
    }
}
```

**사용:**
```java
if (product.getStock() < quantity) {
    throw new InsufficientStockException(
            product.getName(), 
            quantity, 
            product.getStock()
    );
}
```

## 예외 계층 구조

```
RuntimeException
└── BusinessException (비즈니스 예외의 최상위)
    ├── UserException (사용자 관련 예외)
    │   ├── UserNotFoundException
    │   ├── EmailDuplicatedException
    │   └── InvalidPasswordException
    ├── OrderException (주문 관련 예외)
    │   ├── OrderNotFoundException
    │   ├── OrderAlreadyCancelledException
    │   └── InsufficientStockException
    ├── PaymentException (결제 관련 예외)
    │   ├── PaymentFailedException
    │   └── InvalidPaymentAmountException
    └── AuthenticationException (인증 관련 예외)
        ├── InvalidTokenException
        └── TokenExpiredException
```

### 계층 구조 구현

```java
// 도메인별 최상위 예외
public abstract class UserException extends BusinessException {
    public UserException(ErrorCode errorCode) {
        super(errorCode);
    }
    
    public UserException(ErrorCode errorCode, Object... args) {
        super(errorCode, args);
    }
}

// 구체적인 예외
public class UserNotFoundException extends UserException {
    public UserNotFoundException(Long userId) {
        super(ErrorCode.USER_NOT_FOUND, userId);
    }
}

public class EmailDuplicatedException extends UserException {
    public EmailDuplicatedException(String email) {
        super(ErrorCode.EMAIL_DUPLICATED, email);
    }
}
```

## Service에서의 예외 활용

### UserService 예시

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserServiceImpl implements UserService {
    
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    
    @Override
    public UserResponse getUser(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new UserNotFoundException(userId));
        
        return UserResponse.from(user);
    }
    
    @Override
    @Transactional
    public UserResponse createUser(UserCreateRequest request) {
        // 이메일 중복 체크
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new EmailDuplicatedException(request.getEmail());
        }
        
        User user = User.builder()
                .name(request.getName())
                .email(request.getEmail())
                .password(passwordEncoder.encode(request.getPassword()))
                .build();
        
        User savedUser = userRepository.save(user);
        return UserResponse.from(savedUser);
    }
    
    @Override
    public void verifyPassword(String email, String rawPassword) {
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new UserNotFoundException(email));
        
        if (!passwordEncoder.matches(rawPassword, user.getPassword())) {
            throw new InvalidPasswordException();
        }
    }
}
```

### OrderService 예시

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class OrderServiceImpl implements OrderService {
    
    private final OrderRepository orderRepository;
    private final ProductRepository productRepository;
    
    @Override
    @Transactional
    public OrderResponse createOrder(OrderCreateRequest request) {
        // 상품 조회
        Product product = productRepository.findById(request.getProductId())
                .orElseThrow(() -> new ProductNotFoundException(request.getProductId()));
        
        // 재고 확인
        if (product.getStock() < request.getQuantity()) {
            throw new InsufficientStockException(
                    product.getName(),
                    request.getQuantity(),
                    product.getStock()
            );
        }
        
        // 주문 생성
        Order order = Order.create(product, request.getQuantity());
        Order savedOrder = orderRepository.save(order);
        
        return OrderResponse.from(savedOrder);
    }
    
    @Override
    @Transactional
    public void cancelOrder(Long orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException(orderId));
        
        // 이미 취소된 주문
        if (order.isCancelled()) {
            throw new OrderAlreadyCancelledException(orderId);
        }
        
        // 배송 시작 후에는 취소 불가
        if (order.isShipped()) {
            throw new OrderCannotCancelException(orderId, "배송이 시작되었습니다");
        }
        
        order.cancel();
    }
}
```

## GlobalExceptionHandler 연동

```java
@Slf4j
@RestControllerAdvice
@RequiredArgsConstructor
public class GlobalExceptionHandler {
    
    private final MessageSource messageSource;
    
    /**
     * 비즈니스 예외 처리
     */
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(
            BusinessException ex,
            HttpServletRequest request) {
        
        log.warn("Business exception: {} - {}", 
                ex.getErrorCode().getCode(), 
                ex.getMessage());
        
        Locale locale = LocaleContextHolder.getLocale();
        
        String message = messageSource.getMessage(
                ex.getErrorCode().getCode(),
                ex.getArgs(),
                ex.getErrorCode().getMessage(),
                locale
        );
        
        ErrorResponse error = ErrorResponse.builder()
                .code(ex.getErrorCode().getCode())
                .message(message)
                .path(request.getRequestURI())
                .build();
        
        return ResponseEntity
                .status(ex.getErrorCode().getStatus())
                .body(error);
    }
    
    /**
     * 도메인별 예외 처리 (선택사항)
     */
    @ExceptionHandler(UserException.class)
    public ResponseEntity<ErrorResponse> handleUserException(
            UserException ex,
            HttpServletRequest request) {
        
        log.warn("User exception: {}", ex.getMessage());
        
        ErrorResponse error = ErrorResponse.builder()
                .code(ex.getErrorCode().getCode())
                .message(ex.getErrorCode().getMessage())
                .path(request.getRequestURI())
                .build();
        
        return ResponseEntity
                .status(ex.getErrorCode().getStatus())
                .body(error);
    }
}
```

## 테스트

### 단위 테스트

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @InjectMocks
    private UserServiceImpl userService;
    
    @Test
    void getUser_NotFound_ThrowException() {
        // given
        Long userId = 999L;
        given(userRepository.findById(userId))
                .willReturn(Optional.empty());
        
        // when & then
        assertThatThrownBy(() -> userService.getUser(userId))
                .isInstanceOf(UserNotFoundException.class)
                .hasMessageContaining("사용자를 찾을 수 없습니다");
    }
    
    @Test
    void createUser_EmailDuplicated_ThrowException() {
        // given
        String email = "test@example.com";
        UserCreateRequest request = new UserCreateRequest();
        request.setEmail(email);
        
        given(userRepository.existsByEmail(email))
                .willReturn(true);
        
        // when & then
        assertThatThrownBy(() -> userService.createUser(request))
                .isInstanceOf(EmailDuplicatedException.class)
                .hasMessageContaining("이미 사용 중인 이메일입니다");
    }
}
```

### 통합 테스트

```java
@SpringBootTest
@AutoConfigureMockMvc
class UserControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    void getUser_NotFound_Returns404() throws Exception {
        mockMvc.perform(get("/api/v1/users/999"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.code").value("USER001"))
                .andExpect(jsonPath("$.message").value("사용자를 찾을 수 없습니다"));
    }
    
    @Test
    void createUser_EmailDuplicated_Returns409() throws Exception {
        // 첫 번째 사용자 생성
        UserCreateRequest request = new UserCreateRequest();
        request.setName("Test User");
        request.setEmail("test@example.com");
        request.setPassword("password123");
        
        mockMvc.perform(post("/api/v1/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated());
        
        // 같은 이메일로 다시 생성 시도
        mockMvc.perform(post("/api/v1/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.code").value("USER003"))
                .andExpect(jsonPath("$.message").value("이미 사용 중인 이메일입니다"));
    }
}
```

## 실전 팁

### 1. 예외 생성 비용 최소화

```java
// ❌ 나쁜 예: 매번 새로운 예외 생성
if (condition) {
    throw new BusinessException(ErrorCode.INVALID_INPUT);
}

// ✅ 좋은 예: 예외는 필요할 때만 생성
User user = userRepository.findById(id)
        .orElseThrow(() -> new UserNotFoundException(id));
```

### 2. 예외 메시지에 컨텍스트 포함

```java
// ❌ 나쁜 예
throw new BusinessException(ErrorCode.INVALID_INPUT);

// ✅ 좋은 예
throw new BusinessException(
        ErrorCode.INVALID_INPUT, 
        "userId", userId, "email", email
);
```

### 3. 체크 예외 vs 언체크 예외

```java
// ✅ 비즈니스 예외는 RuntimeException 상속 (언체크)
public class BusinessException extends RuntimeException {
    // ...
}

// ❌ 체크 예외는 사용하지 않음
public class BusinessException extends Exception {
    // throws 선언 필요, 코드 복잡도 증가
}
```

### 4. 예외 로깅 레벨

```java
@ExceptionHandler(BusinessException.class)
public ResponseEntity<ErrorResponse> handleBusinessException(BusinessException ex) {
    // 비즈니스 예외는 WARN 레벨
    log.warn("Business exception: {}", ex.getMessage());
    // ...
}

@ExceptionHandler(Exception.class)
public ResponseEntity<ErrorResponse> handleException(Exception ex) {
    // 예상치 못한 예외는 ERROR 레벨
    log.error("Unexpected error", ex);
    // ...
}
```

## 패키지 구조

```
com.example.demo/
├── exception/
│   ├── BusinessException.java          # 최상위 비즈니스 예외
│   ├── ErrorCode.java                  # 에러 코드 enum
│   ├── ErrorResponse.java              # 에러 응답 DTO
│   ├── GlobalExceptionHandler.java     # 전역 예외 핸들러
│   ├── user/
│   │   ├── UserException.java          # 사용자 예외 최상위
│   │   ├── UserNotFoundException.java
│   │   ├── EmailDuplicatedException.java
│   │   └── InvalidPasswordException.java
│   ├── order/
│   │   ├── OrderException.java
│   │   ├── OrderNotFoundException.java
│   │   └── InsufficientStockException.java
│   └── payment/
│       ├── PaymentException.java
│       └── PaymentFailedException.java
```

## 다음 단계

커스텀 예외를 설계했습니다. 이제 다국어 처리를 알아봅시다.

👉 [다음: 다국어 처리](30-internationalization.md)

## 참고 자료

- [Effective Java - Item 70: Use checked exceptions for recoverable conditions](https://www.oreilly.com/library/view/effective-java/9780134686097/)
- [Spring Exception Handling Best Practices](https://www.baeldung.com/exception-handling-for-rest-with-spring)
