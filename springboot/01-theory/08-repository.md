# Repository 계층

데이터베이스 접근을 담당하는 Repository 계층의 역할과 Spring Data JPA 사용법을 알아봅니다.

## Repository 계층이란?

**Repository 계층:** 데이터 영속성을 담당하는 계층으로, 데이터베이스 CRUD 작업을 추상화

### 역할

1. **데이터 액세스:** 데이터베이스 CRUD 작업
2. **쿼리 실행:** SQL/JPQL 쿼리 실행
3. **영속성 관리:** Entity의 생명주기 관리
4. **트랜잭션 경계:** 데이터베이스 트랜잭션 처리

## Spring Data JPA

### JpaRepository 인터페이스

```java
package com.example.demo.repository;

import com.example.demo.domain.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    // 기본 메서드가 모두 제공됨
    // save(), findById(), findAll(), delete(), count() 등
}
```

**JpaRepository가 제공하는 메서드:**

```java
// 저장
<S extends T> S save(S entity);
<S extends T> List<S> saveAll(Iterable<S> entities);

// 조회
Optional<T> findById(ID id);
List<T> findAll();
List<T> findAllById(Iterable<ID> ids);
Page<T> findAll(Pageable pageable);

// 존재 확인
boolean existsById(ID id);

// 개수
long count();

// 삭제
void deleteById(ID id);
void delete(T entity);
void deleteAll(Iterable<? extends T> entities);
void deleteAll();
```

### Repository 계층 구조

```
Repository (마커 인터페이스)
└── CrudRepository (기본 CRUD)
    └── PagingAndSortingRepository (페이징, 정렬)
        └── JpaRepository (JPA 특화)
```

## 쿼리 메서드

### 메서드 이름으로 쿼리 생성

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // SELECT * FROM user WHERE email = ?
    Optional<User> findByEmail(String email);
    
    // SELECT * FROM user WHERE name = ?
    List<User> findByName(String name);
    
    // SELECT * FROM user WHERE name = ? AND email = ?
    Optional<User> findByNameAndEmail(String name, String email);
    
    // SELECT * FROM user WHERE email LIKE ?
    List<User> findByEmailContaining(String email);
    
    // SELECT * FROM user WHERE age > ?
    List<User> findByAgeGreaterThan(Integer age);
    
    // SELECT * FROM user WHERE created_at BETWEEN ? AND ?
    List<User> findByCreatedAtBetween(LocalDateTime start, LocalDateTime end);
    
    // SELECT * FROM user ORDER BY name ASC
    List<User> findByOrderByNameAsc();
    
    // SELECT COUNT(*) FROM user WHERE email = ?
    long countByEmail(String email);
    
    // SELECT EXISTS(SELECT 1 FROM user WHERE email = ?)
    boolean existsByEmail(String email);
    
    // DELETE FROM user WHERE email = ?
    void deleteByEmail(String email);
}
```

### 쿼리 메서드 키워드

| 키워드 | 설명 | 예시 |
|--------|------|------|
| `findBy` | 조회 | `findByName` |
| `getBy` | 조회 (findBy와 동일) | `getByName` |
| `queryBy` | 조회 (findBy와 동일) | `queryByName` |
| `countBy` | 개수 | `countByEmail` |
| `existsBy` | 존재 확인 | `existsByEmail` |
| `deleteBy` | 삭제 | `deleteByName` |
| `And` | 그리고 | `findByNameAndEmail` |
| `Or` | 또는 | `findByNameOrEmail` |
| `Is`, `Equals` | 같음 | `findByNameIs` |
| `Not` | 같지 않음 | `findByNameNot` |
| `Like` | LIKE | `findByNameLike` |
| `Containing` | LIKE %?% | `findByNameContaining` |
| `StartingWith` | LIKE ?% | `findByNameStartingWith` |
| `EndingWith` | LIKE %? | `findByNameEndingWith` |
| `GreaterThan` | > | `findByAgeGreaterThan` |
| `LessThan` | < | `findByAgeLessThan` |
| `Between` | BETWEEN | `findByAgeBetween` |
| `In` | IN | `findByNameIn` |
| `IsNull` | IS NULL | `findByEmailIsNull` |
| `IsNotNull` | IS NOT NULL | `findByEmailIsNotNull` |
| `OrderBy` | 정렬 | `findByOrderByNameAsc` |
| `First`, `Top` | 제한 | `findTop10ByOrderByIdDesc` |

### 페이징과 정렬

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // 페이징
    Page<User> findByName(String name, Pageable pageable);
    
    // 정렬
    List<User> findByName(String name, Sort sort);
    
    // 상위 N개
    List<User> findTop10ByOrderByCreatedAtDesc();
    
    // 첫 번째
    Optional<User> findFirstByOrderByCreatedAtDesc();
}
```

**사용 예시:**

```java
@Service
@RequiredArgsConstructor
public class UserService {
    
    private final UserRepository userRepository;
    
    public Page<User> getUsers(int page, int size) {
        // 페이징 요청 생성
        Pageable pageable = PageRequest.of(page, size);
        return userRepository.findAll(pageable);
    }
    
    public Page<User> getUsersSorted(int page, int size, String sortBy) {
        // 정렬 포함 페이징
        Pageable pageable = PageRequest.of(page, size, Sort.by(sortBy).descending());
        return userRepository.findAll(pageable);
    }
    
    public Page<User> searchUsers(String name, int page, int size) {
        Pageable pageable = PageRequest.of(page, size, 
                Sort.by("createdAt").descending());
        return userRepository.findByName(name, pageable);
    }
}
```

## @Query 어노테이션

### JPQL 쿼리

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // JPQL (Java Persistence Query Language)
    @Query("SELECT u FROM User u WHERE u.email = :email")
    Optional<User> findByEmailJpql(@Param("email") String email);
    
    // 여러 조건
    @Query("SELECT u FROM User u WHERE u.name = :name AND u.status = :status")
    List<User> findByNameAndStatus(
            @Param("name") String name, 
            @Param("status") UserStatus status
    );
    
    // JOIN
    @Query("SELECT u FROM User u JOIN FETCH u.orders WHERE u.id = :id")
    Optional<User> findByIdWithOrders(@Param("id") Long id);
    
    // DTO 프로젝션
    @Query("SELECT new com.example.demo.dto.UserResponse(u.id, u.name, u.email) " +
           "FROM User u WHERE u.id = :id")
    Optional<UserResponse> findUserResponseById(@Param("id") Long id);
}
```

### Native Query

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // Native SQL
    @Query(value = "SELECT * FROM user WHERE email = :email", nativeQuery = true)
    Optional<User> findByEmailNative(@Param("email") String email);
    
    // 복잡한 집계 쿼리
    @Query(value = """
            SELECT u.status, COUNT(*) as count
            FROM user u
            WHERE u.created_at >= :startDate
            GROUP BY u.status
            """, nativeQuery = true)
    List<Object[]> getUserStatistics(@Param("startDate") LocalDateTime startDate);
}
```

### @Modifying

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // UPDATE 쿼리
    @Modifying
    @Query("UPDATE User u SET u.status = :status WHERE u.id = :id")
    int updateStatus(@Param("id") Long id, @Param("status") UserStatus status);
    
    // DELETE 쿼리
    @Modifying
    @Query("DELETE FROM User u WHERE u.createdAt < :date")
    int deleteOldUsers(@Param("date") LocalDateTime date);
    
    // Bulk 업데이트
    @Modifying(clearAutomatically = true)  // 영속성 컨텍스트 자동 클리어
    @Query("UPDATE User u SET u.lastLoginAt = :now WHERE u.id IN :ids")
    int updateLastLoginAt(@Param("ids") List<Long> ids, @Param("now") LocalDateTime now);
}
```

**주의:** `@Modifying` 쿼리는 영속성 컨텍스트를 거치지 않으므로 `clearAutomatically = true` 설정 권장

## QueryDSL

### 의존성 추가

**Maven:**
```xml
<dependency>
    <groupId>com.querydsl</groupId>
    <artifactId>querydsl-jpa</artifactId>
    <version>5.0.0</version>
    <classifier>jakarta</classifier>
</dependency>
<dependency>
    <groupId>com.querydsl</groupId>
    <artifactId>querydsl-apt</artifactId>
    <version>5.0.0</version>
    <classifier>jakarta</classifier>
    <scope>provided</scope>
</dependency>
```

### QueryDSL Repository

```java
public interface UserRepositoryCustom {
    List<User> searchUsers(UserSearchCondition condition);
    Page<User> searchUsersWithPaging(UserSearchCondition condition, Pageable pageable);
}

@Repository
@RequiredArgsConstructor
public class UserRepositoryImpl implements UserRepositoryCustom {
    
    private final JPAQueryFactory queryFactory;
    
    @Override
    public List<User> searchUsers(UserSearchCondition condition) {
        QUser user = QUser.user;
        
        return queryFactory
                .selectFrom(user)
                .where(
                        nameEq(condition.getName()),
                        emailContains(condition.getEmail()),
                        ageGoe(condition.getMinAge())
                )
                .orderBy(user.createdAt.desc())
                .fetch();
    }
    
    @Override
    public Page<User> searchUsersWithPaging(UserSearchCondition condition, Pageable pageable) {
        QUser user = QUser.user;
        
        List<User> content = queryFactory
                .selectFrom(user)
                .where(
                        nameEq(condition.getName()),
                        emailContains(condition.getEmail())
                )
                .offset(pageable.getOffset())
                .limit(pageable.getPageSize())
                .fetch();
        
        long total = queryFactory
                .select(user.count())
                .from(user)
                .where(
                        nameEq(condition.getName()),
                        emailContains(condition.getEmail())
                )
                .fetchOne();
        
        return new PageImpl<>(content, pageable, total);
    }
    
    private BooleanExpression nameEq(String name) {
        return hasText(name) ? QUser.user.name.eq(name) : null;
    }
    
    private BooleanExpression emailContains(String email) {
        return hasText(email) ? QUser.user.email.contains(email) : null;
    }
    
    private BooleanExpression ageGoe(Integer minAge) {
        return minAge != null ? QUser.user.age.goe(minAge) : null;
    }
}
```

### UserRepository 통합

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long>, UserRepositoryCustom {
    // JpaRepository 기본 메서드 + UserRepositoryCustom 메서드 모두 사용 가능
}
```

## 실전 예제

### 1. 검색 조건이 있는 조회

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    @Query("SELECT u FROM User u WHERE " +
           "(:name IS NULL OR u.name LIKE %:name%) AND " +
           "(:email IS NULL OR u.email LIKE %:email%) AND " +
           "(:status IS NULL OR u.status = :status)")
    Page<User> search(
            @Param("name") String name,
            @Param("email") String email,
            @Param("status") UserStatus status,
            Pageable pageable
    );
}
```

### 2. 연관 엔티티 fetch join

```java
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    
    // N+1 문제 해결
    @Query("SELECT o FROM Order o " +
           "JOIN FETCH o.user " +
           "JOIN FETCH o.orderItems " +
           "WHERE o.id = :id")
    Optional<Order> findByIdWithUserAndItems(@Param("id") Long id);
    
    // 컬렉션 여러 개 fetch join은 불가능 (MultipleBagFetchException)
    // 대신 @EntityGraph 사용
    @EntityGraph(attributePaths = {"user", "orderItems"})
    Optional<Order> findWithAllById(Long id);
}
```

### 3. 통계 쿼리

```java
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    
    // 날짜별 주문 통계
    @Query("SELECT new com.example.demo.dto.OrderStatistics(" +
           "    DATE(o.createdAt), " +
           "    COUNT(o), " +
           "    SUM(o.totalAmount)" +
           ") " +
           "FROM Order o " +
           "WHERE o.createdAt BETWEEN :startDate AND :endDate " +
           "GROUP BY DATE(o.createdAt)")
    List<OrderStatistics> getOrderStatistics(
            @Param("startDate") LocalDateTime startDate,
            @Param("endDate") LocalDateTime endDate
    );
}
```

## 테스트

### Repository 테스트

```java
@DataJpaTest
class UserRepositoryTest {
    
    @Autowired
    private UserRepository userRepository;
    
    @Test
    void save() {
        // given
        User user = User.builder()
                .name("홍길동")
                .email("hong@example.com")
                .build();
        
        // when
        User saved = userRepository.save(user);
        
        // then
        assertThat(saved.getId()).isNotNull();
        assertThat(saved.getName()).isEqualTo("홍길동");
    }
    
    @Test
    void findByEmail() {
        // given
        User user = User.builder()
                .name("홍길동")
                .email("hong@example.com")
                .build();
        userRepository.save(user);
        
        // when
        Optional<User> found = userRepository.findByEmail("hong@example.com");
        
        // then
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("홍길동");
    }
    
    @Test
    void findByName_WithPaging() {
        // given
        for (int i = 1; i <= 25; i++) {
            userRepository.save(User.builder()
                    .name("User" + i)
                    .email("user" + i + "@example.com")
                    .build());
        }
        
        // when
        Pageable pageable = PageRequest.of(0, 10);
        Page<User> page = userRepository.findAll(pageable);
        
        // then
        assertThat(page.getContent()).hasSize(10);
        assertThat(page.getTotalElements()).isEqualTo(25);
        assertThat(page.getTotalPages()).isEqualTo(3);
    }
}
```

## 실전 팁

### 1. N+1 문제 방지

```java
// ❌ 나쁜 예: N+1 문제 발생
@Query("SELECT o FROM Order o")
List<Order> findAll();  // 각 Order마다 User 조회 쿼리 실행

// ✅ 좋은 예: fetch join
@Query("SELECT o FROM Order o JOIN FETCH o.user")
List<Order> findAllWithUser();
```

### 2. 벌크 연산 주의

```java
@Modifying(clearAutomatically = true)  // 영속성 컨텍스트 클리어
@Query("UPDATE User u SET u.status = :status WHERE u.id IN :ids")
int updateStatus(@Param("ids") List<Long> ids, @Param("status") UserStatus status);
```

### 3. Optional 사용

```java
// ✅ 좋은 예
Optional<User> findByEmail(String email);

// ❌ 나쁜 예 (null 반환)
User findByEmail(String email);
```

### 4. 정렬과 페이징

```java
// 동적 정렬
Sort sort = Sort.by(Sort.Direction.DESC, "createdAt", "name");
Pageable pageable = PageRequest.of(page, size, sort);
```

## 다음 단계

Repository 계층을 배웠습니다. 이제 DTO와 Entity 관계를 알아봅시다.

👉 [다음: DTO와 Entity](09-dto-entity.md)

## 참고 자료

- [Spring Data JPA](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [Query Methods](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#jpa.query-methods)
- [QueryDSL](http://querydsl.com/)
