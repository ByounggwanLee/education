# Validation (검증)

Spring Boot에서 데이터 검증을 수행하는 다양한 방법을 알아봅니다.

## Validation이란?

**Validation (검증):** 입력 데이터가 애플리케이션의 요구사항을 충족하는지 확인하는 과정

### 검증이 필요한 이유

```java
// ❌ 검증 없이
@PostMapping
public ResponseEntity<?> createUser(@RequestBody UserCreateRequest request) {
    // name이 null이거나 빈 문자열이면?
    // email이 올바른 형식이 아니면?
    // age가 음수이면?
    userService.createUser(request);
    return ResponseEntity.ok().build();
}
```

**문제점:**
- ❌ 잘못된 데이터가 비즈니스 로직까지 전달됨
- ❌ 데이터베이스 제약 조건 위반
- ❌ 보안 취약점
- ❌ 사용자에게 불친절한 에러 메시지

## Bean Validation (JSR-380)

Java 표준 검증 API입니다.

### 의존성 추가

**Maven:**
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

**Gradle:**
```gradle
implementation 'org.springframework.boot:spring-boot-starter-validation'
```

## 기본 제약 조건 어노테이션

### 문자열 검증

```java
@Getter
@Setter
public class UserCreateRequest {
    
    @NotNull                          // null 불가
    @NotEmpty                         // null, "" 불가
    @NotBlank                         // null, "", " " 불가
    private String name;
    
    @Size(min = 2, max = 50)         // 길이 제한
    private String username;
    
    @Pattern(regexp = "^[a-zA-Z0-9]*$")  // 정규식
    private String nickname;
}
```

### 숫자 검증

```java
@Getter
@Setter
public class ProductCreateRequest {
    
    @NotNull
    @Min(0)                           // 최솟값
    @Max(100)                         // 최댓값
    private Integer stock;
    
    @NotNull
    @Positive                         // 양수 (0 제외)
    @DecimalMin("0.01")
    private BigDecimal price;
    
    @PositiveOrZero                   // 0 또는 양수
    private Integer discount;
    
    @Negative                         // 음수
    @NegativeOrZero                   // 0 또는 음수
    private Integer adjustment;
}
```

### 날짜/시간 검증

```java
@Getter
@Setter
public class EventCreateRequest {
    
    @NotNull
    @Future                           // 미래 날짜
    private LocalDateTime startDate;
    
    @FutureOrPresent                  // 현재 또는 미래
    private LocalDateTime endDate;
    
    @Past                             // 과거 날짜
    private LocalDate birthDate;
    
    @PastOrPresent                    // 현재 또는 과거
    private LocalDate registeredDate;
}
```

### 이메일 검증

```java
@Getter
@Setter
public class UserCreateRequest {
    
    @NotBlank
    @Email                            // 이메일 형식
    private String email;
    
    @Email(regexp = "^[A-Za-z0-9+_.-]+@(.+)$")
    private String customEmail;
}
```

### 불린 검증

```java
@Getter
@Setter
public class AgreementRequest {
    
    @NotNull
    @AssertTrue                       // true여야 함
    private Boolean termsAgreed;
    
    @AssertFalse                      // false여야 함
    private Boolean spamOptOut;
}
```

### 컬렉션 검증

```java
@Getter
@Setter
public class OrderCreateRequest {
    
    @NotEmpty                         // 비어있지 않아야 함
    @Size(min = 1, max = 10)         // 요소 개수 제한
    private List<@Valid OrderItemRequest> items;
}
```

## 제약 조건 어노테이션 요약

| 어노테이션 | 설명 | 지원 타입 |
|-----------|------|----------|
| `@NotNull` | null이 아니어야 함 | 모든 타입 |
| `@NotEmpty` | null이나 empty가 아니어야 함 | String, Collection, Map, Array |
| `@NotBlank` | null, empty, 공백 불가 | String |
| `@Size(min, max)` | 크기 제한 | String, Collection, Map, Array |
| `@Min(value)` | 최솟값 | Number |
| `@Max(value)` | 최댓값 | Number |
| `@Positive` | 양수 (0 제외) | Number |
| `@PositiveOrZero` | 0 또는 양수 | Number |
| `@Negative` | 음수 (0 제외) | Number |
| `@NegativeOrZero` | 0 또는 음수 | Number |
| `@DecimalMin(value)` | 최솟값 (소수) | Number, String |
| `@DecimalMax(value)` | 최댓값 (소수) | Number, String |
| `@Digits(integer, fraction)` | 정수/소수 자릿수 제한 | Number, String |
| `@Email` | 이메일 형식 | String |
| `@Pattern(regexp)` | 정규식 패턴 | String |
| `@Future` | 미래 날짜/시간 | Date, Calendar, Instant, LocalDate, LocalDateTime, ... |
| `@FutureOrPresent` | 현재 또는 미래 | 위와 동일 |
| `@Past` | 과거 날짜/시간 | 위와 동일 |
| `@PastOrPresent` | 현재 또는 과거 | 위와 동일 |
| `@AssertTrue` | true여야 함 | boolean, Boolean |
| `@AssertFalse` | false여야 함 | boolean, Boolean |

## Controller에서 검증

### @Valid 사용

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {
    
    private final UserService userService;
    
    @PostMapping
    public ResponseEntity<ApiResponse<UserResponse>> createUser(
            @Valid @RequestBody UserCreateRequest request) {
        
        UserResponse user = userService.createUser(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success("사용자가 생성되었습니다", user));
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<ApiResponse<UserResponse>> updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UserUpdateRequest request) {
        
        UserResponse user = userService.updateUser(id, request);
        return ResponseEntity.ok(ApiResponse.success("사용자가 수정되었습니다", user));
    }
}
```

### 검증 실패 시

검증 실패 시 `MethodArgumentNotValidException`이 발생합니다.

## 커스텀 에러 메시지

### message 속성 사용

```java
@Getter
@Setter
public class UserCreateRequest {
    
    @NotBlank(message = "이름은 필수입니다")
    @Size(min = 2, max = 50, message = "이름은 2자에서 50자 사이여야 합니다")
    private String name;
    
    @NotBlank(message = "이메일은 필수입니다")
    @Email(message = "올바른 이메일 형식이 아닙니다")
    private String email;
    
    @NotNull(message = "나이는 필수입니다")
    @Min(value = 0, message = "나이는 0 이상이어야 합니다")
    @Max(value = 150, message = "나이는 150 이하여야 합니다")
    private Integer age;
}
```

### 메시지 파일 사용 (다국어 지원)

**DTO:**
```java
@Getter
@Setter
public class UserCreateRequest {
    
    @NotBlank(message = "{user.name.required}")
    @Size(min = 2, max = 50, message = "{user.name.size}")
    private String name;
    
    @NotBlank(message = "{user.email.required}")
    @Email(message = "{user.email.invalid}")
    private String email;
}
```

**ValidationMessages.properties:**
```properties
user.name.required=이름은 필수입니다
user.name.size=이름은 {min}자에서 {max}자 사이여야 합니다
user.email.required=이메일은 필수입니다
user.email.invalid=올바른 이메일 형식이 아닙니다
```

## 중첩 객체 검증

### @Valid 중첩

```java
@Getter
@Setter
public class OrderCreateRequest {
    
    @NotNull(message = "사용자 정보는 필수입니다")
    @Valid                            // 중첩 객체도 검증
    private UserInfo user;
    
    @NotEmpty(message = "주문 항목은 필수입니다")
    @Size(min = 1, max = 10, message = "주문 항목은 1개에서 10개 사이여야 합니다")
    private List<@Valid OrderItemRequest> items;
    
    @Getter
    @Setter
    public static class UserInfo {
        @NotBlank(message = "사용자 이름은 필수입니다")
        private String name;
        
        @NotBlank(message = "전화번호는 필수입니다")
        @Pattern(regexp = "^010-\\d{4}-\\d{4}$", message = "올바른 전화번호 형식이 아닙니다")
        private String phone;
    }
}

@Getter
@Setter
public class OrderItemRequest {
    
    @NotNull(message = "상품 ID는 필수입니다")
    @Positive(message = "상품 ID는 양수여야 합니다")
    private Long productId;
    
    @NotNull(message = "수량은 필수입니다")
    @Min(value = 1, message = "수량은 최소 1개여야 합니다")
    private Integer quantity;
}
```

## 커스텀 Validator

### 어노테이션 정의

```java
package com.example.demo.validation;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;

import java.lang.annotation.*;

@Target({ElementType.FIELD, ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = PhoneNumberValidator.class)
@Documented
public @interface PhoneNumber {
    
    String message() default "올바른 전화번호 형식이 아닙니다";
    
    Class<?>[] groups() default {};
    
    Class<? extends Payload>[] payload() default {};
}
```

### Validator 구현

```java
package com.example.demo.validation;

import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

public class PhoneNumberValidator implements ConstraintValidator<PhoneNumber, String> {
    
    private static final String PHONE_PATTERN = "^010-\\d{4}-\\d{4}$";
    
    @Override
    public void initialize(PhoneNumber constraintAnnotation) {
        // 초기화 작업 (필요시)
    }
    
    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        // null은 @NotNull로 검증
        if (value == null) {
            return true;
        }
        
        return value.matches(PHONE_PATTERN);
    }
}
```

### 사용

```java
@Getter
@Setter
public class UserCreateRequest {
    
    @NotBlank(message = "전화번호는 필수입니다")
    @PhoneNumber                      // 커스텀 validator
    private String phone;
}
```

## 복잡한 커스텀 Validator

### 클래스 레벨 검증

**어노테이션:**
```java
package com.example.demo.validation;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;

import java.lang.annotation.*;

@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = PasswordMatchValidator.class)
@Documented
public @interface PasswordMatch {
    
    String message() default "비밀번호가 일치하지 않습니다";
    
    Class<?>[] groups() default {};
    
    Class<? extends Payload>[] payload() default {};
}
```

**Validator:**
```java
package com.example.demo.validation;

import com.example.demo.dto.UserCreateRequest;
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

public class PasswordMatchValidator implements ConstraintValidator<PasswordMatch, UserCreateRequest> {
    
    @Override
    public boolean isValid(UserCreateRequest request, ConstraintValidatorContext context) {
        if (request == null) {
            return true;
        }
        
        String password = request.getPassword();
        String passwordConfirm = request.getPasswordConfirm();
        
        if (password == null || passwordConfirm == null) {
            return true;
        }
        
        return password.equals(passwordConfirm);
    }
}
```

**DTO:**
```java
@Getter
@Setter
@PasswordMatch                        // 클래스 레벨 검증
public class UserCreateRequest {
    
    @NotBlank(message = "이름은 필수입니다")
    private String name;
    
    @NotBlank(message = "비밀번호는 필수입니다")
    @Size(min = 8, message = "비밀번호는 최소 8자 이상이어야 합니다")
    private String password;
    
    @NotBlank(message = "비밀번호 확인은 필수입니다")
    private String passwordConfirm;
}
```

## 조건부 검증 (Groups)

### Validation Group 정의

```java
public interface ValidationGroups {
    interface Create {}
    interface Update {}
}
```

### DTO에서 Group 사용

```java
@Getter
@Setter
public class UserRequest {
    
    @Null(groups = Create.class, message = "생성 시 ID는 null이어야 합니다")
    @NotNull(groups = Update.class, message = "수정 시 ID는 필수입니다")
    private Long id;
    
    @NotBlank(groups = {Create.class, Update.class}, message = "이름은 필수입니다")
    private String name;
    
    @NotBlank(groups = Create.class, message = "비밀번호는 필수입니다")
    private String password;
}
```

### Controller에서 Group 사용

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    
    @PostMapping
    public ResponseEntity<?> createUser(
            @Validated(Create.class) @RequestBody UserRequest request) {
        // Create 그룹 검증만 실행
        // ...
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<?> updateUser(
            @PathVariable Long id,
            @Validated(Update.class) @RequestBody UserRequest request) {
        // Update 그룹 검증만 실행
        // ...
    }
}
```

## 프로그래밍 방식 검증

### Validator 주입

```java
@Service
@RequiredArgsConstructor
public class UserService {
    
    private final Validator validator;
    
    public void validateAndCreate(UserCreateRequest request) {
        // 수동 검증
        Set<ConstraintViolation<UserCreateRequest>> violations = 
                validator.validate(request);
        
        if (!violations.isEmpty()) {
            String message = violations.stream()
                    .map(ConstraintViolation::getMessage)
                    .collect(Collectors.joining(", "));
            throw new ValidationException(message);
        }
        
        // 비즈니스 로직...
    }
}
```

## 검증 실패 응답 처리

### GlobalExceptionHandler

```java
@RestControllerAdvice
@RequiredArgsConstructor
public class GlobalExceptionHandler {
    
    /**
     * @Valid 검증 실패
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
            MethodArgumentNotValidException ex,
            HttpServletRequest request) {
        
        List<ErrorResponse.FieldError> fieldErrors = ex.getBindingResult()
                .getFieldErrors()
                .stream()
                .map(error -> ErrorResponse.FieldError.builder()
                        .field(error.getField())
                        .rejectedValue(error.getRejectedValue())
                        .message(error.getDefaultMessage())
                        .build())
                .toList();
        
        ErrorResponse error = ErrorResponse.builder()
                .code("VALIDATION_FAILED")
                .message("입력값 검증에 실패했습니다")
                .path(request.getRequestURI())
                .errors(fieldErrors)
                .build();
        
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }
    
    /**
     * @Validated 검증 실패 (파라미터)
     */
    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<ErrorResponse> handleConstraintViolation(
            ConstraintViolationException ex,
            HttpServletRequest request) {
        
        List<ErrorResponse.FieldError> fieldErrors = ex.getConstraintViolations()
                .stream()
                .map(violation -> ErrorResponse.FieldError.builder()
                        .field(violation.getPropertyPath().toString())
                        .rejectedValue(violation.getInvalidValue())
                        .message(violation.getMessage())
                        .build())
                .toList();
        
        ErrorResponse error = ErrorResponse.builder()
                .code("CONSTRAINT_VIOLATION")
                .message("제약 조건 위반")
                .path(request.getRequestURI())
                .errors(fieldErrors)
                .build();
        
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }
}
```

### 검증 실패 응답 예시

```json
{
    "success": false,
    "code": "VALIDATION_FAILED",
    "message": "입력값 검증에 실패했습니다",
    "path": "/api/v1/users",
    "timestamp": "2025-11-22T10:30:00",
    "errors": [
        {
            "field": "name",
            "rejectedValue": "",
            "message": "이름은 필수입니다"
        },
        {
            "field": "email",
            "rejectedValue": "invalid-email",
            "message": "올바른 이메일 형식이 아닙니다"
        },
        {
            "field": "age",
            "rejectedValue": -5,
            "message": "나이는 0 이상이어야 합니다"
        }
    ]
}
```

## 실전 팁

### 1. @Valid vs @Validated

```java
// @Valid: 표준 Bean Validation (중첩 객체 검증 가능)
@PostMapping
public ResponseEntity<?> create(@Valid @RequestBody UserRequest request) {
    // ...
}

// @Validated: Spring 확장 (Group 검증 가능)
@PostMapping
public ResponseEntity<?> create(
        @Validated(Create.class) @RequestBody UserRequest request) {
    // ...
}

// 메서드 파라미터 검증은 @Validated 필요
@Validated
@RestController
public class UserController {
    @GetMapping("/{id}")
    public ResponseEntity<?> getUser(@PathVariable @Min(1) Long id) {
        // ...
    }
}
```

### 2. 검증 순서

```java
@Getter
@Setter
public class UserCreateRequest {
    
    // 1. @NotBlank 먼저 검증
    // 2. @Size 검증
    // 3. @Pattern 검증
    @NotBlank(message = "이름은 필수입니다")
    @Size(min = 2, max = 50, message = "이름은 2자에서 50자 사이여야 합니다")
    @Pattern(regexp = "^[가-힣a-zA-Z]*$", message = "이름은 한글 또는 영문만 가능합니다")
    private String name;
}
```

### 3. null 처리

```java
// ✅ 좋은 예: null 체크 분리
@NotNull(message = "나이는 필수입니다")
@Min(value = 0, message = "나이는 0 이상이어야 합니다")
private Integer age;

// ❌ 나쁜 예: @Min만 사용 (null일 때 통과)
@Min(value = 0, message = "나이는 0 이상이어야 합니다")
private Integer age;
```

## 테스트

### Controller 검증 테스트

```java
@WebMvcTest(UserController.class)
class UserControllerValidationTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private UserService userService;
    
    @Test
    void createUser_InvalidInput_ReturnsBadRequest() throws Exception {
        UserCreateRequest request = new UserCreateRequest();
        request.setName("");  // 빈 이름
        request.setEmail("invalid-email");  // 잘못된 이메일
        request.setAge(-5);  // 음수 나이
        
        mockMvc.perform(post("/api/v1/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("VALIDATION_FAILED"))
                .andExpect(jsonPath("$.errors").isArray())
                .andExpect(jsonPath("$.errors.length()").value(3));
    }
}
```

## 다음 단계

Validation을 배웠습니다. 이제 실습 프로젝트로 넘어갑니다!

👉 [다음: 실습 - 프로젝트 생성](../02-practice/lab01-project-creation.md)

## 참고 자료

- [Bean Validation 2.0 (JSR-380)](https://beanvalidation.org/2.0/)
- [Spring Validation](https://docs.spring.io/spring-framework/reference/core/validation/beanvalidation.html)
- [Hibernate Validator](https://hibernate.org/validator/)
