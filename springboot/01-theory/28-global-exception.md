# GlobalExceptionHandler

전역 예외 처리를 통해 일관된 에러 응답을 제공하는 방법을 알아봅니다.

## 전역 예외 처리의 필요성

### 문제 상황

**각 Controller에서 예외 처리:**
```java
@RestController
public class UserController {
    
    @GetMapping("/{id}")
    public ResponseEntity<?> getUser(@PathVariable Long id) {
        try {
            return ResponseEntity.ok(userService.getUser(id));
        } catch (UserNotFoundException e) {
            return ResponseEntity.notFound().build();
        } catch (Exception e) {
            return ResponseEntity.status(500).body("서버 오류");
        }
    }
}
```

**문제점:**
- ❌ 코드 중복
- ❌ 일관성 없는 에러 응답
- ❌ 유지보수 어려움
- ❌ 비즈니스 로직과 예외 처리 섞임

## @ControllerAdvice

모든 Controller의 예외를 한 곳에서 처리합니다.

### 기본 구조

```java
package com.example.demo.exception;

import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    // 특정 예외 처리
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException ex) {
        log.error("User not found: {}", ex.getMessage());
        
        ErrorResponse error = ErrorResponse.builder()
                .code("USER_NOT_FOUND")
                .message(ex.getMessage())
                .build();
        
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }
    
    // 모든 예외 처리 (최종 방어선)
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(Exception ex) {
        log.error("Unexpected error occurred", ex);
        
        ErrorResponse error = ErrorResponse.builder()
                .code("INTERNAL_SERVER_ERROR")
                .message("서버 내부 오류가 발생했습니다")
                .build();
        
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

## ErrorResponse 클래스

### 기본 ErrorResponse

```java
package com.example.demo.exception;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;
import java.util.List;

@Getter
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ErrorResponse {
    
    private final String code;           // 에러 코드
    private final String message;        // 에러 메시지
    private final LocalDateTime timestamp;  // 발생 시간
    private final String path;           // 요청 경로
    private final List<FieldError> errors;  // 필드 에러 목록 (검증 실패 시)
    
    @Getter
    @Builder
    public static class FieldError {
        private final String field;      // 필드명
        private final Object rejectedValue;  // 거부된 값
        private final String message;    // 에러 메시지
    }
    
    // 빌더 기본값 설정
    public static class ErrorResponseBuilder {
        private LocalDateTime timestamp = LocalDateTime.now();
    }
}
```

### 응답 예시

```json
{
    "code": "USER_NOT_FOUND",
    "message": "사용자를 찾을 수 없습니다",
    "timestamp": "2025-11-22T10:30:00",
    "path": "/api/v1/users/999"
}
```

## 예외 처리 패턴

### 1. 비즈니스 예외 처리

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(
            BusinessException ex,
            HttpServletRequest request) {
        
        log.warn("Business exception: {}", ex.getMessage());
        
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

### 2. 검증 실패 처리 (@Valid)

```java
@ExceptionHandler(MethodArgumentNotValidException.class)
public ResponseEntity<ErrorResponse> handleValidationException(
        MethodArgumentNotValidException ex,
        HttpServletRequest request) {
    
    log.warn("Validation failed: {}", ex.getMessage());
    
    // 필드 에러 목록 생성
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
```

**응답 예시:**
```json
{
    "code": "VALIDATION_FAILED",
    "message": "입력값 검증에 실패했습니다",
    "timestamp": "2025-11-22T10:30:00",
    "path": "/api/v1/users",
    "errors": [
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

### 3. 요청 파라미터 타입 불일치

```java
@ExceptionHandler(MethodArgumentTypeMismatchException.class)
public ResponseEntity<ErrorResponse> handleTypeMismatch(
        MethodArgumentTypeMismatchException ex,
        HttpServletRequest request) {
    
    String message = String.format("'%s' 파라미터의 값 '%s'은(는) %s 타입이 아닙니다",
            ex.getName(), ex.getValue(), ex.getRequiredType().getSimpleName());
    
    ErrorResponse error = ErrorResponse.builder()
            .code("TYPE_MISMATCH")
            .message(message)
            .path(request.getRequestURI())
            .build();
    
    return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
}
```

### 4. HTTP 메서드 불일치

```java
@ExceptionHandler(HttpRequestMethodNotSupportedException.class)
public ResponseEntity<ErrorResponse> handleMethodNotSupported(
        HttpRequestMethodNotSupportedException ex,
        HttpServletRequest request) {
    
    String message = String.format("%s 메서드는 지원하지 않습니다. 지원하는 메서드: %s",
            ex.getMethod(), String.join(", ", ex.getSupportedMethods()));
    
    ErrorResponse error = ErrorResponse.builder()
            .code("METHOD_NOT_ALLOWED")
            .message(message)
            .path(request.getRequestURI())
            .build();
    
    return ResponseEntity.status(HttpStatus.METHOD_NOT_ALLOWED).body(error);
}
```

### 5. 요청 본문 누락

```java
@ExceptionHandler(HttpMessageNotReadableException.class)
public ResponseEntity<ErrorResponse> handleMessageNotReadable(
        HttpMessageNotReadableException ex,
        HttpServletRequest request) {
    
    ErrorResponse error = ErrorResponse.builder()
            .code("MESSAGE_NOT_READABLE")
            .message("요청 본문을 읽을 수 없습니다. JSON 형식을 확인해주세요")
            .path(request.getRequestURI())
            .build();
    
    return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
}
```

### 6. 데이터베이스 제약 조건 위반

```java
@ExceptionHandler(DataIntegrityViolationException.class)
public ResponseEntity<ErrorResponse> handleDataIntegrityViolation(
        DataIntegrityViolationException ex,
        HttpServletRequest request) {
    
    log.error("Data integrity violation", ex);
    
    ErrorResponse error = ErrorResponse.builder()
            .code("DATA_INTEGRITY_VIOLATION")
            .message("데이터 무결성 제약 조건을 위반했습니다")
            .path(request.getRequestURI())
            .build();
    
    return ResponseEntity.status(HttpStatus.CONFLICT).body(error);
}
```

### 7. 인증/인가 실패

```java
@ExceptionHandler(AccessDeniedException.class)
public ResponseEntity<ErrorResponse> handleAccessDenied(
        AccessDeniedException ex,
        HttpServletRequest request) {
    
    log.warn("Access denied: {}", ex.getMessage());
    
    ErrorResponse error = ErrorResponse.builder()
            .code("ACCESS_DENIED")
            .message("접근 권한이 없습니다")
            .path(request.getRequestURI())
            .build();
    
    return ResponseEntity.status(HttpStatus.FORBIDDEN).body(error);
}
```

## 완전한 GlobalExceptionHandler

```java
package com.example.demo.exception;

import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.validation.FieldError;
import org.springframework.web.HttpRequestMethodNotSupportedException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;

import java.util.List;

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    /**
     * 비즈니스 예외 처리
     */
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(
            BusinessException ex,
            HttpServletRequest request) {
        
        log.warn("Business exception: {}", ex.getMessage());
        
        ErrorResponse error = ErrorResponse.builder()
                .code(ex.getErrorCode().getCode())
                .message(ex.getErrorCode().getMessage())
                .path(request.getRequestURI())
                .build();
        
        return ResponseEntity
                .status(ex.getErrorCode().getStatus())
                .body(error);
    }
    
    /**
     * @Valid 검증 실패
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
            MethodArgumentNotValidException ex,
            HttpServletRequest request) {
        
        log.warn("Validation failed: {}", ex.getMessage());
        
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
     * 타입 불일치
     */
    @ExceptionHandler(MethodArgumentTypeMismatchException.class)
    public ResponseEntity<ErrorResponse> handleTypeMismatch(
            MethodArgumentTypeMismatchException ex,
            HttpServletRequest request) {
        
        String message = String.format("'%s' 파라미터의 값 '%s'은(는) %s 타입이 아닙니다",
                ex.getName(), ex.getValue(), ex.getRequiredType().getSimpleName());
        
        ErrorResponse error = ErrorResponse.builder()
                .code("TYPE_MISMATCH")
                .message(message)
                .path(request.getRequestURI())
                .build();
        
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }
    
    /**
     * HTTP 메서드 불일치
     */
    @ExceptionHandler(HttpRequestMethodNotSupportedException.class)
    public ResponseEntity<ErrorResponse> handleMethodNotSupported(
            HttpRequestMethodNotSupportedException ex,
            HttpServletRequest request) {
        
        String message = String.format("%s 메서드는 지원하지 않습니다",
                ex.getMethod());
        
        ErrorResponse error = ErrorResponse.builder()
                .code("METHOD_NOT_ALLOWED")
                .message(message)
                .path(request.getRequestURI())
                .build();
        
        return ResponseEntity.status(HttpStatus.METHOD_NOT_ALLOWED).body(error);
    }
    
    /**
     * 요청 본문 읽기 실패
     */
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorResponse> handleMessageNotReadable(
            HttpMessageNotReadableException ex,
            HttpServletRequest request) {
        
        ErrorResponse error = ErrorResponse.builder()
                .code("MESSAGE_NOT_READABLE")
                .message("요청 본문을 읽을 수 없습니다. JSON 형식을 확인해주세요")
                .path(request.getRequestURI())
                .build();
        
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }
    
    /**
     * 데이터 무결성 위반
     */
    @ExceptionHandler(DataIntegrityViolationException.class)
    public ResponseEntity<ErrorResponse> handleDataIntegrityViolation(
            DataIntegrityViolationException ex,
            HttpServletRequest request) {
        
        log.error("Data integrity violation", ex);
        
        ErrorResponse error = ErrorResponse.builder()
                .code("DATA_INTEGRITY_VIOLATION")
                .message("데이터 무결성 제약 조건을 위반했습니다")
                .path(request.getRequestURI())
                .build();
        
        return ResponseEntity.status(HttpStatus.CONFLICT).body(error);
    }
    
    /**
     * 접근 거부
     */
    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<ErrorResponse> handleAccessDenied(
            AccessDeniedException ex,
            HttpServletRequest request) {
        
        log.warn("Access denied: {}", ex.getMessage());
        
        ErrorResponse error = ErrorResponse.builder()
                .code("ACCESS_DENIED")
                .message("접근 권한이 없습니다")
                .path(request.getRequestURI())
                .build();
        
        return ResponseEntity.status(HttpStatus.FORBIDDEN).body(error);
    }
    
    /**
     * 그 외 모든 예외 (최종 방어선)
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(
            Exception ex,
            HttpServletRequest request) {
        
        log.error("Unexpected error occurred", ex);
        
        ErrorResponse error = ErrorResponse.builder()
                .code("INTERNAL_SERVER_ERROR")
                .message("서버 내부 오류가 발생했습니다")
                .path(request.getRequestURI())
                .build();
        
        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(error);
    }
}
```

## 환경별 에러 응답

### 개발 환경: 상세한 에러 정보

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @Value("${spring.profiles.active:local}")
    private String activeProfile;
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(
            Exception ex,
            HttpServletRequest request) {
        
        log.error("Unexpected error occurred", ex);
        
        ErrorResponse.ErrorResponseBuilder builder = ErrorResponse.builder()
                .code("INTERNAL_SERVER_ERROR")
                .message("서버 내부 오류가 발생했습니다")
                .path(request.getRequestURI());
        
        // 개발 환경에서만 상세 정보 포함
        if ("local".equals(activeProfile) || "dev".equals(activeProfile)) {
            builder.detail(ex.getMessage())
                   .stackTrace(getStackTrace(ex));
        }
        
        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(builder.build());
    }
    
    private String getStackTrace(Exception ex) {
        StringWriter sw = new StringWriter();
        ex.printStackTrace(new PrintWriter(sw));
        return sw.toString();
    }
}
```

## @ExceptionHandler 우선순위

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    // 1순위: 가장 구체적인 예외
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<?> handleUserNotFound(UserNotFoundException ex) {
        // UserNotFoundException 처리
    }
    
    // 2순위: 부모 예외
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<?> handleBusinessException(BusinessException ex) {
        // BusinessException 및 하위 예외 처리
    }
    
    // 3순위: 최상위 예외 (최종 방어선)
    @ExceptionHandler(Exception.class)
    public ResponseEntity<?> handleException(Exception ex) {
        // 모든 예외 처리
    }
}
```

## ResponseEntityExceptionHandler 상속

Spring이 제공하는 기본 예외 처리를 확장할 수 있습니다.

```java
@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {
    
    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(
            MethodArgumentNotValidException ex,
            HttpHeaders headers,
            HttpStatusCode status,
            WebRequest request) {
        
        // 커스텀 처리
        ErrorResponse error = createValidationErrorResponse(ex);
        
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }
    
    // 다른 Spring 기본 예외들도 오버라이드 가능
}
```

## 테스트

### GlobalExceptionHandler 테스트

```java
@WebMvcTest(UserController.class)
class GlobalExceptionHandlerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private UserService userService;
    
    @Test
    void handleUserNotFoundException() throws Exception {
        // given
        given(userService.getUser(999L))
                .willThrow(new UserNotFoundException("사용자를 찾을 수 없습니다"));
        
        // when & then
        mockMvc.perform(get("/api/v1/users/999"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.code").value("USER_NOT_FOUND"))
                .andExpect(jsonPath("$.message").value("사용자를 찾을 수 없습니다"));
    }
    
    @Test
    void handleValidationException() throws Exception {
        // given
        UserCreateRequest request = new UserCreateRequest();
        request.setName("");  // 빈 이름 (검증 실패)
        request.setEmail("invalid-email");  // 잘못된 이메일
        
        // when & then
        mockMvc.perform(post("/api/v1/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("VALIDATION_FAILED"))
                .andExpect(jsonPath("$.errors").isArray());
    }
}
```

## 실전 팁

### 1. 민감한 정보 노출 방지

```java
@ExceptionHandler(Exception.class)
public ResponseEntity<ErrorResponse> handleException(Exception ex) {
    // ❌ 나쁜 예: 예외 메시지 그대로 노출
    return ResponseEntity.status(500)
            .body(ErrorResponse.builder()
                    .message(ex.getMessage())  // SQL 쿼리, 파일 경로 등 노출 위험
                    .build());
    
    // ✅ 좋은 예: 일반적인 메시지
    return ResponseEntity.status(500)
            .body(ErrorResponse.builder()
                    .message("서버 내부 오류가 발생했습니다")
                    .build());
}
```

### 2. 로깅 전략

```java
@ExceptionHandler(BusinessException.class)
public ResponseEntity<ErrorResponse> handleBusinessException(BusinessException ex) {
    // 비즈니스 예외는 WARN 레벨
    log.warn("Business exception: {}", ex.getMessage());
    // ...
}

@ExceptionHandler(Exception.class)
public ResponseEntity<ErrorResponse> handleException(Exception ex) {
    // 예상치 못한 예외는 ERROR 레벨 + 스택 트레이스
    log.error("Unexpected error occurred", ex);
    // ...
}
```

### 3. 에러 코드 일관성

```java
// ErrorCode enum 사용
public enum ErrorCode {
    USER_NOT_FOUND("USER_NOT_FOUND", "사용자를 찾을 수 없습니다", HttpStatus.NOT_FOUND),
    EMAIL_DUPLICATED("EMAIL_DUPLICATED", "이미 사용 중인 이메일입니다", HttpStatus.CONFLICT);
    
    private final String code;
    private final String message;
    private final HttpStatus status;
    
    // getter, constructor
}
```

## 다음 단계

전역 예외 처리를 구현했습니다. 이제 커스텀 예외를 설계해봅시다.

👉 [다음: 커스텀 예외 설계](29-custom-exception.md)

## 참고 자료

- [Spring Error Handling](https://spring.io/guides/tutorials/rest/)
- [Exception Handling in Spring Boot](https://www.baeldung.com/exception-handling-for-rest-with-spring)
