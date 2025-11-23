# MapStruct

Entity와 DTO 간 변환을 자동화하는 MapStruct 라이브러리를 알아봅니다.

## MapStruct란?

**MapStruct:** 컴파일 타임에 매핑 코드를 자동 생성하는 Java Bean 매퍼

### 장점

- ✅ **컴파일 타임 생성:** 빠른 성능 (리플렉션 사용 안 함)
- ✅ **타입 안정성:** 컴파일 시 오류 검출
- ✅ **코드 가독성:** 매핑 로직 명확
- ✅ **유지보수성:** 자동 생성으로 실수 방지

### ModelMapper vs MapStruct

| 특성 | ModelMapper | MapStruct |
|------|-------------|-----------|
| 동작 방식 | 런타임 (리플렉션) | 컴파일 타임 (코드 생성) |
| 성능 | 느림 | 빠름 |
| 타입 안정성 | 런타임 오류 | 컴파일 오류 |
| 설정 | 간단 | 약간 복잡 |
| 복잡한 매핑 | 어려움 | 쉬움 |

## 의존성 추가

### Maven

```xml
<properties>
    <mapstruct.version>1.5.5.Final</mapstruct.version>
    <lombok.version>1.18.30</lombok.version>
</properties>

<dependencies>
    <!-- MapStruct -->
    <dependency>
        <groupId>org.mapstruct</groupId>
        <artifactId>mapstruct</artifactId>
        <version>${mapstruct.version}</version>
    </dependency>
    
    <!-- Lombok (선택) -->
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <version>${lombok.version}</version>
        <scope>provided</scope>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <source>17</source>
                <target>17</target>
                <annotationProcessorPaths>
                    <!-- MapStruct Processor -->
                    <path>
                        <groupId>org.mapstruct</groupId>
                        <artifactId>mapstruct-processor</artifactId>
                        <version>${mapstruct.version}</version>
                    </path>
                    <!-- Lombok (Lombok + MapStruct 함께 사용) -->
                    <path>
                        <groupId>org.projectlombok</groupId>
                        <artifactId>lombok</artifactId>
                        <version>${lombok.version}</version>
                    </path>
                    <!-- Lombok-MapStruct Binding -->
                    <path>
                        <groupId>org.projectlombok</groupId>
                        <artifactId>lombok-mapstruct-binding</artifactId>
                        <version>0.2.0</version>
                    </path>
                </annotationProcessorPaths>
            </configuration>
        </plugin>
    </plugins>
</build>
```

### Gradle

```gradle
dependencies {
    implementation 'org.mapstruct:mapstruct:1.5.5.Final'
    annotationProcessor 'org.mapstruct:mapstruct-processor:1.5.5.Final'
    
    // Lombok 사용 시
    compileOnly 'org.projectlombok:lombok:1.18.30'
    annotationProcessor 'org.projectlombok:lombok:1.18.30'
    annotationProcessor 'org.projectlombok:lombok-mapstruct-binding:0.2.0'
}
```

## 기본 사용법

### 1. Mapper 인터페이스 정의

```java
package com.example.demo.mapper;

import com.example.demo.domain.User;
import com.example.demo.dto.UserCreateRequest;
import com.example.demo.dto.UserResponse;
import org.mapstruct.Mapper;
import org.mapstruct.MappingConstants;

@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public interface UserMapper {
    
    // Entity → Response DTO
    UserResponse toResponse(User user);
    
    // Request DTO → Entity
    User toEntity(UserCreateRequest request);
    
    // List 변환
    List<UserResponse> toResponseList(List<User> users);
}
```

### 2. 생성된 구현체 확인

**target/generated-sources/annotations/** 경로에 자동 생성:

```java
@Component
public class UserMapperImpl implements UserMapper {
    
    @Override
    public UserResponse toResponse(User user) {
        if (user == null) {
            return null;
        }
        
        UserResponse.UserResponseBuilder userResponse = UserResponse.builder();
        
        userResponse.id(user.getId());
        userResponse.name(user.getName());
        userResponse.email(user.getEmail());
        userResponse.status(user.getStatus());
        userResponse.createdAt(user.getCreatedAt());
        
        return userResponse.build();
    }
    
    @Override
    public User toEntity(UserCreateRequest request) {
        if (request == null) {
            return null;
        }
        
        User.UserBuilder user = User.builder();
        
        user.name(request.getName());
        user.email(request.getEmail());
        user.password(request.getPassword());
        
        return user.build();
    }
    
    @Override
    public List<UserResponse> toResponseList(List<User> users) {
        if (users == null) {
            return null;
        }
        
        List<UserResponse> list = new ArrayList<>(users.size());
        for (User user : users) {
            list.add(toResponse(user));
        }
        
        return list;
    }
}
```

### 3. Service에서 사용

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserServiceImpl implements UserService {
    
    private final UserRepository userRepository;
    private final UserMapper userMapper;  // Spring Bean 주입
    
    @Override
    @Transactional
    public UserResponse createUser(UserCreateRequest request) {
        // Request DTO → Entity
        User user = userMapper.toEntity(request);
        User savedUser = userRepository.save(user);
        
        // Entity → Response DTO
        return userMapper.toResponse(savedUser);
    }
    
    @Override
    public UserResponse getUser(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id));
        
        return userMapper.toResponse(user);
    }
    
    @Override
    public List<UserResponse> getUsers() {
        List<User> users = userRepository.findAll();
        return userMapper.toResponseList(users);
    }
}
```

## 필드 매핑

### @Mapping 어노테이션

```java
@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public interface UserMapper {
    
    // 필드명이 다를 때
    @Mapping(source = "email", target = "emailAddress")
    @Mapping(source = "name", target = "fullName")
    UserResponse toResponse(User user);
    
    // 상수값 설정
    @Mapping(target = "status", constant = "ACTIVE")
    User toEntity(UserCreateRequest request);
    
    // 기본값 설정
    @Mapping(target = "role", defaultValue = "USER")
    User toEntityWithDefault(UserCreateRequest request);
    
    // 무시할 필드
    @Mapping(target = "password", ignore = true)
    UserResponse toResponseWithoutPassword(User user);
}
```

### 날짜 포맷

```java
@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public interface UserMapper {
    
    @Mapping(source = "createdAt", target = "createdDate", dateFormat = "yyyy-MM-dd HH:mm:ss")
    UserResponse toResponse(User user);
}
```

### 표현식 사용

```java
@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public interface UserMapper {
    
    // Java 표현식
    @Mapping(target = "fullName", expression = "java(user.getFirstName() + \" \" + user.getLastName())")
    UserResponse toResponse(User user);
    
    // 현재 시간 설정
    @Mapping(target = "createdAt", expression = "java(java.time.LocalDateTime.now())")
    User toEntity(UserCreateRequest request);
}
```

## 중첩 객체 매핑

### Entity

```java
@Entity
@Getter
@NoArgsConstructor
public class Order {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    private User user;
    
    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL)
    private List<OrderItem> orderItems = new ArrayList<>();
    
    private BigDecimal totalAmount;
    private OrderStatus status;
}

@Entity
@Getter
@NoArgsConstructor
public class OrderItem {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    private Order order;
    
    @ManyToOne(fetch = FetchType.LAZY)
    private Product product;
    
    private Integer quantity;
    private BigDecimal price;
}
```

### Mapper

```java
@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public interface OrderMapper {
    
    // 중첩 객체 자동 매핑
    @Mapping(source = "user.id", target = "userId")
    @Mapping(source = "user.name", target = "userName")
    OrderResponse toResponse(Order order);
    
    // OrderItem도 자동 매핑
    @Mapping(source = "product.id", target = "productId")
    @Mapping(source = "product.name", target = "productName")
    OrderItemResponse toOrderItemResponse(OrderItem orderItem);
    
    List<OrderItemResponse> toOrderItemResponseList(List<OrderItem> orderItems);
}
```

### DTO

```java
@Getter
@Builder
public class OrderResponse {
    
    private Long id;
    private Long userId;
    private String userName;
    private List<OrderItemResponse> orderItems;
    private BigDecimal totalAmount;
    private OrderStatus status;
}

@Getter
@Builder
public class OrderItemResponse {
    
    private Long id;
    private Long productId;
    private String productName;
    private Integer quantity;
    private BigDecimal price;
}
```

## 커스텀 매핑 메서드

### @Named 어노테이션

```java
@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public interface UserMapper {
    
    @Mapping(source = "password", target = "password", qualifiedByName = "encodePassword")
    User toEntity(UserCreateRequest request);
    
    @Named("encodePassword")
    default String encodePassword(String password) {
        // 비밀번호 암호화
        return new BCryptPasswordEncoder().encode(password);
    }
}
```

### 추상 클래스로 확장

```java
@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public abstract class UserMapper {
    
    @Autowired
    protected PasswordEncoder passwordEncoder;
    
    @Mapping(source = "password", target = "password", qualifiedByName = "encodePassword")
    public abstract User toEntity(UserCreateRequest request);
    
    public abstract UserResponse toResponse(User user);
    
    @Named("encodePassword")
    protected String encodePassword(String password) {
        return passwordEncoder.encode(password);
    }
}
```

## 업데이트 매핑

### @MappingTarget

```java
@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public interface UserMapper {
    
    // 기존 Entity 업데이트
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "password", ignore = true)
    void updateEntity(UserUpdateRequest request, @MappingTarget User user);
}
```

**사용:**
```java
@Service
@RequiredArgsConstructor
public class UserService {
    
    private final UserRepository userRepository;
    private final UserMapper userMapper;
    
    @Transactional
    public UserResponse updateUser(Long id, UserUpdateRequest request) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id));
        
        // 기존 Entity 업데이트
        userMapper.updateEntity(request, user);
        
        return userMapper.toResponse(user);
    }
}
```

## 다른 Mapper 사용

### @Mapper(uses = ...)

```java
@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public interface UserMapper {
    UserResponse toResponse(User user);
}

@Mapper(
    componentModel = MappingConstants.ComponentModel.SPRING,
    uses = UserMapper.class  // UserMapper 사용
)
public interface OrderMapper {
    
    // user 필드는 UserMapper.toResponse()로 자동 변환
    @Mapping(source = "user", target = "user")
    OrderResponse toResponse(Order order);
}
```

## 매핑 전략

### Null 값 처리

```java
@Mapper(
    componentModel = MappingConstants.ComponentModel.SPRING,
    nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE
)
public interface UserMapper {
    
    // null 값은 무시하고 기존 값 유지
    void updateEntity(UserUpdateRequest request, @MappingTarget User user);
}
```

### 컬렉션 매핑 전략

```java
@Mapper(
    componentModel = MappingConstants.ComponentModel.SPRING,
    collectionMappingStrategy = CollectionMappingStrategy.ADDER_PREFERRED
)
public interface OrderMapper {
    
    OrderResponse toResponse(Order order);
}
```

## 실전 예제

### 복잡한 매핑

```java
@Mapper(
    componentModel = MappingConstants.ComponentModel.SPRING,
    uses = {UserMapper.class, ProductMapper.class}
)
public interface OrderMapper {
    
    @Mapping(source = "user", target = "userInfo")
    @Mapping(source = "orderItems", target = "items")
    @Mapping(target = "orderNumber", expression = "java(generateOrderNumber(order))")
    OrderDetailResponse toDetailResponse(Order order);
    
    @Mapping(source = "product", target = "productInfo")
    @Mapping(target = "subtotal", expression = "java(calculateSubtotal(item))")
    OrderItemResponse toItemResponse(OrderItem item);
    
    default String generateOrderNumber(Order order) {
        return "ORD-" + order.getId() + "-" + 
               order.getCreatedAt().format(DateTimeFormatter.ofPattern("yyyyMMdd"));
    }
    
    default BigDecimal calculateSubtotal(OrderItem item) {
        return item.getPrice().multiply(BigDecimal.valueOf(item.getQuantity()));
    }
}
```

### DTO 상속

```java
// 기본 DTO
@Getter
@Setter
public class UserBaseResponse {
    private Long id;
    private String name;
    private String email;
}

// 확장 DTO
@Getter
@Setter
public class UserDetailResponse extends UserBaseResponse {
    private String phoneNumber;
    private String address;
    private LocalDateTime createdAt;
}

// Mapper
@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public interface UserMapper {
    
    UserBaseResponse toBaseResponse(User user);
    
    UserDetailResponse toDetailResponse(User user);
}
```

## 테스트

### Mapper 테스트

```java
@SpringBootTest
class UserMapperTest {
    
    @Autowired
    private UserMapper userMapper;
    
    @Test
    void toResponse() {
        // given
        User user = User.builder()
                .id(1L)
                .name("홍길동")
                .email("hong@example.com")
                .build();
        
        // when
        UserResponse response = userMapper.toResponse(user);
        
        // then
        assertThat(response.getId()).isEqualTo(1L);
        assertThat(response.getName()).isEqualTo("홍길동");
        assertThat(response.getEmail()).isEqualTo("hong@example.com");
    }
    
    @Test
    void toEntity() {
        // given
        UserCreateRequest request = new UserCreateRequest();
        request.setName("홍길동");
        request.setEmail("hong@example.com");
        request.setPassword("password123");
        
        // when
        User user = userMapper.toEntity(request);
        
        // then
        assertThat(user.getName()).isEqualTo("홍길동");
        assertThat(user.getEmail()).isEqualTo("hong@example.com");
    }
}
```

## 실전 팁

### 1. componentModel 설정

```java
// ✅ Spring Bean으로 등록
@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public interface UserMapper {
    // ...
}
```

### 2. unmappedTargetPolicy

```java
// 매핑되지 않은 필드 경고
@Mapper(
    componentModel = MappingConstants.ComponentModel.SPRING,
    unmappedTargetPolicy = ReportingPolicy.WARN
)
public interface UserMapper {
    // ...
}
```

### 3. 빌더 활용

```java
// Lombok @Builder와 자동 통합
@Mapper(
    componentModel = MappingConstants.ComponentModel.SPRING,
    builder = @Builder(disableBuilder = false)
)
public interface UserMapper {
    UserResponse toResponse(User user);
}
```

### 4. 매핑 설정 공통화

```java
@MapperConfig(
    componentModel = MappingConstants.ComponentModel.SPRING,
    unmappedTargetPolicy = ReportingPolicy.WARN,
    nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE
)
public interface CentralConfig {
    // 공통 설정
}

// 적용
@Mapper(config = CentralConfig.class)
public interface UserMapper {
    // CentralConfig 설정 상속
}
```

## 다음 단계

MapStruct를 배웠습니다. 이제 JPA 기초를 알아봅시다.

👉 [다음: JPA 기초](11-jpa-basics.md)

## 참고 자료

- [MapStruct Reference Guide](https://mapstruct.org/documentation/stable/reference/html/)
- [MapStruct Spring Extensions](https://github.com/mapstruct/mapstruct-spring-extensions)
- [MapStruct Examples](https://github.com/mapstruct/mapstruct-examples)
