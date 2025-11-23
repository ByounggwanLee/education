# MyBatis

SQL 매퍼 프레임워크인 MyBatis를 Spring Boot와 통합하여 사용하는 방법을 알아봅니다.

## MyBatis란?

**MyBatis:** SQL과 저장 프로시저를 자바 객체와 매핑하는 SQL 매퍼 프레임워크

### JPA vs MyBatis

| 특성 | JPA | MyBatis |
|------|-----|---------|
| 방식 | ORM | SQL Mapper |
| SQL | 자동 생성 | 직접 작성 |
| 객체 중심 | ✅ | ❌ |
| SQL 제어 | 제한적 | 완전 제어 |
| 복잡한 쿼리 | 어려움 | 쉬움 |
| 학습 곡선 | 높음 | 낮음 |

### 사용 시나리오

**JPA 적합:**
- 도메인 중심 설계
- CRUD 위주
- 단순한 쿼리

**MyBatis 적합:**
- 복잡한 조인
- 동적 SQL
- 레거시 DB
- 통계/리포트 쿼리

## 의존성 추가

### Maven

```xml
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>3.0.3</version>
</dependency>
```

### Gradle

```gradle
implementation 'org.mybatis.spring.boot:mybatis-spring-boot-starter:3.0.3'
```

## 설정

### application.yml

```yaml
mybatis:
  type-aliases-package: com.example.demo.domain
  mapper-locations: classpath:mapper/**/*.xml
  configuration:
    map-underscore-to-camel-case: true
    default-fetch-size: 100
    default-statement-timeout: 30
    log-impl: org.apache.ibatis.logging.slf4j.Slf4jImpl
```

## Mapper 인터페이스

### 기본 Mapper

```java
package com.example.demo.mapper;

import com.example.demo.domain.User;
import org.apache.ibatis.annotations.*;

import java.util.List;
import java.util.Optional;

@Mapper
public interface UserMapper {
    
    // 조회
    @Select("SELECT * FROM users WHERE id = #{id}")
    Optional<User> findById(Long id);
    
    // 전체 조회
    @Select("SELECT * FROM users")
    List<User> findAll();
    
    // 삽입
    @Insert("INSERT INTO users (name, email, password) VALUES (#{name}, #{email}, #{password})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    void insert(User user);
    
    // 수정
    @Update("UPDATE users SET name = #{name}, email = #{email} WHERE id = #{id}")
    int update(User user);
    
    // 삭제
    @Delete("DELETE FROM users WHERE id = #{id}")
    int deleteById(Long id);
}
```

## XML 매핑

### Mapper XML 파일

**src/main/resources/mapper/UserMapper.xml:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.example.demo.mapper.UserMapper">
    
    <!-- Result Map -->
    <resultMap id="userResultMap" type="User">
        <id property="id" column="id"/>
        <result property="name" column="name"/>
        <result property="email" column="email"/>
        <result property="status" column="status"/>
        <result property="createdAt" column="created_at"/>
    </resultMap>
    
    <!-- 조회 -->
    <select id="findById" resultMap="userResultMap">
        SELECT * FROM users WHERE id = #{id}
    </select>
    
    <!-- 전체 조회 -->
    <select id="findAll" resultMap="userResultMap">
        SELECT * FROM users
    </select>
    
    <!-- 조건 조회 -->
    <select id="findByEmail" resultMap="userResultMap">
        SELECT * FROM users WHERE email = #{email}
    </select>
    
    <!-- 삽입 -->
    <insert id="insert" useGeneratedKeys="true" keyProperty="id">
        INSERT INTO users (name, email, password, status, created_at)
        VALUES (#{name}, #{email}, #{password}, #{status}, NOW())
    </insert>
    
    <!-- 수정 -->
    <update id="update">
        UPDATE users
        SET name = #{name},
            email = #{email},
            updated_at = NOW()
        WHERE id = #{id}
    </update>
    
    <!-- 삭제 -->
    <delete id="deleteById">
        DELETE FROM users WHERE id = #{id}
    </delete>
    
</mapper>
```

## 동적 SQL

### if 조건

```xml
<select id="search" resultMap="userResultMap">
    SELECT * FROM users
    WHERE 1=1
    <if test="name != null and name != ''">
        AND name LIKE CONCAT('%', #{name}, '%')
    </if>
    <if test="email != null and email != ''">
        AND email = #{email}
    </if>
    <if test="status != null">
        AND status = #{status}
    </if>
</select>
```

### choose, when, otherwise

```xml
<select id="findByCondition" resultMap="userResultMap">
    SELECT * FROM users
    WHERE
    <choose>
        <when test="id != null">
            id = #{id}
        </when>
        <when test="email != null">
            email = #{email}
        </when>
        <otherwise>
            status = 'ACTIVE'
        </otherwise>
    </choose>
</select>
```

### where, trim

```xml
<select id="search" resultMap="userResultMap">
    SELECT * FROM users
    <where>
        <if test="name != null">
            AND name = #{name}
        </if>
        <if test="email != null">
            AND email = #{email}
        </if>
    </where>
</select>
```

### foreach

```xml
<!-- IN 절 -->
<select id="findByIds" resultMap="userResultMap">
    SELECT * FROM users
    WHERE id IN
    <foreach collection="ids" item="id" open="(" separator="," close=")">
        #{id}
    </foreach>
</select>

<!-- Batch Insert -->
<insert id="insertBatch">
    INSERT INTO users (name, email, password)
    VALUES
    <foreach collection="users" item="user" separator=",">
        (#{user.name}, #{user.email}, #{user.password})
    </foreach>
</insert>
```

### set

```xml
<update id="updateSelective">
    UPDATE users
    <set>
        <if test="name != null">name = #{name},</if>
        <if test="email != null">email = #{email},</if>
        <if test="status != null">status = #{status},</if>
        updated_at = NOW()
    </set>
    WHERE id = #{id}
</update>
```

## 복잡한 조인

### 일대다 매핑

```xml
<resultMap id="userWithOrdersMap" type="User">
    <id property="id" column="user_id"/>
    <result property="name" column="user_name"/>
    <result property="email" column="email"/>
    <collection property="orders" ofType="Order">
        <id property="id" column="order_id"/>
        <result property="orderNumber" column="order_number"/>
        <result property="totalAmount" column="total_amount"/>
        <result property="status" column="order_status"/>
    </collection>
</resultMap>

<select id="findUserWithOrders" resultMap="userWithOrdersMap">
    SELECT
        u.id AS user_id,
        u.name AS user_name,
        u.email,
        o.id AS order_id,
        o.order_number,
        o.total_amount,
        o.status AS order_status
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.id = #{id}
</select>
```

### 다대일 매핑

```xml
<resultMap id="orderWithUserMap" type="Order">
    <id property="id" column="order_id"/>
    <result property="orderNumber" column="order_number"/>
    <result property="totalAmount" column="total_amount"/>
    <association property="user" javaType="User">
        <id property="id" column="user_id"/>
        <result property="name" column="user_name"/>
        <result property="email" column="email"/>
    </association>
</resultMap>

<select id="findOrderWithUser" resultMap="orderWithUserMap">
    SELECT
        o.id AS order_id,
        o.order_number,
        o.total_amount,
        u.id AS user_id,
        u.name AS user_name,
        u.email
    FROM orders o
    INNER JOIN users u ON o.user_id = u.id
    WHERE o.id = #{id}
</select>
```

## 페이징

### PageHelper 사용

**의존성:**
```xml
<dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper-spring-boot-starter</artifactId>
    <version>1.4.7</version>
</dependency>
```

**Mapper:**
```java
@Mapper
public interface UserMapper {
    List<User> findAll();
}
```

**Service:**
```java
@Service
@RequiredArgsConstructor
public class UserService {
    
    private final UserMapper userMapper;
    
    public PageInfo<User> getUsers(int pageNum, int pageSize) {
        // 페이징 시작
        PageHelper.startPage(pageNum, pageSize);
        
        List<User> users = userMapper.findAll();
        
        // PageInfo로 변환
        return new PageInfo<>(users);
    }
}
```

## Service에서 사용

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserService {
    
    private final UserMapper userMapper;
    private final UserRepository userRepository;  // JPA와 함께 사용
    
    public UserResponse getUser(Long id) {
        // MyBatis 사용
        User user = userMapper.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id));
        
        return UserResponse.from(user);
    }
    
    @Transactional
    public UserResponse createUser(UserCreateRequest request) {
        User user = User.builder()
                .name(request.getName())
                .email(request.getEmail())
                .password(request.getPassword())
                .build();
        
        // MyBatis 사용
        userMapper.insert(user);
        
        return UserResponse.from(user);
    }
    
    public List<UserResponse> searchUsers(UserSearchCondition condition) {
        // 복잡한 검색은 MyBatis
        List<User> users = userMapper.search(condition);
        return users.stream()
                .map(UserResponse::from)
                .toList();
    }
    
    @Transactional
    public UserResponse updateUser(Long id, UserUpdateRequest request) {
        // JPA 사용 (변경 감지)
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id));
        
        user.update(request.getName(), request.getEmail());
        
        return UserResponse.from(user);
    }
}
```

## 실전 예제

### 통계 쿼리

```xml
<select id="getUserStatistics" resultType="map">
    SELECT
        DATE(created_at) AS date,
        status,
        COUNT(*) AS count
    FROM users
    WHERE created_at BETWEEN #{startDate} AND #{endDate}
    GROUP BY DATE(created_at), status
    ORDER BY date DESC, status
</select>
```

### 복잡한 동적 검색

```xml
<select id="searchOrders" resultMap="orderResultMap">
    SELECT
        o.*,
        u.name AS user_name
    FROM orders o
    INNER JOIN users u ON o.user_id = u.id
    <where>
        <if test="userId != null">
            AND o.user_id = #{userId}
        </if>
        <if test="status != null">
            AND o.status = #{status}
        </if>
        <if test="startDate != null and endDate != null">
            AND o.created_at BETWEEN #{startDate} AND #{endDate}
        </if>
        <if test="minAmount != null">
            AND o.total_amount >= #{minAmount}
        </if>
        <if test="maxAmount != null">
            AND o.total_amount &lt;= #{maxAmount}
        </if>
        <if test="orderNumber != null and orderNumber != ''">
            AND o.order_number LIKE CONCAT('%', #{orderNumber}, '%')
        </if>
    </where>
    <choose>
        <when test="sortBy == 'date'">
            ORDER BY o.created_at DESC
        </when>
        <when test="sortBy == 'amount'">
            ORDER BY o.total_amount DESC
        </when>
        <otherwise>
            ORDER BY o.id DESC
        </otherwise>
    </choose>
    <if test="limit != null">
        LIMIT #{limit}
    </if>
</select>
```

## JPA + MyBatis 혼용

### 패키지 구조

```
com.example.demo/
├── domain/
│   └── User.java              # Entity (JPA)
├── repository/
│   └── UserRepository.java    # JpaRepository
├── mapper/
│   └── UserMapper.java        # MyBatis Mapper
└── service/
    └── UserService.java       # 둘 다 사용
```

### 혼용 전략

```java
@Service
@RequiredArgsConstructor
public class OrderService {
    
    private final OrderRepository orderRepository;  // JPA
    private final OrderMapper orderMapper;          // MyBatis
    
    // 단순 CRUD는 JPA
    @Transactional
    public Order createOrder(OrderCreateRequest request) {
        Order order = Order.from(request);
        return orderRepository.save(order);
    }
    
    // 복잡한 조회는 MyBatis
    public List<OrderStatistics> getStatistics(LocalDate start, LocalDate end) {
        return orderMapper.getStatistics(start, end);
    }
    
    // 복잡한 검색은 MyBatis
    public Page<OrderDto> searchOrders(OrderSearchCondition condition, Pageable pageable) {
        PageHelper.startPage(pageable.getPageNumber(), pageable.getPageSize());
        List<OrderDto> orders = orderMapper.search(condition);
        return new PageImpl<>(orders, pageable, ((com.github.pagehelper.Page) orders).getTotal());
    }
}
```

## 실전 팁

### 1. SQL 로깅

```yaml
logging:
  level:
    com.example.demo.mapper: DEBUG
```

### 2. Camel Case 변환

```yaml
mybatis:
  configuration:
    map-underscore-to-camel-case: true
```

### 3. Type Handler

```java
@MappedTypes(UserStatus.class)
public class UserStatusTypeHandler extends BaseTypeHandler<UserStatus> {
    
    @Override
    public void setNonNullParameter(PreparedStatement ps, int i, 
                                    UserStatus parameter, JdbcType jdbcType) throws SQLException {
        ps.setString(i, parameter.name());
    }
    
    @Override
    public UserStatus getNullableResult(ResultSet rs, String columnName) throws SQLException {
        String value = rs.getString(columnName);
        return value == null ? null : UserStatus.valueOf(value);
    }
    
    // 다른 메서드들...
}
```

### 4. XML 재사용

```xml
<sql id="userColumns">
    id, name, email, status, created_at, updated_at
</sql>

<select id="findById" resultMap="userResultMap">
    SELECT <include refid="userColumns"/>
    FROM users
    WHERE id = #{id}
</select>
```

## 다음 단계

MyBatis를 배웠습니다. 이제 REST API 설계를 알아봅시다.

👉 [다음: REST API 설계](14-rest-api-design.md)

## 참고 자료

- [MyBatis Documentation](https://mybatis.org/mybatis-3/)
- [MyBatis-Spring-Boot-Starter](https://mybatis.org/spring-boot-starter/)
- [PageHelper](https://github.com/pagehelper/Mybatis-PageHelper)
