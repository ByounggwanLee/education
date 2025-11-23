# Spring Boot 소개

Spring Boot는 Spring 기반 애플리케이션을 빠르고 쉽게 개발할 수 있도록 도와주는 프레임워크입니다.

## Spring Boot란?

### 정의

Spring Boot는 **"Just Run"** 철학을 가진 프레임워크로, 최소한의 설정으로 프로덕션 레벨의 Spring 애플리케이션을 만들 수 있습니다.

### 탄생 배경

**전통적인 Spring의 문제점:**
- 복잡한 XML 설정
- 의존성 버전 관리의 어려움
- 많은 보일러플레이트 코드
- 애플리케이션 서버 설정의 복잡성

**Spring Boot의 해결책:**
- Convention over Configuration (관례에 의한 설정)
- 자동 설정 (Auto Configuration)
- 내장 서버 (Embedded Server)
- Starter 의존성

## 주요 특징

### 1. 자동 설정 (Auto Configuration)

클래스패스에 있는 라이브러리를 감지하여 자동으로 설정합니다.

```java
// Spring Boot가 자동으로 설정하는 것들
- DataSource (데이터베이스 연결)
- JPA EntityManager
- 트랜잭션 관리
- 웹 서버 (Tomcat, Jetty)
- 보안 설정
```

### 2. Starter 의존성

관련된 의존성을 묶어서 제공합니다.

```xml
<!-- 웹 개발에 필요한 모든 것 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>

<!-- 포함되는 것들:
  - Spring MVC
  - Jackson (JSON)
  - Tomcat (내장 서버)
  - Validation
-->
```

### 3. 내장 서버

별도의 서버 설치 없이 JAR 파일 하나로 실행 가능합니다.

```bash
# 기존 방식: WAR 파일을 Tomcat에 배포
# Spring Boot: JAR 실행
java -jar myapp.jar
```

### 4. 프로덕션 준비 기능

운영에 필요한 기능들이 기본 제공됩니다.

- **Actuator**: 헬스 체크, 메트릭, 모니터링
- **외부 설정**: Properties, YAML
- **프로파일**: 환경별 설정 분리
- **로깅**: 기본 로깅 설정

## Spring vs Spring Boot 비교

### 전통적인 Spring 애플리케이션

```xml
<!-- web.xml -->
<web-app>
    <servlet>
        <servlet-name>dispatcher</servlet-name>
        <servlet-class>
            org.springframework.web.servlet.DispatcherServlet
        </servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>/WEB-INF/spring/appServlet/servlet-context.xml</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <!-- ... 수십 줄의 설정 ... -->
</web-app>
```

```xml
<!-- applicationContext.xml -->
<beans>
    <context:component-scan base-package="com.example"/>
    <mvc:annotation-driven/>
    <bean id="dataSource" class="...">
        <property name="driverClassName" value="..."/>
        <property name="url" value="..."/>
        <!-- ... -->
    </bean>
    <!-- ... 수십 개의 Bean 설정 ... -->
</beans>
```

### Spring Boot 애플리케이션

```java
// DemoApplication.java - 이게 전부!
@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

```yaml
# application.yml - 간단한 설정
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb
    username: user
    password: pass
```

## Spring Boot의 핵심 어노테이션

### @SpringBootApplication

세 가지 어노테이션의 조합입니다:

```java
@SpringBootApplication
// = @SpringBootConfiguration + @EnableAutoConfiguration + @ComponentScan
public class DemoApplication {
    // ...
}
```

**구성 요소:**

1. **@SpringBootConfiguration**
   - Spring의 @Configuration과 동일
   - 설정 클래스임을 나타냄

2. **@EnableAutoConfiguration**
   - 자동 설정 활성화
   - 클래스패스의 라이브러리 기반으로 자동 설정

3. **@ComponentScan**
   - @Component, @Service, @Repository, @Controller 스캔
   - 현재 패키지 및 하위 패키지 스캔

## 프로젝트 구조

### 표준 Maven 프로젝트 구조

```
demo/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/demo/
│   │   │       ├── controller/
│   │   │       ├── service/
│   │   │       ├── repository/
│   │   │       ├── domain/
│   │   │       ├── dto/
│   │   │       ├── config/
│   │   │       └── DemoApplication.java
│   │   └── resources/
│   │       ├── application.yml
│   │       ├── static/           # 정적 리소스
│   │       ├── templates/        # 템플릿 (Thymeleaf 등)
│   │       └── mybatis/          # MyBatis 매퍼
│   └── test/
│       └── java/
│           └── com/example/demo/
│               └── DemoApplicationTests.java
├── target/                        # 빌드 결과물
├── pom.xml                        # Maven 설정
└── README.md
```

### 패키지 구조 (계층형 아키텍처)

```java
com.example.demo
├── controller      // 웹 요청 처리
├── service         // 비즈니스 로직
├── repository      // 데이터 접근
├── domain          // 엔티티 (JPA Entity)
├── dto             // 데이터 전송 객체
│   ├── request     // 요청 DTO
│   └── response    // 응답 DTO
├── mapper          // MapStruct 매퍼
├── config          // 설정 클래스
├── exception       // 예외 클래스
├── interceptor     // 인터셉터
├── aop             // AOP
└── common          // 공통 유틸리티
```

## Spring Boot Starters

### 주요 Starter 목록

| Starter | 설명 | 포함 라이브러리 |
|---------|------|-----------------|
| `spring-boot-starter-web` | 웹 애플리케이션 | Spring MVC, Tomcat, Jackson |
| `spring-boot-starter-data-jpa` | JPA | Hibernate, Spring Data JPA |
| `spring-boot-starter-validation` | 검증 | Hibernate Validator |
| `spring-boot-starter-security` | 보안 | Spring Security |
| `spring-boot-starter-actuator` | 모니터링 | Actuator |
| `spring-boot-starter-test` | 테스트 | JUnit, Mockito, AssertJ |
| `spring-boot-starter-cache` | 캐싱 | Spring Cache |
| `spring-boot-starter-aop` | AOP | AspectJ |

### Starter 사용 예시

**Maven:**
```xml
<dependencies>
    <!-- 웹 개발 -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    
    <!-- JPA -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    
    <!-- H2 데이터베이스 -->
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>runtime</scope>
    </dependency>
</dependencies>
```

**Gradle:**
```gradle
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    runtimeOnly 'com.h2database:h2'
}
```

## Spring Boot의 장점

### 1. 빠른 개발 시작

```bash
# 5분 안에 실행 가능한 애플리케이션 생성
1. start.spring.io 접속
2. 의존성 선택
3. 프로젝트 다운로드
4. ./mvnw spring-boot:run
```

### 2. 운영 환경 준비

```yaml
# application.yml 만으로 대부분 설정 완료
spring:
  profiles:
    active: prod
  datasource:
    url: ${DB_URL}
    username: ${DB_USER}
    password: ${DB_PASSWORD}
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
```

### 3. 마이크로서비스 친화적

- 독립 실행 가능 (Standalone)
- 가볍고 빠른 시작 시간
- 클라우드 네이티브
- Docker 컨테이너화 용이

### 4. 강력한 커뮤니티

- 방대한 문서
- 활발한 오픈소스 생태계
- 정기적인 업데이트

## Spring Boot 버전

### Long-Term Support (LTS)

| 버전 | 출시일 | Java 버전 | 지원 종료 |
|------|--------|-----------|----------|
| 2.7.x | 2022.05 | 8, 11, 17 | 2025.05 |
| 3.0.x | 2022.11 | 17+ | 2024.11 |
| 3.1.x | 2023.05 | 17+ | 2025.05 |
| 3.2.x | 2023.11 | 17+ | 2025.11 |

### 버전 선택 가이드

**프로젝트 특성에 따라:**
- **신규 프로젝트**: 최신 안정 버전 (3.2.x 권장)
- **기존 프로젝트**: LTS 버전 유지
- **레거시 시스템**: 2.7.x (Java 8 지원)

## Spring Boot vs 다른 프레임워크

### Spring Boot vs 순수 Spring

| 항목 | Spring Boot | 순수 Spring |
|------|-------------|------------|
| 설정 복잡도 | 낮음 | 높음 |
| 학습 곡선 | 완만함 | 가파름 |
| 개발 속도 | 빠름 | 느림 |
| 유연성 | 높음 | 매우 높음 |
| 프로덕션 준비 | 기본 제공 | 직접 구성 |

### Spring Boot vs Node.js (Express)

| 항목 | Spring Boot | Express |
|------|-------------|---------|
| 언어 | Java | JavaScript |
| 타입 안정성 | 높음 | 낮음 (TypeScript로 개선) |
| 성능 | 높음 (멀티스레드) | 중간 (단일스레드) |
| 생태계 | 엔터프라이즈 | 빠른 개발 |
| 트랜잭션 | 강력함 | 제한적 |

## 언제 Spring Boot를 사용해야 하나?

### ✅ Spring Boot가 적합한 경우

- 엔터프라이즈 애플리케이션
- RESTful API 서버
- 마이크로서비스 아키텍처
- 복잡한 비즈니스 로직
- 트랜잭션이 중요한 시스템
- 데이터베이스 중심 애플리케이션

### ⚠️ 다른 선택지를 고려할 경우

- 초소형 서비스 (Serverless 고려)
- 실시간 채팅 (WebSocket 특화 프레임워크)
- 매우 높은 동시성 (Go, Kotlin Coroutines)
- 빠른 프로토타입 (Node.js, Python Flask)

## 다음 단계

Spring Boot의 기본 개념을 이해했습니다. 이제 프로젝트를 생성하고 구조를 살펴봅시다.

👉 [다음: 프로젝트 생성 및 구조](02-project-setup.md)

## 참고 자료

- [Spring Boot Reference Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Spring Boot GitHub](https://github.com/spring-projects/spring-boot)
- [Spring Initializr](https://start.spring.io/)
- [Baeldung Spring Boot Tutorials](https://www.baeldung.com/spring-boot)
