# DTO와 Entity

DTO(Data Transfer Object)와 Entity의 차이점과 분리 이유를 알아봅니다.

## DTO란?

**DTO (Data Transfer Object):** 계층 간 데이터 전송을 위한 객체

### DTO의 목적

1. **계층 간 데이터 전송:** Controller ↔ Service ↔ Repository
2. **Entity 노출 방지:** 내부 구조 숨김
3. **API 스펙 고정:** Entity 변경에도 API 유지
4. **검증 로직 분리:** @Valid 어노테이션 활용

## Entity vs DTO

### Entity

```java
@Entity
@Table(name = "users")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class User extends BaseEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, length = 50)
    private String name;
    
    @Column(nullable = false, unique = true)
    private String email;
    
    @Column(nullable = false)
    private String password;  // 암호화된 비밀번호
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private UserStatus status;
    
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL)
    private List<Order> orders = new ArrayList<>();
    
    @Builder
    public User(String name, String email, String password) {
        this.name = name;
        this.email = email;
        this.password = password;
        this.status = UserStatus.ACTIVE;
    }
    
    // 비즈니스 로직
    public void updateInfo(String name, String email) {
        this.name = name;
        this.email = email;
    }
}
```

**특징:**
- JPA 어노테이션 포함
- 비즈니스 로직 포함
- 연관관계 매핑
- 민감한 정보 포함 (password)

### DTO

#### Request DTO

```java
@Getter
@Setter
@NoArgsConstructor
public class UserCreateRequest {
    
    @NotBlank(message = "이름은 필수입니다")
    @Size(min = 2, max = 50, message = "이름은 2자에서 50자 사이여야 합니다")
    private String name;
    
    @NotBlank(message = "이메일은 필수입니다")
    @Email(message = "올바른 이메일 형식이 아닙니다")
    private String email;
    
    @NotBlank(message = "비밀번호는 필수입니다")
    @Size(min = 8, message = "비밀번호는 최소 8자 이상이어야 합니다")
    private String password;
}
```

#### Response DTO

```java
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserResponse {
    
    private Long id;
    private String name;
    private String email;
    private UserStatus status;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    
    // Entity → DTO 변환 (정적 팩토리 메서드)
    public static UserResponse from(User user) {
        return UserResponse.builder()
                .id(user.getId())
                .name(user.getName())
                .email(user.getEmail())
                .status(user.getStatus())
                .createdAt(user.getCreatedAt())
                .updatedAt(user.getUpdatedAt())
                .build();
    }
}
```

**특징:**
- 검증 어노테이션 포함
- API 스펙에 맞는 필드만 포함
- 민감한 정보 제외 (password)
- 불변 객체로 설계 가능

## Entity와 DTO를 분리하는 이유

### 1. 보안

```java
// ❌ Entity를 직접 반환 (보안 문제)
@GetMapping("/{id}")
public User getUser(@PathVariable Long id) {
    return userRepository.findById(id).orElseThrow();
    // password 필드가 그대로 노출됨!
}

// ✅ DTO 변환 후 반환
@GetMapping("/{id}")
public UserResponse getUser(@PathVariable Long id) {
    User user = userRepository.findById(id).orElseThrow();
    return UserResponse.from(user);  // password 제외
}
```

### 2. API 안정성

```java
// Entity 변경
@Entity
public class User {
    private String name;
    private String email;
    private String phoneNumber;  // 새로운 필드 추가
}

// DTO는 그대로 유지 → API 스펙 변경 없음
public class UserResponse {
    private String name;
    private String email;
    // phoneNumber는 포함하지 않음
}
```

### 3. 검증 로직 분리

```java
// Entity: 비즈니스 로직
@Entity
public class User {
    private String email;
    
    public void updateEmail(String email) {
        // 비즈니스 규칙
    }
}

// DTO: 입력 검증
public class UserUpdateRequest {
    @Email
    @NotBlank
    private String email;  // 형식 검증
}
```

### 4. 순환 참조 방지

```java
// Entity: 양방향 연관관계
@Entity
public class User {
    @OneToMany(mappedBy = "user")
    private List<Order> orders;  // 순환 참조 가능
}

@Entity
public class Order {
    @ManyToOne
    private User user;  // 순환 참조 가능
}

// DTO: 순환 참조 없음
public class UserResponse {
    private Long id;
    private String name;
    // Order는 포함하지 않음
}
```

## DTO 변환 방법

### 1. 정적 팩토리 메서드

```java
@Getter
@Builder
public class UserResponse {
    private Long id;
    private String name;
    private String email;
    
    public static UserResponse from(User user) {
        return UserResponse.builder()
                .id(user.getId())
                .name(user.getName())
                .email(user.getEmail())
                .build();
    }
    
    // List 변환
    public static List<UserResponse> from(List<User> users) {
        return users.stream()
                .map(UserResponse::from)
                .toList();
    }
}
```

**사용:**
```java
UserResponse response = UserResponse.from(user);
List<UserResponse> responses = UserResponse.from(users);
```

### 2. toEntity 메서드

```java
@Getter
@Setter
public class UserCreateRequest {
    private String name;
    private String email;
    private String password;
    
    public User toEntity() {
        return User.builder()
                .name(this.name)
                .email(this.email)
                .password(this.password)
                .build();
    }
}
```

**사용:**
```java
User user = request.toEntity();
```

### 3. ModelMapper (자동 매핑)

**의존성 추가:**
```xml
<dependency>
    <groupId>org.modelmapper</groupId>
    <artifactId>modelmapper</artifactId>
    <version>3.1.1</version>
</dependency>
```

**설정:**
```java
@Configuration
public class ModelMapperConfig {
    
    @Bean
    public ModelMapper modelMapper() {
        ModelMapper modelMapper = new ModelMapper();
        modelMapper.getConfiguration()
                .setMatchingStrategy(MatchingStrategies.STRICT)
                .setSkipNullEnabled(true);
        return modelMapper;
    }
}
```

**사용:**
```java
@Service
@RequiredArgsConstructor
public class UserService {
    
    private final ModelMapper modelMapper;
    
    public UserResponse getUser(Long id) {
        User user = userRepository.findById(id).orElseThrow();
        return modelMapper.map(user, UserResponse.class);
    }
}
```

**단점:**
- ❌ 리플렉션 사용으로 성능 저하
- ❌ 컴파일 타임 체크 불가
- ❌ 복잡한 매핑 처리 어려움

## DTO 설계 패턴

### Request/Response 분리

```java
// 생성 요청
@Getter
@Setter
public class UserCreateRequest {
    @NotBlank
    private String name;
    
    @Email
    private String email;
    
    @NotBlank
    @Size(min = 8)
    private String password;
}

// 수정 요청
@Getter
@Setter
public class UserUpdateRequest {
    @NotBlank
    private String name;
    
    @Email
    private String email;
    // password는 별도 API로 분리
}

// 응답
@Getter
@Builder
public class UserResponse {
    private Long id;
    private String name;
    private String email;
    private UserStatus status;
    private LocalDateTime createdAt;
}
```

### 중첩 DTO

```java
@Getter
@Builder
public class OrderResponse {
    
    private Long id;
    private BigDecimal totalAmount;
    private OrderStatus status;
    
    // 중첩된 사용자 정보
    private UserSummary user;
    
    // 중첩된 주문 항목
    private List<OrderItemDto> items;
    
    @Getter
    @Builder
    public static class UserSummary {
        private Long id;
        private String name;
        private String email;
    }
    
    @Getter
    @Builder
    public static class OrderItemDto {
        private Long productId;
        private String productName;
        private Integer quantity;
        private BigDecimal price;
    }
}
```

### 페이징 응답

```java
@Getter
public class PageResponse<T> {
    
    private List<T> content;
    private int page;
    private int size;
    private long totalElements;
    private int totalPages;
    private boolean first;
    private boolean last;
    
    public static <T> PageResponse<T> from(Page<T> page) {
        PageResponse<T> response = new PageResponse<>();
        response.content = page.getContent();
        response.page = page.getNumber();
        response.size = page.getSize();
        response.totalElements = page.getTotalElements();
        response.totalPages = page.getTotalPages();
        response.first = page.isFirst();
        response.last = page.isLast();
        return response;
    }
}
```

**사용:**
```java
@GetMapping
public PageResponse<UserResponse> getUsers(Pageable pageable) {
    Page<User> userPage = userService.getUsers(pageable);
    Page<UserResponse> responsePage = userPage.map(UserResponse::from);
    return PageResponse.from(responsePage);
}
```

## 실전 예제

### 복잡한 변환

```java
@Getter
@Builder
public class OrderDetailResponse {
    
    private Long id;
    private String orderNumber;
    private BigDecimal totalAmount;
    private OrderStatus status;
    
    private UserInfo user;
    private List<OrderItemInfo> items;
    
    private LocalDateTime orderedAt;
    private LocalDateTime paidAt;
    
    public static OrderDetailResponse from(Order order) {
        return OrderDetailResponse.builder()
                .id(order.getId())
                .orderNumber(order.getOrderNumber())
                .totalAmount(order.getTotalAmount())
                .status(order.getStatus())
                .user(UserInfo.from(order.getUser()))
                .items(order.getOrderItems().stream()
                        .map(OrderItemInfo::from)
                        .toList())
                .orderedAt(order.getCreatedAt())
                .paidAt(order.getPaidAt())
                .build();
    }
    
    @Getter
    @Builder
    public static class UserInfo {
        private Long id;
        private String name;
        private String email;
        
        public static UserInfo from(User user) {
            return UserInfo.builder()
                    .id(user.getId())
                    .name(user.getName())
                    .email(user.getEmail())
                    .build();
        }
    }
    
    @Getter
    @Builder
    public static class OrderItemInfo {
        private Long productId;
        private String productName;
        private Integer quantity;
        private BigDecimal price;
        private BigDecimal subtotal;
        
        public static OrderItemInfo from(OrderItem item) {
            return OrderItemInfo.builder()
                    .productId(item.getProduct().getId())
                    .productName(item.getProduct().getName())
                    .quantity(item.getQuantity())
                    .price(item.getPrice())
                    .subtotal(item.getPrice().multiply(
                        BigDecimal.valueOf(item.getQuantity())))
                    .build();
        }
    }
}
```

## 실전 팁

### 1. DTO는 불변 객체로

```java
// ✅ 좋은 예: 불변 객체
@Getter
@Builder
public class UserResponse {
    private final Long id;
    private final String name;
    private final String email;
}

// ❌ 나쁜 예: 가변 객체
@Getter
@Setter
public class UserResponse {
    private Long id;
    private String name;
    private String email;
}
```

### 2. Request DTO는 검증 포함

```java
@Getter
@Setter
public class UserCreateRequest {
    
    @NotBlank(message = "이름은 필수입니다")
    @Size(min = 2, max = 50)
    private String name;
    
    @Email(message = "올바른 이메일 형식이 아닙니다")
    private String email;
}
```

### 3. 과도한 DTO 생성 지양

```java
// ❌ 나쁜 예: 필드 하나 차이로 DTO 분리
public class UserResponseWithEmail { ... }
public class UserResponseWithoutEmail { ... }

// ✅ 좋은 예: @JsonView 또는 공통 DTO 사용
@Getter
@Builder
public class UserResponse {
    private Long id;
    private String name;
    
    @JsonInclude(JsonInclude.Include.NON_NULL)
    private String email;  // 필요시만 포함
}
```

### 4. Builder 패턴 활용

```java
@Getter
@Builder
public class UserResponse {
    private Long id;
    private String name;
    private String email;
    
    // Builder를 통한 명확한 객체 생성
    public static UserResponse from(User user) {
        return UserResponse.builder()
                .id(user.getId())
                .name(user.getName())
                .email(user.getEmail())
                .build();
    }
}
```

## 패키지 구조

```
com.example.demo/
├── domain/                    # Entity
│   ├── User.java
│   ├── Order.java
│   └── Product.java
├── dto/                       # DTO
│   ├── request/
│   │   ├── UserCreateRequest.java
│   │   ├── UserUpdateRequest.java
│   │   └── OrderCreateRequest.java
│   └── response/
│       ├── UserResponse.java
│       ├── OrderResponse.java
│       └── ProductResponse.java
└── mapper/                    # Mapper (다음 장)
    ├── UserMapper.java
    └── OrderMapper.java
```

## 다음 단계

DTO와 Entity의 차이를 배웠습니다. 이제 MapStruct로 자동 매핑을 알아봅시다.

👉 [다음: MapStruct](10-mapstruct.md)

## 참고 자료

- [DTO Pattern](https://martinfowler.com/eaaCatalog/dataTransferObject.html)
- [Why DTOs?](https://stackoverflow.com/questions/36174516/rest-api-dtos-or-not)
