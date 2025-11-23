# OpenAPI 문서화

SpringDoc OpenAPI를 사용하여 REST API를 자동으로 문서화하는 방법을 알아봅니다.

## OpenAPI란?

**OpenAPI (구 Swagger):** REST API를 설명하는 표준 명세

### 장점

- ✅ API 자동 문서화
- ✅ 대화형 테스트 UI (Swagger UI)
- ✅ 클라이언트 코드 자동 생성
- ✅ API 표준화

## 의존성 추가

### Maven

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.3.0</version>
</dependency>
```

### Gradle

```gradle
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.3.0'
```

## 기본 설정

### application.yml

```yaml
springdoc:
  api-docs:
    path: /api-docs                    # OpenAPI JSON 경로
    enabled: true
  swagger-ui:
    path: /swagger-ui.html             # Swagger UI 경로
    tags-sorter: alpha                 # 태그 정렬
    operations-sorter: alpha           # 작업 정렬
    display-request-duration: true     # 요청 시간 표시
    doc-expansion: none                # 기본 확장 상태
  default-consumes-media-type: application/json
  default-produces-media-type: application/json
```

**접속:**
- Swagger UI: `http://localhost:8080/swagger-ui.html`
- OpenAPI JSON: `http://localhost:8080/api-docs`

## OpenAPI 설정

### Config 클래스

```java
@Configuration
public class OpenApiConfig {
    
    @Bean
    public OpenAPI openAPI() {
        return new OpenAPI()
                .info(apiInfo())
                .servers(servers())
                .components(securityComponents())
                .addSecurityItem(securityRequirement());
    }
    
    private Info apiInfo() {
        return new Info()
                .title("사용자 관리 API")
                .description("Spring Boot REST API 문서")
                .version("v1.0.0")
                .contact(new Contact()
                        .name("개발팀")
                        .email("dev@example.com")
                        .url("https://example.com"))
                .license(new License()
                        .name("Apache 2.0")
                        .url("https://www.apache.org/licenses/LICENSE-2.0"));
    }
    
    private List<Server> servers() {
        return List.of(
                new Server()
                        .url("http://localhost:8080")
                        .description("로컬 서버"),
                new Server()
                        .url("https://dev.example.com")
                        .description("개발 서버"),
                new Server()
                        .url("https://api.example.com")
                        .description("운영 서버")
        );
    }
    
    private Components securityComponents() {
        return new Components()
                .addSecuritySchemes("bearerAuth",
                        new SecurityScheme()
                                .type(SecurityScheme.Type.HTTP)
                                .scheme("bearer")
                                .bearerFormat("JWT")
                                .description("JWT 토큰을 입력하세요"));
    }
    
    private SecurityRequirement securityRequirement() {
        return new SecurityRequirement()
                .addList("bearerAuth");
    }
}
```

## Controller 문서화

### @Tag (컨트롤러 그룹)

```java
@Tag(name = "사용자", description = "사용자 관리 API")
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {
    
    private final UserService userService;
    
    // ...
}
```

### @Operation (엔드포인트 설명)

```java
@Operation(
    summary = "사용자 목록 조회",
    description = "등록된 모든 사용자 목록을 페이징하여 조회합니다"
)
@GetMapping
public ResponseEntity<Page<UserResponse>> getUsers(Pageable pageable) {
    return ResponseEntity.ok(userService.getUsers(pageable));
}
```

### @Parameter (파라미터 설명)

```java
@Operation(summary = "사용자 조회")
@GetMapping("/{id}")
public ResponseEntity<UserResponse> getUser(
        @Parameter(description = "사용자 ID", required = true, example = "1")
        @PathVariable Long id) {
    return ResponseEntity.ok(userService.getUser(id));
}

@Operation(summary = "사용자 검색")
@GetMapping("/search")
public ResponseEntity<List<UserResponse>> searchUsers(
        @Parameter(description = "이름 (부분 검색)", example = "홍길동")
        @RequestParam(required = false) String name,
        
        @Parameter(description = "이메일", example = "hong@example.com")
        @RequestParam(required = false) String email,
        
        @Parameter(description = "상태", schema = @Schema(implementation = UserStatus.class))
        @RequestParam(required = false) UserStatus status) {
    
    UserSearchCondition condition = UserSearchCondition.builder()
            .name(name)
            .email(email)
            .status(status)
            .build();
    
    return ResponseEntity.ok(userService.search(condition));
}
```

### @ApiResponses (응답 코드)

```java
@Operation(summary = "사용자 생성")
@ApiResponses({
    @ApiResponse(
        responseCode = "201",
        description = "생성 성공",
        content = @Content(schema = @Schema(implementation = UserResponse.class))
    ),
    @ApiResponse(
        responseCode = "400",
        description = "잘못된 요청",
        content = @Content(schema = @Schema(implementation = ErrorResponse.class))
    ),
    @ApiResponse(
        responseCode = "409",
        description = "이메일 중복",
        content = @Content(schema = @Schema(implementation = ErrorResponse.class))
    )
})
@PostMapping
public ResponseEntity<UserResponse> createUser(
        @Valid @RequestBody UserCreateRequest request) {
    UserResponse user = userService.createUser(request);
    return ResponseEntity.status(HttpStatus.CREATED).body(user);
}
```

## DTO 문서화

### @Schema (모델 설명)

```java
@Schema(description = "사용자 생성 요청")
@Getter
@Setter
public class UserCreateRequest {
    
    @Schema(description = "이름", example = "홍길동", requiredMode = Schema.RequiredMode.REQUIRED)
    @NotBlank(message = "이름은 필수입니다")
    @Size(min = 2, max = 50)
    private String name;
    
    @Schema(description = "이메일", example = "hong@example.com", requiredMode = Schema.RequiredMode.REQUIRED)
    @Email
    @NotBlank
    private String email;
    
    @Schema(description = "비밀번호 (8자 이상)", example = "password123", requiredMode = Schema.RequiredMode.REQUIRED)
    @NotBlank
    @Size(min = 8)
    private String password;
    
    @Schema(description = "나이", example = "25", minimum = "0", maximum = "150")
    private Integer age;
}
```

### Response DTO

```java
@Schema(description = "사용자 응답")
@Getter
@Builder
public class UserResponse {
    
    @Schema(description = "사용자 ID", example = "1")
    private Long id;
    
    @Schema(description = "이름", example = "홍길동")
    private String name;
    
    @Schema(description = "이메일", example = "hong@example.com")
    private String email;
    
    @Schema(description = "상태", example = "ACTIVE")
    private UserStatus status;
    
    @Schema(description = "생성일시", example = "2025-11-22T10:30:00")
    private LocalDateTime createdAt;
}
```

### Enum 문서화

```java
@Schema(description = "사용자 상태")
public enum UserStatus {
    
    @Schema(description = "활성")
    ACTIVE,
    
    @Schema(description = "비활성")
    INACTIVE,
    
    @Schema(description = "삭제")
    DELETED
}
```

## 완전한 예제

```java
@Tag(name = "사용자", description = "사용자 관리 API")
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {
    
    private final UserService userService;
    
    @Operation(summary = "사용자 목록 조회", description = "페이징을 지원하는 사용자 목록 조회")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "조회 성공")
    })
    @GetMapping
    public ResponseEntity<Page<UserResponse>> getUsers(
            @Parameter(description = "페이지 번호 (0부터 시작)", example = "0")
            @RequestParam(defaultValue = "0") int page,
            
            @Parameter(description = "페이지 크기", example = "20")
            @RequestParam(defaultValue = "20") int size) {
        
        Pageable pageable = PageRequest.of(page, size);
        return ResponseEntity.ok(userService.getUsers(pageable));
    }
    
    @Operation(summary = "사용자 조회", description = "ID로 사용자 상세 정보를 조회합니다")
    @ApiResponses({
        @ApiResponse(
            responseCode = "200",
            description = "조회 성공",
            content = @Content(schema = @Schema(implementation = UserResponse.class))
        ),
        @ApiResponse(
            responseCode = "404",
            description = "사용자를 찾을 수 없음",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))
        )
    })
    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(
            @Parameter(description = "사용자 ID", required = true, example = "1")
            @PathVariable Long id) {
        return ResponseEntity.ok(userService.getUser(id));
    }
    
    @Operation(summary = "사용자 생성", description = "새로운 사용자를 생성합니다")
    @ApiResponses({
        @ApiResponse(
            responseCode = "201",
            description = "생성 성공",
            content = @Content(schema = @Schema(implementation = UserResponse.class))
        ),
        @ApiResponse(
            responseCode = "400",
            description = "잘못된 입력값",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))
        ),
        @ApiResponse(
            responseCode = "409",
            description = "이메일 중복",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))
        )
    })
    @PostMapping
    public ResponseEntity<UserResponse> createUser(
            @io.swagger.v3.oas.annotations.parameters.RequestBody(
                description = "사용자 생성 정보",
                required = true,
                content = @Content(schema = @Schema(implementation = UserCreateRequest.class))
            )
            @Valid @RequestBody UserCreateRequest request) {
        
        UserResponse user = userService.createUser(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }
    
    @Operation(summary = "사용자 수정", description = "사용자 정보를 수정합니다")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "수정 성공"),
        @ApiResponse(responseCode = "404", description = "사용자를 찾을 수 없음")
    })
    @PutMapping("/{id}")
    public ResponseEntity<UserResponse> updateUser(
            @Parameter(description = "사용자 ID", required = true)
            @PathVariable Long id,
            
            @Valid @RequestBody UserUpdateRequest request) {
        return ResponseEntity.ok(userService.updateUser(id, request));
    }
    
    @Operation(summary = "사용자 삭제", description = "사용자를 삭제합니다")
    @ApiResponses({
        @ApiResponse(responseCode = "204", description = "삭제 성공"),
        @ApiResponse(responseCode = "404", description = "사용자를 찾을 수 없음")
    })
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(
            @Parameter(description = "사용자 ID", required = true)
            @PathVariable Long id) {
        userService.deleteUser(id);
        return ResponseEntity.noContent().build();
    }
}
```

## 보안 설정

### JWT 인증 추가

```java
@SecurityScheme(
    name = "bearerAuth",
    type = SecuritySchemeType.HTTP,
    scheme = "bearer",
    bearerFormat = "JWT",
    description = "JWT 토큰을 입력하세요"
)
@Configuration
public class OpenApiConfig {
    // ...
}
```

### 엔드포인트별 보안 설정

```java
@Operation(
    summary = "내 정보 조회",
    security = @SecurityRequirement(name = "bearerAuth")
)
@GetMapping("/me")
public ResponseEntity<UserResponse> getMyInfo() {
    // JWT에서 사용자 정보 추출
    return ResponseEntity.ok(userService.getMyInfo());
}
```

## 그룹화

### 태그로 그룹화

```java
@Tag(name = "사용자 관리", description = "사용자 CRUD API")
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    // ...
}

@Tag(name = "주문 관리", description = "주문 CRUD API")
@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {
    // ...
}

@Tag(name = "인증", description = "로그인 및 인증 API")
@RestController
@RequestMapping("/api/v1/auth")
public class AuthController {
    // ...
}
```

## 환경별 설정

### 운영 환경에서 비활성화

```yaml
# application-prod.yml
springdoc:
  api-docs:
    enabled: false
  swagger-ui:
    enabled: false
```

## 실전 팁

### 1. 공통 응답 타입

```java
@Schema(description = "공통 API 응답")
@Getter
public class ApiResponse<T> {
    
    @Schema(description = "성공 여부", example = "true")
    private boolean success;
    
    @Schema(description = "메시지", example = "조회 성공")
    private String message;
    
    @Schema(description = "데이터")
    private T data;
    
    @Schema(description = "타임스탬프", example = "2025-11-22T10:30:00")
    private LocalDateTime timestamp;
}
```

### 2. 예제 데이터

```java
@Schema(description = "사용자 정보", example = """
    {
        "name": "홍길동",
        "email": "hong@example.com",
        "password": "password123"
    }
    """)
public class UserCreateRequest {
    // ...
}
```

### 3. Hidden 처리

```java
@Schema(hidden = true)  // Swagger에서 숨김
private String internalField;

@Operation(hidden = true)  // API 문서에서 제외
@GetMapping("/internal")
public ResponseEntity<?> internalApi() {
    // ...
}
```

### 4. 커스텀 어노테이션

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Operation(summary = "조회", description = "ID로 조회합니다")
@ApiResponses({
    @ApiResponse(responseCode = "200", description = "조회 성공"),
    @ApiResponse(responseCode = "404", description = "찾을 수 없음")
})
public @interface GetByIdOperation {
}

// 사용
@GetByIdOperation
@GetMapping("/{id}")
public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
    // ...
}
```

## 다음 단계

OpenAPI 문서화를 배웠습니다. 이제 Feign Client를 알아봅시다.

👉 [다음: Feign Client](16-feign-client.md)

## 참고 자료

- [SpringDoc OpenAPI](https://springdoc.org/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
