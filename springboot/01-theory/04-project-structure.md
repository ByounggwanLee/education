# 프로젝트 구조

Spring Boot 프로젝트의 표준 디렉토리 구조와 패키지 구성 방법을 알아봅니다.

## 기본 디렉토리 구조

### Maven 프로젝트

```
demo/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/demo/
│   │   │       ├── DemoApplication.java
│   │   │       ├── controller/
│   │   │       ├── service/
│   │   │       ├── repository/
│   │   │       ├── domain/
│   │   │       ├── dto/
│   │   │       ├── config/
│   │   │       └── exception/
│   │   └── resources/
│   │       ├── application.yml
│   │       ├── application-local.yml
│   │       ├── application-dev.yml
│   │       ├── application-prod.yml
│   │       ├── messages.properties
│   │       ├── messages_ko.properties
│   │       ├── messages_en.properties
│   │       ├── static/
│   │       │   ├── css/
│   │       │   ├── js/
│   │       │   └── images/
│   │       └── templates/
│   └── test/
│       ├── java/
│       │   └── com/example/demo/
│       │       ├── controller/
│       │       ├── service/
│       │       └── repository/
│       └── resources/
│           └── application.yml
├── pom.xml
└── README.md
```

### Gradle 프로젝트

```
demo/
├── src/
│   ├── main/
│   │   ├── java/
│   │   └── resources/
│   └── test/
│       ├── java/
│       └── resources/
├── build.gradle
├── settings.gradle
└── README.md
```

## 패키지 구조

### 계층형 구조 (Layer-based)

기능별로 패키지를 나누는 전통적인 방식입니다.

```
com.example.demo/
├── DemoApplication.java
├── controller/                  # 컨트롤러 계층
│   ├── UserController.java
│   ├── ProductController.java
│   └── OrderController.java
├── service/                     # 서비스 계층
│   ├── UserService.java
│   ├── UserServiceImpl.java
│   ├── ProductService.java
│   ├── ProductServiceImpl.java
│   ├── OrderService.java
│   └── OrderServiceImpl.java
├── repository/                  # 레포지토리 계층
│   ├── UserRepository.java
│   ├── ProductRepository.java
│   └── OrderRepository.java
├── domain/                      # 도메인 엔티티
│   ├── User.java
│   ├── Product.java
│   └── Order.java
├── dto/                         # 데이터 전송 객체
│   ├── request/
│   │   ├── UserCreateRequest.java
│   │   ├── UserUpdateRequest.java
│   │   └── OrderCreateRequest.java
│   └── response/
│       ├── UserResponse.java
│       ├── ProductResponse.java
│       └── OrderResponse.java
├── config/                      # 설정 클래스
│   ├── WebConfig.java
│   ├── SecurityConfig.java
│   └── JpaConfig.java
├── exception/                   # 예외 처리
│   ├── BusinessException.java
│   ├── ErrorCode.java
│   ├── ErrorResponse.java
│   └── GlobalExceptionHandler.java
├── common/                      # 공통 모듈
│   ├── util/
│   │   ├── DateUtils.java
│   │   └── StringUtils.java
│   └── constants/
│       └── AppConstants.java
└── mapper/                      # 매퍼 (MapStruct 등)
    ├── UserMapper.java
    └── ProductMapper.java
```

**장점:**
- ✅ 계층별로 명확히 구분
- ✅ 역할에 따라 쉽게 찾을 수 있음
- ✅ 소규모 프로젝트에 적합

**단점:**
- ❌ 패키지 간 의존관계 파악 어려움
- ❌ 대규모 프로젝트에서 패키지가 비대해짐
- ❌ 비즈니스 기능 단위 파악 어려움

### 도메인형 구조 (Domain-based / Feature-based)

비즈니스 도메인별로 패키지를 나누는 방식입니다.

```
com.example.demo/
├── DemoApplication.java
├── user/                        # 사용자 도메인
│   ├── domain/
│   │   └── User.java
│   ├── dto/
│   │   ├── UserCreateRequest.java
│   │   ├── UserUpdateRequest.java
│   │   └── UserResponse.java
│   ├── controller/
│   │   └── UserController.java
│   ├── service/
│   │   ├── UserService.java
│   │   └── UserServiceImpl.java
│   ├── repository/
│   │   └── UserRepository.java
│   └── mapper/
│       └── UserMapper.java
├── product/                     # 상품 도메인
│   ├── domain/
│   │   └── Product.java
│   ├── dto/
│   │   ├── ProductCreateRequest.java
│   │   └── ProductResponse.java
│   ├── controller/
│   │   └── ProductController.java
│   ├── service/
│   │   ├── ProductService.java
│   │   └── ProductServiceImpl.java
│   └── repository/
│       └── ProductRepository.java
├── order/                       # 주문 도메인
│   ├── domain/
│   │   ├── Order.java
│   │   └── OrderItem.java
│   ├── dto/
│   │   ├── OrderCreateRequest.java
│   │   └── OrderResponse.java
│   ├── controller/
│   │   └── OrderController.java
│   ├── service/
│   │   ├── OrderService.java
│   │   └── OrderServiceImpl.java
│   └── repository/
│       └── OrderRepository.java
├── common/                      # 공통 모듈
│   ├── config/
│   │   ├── WebConfig.java
│   │   └── JpaConfig.java
│   ├── exception/
│   │   ├── BusinessException.java
│   │   ├── ErrorCode.java
│   │   └── GlobalExceptionHandler.java
│   └── util/
│       ├── DateUtils.java
│       └── StringUtils.java
└── global/                      # 전역 설정
    ├── security/
    │   └── SecurityConfig.java
    └── audit/
        └── AuditingConfig.java
```

**장점:**
- ✅ 비즈니스 기능 단위로 명확히 분리
- ✅ 도메인별 독립성 유지
- ✅ 대규모 프로젝트에 적합
- ✅ 마이크로서비스로 전환 용이

**단점:**
- ❌ 초반 구조 설계 필요
- ❌ 공통 모듈 관리 필요
- ❌ 소규모 프로젝트에는 과할 수 있음

## resources 디렉토리

### application.yml/properties

환경 설정 파일입니다.

```
resources/
├── application.yml              # 기본 설정
├── application-local.yml        # 로컬 환경
├── application-dev.yml          # 개발 환경
├── application-prod.yml         # 운영 환경
└── application-test.yml         # 테스트 환경
```

**application.yml:**
```yaml
spring:
  profiles:
    active: local              # 활성화할 프로파일

  application:
    name: demo-application

server:
  port: 8080
```

**application-local.yml:**
```yaml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password:

logging:
  level:
    root: INFO
    com.example.demo: DEBUG
```

### 다국어 메시지

```
resources/
├── messages.properties          # 기본
├── messages_ko.properties       # 한국어
├── messages_en.properties       # 영어
└── messages_ja.properties       # 일본어
```

### static 디렉토리

정적 리소스 (CSS, JavaScript, 이미지 등)

```
static/
├── css/
│   └── style.css
├── js/
│   └── app.js
└── images/
    └── logo.png
```

**접근 경로:** `http://localhost:8080/css/style.css`

### templates 디렉토리

템플릿 파일 (Thymeleaf, FreeMarker 등)

```
templates/
├── index.html
├── user/
│   ├── list.html
│   └── detail.html
└── error/
    ├── 404.html
    └── 500.html
```

## 테스트 구조

### 테스트 패키지 구조

```
src/test/java/com/example/demo/
├── controller/
│   ├── UserControllerTest.java
│   └── ProductControllerTest.java
├── service/
│   ├── UserServiceTest.java
│   └── ProductServiceTest.java
├── repository/
│   ├── UserRepositoryTest.java
│   └── ProductRepositoryTest.java
└── integration/
    ├── UserIntegrationTest.java
    └── OrderIntegrationTest.java
```

### 테스트 리소스

```
src/test/resources/
├── application.yml              # 테스트용 설정
├── data.sql                     # 테스트 데이터
└── schema.sql                   # 테스트 스키마
```

## 멀티 모듈 프로젝트

대규모 프로젝트는 멀티 모듈로 구성할 수 있습니다.

```
demo/
├── demo-api/                    # REST API 모듈
│   ├── src/
│   └── pom.xml
├── demo-core/                   # 핵심 비즈니스 로직
│   ├── src/
│   └── pom.xml
├── demo-domain/                 # 도메인 모델
│   ├── src/
│   └── pom.xml
├── demo-infrastructure/         # 인프라 (DB, 외부 API)
│   ├── src/
│   └── pom.xml
├── demo-batch/                  # 배치 작업
│   ├── src/
│   └── pom.xml
└── pom.xml                      # 부모 POM
```

**부모 pom.xml:**
```xml
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>demo</artifactId>
    <version>1.0.0</version>
    <packaging>pom</packaging>

    <modules>
        <module>demo-api</module>
        <module>demo-core</module>
        <module>demo-domain</module>
        <module>demo-infrastructure</module>
        <module>demo-batch</module>
    </modules>
</project>
```

## 네이밍 규칙

### 클래스 네이밍

| 타입 | 네이밍 규칙 | 예시 |
|------|------------|------|
| Controller | `*Controller` | `UserController` |
| RestController | `*Controller` | `UserController` |
| Service (인터페이스) | `*Service` | `UserService` |
| Service (구현체) | `*ServiceImpl` | `UserServiceImpl` |
| Repository | `*Repository` | `UserRepository` |
| Entity | 도메인명 | `User`, `Product` |
| DTO (Request) | `*Request` / `*Dto` | `UserCreateRequest` |
| DTO (Response) | `*Response` / `*Dto` | `UserResponse` |
| Mapper | `*Mapper` | `UserMapper` |
| Config | `*Config` | `WebConfig` |
| Exception | `*Exception` | `UserNotFoundException` |
| Util | `*Utils` / `*Helper` | `DateUtils` |

### 패키지 네이밍

- 소문자만 사용
- 단수형 사용 (user, product)
- 명확하고 간결하게

```java
// ✅ 좋은 예
com.example.demo.user.controller
com.example.demo.product.service
com.example.demo.order.repository

// ❌ 나쁜 예
com.example.demo.User.Controller    // 대문자 사용
com.example.demo.users.service      // 복수형 사용
com.example.demo.p.s                // 약어 사용
```

## 실전 팁

### 1. 프로젝트 규모에 따른 선택

**소규모 프로젝트 (~10개 도메인):**
- 계층형 구조 권장
- 간단하고 직관적

**중대규모 프로젝트 (10개 이상):**
- 도메인형 구조 권장
- 비즈니스 기능별 독립성 확보

### 2. 패키지 접근 제어

```java
// package-private: 같은 패키지 내에서만 접근 가능
class UserValidator {
    boolean validate(User user) {
        // ...
    }
}

// public: 다른 패키지에서도 접근 가능
public class UserService {
    // ...
}
```

### 3. 공통 모듈 분리

```
common/
├── util/              # 유틸리티
├── constants/         # 상수
├── exception/         # 공통 예외
└── dto/              # 공통 DTO
```

### 4. 설정 파일 분리

```yaml
# application.yml (공통)
spring:
  application:
    name: demo

---
# application-local.yml (로컬 환경)
spring:
  config:
    activate:
      on-profile: local
  datasource:
    url: jdbc:h2:mem:testdb

---
# application-prod.yml (운영 환경)
spring:
  config:
    activate:
      on-profile: prod
  datasource:
    url: jdbc:mysql://prod-server:3306/db
```

## 프로젝트 생성

### Spring Initializr 사용

**웹사이트:** https://start.spring.io/

**옵션 선택:**
- Project: Maven/Gradle
- Language: Java
- Spring Boot: 3.2.x
- Packaging: Jar
- Java: 17 이상

**Dependencies:**
- Spring Web
- Spring Data JPA
- Lombok
- Validation
- H2 Database

### IDE에서 생성

**IntelliJ IDEA:**
1. File → New → Project
2. Spring Initializr 선택
3. 설정 입력 후 생성

**VS Code:**
1. Command Palette (Ctrl+Shift+P)
2. "Spring Initializr: Create a Maven Project"
3. 설정 입력 후 생성

## 정리

### 핵심 내용

1. **계층형 구조:** 소규모 프로젝트, 역할별 분리
2. **도메인형 구조:** 대규모 프로젝트, 기능별 분리
3. **resources:** 설정 파일, 정적 리소스, 템플릿
4. **test:** 프로덕션 코드와 동일한 패키지 구조

### 권장사항

- ✅ 프로젝트 규모에 맞는 구조 선택
- ✅ 일관된 네이밍 규칙 적용
- ✅ 환경별 설정 분리
- ✅ 공통 모듈 재사용

## 다음 단계

프로젝트 구조를 배웠습니다. 이제 계층형 아키텍처를 자세히 알아봅시다.

👉 [다음: 계층형 아키텍처](05-layered-architecture.md)

## 참고 자료

- [Spring Boot Project Structure](https://docs.spring.io/spring-boot/docs/current/reference/html/using.html#using.structuring-your-code)
- [Package by Feature](https://phauer.com/2020/package-by-feature/)
