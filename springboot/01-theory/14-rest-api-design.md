# REST API 설계

RESTful API 설계 원칙과 모범 사례를 알아봅니다.

## REST란?

**REST (Representational State Transfer):** HTTP 프로토콜을 활용한 아키텍처 스타일

### REST 원칙

1. **Client-Server:** 클라이언트와 서버의 분리
2. **Stateless:** 무상태성
3. **Cacheable:** 캐시 가능
4. **Uniform Interface:** 일관된 인터페이스
5. **Layered System:** 계층화된 시스템
6. **Code on Demand:** 선택적 코드 실행

## HTTP 메서드

### CRUD 매핑

| HTTP 메서드 | 용도 | 멱등성 | 안전성 |
|-------------|------|--------|--------|
| GET | 조회 (Read) | ✅ | ✅ |
| POST | 생성 (Create) | ❌ | ❌ |
| PUT | 전체 수정 | ✅ | ❌ |
| PATCH | 부분 수정 | ❌ | ❌ |
| DELETE | 삭제 (Delete) | ✅ | ❌ |

### 사용 예시

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    
    // GET: 목록 조회
    @GetMapping
    public ResponseEntity<List<UserResponse>> getUsers() {
        return ResponseEntity.ok(userService.getUsers());
    }
    
    // GET: 단건 조회
    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.getUser(id));
    }
    
    // POST: 생성
    @PostMapping
    public ResponseEntity<UserResponse> createUser(@Valid @RequestBody UserCreateRequest request) {
        UserResponse user = userService.createUser(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }
    
    // PUT: 전체 수정
    @PutMapping("/{id}")
    public ResponseEntity<UserResponse> updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UserUpdateRequest request) {
        return ResponseEntity.ok(userService.updateUser(id, request));
    }
    
    // PATCH: 부분 수정
    @PatchMapping("/{id}")
    public ResponseEntity<UserResponse> patchUser(
            @PathVariable Long id,
            @RequestBody Map<String, Object> updates) {
        return ResponseEntity.ok(userService.patchUser(id, updates));
    }
    
    // DELETE: 삭제
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        userService.deleteUser(id);
        return ResponseEntity.noContent().build();
    }
}
```

## URI 설계

### 리소스 중심 설계

```java
// ✅ 좋은 예: 명사 사용
GET    /api/v1/users              # 사용자 목록
GET    /api/v1/users/{id}         # 사용자 조회
POST   /api/v1/users              # 사용자 생성
PUT    /api/v1/users/{id}         # 사용자 수정
DELETE /api/v1/users/{id}         # 사용자 삭제

// ❌ 나쁜 예: 동사 사용
GET    /api/v1/getUsers
POST   /api/v1/createUser
POST   /api/v1/updateUser
POST   /api/v1/deleteUser
```

### 계층 구조

```java
// 중첩 리소스
GET    /api/v1/users/{userId}/orders              # 사용자의 주문 목록
GET    /api/v1/users/{userId}/orders/{orderId}    # 특정 주문
POST   /api/v1/users/{userId}/orders              # 주문 생성

// 컬렉션과 문서
GET    /api/v1/users                              # 컬렉션
GET    /api/v1/users/{id}                         # 문서
GET    /api/v1/users/{id}/profile                 # 하위 문서
```

### URI 규칙

```
✅ 소문자 사용: /api/v1/users
❌ 대문자 사용: /api/v1/Users

✅ 하이픈 사용: /api/v1/user-profiles
❌ 언더스코어: /api/v1/user_profiles

✅ 복수형: /api/v1/users
❌ 단수형: /api/v1/user

✅ 파일 확장자 제외: /api/v1/users/1
❌ 확장자 포함: /api/v1/users/1.json
```

## HTTP 상태 코드

### 2xx: 성공

```java
// 200 OK: 성공
@GetMapping("/{id}")
public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
    return ResponseEntity.ok(userService.getUser(id));
}

// 201 Created: 생성 성공
@PostMapping
public ResponseEntity<UserResponse> createUser(@RequestBody UserCreateRequest request) {
    UserResponse user = userService.createUser(request);
    URI location = URI.create("/api/v1/users/" + user.getId());
    return ResponseEntity.created(location).body(user);
}

// 204 No Content: 성공, 응답 본문 없음
@DeleteMapping("/{id}")
public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
    userService.deleteUser(id);
    return ResponseEntity.noContent().build();
}
```

### 4xx: 클라이언트 오류

```java
// 400 Bad Request: 잘못된 요청
// 401 Unauthorized: 인증 필요
// 403 Forbidden: 권한 없음
// 404 Not Found: 리소스 없음
// 409 Conflict: 충돌 (중복 등)
// 422 Unprocessable Entity: 검증 실패

@ExceptionHandler(UserNotFoundException.class)
public ResponseEntity<ErrorResponse> handleNotFound(UserNotFoundException e) {
    return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse("USER_NOT_FOUND", e.getMessage()));
}
```

### 5xx: 서버 오류

```java
// 500 Internal Server Error: 서버 오류
// 503 Service Unavailable: 서비스 이용 불가

@ExceptionHandler(Exception.class)
public ResponseEntity<ErrorResponse> handleException(Exception e) {
    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(new ErrorResponse("INTERNAL_ERROR", "서버 오류"));
}
```

## 응답 포맷

### 성공 응답

```java
@Getter
@Builder
public class ApiResponse<T> {
    private boolean success;
    private String message;
    private T data;
    private LocalDateTime timestamp;
    
    public static <T> ApiResponse<T> success(T data) {
        return ApiResponse.<T>builder()
                .success(true)
                .data(data)
                .timestamp(LocalDateTime.now())
                .build();
    }
    
    public static <T> ApiResponse<T> success(String message, T data) {
        return ApiResponse.<T>builder()
                .success(true)
                .message(message)
                .data(data)
                .timestamp(LocalDateTime.now())
                .build();
    }
}
```

**응답 예시:**
```json
{
    "success": true,
    "message": "사용자 조회 성공",
    "data": {
        "id": 1,
        "name": "홍길동",
        "email": "hong@example.com"
    },
    "timestamp": "2025-11-22T10:30:00"
}
```

### 에러 응답

```java
@Getter
@Builder
public class ErrorResponse {
    private boolean success;
    private String code;
    private String message;
    private List<FieldError> errors;
    private String path;
    private LocalDateTime timestamp;
    
    @Getter
    @Builder
    public static class FieldError {
        private String field;
        private Object rejectedValue;
        private String message;
    }
}
```

**에러 응답 예시:**
```json
{
    "success": false,
    "code": "VALIDATION_FAILED",
    "message": "입력값 검증 실패",
    "errors": [
        {
            "field": "email",
            "rejectedValue": "invalid-email",
            "message": "올바른 이메일 형식이 아닙니다"
        }
    ],
    "path": "/api/v1/users",
    "timestamp": "2025-11-22T10:30:00"
}
```

## 페이징

### 페이징 파라미터

```java
@GetMapping
public ResponseEntity<Page<UserResponse>> getUsers(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size,
        @RequestParam(defaultValue = "id,desc") String[] sort) {
    
    Sort sortObj = Sort.by(
        sort[1].equals("asc") ? Sort.Direction.ASC : Sort.Direction.DESC,
        sort[0]
    );
    Pageable pageable = PageRequest.of(page, size, sortObj);
    
    return ResponseEntity.ok(userService.getUsers(pageable));
}
```

### 페이징 응답

```json
{
    "content": [
        {
            "id": 1,
            "name": "홍길동",
            "email": "hong@example.com"
        }
    ],
    "pageable": {
        "pageNumber": 0,
        "pageSize": 20,
        "sort": {
            "sorted": true,
            "unsorted": false
        }
    },
    "totalPages": 5,
    "totalElements": 100,
    "last": false,
    "first": true,
    "size": 20,
    "number": 0
}
```

## 검색 및 필터링

### 쿼리 파라미터

```java
@GetMapping("/search")
public ResponseEntity<List<UserResponse>> searchUsers(
        @RequestParam(required = false) String name,
        @RequestParam(required = false) String email,
        @RequestParam(required = false) UserStatus status,
        @RequestParam(required = false) Integer minAge,
        @RequestParam(required = false) Integer maxAge) {
    
    UserSearchCondition condition = UserSearchCondition.builder()
            .name(name)
            .email(email)
            .status(status)
            .minAge(minAge)
            .maxAge(maxAge)
            .build();
    
    return ResponseEntity.ok(userService.search(condition));
}
```

**요청 예시:**
```
GET /api/v1/users/search?name=홍&status=ACTIVE&minAge=20&maxAge=30
```

## 버전 관리

### URI 버전

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserV1Controller {
    // v1 API
}

@RestController
@RequestMapping("/api/v2/users")
public class UserV2Controller {
    // v2 API
}
```

### 헤더 버전

```java
@GetMapping(value = "/users", headers = "API-Version=1")
public List<UserResponse> getUsersV1() {
    // v1
}

@GetMapping(value = "/users", headers = "API-Version=2")
public List<UserResponse> getUsersV2() {
    // v2
}
```

## HATEOAS

### 링크 추가

```java
@Getter
public class UserResponse extends RepresentationModel<UserResponse> {
    private Long id;
    private String name;
    private String email;
    
    public static UserResponse from(User user) {
        UserResponse response = new UserResponse();
        response.id = user.getId();
        response.name = user.getName();
        response.email = user.getEmail();
        
        // 링크 추가
        response.add(linkTo(methodOn(UserController.class).getUser(user.getId())).withSelfRel());
        response.add(linkTo(methodOn(UserController.class).getOrders(user.getId())).withRel("orders"));
        
        return response;
    }
}
```

**응답:**
```json
{
    "id": 1,
    "name": "홍길동",
    "email": "hong@example.com",
    "_links": {
        "self": {
            "href": "http://localhost:8080/api/v1/users/1"
        },
        "orders": {
            "href": "http://localhost:8080/api/v1/users/1/orders"
        }
    }
}
```

## 실전 팁

### 1. DTO 분리

```java
// Request DTO
public class UserCreateRequest { }
public class UserUpdateRequest { }

// Response DTO
public class UserResponse { }
public class UserDetailResponse { }
```

### 2. 일관된 응답 구조

```java
// 모든 API가 동일한 구조 사용
ApiResponse<UserResponse>
ApiResponse<List<UserResponse>>
ApiResponse<Page<UserResponse>>
```

### 3. 에러 처리 표준화

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    // 모든 에러를 일관되게 처리
}
```

### 4. 문서화

```java
@Operation(summary = "사용자 조회", description = "ID로 사용자를 조회합니다")
@ApiResponses({
    @ApiResponse(responseCode = "200", description = "조회 성공"),
    @ApiResponse(responseCode = "404", description = "사용자 없음")
})
@GetMapping("/{id}")
public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
    // ...
}
```

## 다음 단계

REST API 설계를 배웠습니다. 이제 OpenAPI로 문서화를 알아봅시다.

👉 [다음: OpenAPI 문서화](15-openapi.md)

## 참고 자료

- [REST API Tutorial](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html)
