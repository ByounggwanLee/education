# JPA 고급

JPA의 고급 기능인 상속, 임베디드 타입, 복합 키, JPQL 등을 알아봅니다.

## 상속 관계 매핑

### 전략 1: JOINED (조인 전략)

```java
@Entity
@Inheritance(strategy = InheritanceType.JOINED)
@DiscriminatorColumn(name = "dtype")
public abstract class Item {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    private int price;
}

@Entity
@DiscriminatorValue("B")
public class Book extends Item {
    private String author;
    private String isbn;
}

@Entity
@DiscriminatorValue("M")
public class Movie extends Item {
    private String director;
    private String actor;
}
```

**테이블 구조:**
```sql
CREATE TABLE item (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    price INT,
    dtype VARCHAR(31)
);

CREATE TABLE book (
    id BIGINT PRIMARY KEY,
    author VARCHAR(255),
    isbn VARCHAR(255),
    FOREIGN KEY (id) REFERENCES item(id)
);

CREATE TABLE movie (
    id BIGINT PRIMARY KEY,
    director VARCHAR(255),
    actor VARCHAR(255),
    FOREIGN KEY (id) REFERENCES item(id)
);
```

### 전략 2: SINGLE_TABLE (단일 테이블 전략)

```java
@Entity
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@DiscriminatorColumn(name = "dtype")
public abstract class Item {
    @Id
    @GeneratedValue
    private Long id;
    
    private String name;
    private int price;
}
```

**테이블 구조:**
```sql
CREATE TABLE item (
    id BIGINT PRIMARY KEY,
    dtype VARCHAR(31),
    name VARCHAR(255),
    price INT,
    author VARCHAR(255),    -- Book 필드
    isbn VARCHAR(255),      -- Book 필드
    director VARCHAR(255),  -- Movie 필드
    actor VARCHAR(255)      -- Movie 필드
);
```

### 전략 3: TABLE_PER_CLASS (구현 클래스마다 테이블)

```java
@Entity
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
public abstract class Item {
    @Id
    @GeneratedValue
    private Long id;
    
    private String name;
    private int price;
}
```

## @MappedSuperclass

```java
@MappedSuperclass
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

@Entity
public class User extends BaseEntity {
    @Id
    @GeneratedValue
    private Long id;
    
    private String name;
    
    // createdAt, updatedAt 등 상속받음
}
```

## 임베디드 타입 (@Embeddable)

### 값 타입 정의

```java
@Embeddable
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Address {
    
    @Column(name = "city")
    private String city;
    
    @Column(name = "street")
    private String street;
    
    @Column(name = "zipcode")
    private String zipcode;
    
    @Builder
    public Address(String city, String street, String zipcode) {
        this.city = city;
        this.street = street;
        this.zipcode = zipcode;
    }
}
```

### 임베디드 타입 사용

```java
@Entity
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    
    @Embedded
    private Address address;
    
    @Embedded
    @AttributeOverrides({
        @AttributeOverride(name = "city", column = @Column(name = "work_city")),
        @AttributeOverride(name = "street", column = @Column(name = "work_street")),
        @AttributeOverride(name = "zipcode", column = @Column(name = "work_zipcode"))
    })
    private Address workAddress;
}
```

## 복합 키

### @IdClass

```java
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode
public class OrderItemId implements Serializable {
    private Long orderId;
    private Long productId;
}

@Entity
@IdClass(OrderItemId.class)
@Getter
@NoArgsConstructor
public class OrderItem {
    
    @Id
    @Column(name = "order_id")
    private Long orderId;
    
    @Id
    @Column(name = "product_id")
    private Long productId;
    
    private Integer quantity;
}
```

### @EmbeddedId

```java
@Embeddable
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@EqualsAndHashCode
public class OrderItemId implements Serializable {
    
    @Column(name = "order_id")
    private Long orderId;
    
    @Column(name = "product_id")
    private Long productId;
    
    @Builder
    public OrderItemId(Long orderId, Long productId) {
        this.orderId = orderId;
        this.productId = productId;
    }
}

@Entity
@Getter
@NoArgsConstructor
public class OrderItem {
    
    @EmbeddedId
    private OrderItemId id;
    
    private Integer quantity;
}
```

## JPQL (Java Persistence Query Language)

### 기본 쿼리

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // 엔티티 조회
    @Query("SELECT u FROM User u WHERE u.email = :email")
    Optional<User> findByEmail(@Param("email") String email);
    
    // 필드 조회
    @Query("SELECT u.name FROM User u WHERE u.id = :id")
    String findNameById(@Param("id") Long id);
    
    // 여러 조건
    @Query("SELECT u FROM User u WHERE u.name = :name AND u.status = :status")
    List<User> findByNameAndStatus(
        @Param("name") String name,
        @Param("status") UserStatus status
    );
}
```

### JOIN

```java
// INNER JOIN
@Query("SELECT o FROM Order o INNER JOIN o.user u WHERE u.name = :userName")
List<Order> findByUserName(@Param("userName") String userName);

// LEFT JOIN
@Query("SELECT u FROM User u LEFT JOIN u.orders o WHERE u.id = :userId")
User findUserWithOrders(@Param("userId") Long userId);

// FETCH JOIN (N+1 해결)
@Query("SELECT o FROM Order o JOIN FETCH o.user WHERE o.id = :id")
Optional<Order> findByIdWithUser(@Param("id") Long id);

// 여러 연관관계 FETCH JOIN
@Query("SELECT DISTINCT o FROM Order o " +
       "JOIN FETCH o.user " +
       "JOIN FETCH o.orderItems")
List<Order> findAllWithUserAndItems();
```

### 집계 함수

```java
// COUNT
@Query("SELECT COUNT(u) FROM User u WHERE u.status = :status")
long countByStatus(@Param("status") UserStatus status);

// SUM
@Query("SELECT SUM(o.totalAmount) FROM Order o WHERE o.user.id = :userId")
BigDecimal getTotalAmountByUserId(@Param("userId") Long userId);

// AVG
@Query("SELECT AVG(p.price) FROM Product p")
Double getAveragePrice();

// MAX, MIN
@Query("SELECT MAX(p.price), MIN(p.price) FROM Product p")
Object[] getPriceRange();
```

### GROUP BY, HAVING

```java
@Query("SELECT u.status, COUNT(u) FROM User u GROUP BY u.status")
List<Object[]> getUserCountByStatus();

@Query("SELECT u.status, COUNT(u) FROM User u " +
       "GROUP BY u.status HAVING COUNT(u) > :minCount")
List<Object[]> getUserCountByStatusHaving(@Param("minCount") long minCount);
```

### 서브쿼리

```java
// EXISTS
@Query("SELECT u FROM User u WHERE EXISTS " +
       "(SELECT o FROM Order o WHERE o.user = u AND o.status = 'COMPLETED')")
List<User> findUsersWithCompletedOrders();

// IN
@Query("SELECT u FROM User u WHERE u.id IN " +
       "(SELECT o.user.id FROM Order o WHERE o.totalAmount > :amount)")
List<User> findUsersWithOrdersAboveAmount(@Param("amount") BigDecimal amount);
```

### DTO 프로젝션

```java
@Query("SELECT new com.example.demo.dto.UserDto(u.id, u.name, u.email) " +
       "FROM User u WHERE u.id = :id")
Optional<UserDto> findUserDtoById(@Param("id") Long id);

// DTO 클래스
@Getter
@AllArgsConstructor
public class UserDto {
    private Long id;
    private String name;
    private String email;
}
```

## Querydsl 고급

### 동적 쿼리

```java
@Repository
@RequiredArgsConstructor
public class UserRepositoryImpl implements UserRepositoryCustom {
    
    private final JPAQueryFactory queryFactory;
    
    @Override
    public List<User> search(UserSearchCondition condition) {
        QUser user = QUser.user;
        
        return queryFactory
            .selectFrom(user)
            .where(
                nameEq(condition.getName()),
                emailContains(condition.getEmail()),
                statusEq(condition.getStatus()),
                ageBetween(condition.getMinAge(), condition.getMaxAge())
            )
            .orderBy(user.createdAt.desc())
            .fetch();
    }
    
    private BooleanExpression nameEq(String name) {
        return hasText(name) ? QUser.user.name.eq(name) : null;
    }
    
    private BooleanExpression emailContains(String email) {
        return hasText(email) ? QUser.user.email.contains(email) : null;
    }
    
    private BooleanExpression statusEq(UserStatus status) {
        return status != null ? QUser.user.status.eq(status) : null;
    }
    
    private BooleanExpression ageBetween(Integer minAge, Integer maxAge) {
        if (minAge != null && maxAge != null) {
            return QUser.user.age.between(minAge, maxAge);
        } else if (minAge != null) {
            return QUser.user.age.goe(minAge);
        } else if (maxAge != null) {
            return QUser.user.age.loe(maxAge);
        }
        return null;
    }
}
```

### 조인과 페이징

```java
public Page<OrderDto> searchOrders(OrderSearchCondition condition, Pageable pageable) {
    QOrder order = QOrder.order;
    QUser user = QUser.user;
    
    List<OrderDto> content = queryFactory
        .select(new QOrderDto(
            order.id,
            order.orderNumber,
            user.name,
            order.totalAmount,
            order.status
        ))
        .from(order)
        .join(order.user, user)
        .where(
            orderNumberContains(condition.getOrderNumber()),
            userNameEq(condition.getUserName()),
            statusEq(condition.getStatus())
        )
        .offset(pageable.getOffset())
        .limit(pageable.getPageSize())
        .orderBy(order.createdAt.desc())
        .fetch();
    
    Long total = queryFactory
        .select(order.count())
        .from(order)
        .join(order.user, user)
        .where(
            orderNumberContains(condition.getOrderNumber()),
            userNameEq(condition.getUserName()),
            statusEq(condition.getStatus())
        )
        .fetchOne();
    
    return new PageImpl<>(content, pageable, total);
}
```

## 성능 최적화

### 1. Batch Size

```yaml
spring:
  jpa:
    properties:
      hibernate:
        default_batch_fetch_size: 100
```

### 2. 읽기 전용 쿼리

```java
@Transactional(readOnly = true)
public List<User> getUsers() {
    // flush 생략, 변경 감지 안 함
    return userRepository.findAll();
}
```

### 3. 벌크 연산

```java
@Modifying(clearAutomatically = true)
@Query("UPDATE User u SET u.status = :status WHERE u.lastLoginAt < :date")
int updateInactiveUsers(@Param("status") UserStatus status, @Param("date") LocalDateTime date);
```

### 4. 영속성 컨텍스트 관리

```java
@Transactional
public void processLargeData() {
    List<User> users = userRepository.findAll();
    
    for (int i = 0; i < users.size(); i++) {
        User user = users.get(i);
        user.process();
        
        // 100개마다 flush & clear
        if (i % 100 == 0) {
            entityManager.flush();
            entityManager.clear();
        }
    }
}
```

## Soft Delete

```java
@Entity
@SQLDelete(sql = "UPDATE users SET deleted = true WHERE id = ?")
@Where(clause = "deleted = false")
@Getter
@NoArgsConstructor
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    
    @Column(nullable = false)
    private boolean deleted = false;
    
    public void delete() {
        this.deleted = true;
    }
}
```

## 실전 팁

### 1. N+1 문제 해결

```java
// ❌ N+1 문제
@Query("SELECT o FROM Order o")
List<Order> findAll();  // 1번 조회 + N번 user 조회

// ✅ Fetch Join
@Query("SELECT o FROM Order o JOIN FETCH o.user")
List<Order> findAllWithUser();  // 1번에 조회
```

### 2. 컬렉션 Fetch Join 주의

```java
// ❌ 여러 컬렉션 Fetch Join 불가
@Query("SELECT o FROM Order o " +
       "JOIN FETCH o.orderItems " +
       "JOIN FETCH o.payments")  // MultipleBagFetchException

// ✅ @EntityGraph 또는 Batch Size 사용
@EntityGraph(attributePaths = {"orderItems", "payments"})
List<Order> findAll();
```

### 3. DTO 프로젝션 활용

```java
// 필요한 필드만 조회
@Query("SELECT new com.example.demo.dto.UserSummary(u.id, u.name) FROM User u")
List<UserSummary> findUserSummaries();
```

## 다음 단계

JPA 고급을 배웠습니다. 이제 MyBatis를 알아봅시다.

👉 [다음: MyBatis](13-mybatis.md)

## 참고 자료

- [Hibernate Performance Tuning](https://vladmihalcea.com/)
- [Querydsl Reference](http://querydsl.com/static/querydsl/latest/reference/html/)
