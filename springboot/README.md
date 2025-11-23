# Spring Boot 완벽 가이드

프로젝트 개발자를 위한 Spring Boot 실전 학습 자료입니다.

## 📋 대상

- 엔터프라이즈 애플리케이션 개발자
- Spring Boot 프로젝트 개발팀
- 백엔드 개발 입문자 및 실무자

## 🎯 학습 목표

이 과정을 통해 다음을 학습할 수 있습니다:

- Spring Boot 프로젝트 구조 및 설정
- Maven/Gradle 빌드 도구 활용
- JPA와 MyBatis를 활용한 데이터 접근
- RESTful API 설계 및 OpenAPI 문서화
- Feign Client를 활용한 마이크로서비스 통신
- Kafka를 활용한 메시지 기반 아키텍처
- 계층형 아키텍처 (Controller, Service, Repository)
- DTO 패턴과 MapStruct를 활용한 객체 변환
- 설정 관리 (Config, Properties)
- AOP와 Interceptor를 활용한 횡단 관심사
- 환경별 설정 관리 (local, dev, prod)
- 전역 예외 처리 및 비즈니스 예외
- 다국어 처리 (i18n)

## 📚 과정 구성

### 1. 이론 (01-theory)

#### 기초
1. [Spring Boot 소개](01-theory/01-intro.md)
2. [프로젝트 생성 및 구조](01-theory/02-project-setup.md)
3. [Maven vs Gradle](01-theory/03-build-tools.md)
4. [의존성 관리](01-theory/04-dependencies.md)

#### 계층 아키텍처
5. [계층형 아키텍처 개요](01-theory/05-layered-architecture.md)
6. [Controller 레이어](01-theory/06-controller.md)
7. [Service 레이어](01-theory/07-service.md)
8. [Repository 레이어](01-theory/08-repository.md)
9. [DTO와 Entity](01-theory/09-dto-entity.md)
10. [MapStruct 객체 변환](01-theory/10-mapstruct.md)

#### 데이터 접근
11. [JPA 기본](01-theory/11-jpa-basics.md)
12. [JPA 고급](01-theory/12-jpa-advanced.md)
13. [MyBatis 통합](01-theory/13-mybatis.md)

#### API 설계
14. [RESTful API 설계](01-theory/14-restful-api.md)
15. [OpenAPI/Swagger 문서화](01-theory/15-openapi.md)
16. [API 버전 관리](01-theory/16-api-versioning.md)

#### 외부 통신
17. [Feign Client](01-theory/17-feign-client.md)
18. [RestTemplate vs WebClient](01-theory/18-rest-clients.md)

#### 메시징
19. [Kafka 기본](01-theory/19-kafka-basics.md)
20. [Kafka Producer/Consumer](01-theory/20-kafka-implementation.md)

#### 설정 및 구성
21. [Application.yml 설정](01-theory/21-application-properties.md)
22. [환경별 설정 (Profile)](01-theory/22-profiles.md)
23. [Config 클래스](01-theory/23-configuration.md)

#### 횡단 관심사
24. [Interceptor](01-theory/24-interceptor.md)
25. [AOP (Aspect Oriented Programming)](01-theory/25-aop.md)
26. [Filter vs Interceptor vs AOP](01-theory/26-filter-interceptor-aop.md)

#### 예외 처리
27. [예외 처리 전략](01-theory/27-exception-strategy.md)
28. [GlobalExceptionHandler](01-theory/28-global-exception.md)
29. [커스텀 예외 설계](01-theory/29-custom-exception.md)

#### 다국어 및 보안
30. [다국어 처리 (i18n)](01-theory/30-internationalization.md)
31. [Validation](01-theory/31-validation.md)

### 2. 실습 (02-practice)

1. [Lab 1: Spring Boot 프로젝트 생성](02-practice/lab01-project-creation.md)
2. [Lab 2: 기본 CRUD API 구현](02-practice/lab02-basic-crud.md)
3. [Lab 3: JPA 엔티티 및 Repository](02-practice/lab03-jpa-repository.md)
4. [Lab 4: Service 레이어 구현](02-practice/lab04-service-layer.md)
5. [Lab 5: DTO와 MapStruct](02-practice/lab05-dto-mapstruct.md)
6. [Lab 6: OpenAPI 문서화](02-practice/lab06-openapi-docs.md)
7. [Lab 7: MyBatis 통합](02-practice/lab07-mybatis.md)
8. [Lab 8: Feign Client 구현](02-practice/lab08-feign-client.md)
9. [Lab 9: Kafka Producer/Consumer](02-practice/lab09-kafka.md)
10. [Lab 10: AOP 로깅](02-practice/lab10-aop-logging.md)
11. [Lab 11: 전역 예외 처리](02-practice/lab11-exception-handling.md)
12. [Lab 12: 다국어 처리](02-practice/lab12-i18n.md)
13. [Lab 13: 환경별 설정](02-practice/lab13-profiles.md)
14. [Lab 14: 통합 프로젝트](02-practice/lab14-full-project.md)

### 3. 참고 자료 (03-reference)

- [어노테이션 참조](03-reference/annotations.md)
- [JPA 쿼리 메서드](03-reference/jpa-query-methods.md)
- [MyBatis XML 매퍼](03-reference/mybatis-mapper.md)
- [HTTP 상태 코드](03-reference/http-status-codes.md)
- [자주 묻는 질문](03-reference/faq.md)
- [코딩 컨벤션](03-reference/coding-convention.md)
- [프로젝트 템플릿](03-reference/project-template.md)

## 🏗️ 프로젝트 구조

실습에서 구현할 표준 프로젝트 구조:

```
src/main/java/com/example/demo/
├── config/                      # 설정 클래스
│   ├── WebConfig.java
│   ├── JpaConfig.java
│   ├── KafkaConfig.java
│   └── FeignConfig.java
├── controller/                  # 컨트롤러
│   ├── api/
│   │   └── v1/
│   │       └── UserController.java
│   └── advice/
│       └── GlobalExceptionHandler.java
├── service/                     # 서비스 인터페이스
│   └── UserService.java
├── service/impl/               # 서비스 구현
│   └── UserServiceImpl.java
├── repository/                 # 데이터 접근
│   ├── jpa/
│   │   └── UserRepository.java
│   └── mybatis/
│       └── UserMapper.java
├── domain/                     # 엔티티
│   └── User.java
├── dto/                        # DTO
│   ├── request/
│   │   └── UserCreateRequest.java
│   └── response/
│       └── UserResponse.java
├── mapper/                     # MapStruct 매퍼
│   └── UserMapper.java
├── client/                     # Feign Client
│   └── ExternalApiClient.java
├── kafka/                      # Kafka
│   ├── producer/
│   │   └── UserEventProducer.java
│   └── consumer/
│       └── UserEventConsumer.java
├── interceptor/                # 인터셉터
│   └── LoggingInterceptor.java
├── aop/                        # AOP
│   └── LoggingAspect.java
├── exception/                  # 예외
│   ├── BusinessException.java
│   ├── ErrorCode.java
│   └── GlobalExceptionHandler.java
├── common/                     # 공통
│   ├── response/
│   │   └── ApiResponse.java
│   └── constants/
│       └── Constants.java
└── DemoApplication.java        # 메인 클래스
```

```
src/main/resources/
├── application.yml              # 공통 설정
├── application-local.yml        # 로컬 환경
├── application-dev.yml          # 개발 환경
├── application-prod.yml         # 운영 환경
├── messages.properties          # 기본 메시지
├── messages_ko.properties       # 한국어 메시지
├── messages_en.properties       # 영어 메시지
└── mybatis/
    └── mapper/
        └── UserMapper.xml       # MyBatis 매퍼
```

## 🚀 시작하기

### 사전 요구사항

- **JDK**: 17 이상
- **IDE**: IntelliJ IDEA 또는 VS Code
- **빌드 도구**: Maven 또는 Gradle
- **데이터베이스**: H2 (개발), PostgreSQL/MySQL (운영)
- **Docker**: Kafka 실습용 (선택)

### 빠른 시작

1. Spring Initializr로 프로젝트 생성
2. 기본 의존성 추가
3. 첫 번째 Controller 작성
4. 애플리케이션 실행

## 💡 학습 방법

### 권장 학습 순서

1. **기초 다지기** (이론 1-10장)
   - Spring Boot 기본 개념
   - 계층형 아키텍처 이해

2. **실전 구현** (실습 1-7)
   - 기본 CRUD API 구현
   - JPA와 MyBatis 활용

3. **고급 기능** (이론 11-31장)
   - 마이크로서비스 통신
   - 메시징, 예외 처리

4. **통합 프로젝트** (실습 8-14)
   - 실무 프로젝트 구현
   - 모든 개념 통합

### 학습 팁

- 각 실습은 이전 실습을 기반으로 진행됩니다
- 코드를 직접 입력하며 학습하세요
- 에러를 경험하고 해결하는 과정이 중요합니다
- 공식 문서를 참고하는 습관을 기르세요

## 🔗 주요 기술 스택

| 기술 | 버전 | 용도 |
|------|------|------|
| Spring Boot | 3.2.x | 프레임워크 |
| Spring Data JPA | 3.2.x | ORM |
| MyBatis | 3.0.x | SQL 매퍼 |
| MapStruct | 1.5.x | 객체 변환 |
| SpringDoc OpenAPI | 2.3.x | API 문서화 |
| Feign Client | 4.1.x | HTTP 클라이언트 |
| Kafka | 3.6.x | 메시징 |
| H2 Database | 2.2.x | 개발용 DB |
| Lombok | 1.18.x | 보일러플레이트 제거 |

## 📖 추천 학습 리소스

### 공식 문서
- [Spring Boot Reference](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Spring Data JPA](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [MyBatis Documentation](https://mybatis.org/mybatis-3/)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)

### 관련 강좌
- [Git 튜토리얼](../git/git-tutorial/README.md)
- [VS Code 가이드](../vscode/README.md)

## 🆘 도움말

### 문제 해결
- [자주 묻는 질문](03-reference/faq.md) 확인
- GitHub Issues 검색
- Stack Overflow 활용

### 커뮤니티
- [Spring 공식 커뮤니티](https://spring.io/community)
- [한국 스프링 사용자 모임](https://www.facebook.com/groups/springkorea/)

## 📝 실습 프로젝트

### 구현할 애플리케이션
**사용자 관리 시스템 (User Management System)**

주요 기능:
- 사용자 CRUD
- 권한 관리
- 이벤트 발행/구독 (Kafka)
- 외부 API 연동 (Feign)
- 다국어 지원
- API 문서 자동화

## 🎓 수료 후

이 과정을 완료하면 다음을 할 수 있습니다:

✅ 엔터프라이즈급 Spring Boot 애플리케이션 설계 및 구현  
✅ JPA와 MyBatis를 상황에 맞게 선택하여 사용  
✅ 마이크로서비스 아키텍처에서 서비스 간 통신 구현  
✅ 이벤트 기반 아키텍처 설계  
✅ 확장 가능하고 유지보수가 쉬운 코드 작성  
✅ 프로덕션 레벨의 예외 처리 및 로깅 구현  

---

**준비되셨나요? 시작해봅시다!**

👉 [이론 1장: Spring Boot 소개](01-theory/01-intro.md)

**마지막 업데이트:** 2025년 11월 22일
