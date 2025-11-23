# Controller 레이어

Spring Boot에서 HTTP 요청을 처리하는 Controller 레이어의 역할과 구현 방법을 알아봅니다.

## Controller란?

**정의:** 클라이언트의 HTTP 요청을 받아 처리하고 응답을 반환하는 표현 계층(Presentation Layer)의 핵심 컴포넌트

**주요 책임:**
- HTTP 요청 수신 및 라우팅
- 요청 데이터 검증
- Service 계층 호출
- 응답 데이터 반환
- HTTP 상태 코드 설정

## @RestController vs @Controller

### @Controller (전통적인 MVC)

```java
@Controller
public class UserController {
    
    @GetMapping("/users")
    public String userList(Model model) {
        List<User> users = userService.getAllUsers();
        model.addAttribute("users", users);
        return "user/list";  // 뷰 이름 반환 (Thymeleaf, JSP 등)
    }
}
```

**용도:** 서버 사이드 렌더링 (SSR), View 반환

### @RestController (RESTful API)

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    
    @GetMapping
    public ResponseEntity<List<UserResponse>> getAllUsers() {
        List<UserResponse> users = userService.getAllUsers();
        return ResponseEntity.ok(users);  // JSON 응답
    }
}
```

**용도:** RESTful API, JSON/XML 응답

**@RestController = @Controller + @ResponseBody**

## 기본 구조

### 전형적인 Controller 구조

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Validated
public class UserController {
    
    // 의존성 주입
    private final UserService userService;
    
    // GET: 전체 조회
    @GetMapping
    public ResponseEntity<List<UserResponse>> getAllUsers() {
        // ...
    }
    
    // GET: 단건 조회
    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
        // ...
    }
    
    // POST: 생성
    @PostMapping
    public ResponseEntity<UserResponse> createUser(@Valid @RequestBody UserCreateRequest request) {
        // ...
    }
    
    // PUT: 전체 수정
    @PutMapping("/{id}")
    public ResponseEntity<UserResponse> updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UserUpdateRequest request) {
        // ...
    }
    
    // PATCH: 부분 수정
    @PatchMapping("/{id}")
    public ResponseEntity<UserResponse> partialUpdateUser(
            @PathVariable Long id,
            @Valid @RequestBody UserPatchRequest request) {
        // ...
    }
    
    // DELETE: 삭제
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        // ...
    }
}
```

## HTTP 메서드 매핑

### @GetMapping - 조회

```java
// 전체 조회
@GetMapping
public ResponseEntity<List<UserResponse>> getAllUsers() {
    return ResponseEntity.ok(userService.getAllUsers());
}

// 단건 조회
@GetMapping("/{id}")
public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
    return ResponseEntity.ok(userService.getUser(id));
}

// 쿼리 파라미터로 조회
@GetMapping("/search")
public ResponseEntity<List<UserResponse>> searchUsers(
        @RequestParam(required = false) String name,
        @RequestParam(required = false) String email) {
    return ResponseEntity.ok(userService.searchUsers(name, email));
}

// 페이징 조회
@GetMapping("/page")
public ResponseEntity<Page<UserResponse>> getUsersPage(
        @PageableDefault(size = 20, sort = "createdAt", direction = Sort.Direction.DESC) 
        Pageable pageable) {
    return ResponseEntity.ok(userService.getUsersPage(pageable));
}
```

### @PostMapping - 생성

```java
@PostMapping
public ResponseEntity<UserResponse> createUser(
        @Valid @RequestBody UserCreateRequest request) {
    UserResponse response = userService.createUser(request);
    
    // 201 Created 상태 코드와 Location 헤더 추가
    URI location = ServletUriComponentsBuilder
            .fromCurrentRequest()
            .path("/{id}")
            .buildAndExpand(response.getId())
            .toUri();
    
    return ResponseEntity.created(location).body(response);
}
```

### @PutMapping - 전체 수정

```java
@PutMapping("/{id}")
public ResponseEntity<UserResponse> updateUser(
        @PathVariable Long id,
        @Valid @RequestBody UserUpdateRequest request) {
    UserResponse response = userService.updateUser(id, request);
    return ResponseEntity.ok(response);
}
```

### @PatchMapping - 부분 수정

```java
@PatchMapping("/{id}")
public ResponseEntity<UserResponse> partialUpdateUser(
        @PathVariable Long id,
        @Valid @RequestBody UserPatchRequest request) {
    UserResponse response = userService.partialUpdateUser(id, request);
    return ResponseEntity.ok(response);
}
```

### @DeleteMapping - 삭제

```java
@DeleteMapping("/{id}")
public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
    userService.deleteUser(id);
    return ResponseEntity.noContent().build();  // 204 No Content
}
```

## 요청 데이터 바인딩

### @PathVariable - 경로 변수

```java
// /api/v1/users/123
@GetMapping("/{id}")
public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
    return ResponseEntity.ok(userService.getUser(id));
}

// 여러 경로 변수
// /api/v1/users/123/orders/456
@GetMapping("/{userId}/orders/{orderId}")
public ResponseEntity<OrderResponse> getUserOrder(
        @PathVariable Long userId,
        @PathVariable Long orderId) {
    return ResponseEntity.ok(orderService.getUserOrder(userId, orderId));
}

// 경로 변수 이름 명시
@GetMapping("/{id}")
public ResponseEntity<UserResponse> getUser(
        @PathVariable("id") Long userId) {  // 변수명이 다를 때
    return ResponseEntity.ok(userService.getUser(userId));
}
```

### @RequestParam - 쿼리 파라미터

```java
// /api/v1/users/search?name=홍길동&email=hong@example.com
@GetMapping("/search")
public ResponseEntity<List<UserResponse>> searchUsers(
        @RequestParam String name,
        @RequestParam String email) {
    return ResponseEntity.ok(userService.searchUsers(name, email));
}

// 선택적 파라미터
@GetMapping("/search")
public ResponseEntity<List<UserResponse>> searchUsers(
        @RequestParam(required = false) String name,
        @RequestParam(required = false) String email,
        @RequestParam(defaultValue = "10") int size) {
    return ResponseEntity.ok(userService.searchUsers(name, email, size));
}

// Map으로 모든 파라미터 받기
@GetMapping("/search")
public ResponseEntity<List<UserResponse>> searchUsers(
        @RequestParam Map<String, String> params) {
    return ResponseEntity.ok(userService.searchUsers(params));
}
```

### @RequestBody - 요청 본문

```java
@PostMapping
public ResponseEntity<UserResponse> createUser(
        @Valid @RequestBody UserCreateRequest request) {
    // request: JSON → Java Object 자동 변환
    UserResponse response = userService.createUser(request);
    return ResponseEntity.status(HttpStatus.CREATED).body(response);
}

// 여러 RequestBody는 불가능 (HTTP 명세상 하나만)
```

### @RequestHeader - HTTP 헤더

```java
@GetMapping("/{id}")
public ResponseEntity<UserResponse> getUser(
        @PathVariable Long id,
        @RequestHeader("Authorization") String token,
        @RequestHeader(value = "User-Agent", required = false) String userAgent) {
    // 헤더 값 활용
    return ResponseEntity.ok(userService.getUser(id));
}
```

### @CookieValue - 쿠키

```java
@GetMapping("/{id}")
public ResponseEntity<UserResponse> getUser(
        @PathVariable Long id,
        @CookieValue(value = "sessionId", required = false) String sessionId) {
    return ResponseEntity.ok(userService.getUser(id));
}
```

## 검증 (Validation)

### @Valid와 DTO 검증

```java
// DTO
@Getter
@Setter
public class UserCreateRequest {
    
    @NotBlank(message = "이름은 필수입니다")
    @Size(min = 2, max = 50, message = "이름은 2-50자 사이여야 합니다")
    private String name;
    
    @NotBlank(message = "이메일은 필수입니다")
    @Email(message = "올바른 이메일 형식이 아닙니다")
    private String email;
    
    @NotNull(message = "나이는 필수입니다")
    @Min(value = 0, message = "나이는 0 이상이어야 합니다")
    @Max(value = 150, message = "나이는 150 이하여야 합니다")
    private Integer age;
    
    @Pattern(regexp = "^01[0-9]{8,9}$", message = "올바른 전화번호 형식이 아닙니다")
    private String phone;
}

// Controller
@PostMapping
public ResponseEntity<UserResponse> createUser(
        @Valid @RequestBody UserCreateRequest request) {  // @Valid 필수!
    // 검증 실패 시 MethodArgumentNotValidException 발생
    return ResponseEntity.status(HttpStatus.CREATED)
            .body(userService.createUser(request));
}
```

### 검증 어노테이션

| 어노테이션 | 설명 | 예시 |
|-----------|------|------|
| `@NotNull` | null 불가 | `@NotNull private String name;` |
| `@NotBlank` | null, 빈 문자열, 공백 불가 | `@NotBlank private String name;` |
| `@NotEmpty` | null, 빈 컬렉션 불가 | `@NotEmpty private List<String> tags;` |
| `@Size` | 크기 제한 | `@Size(min=2, max=50)` |
| `@Min` / `@Max` | 최소/최대 값 | `@Min(0) @Max(150)` |
| `@Email` | 이메일 형식 | `@Email private String email;` |
| `@Pattern` | 정규식 패턴 | `@Pattern(regexp="^01[0-9]{8,9}$")` |
| `@Past` / `@Future` | 과거/미래 날짜 | `@Past private LocalDate birthDate;` |
| `@Positive` / `@Negative` | 양수/음수 | `@Positive private int price;` |

### 커스텀 검증

```java
// 커스텀 어노테이션
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = PhoneNumberValidator.class)
public @interface PhoneNumber {
    String message() default "올바른 전화번호 형식이 아닙니다";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

// Validator 구현
public class PhoneNumberValidator implements ConstraintValidator<PhoneNumber, String> {
    
    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        if (value == null) {
            return true;  // @NotNull이 처리
        }
        return value.matches("^01[0-9]{8,9}$");
    }
}

// 사용
public class UserCreateRequest {
    @PhoneNumber
    private String phone;
}
```

## ResponseEntity

### 상태 코드와 함께 응답

```java
// 200 OK
return ResponseEntity.ok(data);
return ResponseEntity.status(HttpStatus.OK).body(data);

// 201 Created
return ResponseEntity.status(HttpStatus.CREATED).body(data);
return ResponseEntity.created(location).body(data);

// 204 No Content
return ResponseEntity.noContent().build();

// 400 Bad Request
return ResponseEntity.badRequest().body(errorResponse);

// 404 Not Found
return ResponseEntity.notFound().build();

// 500 Internal Server Error
return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
```

### 헤더 추가

```java
@GetMapping("/{id}")
public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
    UserResponse response = userService.getUser(id);
    
    return ResponseEntity.ok()
            .header("X-Custom-Header", "value")
            .header(HttpHeaders.CACHE_CONTROL, "max-age=3600")
            .body(response);
}
```

### 공통 응답 래퍼

```java
// ApiResponse 클래스
@Getter
@AllArgsConstructor
public class ApiResponse<T> {
    private boolean success;
    private String message;
    private T data;
    
    public static <T> ApiResponse<T> success(T data) {
        return new ApiResponse<>(true, "Success", data);
    }
    
    public static <T> ApiResponse<T> success(String message, T data) {
        return new ApiResponse<>(true, message, data);
    }
    
    public static <T> ApiResponse<T> error(String message) {
        return new ApiResponse<>(false, message, null);
    }
}

// Controller에서 사용
@GetMapping("/{id}")
public ResponseEntity<ApiResponse<UserResponse>> getUser(@PathVariable Long id) {
    UserResponse user = userService.getUser(id);
    return ResponseEntity.ok(ApiResponse.success(user));
}

// 응답 JSON
{
    "success": true,
    "message": "Success",
    "data": {
        "id": 1,
        "name": "홍길동",
        "email": "hong@example.com"
    }
}
```

## 예외 처리

### Controller 내 예외 처리

```java
@GetMapping("/{id}")
public ResponseEntity<?> getUser(@PathVariable Long id) {
    try {
        UserResponse user = userService.getUser(id);
        return ResponseEntity.ok(user);
    } catch (UserNotFoundException e) {
        return ResponseEntity.notFound().build();
    } catch (Exception e) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
    }
}
```

**문제점:** 모든 Controller에 중복 코드 발생

### @ExceptionHandler (Controller 레벨)

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    
    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
        // 예외가 발생하면 아래 핸들러가 처리
        return ResponseEntity.ok(userService.getUser(id));
    }
    
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException e) {
        ErrorResponse error = new ErrorResponse("USER_NOT_FOUND", e.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }
}
```

**문제점:** 각 Controller마다 중복

### @ControllerAdvice (전역 예외 처리)

GlobalExceptionHandler에서 처리 (이론 28장 참조)

## 비동기 처리

### @Async

```java
@GetMapping("/async")
public CompletableFuture<ResponseEntity<List<UserResponse>>> getUsers Async() {
    return userService.getAllUsersAsync()
            .thenApply(users -> ResponseEntity.ok(users));
}
```

### DeferredResult

```java
@GetMapping("/deferred")
public DeferredResult<ResponseEntity<UserResponse>> getUser(@PathVariable Long id) {
    DeferredResult<ResponseEntity<UserResponse>> result = new DeferredResult<>(5000L);
    
    // 비동기 작업
    CompletableFuture.supplyAsync(() -> userService.getUser(id))
            .whenComplete((user, throwable) -> {
                if (throwable != null) {
                    result.setErrorResult(throwable);
                } else {
                    result.setResult(ResponseEntity.ok(user));
                }
            });
    
    return result;
}
```

## 파일 업로드/다운로드

### 파일 업로드

```java
@PostMapping("/upload")
public ResponseEntity<String> uploadFile(
        @RequestParam("file") MultipartFile file) {
    
    if (file.isEmpty()) {
        return ResponseEntity.badRequest().body("파일이 비어있습니다");
    }
    
    try {
        String fileName = fileService.storeFile(file);
        return ResponseEntity.ok("파일 업로드 성공: " + fileName);
    } catch (IOException e) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("파일 업로드 실패");
    }
}
```

### 파일 다운로드

```java
@GetMapping("/download/{fileName}")
public ResponseEntity<Resource> downloadFile(@PathVariable String fileName) {
    Resource resource = fileService.loadFileAsResource(fileName);
    
    return ResponseEntity.ok()
            .contentType(MediaType.APPLICATION_OCTET_STREAM)
            .header(HttpHeaders.CONTENT_DISPOSITION, 
                    "attachment; filename=\"" + resource.getFilename() + "\"")
            .body(resource);
}
```

## 다음 단계

Controller 레이어를 이해했습니다. 이제 비즈니스 로직을 처리하는 Service 레이어를 알아봅시다.

👉 [다음: Service 레이어](07-service.md)

## 참고 자료

- [Spring MVC Reference](https://docs.spring.io/spring-framework/reference/web/webmvc.html)
- [Spring Boot REST API](https://spring.io/guides/tutorials/rest/)
- [Bean Validation](https://beanvalidation.org/)
