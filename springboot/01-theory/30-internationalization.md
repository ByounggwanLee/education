# 다국어 처리 (i18n)

Spring Boot에서 다국어 지원(Internationalization)을 구현하는 방법을 알아봅니다.

## 다국어 처리란?

**i18n (Internationalization):** 소프트웨어를 여러 언어와 지역에 맞게 쉽게 변경할 수 있도록 설계하는 것

**L10n (Localization):** 특정 언어와 지역에 맞게 소프트웨어를 실제로 적용하는 것

## Spring Boot에서의 i18n

Spring Boot는 `MessageSource`를 통해 다국어 처리를 지원합니다.

### 기본 설정

`application.yml`:
```yaml
spring:
  messages:
    basename: messages  # 메시지 파일 이름
    encoding: UTF-8     # 인코딩
    cache-duration: 3600  # 캐시 시간 (초)
```

### 메시지 파일 생성

`src/main/resources/` 디렉토리에 생성:

```
resources/
├── messages.properties          # 기본 (fallback)
├── messages_ko.properties       # 한국어
├── messages_en.properties       # 영어
├── messages_ja.properties       # 일본어
└── messages_zh.properties       # 중국어
```

## 메시지 파일 작성

### messages.properties (기본)

```properties
# 사용자 관련
user.not.found=User not found
user.created=User created successfully
user.updated=User updated successfully
user.deleted=User deleted successfully
user.email.duplicated=Email already exists

# 검증 메시지
validation.required={0} is required
validation.email.invalid=Invalid email format
validation.size={0} must be between {1} and {2} characters
validation.min={0} must be at least {1}
validation.max={0} must be at most {1}

# 에러 메시지
error.internal=Internal server error
error.bad.request=Bad request
error.unauthorized=Unauthorized
error.forbidden=Forbidden
error.not.found=Not found
```

### messages_ko.properties (한국어)

```properties
# 사용자 관련
user.not.found=사용자를 찾을 수 없습니다
user.created=사용자가 생성되었습니다
user.updated=사용자가 수정되었습니다
user.deleted=사용자가 삭제되었습니다
user.email.duplicated=이미 사용 중인 이메일입니다

# 검증 메시지
validation.required={0}은(는) 필수입니다
validation.email.invalid=올바른 이메일 형식이 아닙니다
validation.size={0}은(는) {1}자에서 {2}자 사이여야 합니다
validation.min={0}은(는) 최소 {1}이어야 합니다
validation.max={0}은(는) 최대 {1}이어야 합니다

# 에러 메시지
error.internal=서버 내부 오류가 발생했습니다
error.bad.request=잘못된 요청입니다
error.unauthorized=인증이 필요합니다
error.forbidden=접근 권한이 없습니다
error.not.found=요청한 리소스를 찾을 수 없습니다
```

### messages_en.properties (영어)

```properties
# 사용자 관련
user.not.found=User not found
user.created=User created successfully
user.updated=User updated successfully
user.deleted=User deleted successfully
user.email.duplicated=Email already exists

# 검증 메시지
validation.required={0} is required
validation.email.invalid=Invalid email format
validation.size={0} must be between {1} and {2} characters
validation.min={0} must be at least {1}
validation.max={0} must be at most {1}

# 에러 메시지
error.internal=Internal server error
error.bad.request=Bad request
error.unauthorized=Unauthorized
error.forbidden=Forbidden
error.not.found=Resource not found
```

## MessageSource 설정

### Config 클래스

```java
package com.example.demo.config;

import org.springframework.context.MessageSource;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.support.ReloadableResourceBundleMessageSource;
import org.springframework.web.servlet.LocaleResolver;
import org.springframework.web.servlet.i18n.AcceptHeaderLocaleResolver;
import org.springframework.web.servlet.i18n.LocaleChangeInterceptor;

import java.util.Locale;

@Configuration
public class I18nConfig {
    
    /**
     * MessageSource 설정
     */
    @Bean
    public MessageSource messageSource() {
        ReloadableResourceBundleMessageSource messageSource = 
                new ReloadableResourceBundleMessageSource();
        
        messageSource.setBasename("classpath:messages");
        messageSource.setDefaultEncoding("UTF-8");
        messageSource.setCacheSeconds(3600);  // 1시간 캐시
        messageSource.setDefaultLocale(Locale.KOREAN);
        
        return messageSource;
    }
    
    /**
     * LocaleResolver 설정
     * Accept-Language 헤더에서 로케일 추출
     */
    @Bean
    public LocaleResolver localeResolver() {
        AcceptHeaderLocaleResolver localeResolver = new AcceptHeaderLocaleResolver();
        localeResolver.setDefaultLocale(Locale.KOREAN);
        localeResolver.setSupportedLocales(List.of(
                Locale.KOREAN,
                Locale.ENGLISH,
                Locale.JAPANESE,
                Locale.CHINESE
        ));
        return localeResolver;
    }
    
    /**
     * 쿼리 파라미터로 로케일 변경 (선택사항)
     * 예: ?lang=en
     */
    @Bean
    public LocaleChangeInterceptor localeChangeInterceptor() {
        LocaleChangeInterceptor interceptor = new LocaleChangeInterceptor();
        interceptor.setParamName("lang");
        return interceptor;
    }
}
```

### WebMvcConfigurer 등록

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {
    
    private final LocaleChangeInterceptor localeChangeInterceptor;
    
    public WebConfig(LocaleChangeInterceptor localeChangeInterceptor) {
        this.localeChangeInterceptor = localeChangeInterceptor;
    }
    
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(localeChangeInterceptor);
    }
}
```

## LocaleResolver 전략

### 1. AcceptHeaderLocaleResolver (기본, 권장)

HTTP `Accept-Language` 헤더에서 로케일 추출

```java
@Bean
public LocaleResolver localeResolver() {
    AcceptHeaderLocaleResolver resolver = new AcceptHeaderLocaleResolver();
    resolver.setDefaultLocale(Locale.KOREAN);
    return resolver;
}
```

**요청 예시:**
```http
GET /api/v1/users
Accept-Language: ko-KR
```

### 2. SessionLocaleResolver

세션에 로케일 저장

```java
@Bean
public LocaleResolver localeResolver() {
    SessionLocaleResolver resolver = new SessionLocaleResolver();
    resolver.setDefaultLocale(Locale.KOREAN);
    return resolver;
}
```

### 3. CookieLocaleResolver

쿠키에 로케일 저장

```java
@Bean
public LocaleResolver localeResolver() {
    CookieLocaleResolver resolver = new CookieLocaleResolver();
    resolver.setDefaultLocale(Locale.KOREAN);
    resolver.setCookieName("lang");
    resolver.setCookieMaxAge(3600);
    return resolver;
}
```

## MessageSource 사용

### Service에서 사용

```java
@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {
    
    private final UserRepository userRepository;
    private final MessageSource messageSource;
    
    @Override
    public UserResponse createUser(UserCreateRequest request) {
        // 이메일 중복 체크
        if (userRepository.existsByEmail(request.getEmail())) {
            String message = messageSource.getMessage(
                    "user.email.duplicated",
                    null,
                    LocaleContextHolder.getLocale()
            );
            throw new BusinessException(ErrorCode.EMAIL_DUPLICATED, message);
        }
        
        // 사용자 생성...
        
        return response;
    }
}
```

### Controller에서 사용

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {
    
    private final UserService userService;
    private final MessageSource messageSource;
    
    @PostMapping
    public ResponseEntity<ApiResponse<UserResponse>> createUser(
            @Valid @RequestBody UserCreateRequest request) {
        
        UserResponse user = userService.createUser(request);
        
        String message = messageSource.getMessage(
                "user.created",
                null,
                LocaleContextHolder.getLocale()
        );
        
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success(message, user));
    }
}
```

### Exception Handler에서 사용

```java
@RestControllerAdvice
@RequiredArgsConstructor
public class GlobalExceptionHandler {
    
    private final MessageSource messageSource;
    
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(
            BusinessException ex,
            HttpServletRequest request) {
        
        Locale locale = LocaleContextHolder.getLocale();
        
        String message = messageSource.getMessage(
                ex.getErrorCode().getMessageKey(),
                ex.getArgs(),
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
}
```

## MessageHelper 유틸리티

### 편의 클래스 작성

```java
package com.example.demo.common.util;

import lombok.RequiredArgsConstructor;
import org.springframework.context.MessageSource;
import org.springframework.context.i18n.LocaleContextHolder;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class MessageHelper {
    
    private final MessageSource messageSource;
    
    /**
     * 메시지 조회
     */
    public String getMessage(String code) {
        return messageSource.getMessage(
                code,
                null,
                LocaleContextHolder.getLocale()
        );
    }
    
    /**
     * 파라미터가 있는 메시지 조회
     */
    public String getMessage(String code, Object... args) {
        return messageSource.getMessage(
                code,
                args,
                LocaleContextHolder.getLocale()
        );
    }
    
    /**
     * 기본 메시지와 함께 조회
     */
    public String getMessage(String code, String defaultMessage, Object... args) {
        return messageSource.getMessage(
                code,
                args,
                defaultMessage,
                LocaleContextHolder.getLocale()
        );
    }
    
    /**
     * 현재 로케일 조회
     */
    public String getCurrentLocale() {
        return LocaleContextHolder.getLocale().toString();
    }
}
```

### 사용 예시

```java
@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {
    
    private final MessageHelper messageHelper;
    
    @Override
    public UserResponse createUser(UserCreateRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new BusinessException(
                    ErrorCode.EMAIL_DUPLICATED,
                    messageHelper.getMessage("user.email.duplicated")
            );
        }
        
        // ...
    }
}
```

## Validation 메시지 다국어화

### DTO에서 메시지 키 사용

```java
@Getter
@Setter
public class UserCreateRequest {
    
    @NotBlank(message = "{validation.required}")
    @Size(min = 2, max = 50, message = "{validation.size}")
    private String name;
    
    @NotBlank(message = "{validation.required}")
    @Email(message = "{validation.email.invalid}")
    private String email;
    
    @NotNull(message = "{validation.required}")
    @Min(value = 0, message = "{validation.min}")
    @Max(value = 150, message = "{validation.max}")
    private Integer age;
}
```

### ValidationMessages.properties

Spring Boot는 `ValidationMessages.properties`도 지원합니다.

`src/main/resources/ValidationMessages.properties`:
```properties
validation.required={0}은(는) 필수입니다
validation.email.invalid=올바른 이메일 형식이 아닙니다
validation.size={0}은(는) {min}자에서 {max}자 사이여야 합니다
```

## ErrorCode 다국어화

### ErrorCode enum

```java
package com.example.demo.exception;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;

@Getter
@RequiredArgsConstructor
public enum ErrorCode {
    
    // User
    USER_NOT_FOUND("USER_NOT_FOUND", "user.not.found", HttpStatus.NOT_FOUND),
    EMAIL_DUPLICATED("EMAIL_DUPLICATED", "user.email.duplicated", HttpStatus.CONFLICT),
    
    // Common
    INTERNAL_SERVER_ERROR("INTERNAL_SERVER_ERROR", "error.internal", HttpStatus.INTERNAL_SERVER_ERROR),
    BAD_REQUEST("BAD_REQUEST", "error.bad.request", HttpStatus.BAD_REQUEST),
    UNAUTHORIZED("UNAUTHORIZED", "error.unauthorized", HttpStatus.UNAUTHORIZED),
    FORBIDDEN("FORBIDDEN", "error.forbidden", HttpStatus.FORBIDDEN);
    
    private final String code;
    private final String messageKey;  // 메시지 파일의 키
    private final HttpStatus status;
}
```

### 사용

```java
@ExceptionHandler(BusinessException.class)
public ResponseEntity<ErrorResponse> handleBusinessException(BusinessException ex) {
    String message = messageHelper.getMessage(
            ex.getErrorCode().getMessageKey(),
            ex.getArgs()
    );
    
    ErrorResponse error = ErrorResponse.builder()
            .code(ex.getErrorCode().getCode())
            .message(message)
            .build();
    
    return ResponseEntity.status(ex.getErrorCode().getStatus()).body(error);
}
```

## API 응답 예시

### 한국어 요청

```http
GET /api/v1/users/999
Accept-Language: ko-KR
```

**응답:**
```json
{
    "success": false,
    "code": "USER_NOT_FOUND",
    "message": "사용자를 찾을 수 없습니다",
    "timestamp": "2025-11-22T10:30:00"
}
```

### 영어 요청

```http
GET /api/v1/users/999
Accept-Language: en-US
```

**응답:**
```json
{
    "success": false,
    "code": "USER_NOT_FOUND",
    "message": "User not found",
    "timestamp": "2025-11-22T10:30:00"
}
```

## 동적 메시지 파라미터

### 메시지 파일

```properties
# messages_ko.properties
user.welcome=환영합니다, {0}님!
order.total={0}개의 상품, 총 {1}원

# messages_en.properties
user.welcome=Welcome, {0}!
order.total={0} items, total {1} USD
```

### 사용

```java
// 한국어: "환영합니다, 홍길동님!"
String message = messageHelper.getMessage("user.welcome", "홍길동");

// 영어: "Welcome, John!"
String message = messageHelper.getMessage("user.welcome", "John");

// 여러 파라미터
String message = messageHelper.getMessage("order.total", 5, 50000);
// 한국어: "5개의 상품, 총 50000원"
// 영어: "5 items, total 50000 USD"
```

## 테스트

### MessageSource 테스트

```java
@SpringBootTest
class MessageSourceTest {
    
    @Autowired
    private MessageSource messageSource;
    
    @Test
    void testKoreanMessage() {
        String message = messageSource.getMessage(
                "user.not.found",
                null,
                Locale.KOREAN
        );
        
        assertThat(message).isEqualTo("사용자를 찾을 수 없습니다");
    }
    
    @Test
    void testEnglishMessage() {
        String message = messageSource.getMessage(
                "user.not.found",
                null,
                Locale.ENGLISH
        );
        
        assertThat(message).isEqualTo("User not found");
    }
    
    @Test
    void testMessageWithParameters() {
        String message = messageSource.getMessage(
                "user.welcome",
                new Object[]{"홍길동"},
                Locale.KOREAN
        );
        
        assertThat(message).isEqualTo("환영합니다, 홍길동님!");
    }
}
```

### Controller 테스트

```java
@WebMvcTest(UserController.class)
class UserControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    void getUserNotFound_Korean() throws Exception {
        mockMvc.perform(get("/api/v1/users/999")
                        .header("Accept-Language", "ko-KR"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.message").value("사용자를 찾을 수 없습니다"));
    }
    
    @Test
    void getUserNotFound_English() throws Exception {
        mockMvc.perform(get("/api/v1/users/999")
                        .header("Accept-Language", "en-US"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.message").value("User not found"));
    }
}
```

## 실전 팁

### 1. 메시지 키 네이밍 컨벤션

```properties
# 도메인.동작.상태
user.create.success=사용자가 생성되었습니다
user.update.success=사용자가 수정되었습니다
user.delete.success=사용자가 삭제되었습니다
user.find.not.found=사용자를 찾을 수 없습니다

# 도메인.필드.에러
user.email.required=이메일은 필수입니다
user.email.invalid=올바른 이메일 형식이 아닙니다
user.email.duplicated=이미 사용 중인 이메일입니다
```

### 2. 기본 로케일 설정

```yaml
spring:
  messages:
    basename: messages
    encoding: UTF-8
  web:
    locale: ko_KR  # 기본 로케일
```

### 3. 메시지 파일 Hot Reload

개발 환경에서 메시지 변경 시 재시작 없이 반영:

```yaml
spring:
  messages:
    cache-duration: 0  # 캐시 비활성화 (개발 환경만)
```

### 4. 누락된 메시지 처리

```java
@Bean
public MessageSource messageSource() {
    ReloadableResourceBundleMessageSource messageSource = 
            new ReloadableResourceBundleMessageSource();
    
    messageSource.setBasename("classpath:messages");
    messageSource.setDefaultEncoding("UTF-8");
    messageSource.setUseCodeAsDefaultMessage(true);  // 키를 기본 메시지로 사용
    
    return messageSource;
}
```

## 다음 단계

다국어 처리를 구현했습니다. 이제 검증(Validation)을 자세히 알아봅시다.

👉 [다음: Validation](31-validation.md)

## 참고 자료

- [Spring Boot Internationalization](https://spring.io/guides/gs/serving-web-content/)
- [MessageSource Documentation](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/MessageSource.html)
- [Locale Resolution](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet/localeresolver.html)
