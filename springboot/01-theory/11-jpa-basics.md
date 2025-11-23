# JPA 기초

JPA(Java Persistence API)의 핵심 개념과 기본 사용법을 알아봅니다.

## JPA란?

**JPA (Java Persistence API):** 자바 ORM 기술의 표준 명세

**ORM (Object-Relational Mapping):** 객체와 관계형 데이터베이스를 매핑

### JPA 구성 요소

```
JPA (표준 명세)
└── Hibernate (구현체)
    └── Spring Data JPA (추상화)
```

## Entity 기본

### @Entity와 @Table

```java
@Entity
@Table(name = "users")  // 테이블명 지정 (기본값: 클래스명 소문자)
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "user_name", nullable = false, length = 50)
    private String name;
    
    @Column(unique = true, nullable = false)
    private String email;
    
    @Builder
    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }
}
```

### 기본 키 생성 전략

#### 1. IDENTITY (Auto Increment)

```java
@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)
private Long id;
```

**특징:**
- MySQL, PostgreSQL의 AUTO_INCREMENT
- DB에 위임
- INSERT 후 ID 조회

#### 2. SEQUENCE

```java
@Id
@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "user_seq")
@SequenceGenerator(
    name = "user_seq",
    sequenceName = "user_sequence",
    initialValue = 1,
    allocationSize = 50
)
private Long id;
```

**특징:**
- Oracle, PostgreSQL의 SEQUENCE
- DB 시퀀스 사용
- 성능 최적화 (allocationSize)

#### 3. TABLE

```java
@Id
@GeneratedValue(strategy = GenerationType.TABLE, generator = "user_id_gen")
@TableGenerator(
    name = "user_id_gen",
    table = "id_generator",
    pkColumnName = "gen_name",
    valueColumnName = "gen_value",
    allocationSize = 50
)
private Long id;
```

#### 4. UUID

```java
@Id
@GeneratedValue(generator = "uuid2")
@GenericGenerator(name = "uuid2", strategy = "uuid2")
@Column(columnDefinition = "BINARY(16)")
private UUID id;
```

### @Column 속성

```java
@Entity
public class User {
    
    @Column(
        name = "user_name",          // 컬럼명
        nullable = false,            // NOT NULL
        unique = true,               // UNIQUE
        length = 50,                 // VARCHAR(50)
        precision = 10,              // DECIMAL(10,2)
        scale = 2,
        columnDefinition = "TEXT",   // 직접 정의
        insertable = true,           // INSERT 가능
        updatable = true             // UPDATE 가능
    )
    private String name;
}
```

## 필드 매핑

### 날짜/시간

```java
@Entity
public class User {
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "birth_date")
    private LocalDate birthDate;
    
    @Column(name = "start_time")
    private LocalTime startTime;
    
    // Java 8 이전
    @Temporal(TemporalType.TIMESTAMP)
    private Date registeredDate;
}
```

### Enum

```java
public enum UserStatus {
    ACTIVE, INACTIVE, DELETED
}

@Entity
public class User {
    
    // ✅ 권장: String 저장
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private UserStatus status;
    
    // ❌ 비권장: 순서(0,1,2) 저장
    @Enumerated(EnumType.ORDINAL)
    private UserStatus status;
}
```

### LOB (Large Object)

```java
@Entity
public class Article {
    
    @Lob
    @Column(columnDefinition = "TEXT")
    private String content;  // CLOB
    
    @Lob
    private byte[] image;    // BLOB
}
```

### @Transient

```java
@Entity
public class User {
    
    private String email;
    
    @Transient  // DB에 저장하지 않음
    private String tempPassword;
}
```

## 영속성 컨텍스트

### Entity 생명주기

```
비영속 (New/Transient)
    ↓ em.persist()
영속 (Managed)
    ↓ em.detach() / em.clear() / em.close()
준영속 (Detached)
    ↓ em.merge()
영속 (Managed)
    ↓ em.remove()
삭제 (Removed)
```

### 예제

```java
@Service
@RequiredArgsConstructor
public class UserService {
    
    @PersistenceContext
    private EntityManager em;
    
    @Transactional
    public void lifecycle() {
        // 비영속
        User user = new User("홍길동", "hong@example.com");
        
        // 영속
        em.persist(user);
        
        // 영속 상태에서 조회
        User found = em.find(User.class, user.getId());
        
        // 준영속
        em.detach(user);
        
        // 다시 영속
        User merged = em.merge(user);
        
        // 삭제
        em.remove(merged);
    }
}
```

### 1차 캐시

```java
@Transactional
public void firstLevelCache() {
    // 1. DB에서 조회하여 1차 캐시에 저장
    User user1 = em.find(User.class, 1L);
    
    // 2. 1차 캐시에서 조회 (SELECT 쿼리 실행 안 함)
    User user2 = em.find(User.class, 1L);
    
    // 동일성 보장
    assertThat(user1 == user2).isTrue();
}
```

### 변경 감지 (Dirty Checking)

```java
@Transactional
public void dirtyChecking() {
    User user = em.find(User.class, 1L);
    
    // 엔티티 수정
    user.updateName("김철수");
    
    // em.persist() 호출 불필요!
    // 트랜잭션 커밋 시 자동으로 UPDATE 쿼리 실행
}
```

### 쓰기 지연 (Write-Behind)

```java
@Transactional
public void writeBehind() {
    User user1 = new User("홍길동", "hong@example.com");
    User user2 = new User("김철수", "kim@example.com");
    
    em.persist(user1);  // INSERT 쿼리 실행 안 함
    em.persist(user2);  // INSERT 쿼리 실행 안 함
    
    // 트랜잭션 커밋 시 한 번에 실행
    // INSERT INTO users ...
    // INSERT INTO users ...
}
```

## 연관관계 기본

### @ManyToOne (다대일)

```java
@Entity
public class Order {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")  // FK 컬럼명
    private User user;
}
```

### @OneToMany (일대다)

```java
@Entity
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @OneToMany(mappedBy = "user")  // Order.user 필드
    private List<Order> orders = new ArrayList<>();
}
```

### 양방향 연관관계

```java
@Entity
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL)
    private List<Order> orders = new ArrayList<>();
    
    // 연관관계 편의 메서드
    public void addOrder(Order order) {
        this.orders.add(order);
        order.setUser(this);
    }
}

@Entity
public class Order {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;
    
    // Setter (양방향 편의 메서드에서 사용)
    public void setUser(User user) {
        this.user = user;
    }
}
```

### @OneToOne (일대일)

```java
@Entity
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @OneToOne(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private UserProfile profile;
}

@Entity
public class UserProfile {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;
}
```

### @ManyToMany (다대다)

```java
@Entity
public class Student {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToMany
    @JoinTable(
        name = "student_course",
        joinColumns = @JoinColumn(name = "student_id"),
        inverseJoinColumns = @JoinColumn(name = "course_id")
    )
    private List<Course> courses = new ArrayList<>();
}

@Entity
public class Course {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToMany(mappedBy = "courses")
    private List<Student> students = new ArrayList<>();
}
```

**권장:** 다대다는 일대다, 다대일로 풀어서 사용

## Fetch 전략

### EAGER vs LAZY

```java
@Entity
public class Order {
    
    // ✅ 권장: 지연 로딩
    @ManyToOne(fetch = FetchType.LAZY)
    private User user;
    
    // ❌ 비권장: 즉시 로딩 (N+1 문제)
    @ManyToOne(fetch = FetchType.EAGER)
    private User user;
}
```

### N+1 문제 해결

#### 1. Fetch Join

```java
@Query("SELECT o FROM Order o JOIN FETCH o.user")
List<Order> findAllWithUser();
```

#### 2. @EntityGraph

```java
@EntityGraph(attributePaths = {"user"})
@Query("SELECT o FROM Order o")
List<Order> findAllWithUser();
```

#### 3. @BatchSize

```java
@Entity
public class User {
    
    @BatchSize(size = 100)
    @OneToMany(mappedBy = "user")
    private List<Order> orders = new ArrayList<>();
}
```

## Cascade와 orphanRemoval

### Cascade

```java
@Entity
public class Order {
    
    @OneToMany(
        mappedBy = "order",
        cascade = CascadeType.ALL  // 모든 작업 전파
    )
    private List<OrderItem> orderItems = new ArrayList<>();
}
```

**Cascade 옵션:**
- `ALL`: 모든 작업
- `PERSIST`: 저장
- `MERGE`: 병합
- `REMOVE`: 삭제
- `REFRESH`: 새로고침
- `DETACH`: 준영속

### orphanRemoval

```java
@Entity
public class Order {
    
    @OneToMany(
        mappedBy = "order",
        cascade = CascadeType.ALL,
        orphanRemoval = true  // 고아 객체 자동 삭제
    )
    private List<OrderItem> orderItems = new ArrayList<>();
    
    public void removeItem(OrderItem item) {
        orderItems.remove(item);
        item.setOrder(null);
        // orphanRemoval = true이면 자동 DELETE
    }
}
```

## BaseEntity (공통 필드)

```java
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
@Getter
public abstract class BaseEntity {
    
    @CreatedDate
    @Column(updatable = false)
    private LocalDateTime createdAt;
    
    @LastModifiedDate
    private LocalDateTime updatedAt;
    
    @CreatedBy
    @Column(updatable = false)
    private String createdBy;
    
    @LastModifiedBy
    private String updatedBy;
}
```

**활성화:**
```java
@EnableJpaAuditing
@SpringBootApplication
public class Application {
    // ...
}
```

**사용:**
```java
@Entity
public class User extends BaseEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    
    // createdAt, updatedAt, createdBy, updatedBy 자동 설정
}
```

## 실전 팁

### 1. 양방향보다 단방향

```java
// ✅ 단방향으로도 충분
@Entity
public class Order {
    @ManyToOne(fetch = FetchType.LAZY)
    private User user;
}
```

### 2. @ToString 순환 참조 주의

```java
@Entity
@ToString(exclude = "orders")  // 양방향 관계 제외
public class User {
    @OneToMany(mappedBy = "user")
    private List<Order> orders = new ArrayList<>();
}
```

### 3. 기본 생성자는 protected

```java
@Entity
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class User {
    // JPA는 기본 생성자 필요
}
```

### 4. Setter 지양

```java
// ❌ Setter 남용
user.setName("홍길동");

// ✅ 의미 있는 메서드
user.updateName("홍길동");
```

## 다음 단계

JPA 기초를 배웠습니다. 이제 JPA 고급 기능을 알아봅시다.

👉 [다음: JPA 고급](12-jpa-advanced.md)

## 참고 자료

- [JPA Specification](https://jakarta.ee/specifications/persistence/)
- [Hibernate ORM](https://hibernate.org/orm/documentation/)
- [Spring Data JPA](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
