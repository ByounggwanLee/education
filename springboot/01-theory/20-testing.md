# Testing

Spring Boot 애플리케이션의 다양한 계층을 테스트하는 방법을 알아봅니다.

## 테스트 종류

### 테스트 피라미드

```
        /\
       /E2E\         통합 테스트 (느림, 적음)
      /------\
     /통합테스트\
    /----------\
   / 단위 테스트  \    단위 테스트 (빠름, 많음)
  /--------------\
```

### 레이어별 테스트

- **단위 테스트:** Service, Repository, Util
- **통합 테스트:** Controller + Service + Repository
- **E2E 테스트:** 전체 애플리케이션

## 의존성 추가

### Maven

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>

<!-- H2 (테스트용 DB) -->
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>test</scope>
</dependency>
```

### Gradle

```gradle
testImplementation 'org.springframework.boot:spring-boot-starter-test'
testRuntimeOnly 'com.h2database:h2'
```

## Repository 테스트

### @DataJpaTest

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class UserRepositoryTest {
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private TestEntityManager entityManager;
    
    @BeforeEach
    void setUp() {
        // 테스트 데이터 준비
        User user = User.builder()
                .name("홍길동")
                .email("hong@example.com")
                .password("password")
                .build();
        entityManager.persist(user);
        entityManager.flush();
    }
    
    @Test
    @DisplayName("이메일로 사용자 조회")
    void findByEmailTest() {
        // When
        Optional<User> found = userRepository.findByEmail("hong@example.com");
        
        // Then
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("홍길동");
    }
    
    @Test
    @DisplayName("이름으로 사용자 검색")
    void findByNameContainingTest() {
        // When
        List<User> users = userRepository.findByNameContaining("홍");
        
        // Then
        assertThat(users).hasSize(1);
        assertThat(users.get(0).getName()).contains("홍");
    }
    
    @Test
    @DisplayName("사용자 생성")
    void saveTest() {
        // Given
        User newUser = User.builder()
                .name("김철수")
                .email("kim@example.com")
                .password("password")
                .build();
        
        // When
        User saved = userRepository.save(newUser);
        
        // Then
        assertThat(saved.getId()).isNotNull();
        assertThat(saved.getName()).isEqualTo("김철수");
    }
    
    @Test
    @DisplayName("이메일 중복 확인")
    void existsByEmailTest() {
        // When
        boolean exists = userRepository.existsByEmail("hong@example.com");
        
        // Then
        assertThat(exists).isTrue();
    }
}
```

## Service 테스트

### @ExtendWith(MockitoExtension.class)

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @Mock
    private PasswordEncoder passwordEncoder;
    
    @InjectMocks
    private UserService userService;
    
    @Test
    @DisplayName("사용자 생성 성공")
    void createUserSuccessTest() {
        // Given
        UserCreateRequest request = UserCreateRequest.builder()
                .name("홍길동")
                .email("hong@example.com")
                .password("password123")
                .build();
        
        User user = User.builder()
                .id(1L)
                .name(request.getName())
                .email(request.getEmail())
                .password("encoded_password")
                .build();
        
        when(userRepository.existsByEmail(request.getEmail())).thenReturn(false);
        when(passwordEncoder.encode(request.getPassword())).thenReturn("encoded_password");
        when(userRepository.save(any(User.class))).thenReturn(user);
        
        // When
        UserResponse response = userService.createUser(request);
        
        // Then
        assertThat(response.getId()).isEqualTo(1L);
        assertThat(response.getName()).isEqualTo("홍길동");
        
        verify(userRepository).existsByEmail(request.getEmail());
        verify(passwordEncoder).encode(request.getPassword());
        verify(userRepository).save(any(User.class));
    }
    
    @Test
    @DisplayName("이메일 중복 시 예외 발생")
    void createUserDuplicateEmailTest() {
        // Given
        UserCreateRequest request = UserCreateRequest.builder()
                .email("hong@example.com")
                .build();
        
        when(userRepository.existsByEmail(request.getEmail())).thenReturn(true);
        
        // When & Then
        assertThatThrownBy(() -> userService.createUser(request))
                .isInstanceOf(EmailDuplicatedException.class)
                .hasMessage("이미 사용 중인 이메일입니다: hong@example.com");
        
        verify(userRepository).existsByEmail(request.getEmail());
        verify(userRepository, never()).save(any(User.class));
    }
    
    @Test
    @DisplayName("사용자 조회 성공")
    void getUserSuccessTest() {
        // Given
        Long userId = 1L;
        User user = User.builder()
                .id(userId)
                .name("홍길동")
                .email("hong@example.com")
                .build();
        
        when(userRepository.findById(userId)).thenReturn(Optional.of(user));
        
        // When
        UserResponse response = userService.getUser(userId);
        
        // Then
        assertThat(response.getId()).isEqualTo(userId);
        assertThat(response.getName()).isEqualTo("홍길동");
        
        verify(userRepository).findById(userId);
    }
    
    @Test
    @DisplayName("사용자 조회 실패 - 존재하지 않음")
    void getUserNotFoundTest() {
        // Given
        Long userId = 999L;
        when(userRepository.findById(userId)).thenReturn(Optional.empty());
        
        // When & Then
        assertThatThrownBy(() -> userService.getUser(userId))
                .isInstanceOf(UserNotFoundException.class);
        
        verify(userRepository).findById(userId);
    }
}
```

## Controller 테스트

### @WebMvcTest

```java
@WebMvcTest(UserController.class)
class UserControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private UserService userService;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Test
    @DisplayName("사용자 목록 조회")
    void getUsersTest() throws Exception {
        // Given
        List<UserResponse> users = List.of(
            UserResponse.builder()
                    .id(1L)
                    .name("홍길동")
                    .email("hong@example.com")
                    .build(),
            UserResponse.builder()
                    .id(2L)
                    .name("김철수")
                    .email("kim@example.com")
                    .build()
        );
        
        when(userService.getUsers()).thenReturn(users);
        
        // When & Then
        mockMvc.perform(get("/api/v1/users")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(2)))
                .andExpect(jsonPath("$[0].name").value("홍길동"))
                .andExpect(jsonPath("$[1].name").value("김철수"))
                .andDo(print());
        
        verify(userService).getUsers();
    }
    
    @Test
    @DisplayName("사용자 조회")
    void getUserTest() throws Exception {
        // Given
        Long userId = 1L;
        UserResponse user = UserResponse.builder()
                .id(userId)
                .name("홍길동")
                .email("hong@example.com")
                .build();
        
        when(userService.getUser(userId)).thenReturn(user);
        
        // When & Then
        mockMvc.perform(get("/api/v1/users/{id}", userId)
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.name").value("홍길동"))
                .andExpect(jsonPath("$.email").value("hong@example.com"))
                .andDo(print());
        
        verify(userService).getUser(userId);
    }
    
    @Test
    @DisplayName("사용자 생성")
    void createUserTest() throws Exception {
        // Given
        UserCreateRequest request = UserCreateRequest.builder()
                .name("홍길동")
                .email("hong@example.com")
                .password("password123")
                .build();
        
        UserResponse response = UserResponse.builder()
                .id(1L)
                .name(request.getName())
                .email(request.getEmail())
                .build();
        
        when(userService.createUser(any(UserCreateRequest.class))).thenReturn(response);
        
        // When & Then
        mockMvc.perform(post("/api/v1/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.name").value("홍길동"))
                .andDo(print());
        
        verify(userService).createUser(any(UserCreateRequest.class));
    }
    
    @Test
    @DisplayName("사용자 생성 실패 - 유효성 검증")
    void createUserValidationTest() throws Exception {
        // Given
        UserCreateRequest request = UserCreateRequest.builder()
                .name("")  // 빈 이름
                .email("invalid-email")  // 잘못된 이메일
                .password("123")  // 짧은 비밀번호
                .build();
        
        // When & Then
        mockMvc.perform(post("/api/v1/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andDo(print());
        
        verify(userService, never()).createUser(any(UserCreateRequest.class));
    }
    
    @Test
    @DisplayName("사용자 삭제")
    void deleteUserTest() throws Exception {
        // Given
        Long userId = 1L;
        doNothing().when(userService).deleteUser(userId);
        
        // When & Then
        mockMvc.perform(delete("/api/v1/users/{id}", userId))
                .andExpect(status().isNoContent())
                .andDo(print());
        
        verify(userService).deleteUser(userId);
    }
}
```

## 통합 테스트

### @SpringBootTest

```java
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class UserIntegrationTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Autowired
    private UserRepository userRepository;
    
    @BeforeEach
    void setUp() {
        userRepository.deleteAll();
    }
    
    @Test
    @DisplayName("사용자 CRUD 통합 테스트")
    void userCrudTest() throws Exception {
        // 1. 생성
        UserCreateRequest createRequest = UserCreateRequest.builder()
                .name("홍길동")
                .email("hong@example.com")
                .password("password123")
                .build();
        
        String createResponse = mockMvc.perform(post("/api/v1/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(createRequest)))
                .andExpect(status().isCreated())
                .andReturn()
                .getResponse()
                .getContentAsString();
        
        UserResponse created = objectMapper.readValue(createResponse, UserResponse.class);
        Long userId = created.getId();
        
        // 2. 조회
        mockMvc.perform(get("/api/v1/users/{id}", userId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("홍길동"));
        
        // 3. 수정
        UserUpdateRequest updateRequest = UserUpdateRequest.builder()
                .name("홍길동2")
                .build();
        
        mockMvc.perform(put("/api/v1/users/{id}", userId)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updateRequest)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("홍길동2"));
        
        // 4. 삭제
        mockMvc.perform(delete("/api/v1/users/{id}", userId))
                .andExpect(status().isNoContent());
        
        // 5. 삭제 확인
        mockMvc.perform(get("/api/v1/users/{id}", userId))
                .andExpect(status().isNotFound());
    }
}
```

## 테스트 컨테이너

### 의존성 추가

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers</artifactId>
    <version>1.19.3</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>postgresql</artifactId>
    <version>1.19.3</version>
    <scope>test</scope>
</dependency>
```

### 사용

```java
@SpringBootTest
@Testcontainers
class TestContainersTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");
    
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
    
    @Test
    void testWithRealDatabase() {
        // 실제 PostgreSQL 컨테이너로 테스트
    }
}
```

## Mocking

### @Mock vs @MockBean

```java
// @Mock: Mockito 단독 사용
@ExtendWith(MockitoExtension.class)
class ServiceTest {
    @Mock
    private UserRepository userRepository;
    
    @InjectMocks
    private UserService userService;
}

// @MockBean: Spring Context와 함께
@SpringBootTest
class IntegrationTest {
    @MockBean
    private UserRepository userRepository;
    
    @Autowired
    private UserService userService;
}
```

### Stubbing

```java
@Test
void stubbingTest() {
    // 반환값 설정
    when(userRepository.findById(1L)).thenReturn(Optional.of(user));
    
    // 예외 발생
    when(userRepository.findById(999L))
            .thenThrow(new UserNotFoundException(999L));
    
    // 여러 호출에 대한 설정
    when(userRepository.count())
            .thenReturn(1L)
            .thenReturn(2L)
            .thenReturn(3L);
    
    // 조건부 반환
    when(userRepository.findById(anyLong()))
            .thenAnswer(invocation -> {
                Long id = invocation.getArgument(0);
                if (id > 0) {
                    return Optional.of(user);
                }
                return Optional.empty();
            });
}
```

### Verification

```java
@Test
void verificationTest() {
    // 메서드 호출 확인
    verify(userRepository).save(any(User.class));
    
    // 호출 횟수 확인
    verify(userRepository, times(1)).save(any(User.class));
    verify(userRepository, never()).delete(any(User.class));
    verify(userRepository, atLeast(1)).findAll();
    verify(userRepository, atMost(3)).findById(anyLong());
    
    // 호출 순서 확인
    InOrder inOrder = inOrder(userRepository);
    inOrder.verify(userRepository).findById(1L);
    inOrder.verify(userRepository).save(any(User.class));
    
    // 인자 검증
    ArgumentCaptor<User> captor = ArgumentCaptor.forClass(User.class);
    verify(userRepository).save(captor.capture());
    User savedUser = captor.getValue();
    assertThat(savedUser.getName()).isEqualTo("홍길동");
}
```

## AssertJ

### 기본 Assertions

```java
@Test
void assertJTest() {
    // 기본 검증
    assertThat(user).isNotNull();
    assertThat(user.getName()).isEqualTo("홍길동");
    assertThat(user.getAge()).isGreaterThan(18);
    
    // 컬렉션 검증
    List<User> users = Arrays.asList(user1, user2, user3);
    assertThat(users)
            .hasSize(3)
            .contains(user1, user2)
            .extracting("name")
            .containsExactly("홍길동", "김철수", "이영희");
    
    // 예외 검증
    assertThatThrownBy(() -> userService.getUser(999L))
            .isInstanceOf(UserNotFoundException.class)
            .hasMessage("사용자를 찾을 수 없습니다: 999");
    
    // Optional 검증
    Optional<User> optionalUser = userRepository.findById(1L);
    assertThat(optionalUser)
            .isPresent()
            .hasValueSatisfying(u -> {
                assertThat(u.getName()).isEqualTo("홍길동");
                assertThat(u.getEmail()).contains("@");
            });
}
```

## 테스트 설정

### application-test.yml

```yaml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password:
  
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true
    properties:
      hibernate:
        format_sql: true
  
  h2:
    console:
      enabled: true

logging:
  level:
    org.hibernate.SQL: DEBUG
    org.hibernate.type.descriptor.sql.BasicBinder: TRACE
```

## 테스트 유틸

### TestDataBuilder

```java
public class UserTestBuilder {
    
    public static User createUser() {
        return User.builder()
                .id(1L)
                .name("홍길동")
                .email("hong@example.com")
                .password("password123")
                .role(Role.USER)
                .build();
    }
    
    public static User createUser(String name, String email) {
        return User.builder()
                .id(1L)
                .name(name)
                .email(email)
                .password("password123")
                .role(Role.USER)
                .build();
    }
    
    public static UserCreateRequest createUserRequest() {
        return UserCreateRequest.builder()
                .name("홍길동")
                .email("hong@example.com")
                .password("password123")
                .build();
    }
}
```

## 실전 팁

### 1. Given-When-Then 패턴

```java
@Test
void exampleTest() {
    // Given: 테스트 준비
    User user = createUser();
    when(userRepository.findById(1L)).thenReturn(Optional.of(user));
    
    // When: 테스트 실행
    UserResponse response = userService.getUser(1L);
    
    // Then: 결과 검증
    assertThat(response.getName()).isEqualTo("홍길동");
}
```

### 2. DisplayName 활용

```java
@Test
@DisplayName("이메일 중복 시 EmailDuplicatedException 발생")
void test() {
    // ...
}
```

### 3. @Nested로 그룹화

```java
@DisplayName("UserService 테스트")
class UserServiceTest {
    
    @Nested
    @DisplayName("사용자 생성")
    class CreateUserTest {
        
        @Test
        @DisplayName("성공")
        void success() { }
        
        @Test
        @DisplayName("이메일 중복")
        void duplicateEmail() { }
    }
    
    @Nested
    @DisplayName("사용자 조회")
    class GetUserTest {
        
        @Test
        @DisplayName("성공")
        void success() { }
        
        @Test
        @DisplayName("존재하지 않음")
        void notFound() { }
    }
}
```

### 4. @ParameterizedTest

```java
@ParameterizedTest
@ValueSource(strings = {"", "  ", "a", "too-long-name-over-50-characters"})
@DisplayName("잘못된 이름 검증")
void invalidNameTest(String name) {
    UserCreateRequest request = UserCreateRequest.builder()
            .name(name)
            .build();
    
    assertThatThrownBy(() -> userService.createUser(request))
            .isInstanceOf(ValidationException.class);
}

@ParameterizedTest
@CsvSource({
    "hong@example.com, 홍길동",
    "kim@example.com, 김철수",
    "lee@example.com, 이영희"
})
void multipleUsersTest(String email, String name) {
    // ...
}
```

## 다음 단계

Testing을 배웠습니다. 이제 Configuration을 알아봅시다.

👉 [다음: Configuration](21-configuration.md)

## 참고 자료

- [Spring Boot Testing](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.testing)
- [JUnit 5](https://junit.org/junit5/)
- [Mockito](https://site.mockito.org/)
- [AssertJ](https://assertj.github.io/doc/)
