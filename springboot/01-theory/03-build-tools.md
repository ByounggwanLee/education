# Maven vs Gradle

Spring Boot 프로젝트에서 사용할 수 있는 두 가지 주요 빌드 도구를 비교하고, 각각의 장단점을 알아봅니다.

## 빌드 도구란?

빌드 도구는 다음 작업을 자동화합니다:

- **의존성 관리**: 라이브러리 다운로드 및 버전 관리
- **컴파일**: 소스 코드를 바이트코드로 변환
- **테스트**: 자동화된 테스트 실행
- **패키징**: JAR/WAR 파일 생성
- **배포**: 애플리케이션 배포

## Maven

### 개요

- **출시**: 2004년
- **개발**: Apache Software Foundation
- **설정 파일**: `pom.xml` (Project Object Model)
- **언어**: XML
- **철학**: Convention over Configuration

### pom.xml 구조

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <!-- 1. 프로젝트 정보 -->
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
        <relativePath/>
    </parent>
    
    <groupId>com.example</groupId>
    <artifactId>demo</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>demo</name>
    <description>Demo project for Spring Boot</description>
    
    <!-- 2. 속성 정의 -->
    <properties>
        <java.version>17</java.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
    
    <!-- 3. 의존성 -->
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>
        
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
    
    <!-- 4. 빌드 설정 -->
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

### Maven 라이프사이클

```bash
# 클린 (이전 빌드 삭제)
mvn clean

# 컴파일
mvn compile

# 테스트
mvn test

# 패키징 (JAR/WAR 생성)
mvn package

# 로컬 저장소에 설치
mvn install

# 원격 저장소에 배포
mvn deploy

# 전체 빌드 (클린 + 패키지)
mvn clean package

# Spring Boot 실행
mvn spring-boot:run

# 테스트 스킵하고 패키징
mvn package -DskipTests
```

### Maven 디렉토리 구조

```
demo/
├── src/
│   ├── main/
│   │   ├── java/           # 소스 코드
│   │   └── resources/      # 리소스 파일
│   └── test/
│       ├── java/           # 테스트 코드
│       └── resources/      # 테스트 리소스
├── target/                  # 빌드 결과물
├── pom.xml                  # Maven 설정
└── .mvn/                    # Maven Wrapper
```

### Maven 장점

✅ **안정성**
- 오랜 역사와 검증된 도구
- 대부분의 IDE에서 완벽 지원

✅ **명확한 구조**
- 표준화된 디렉토리 구조
- 일관된 빌드 프로세스

✅ **방대한 생태계**
- 수많은 플러그인
- 풍부한 문서와 예제

✅ **엔터프라이즈 친화적**
- 대기업에서 널리 사용
- 안정적인 버전 관리

### Maven 단점

❌ **장황한 XML**
- 설정 파일이 길어질 수 있음
- 가독성 저하

❌ **유연성 부족**
- 커스텀 빌드 로직 작성 어려움
- 정해진 라이프사이클을 벗어나기 어려움

❌ **빌드 속도**
- Gradle보다 느린 빌드
- 증분 빌드 미지원

## Gradle

### 개요

- **출시**: 2012년
- **개발**: Gradle Inc.
- **설정 파일**: `build.gradle` (Groovy) 또는 `build.gradle.kts` (Kotlin)
- **언어**: Groovy DSL 또는 Kotlin DSL
- **철학**: 유연성과 성능

### build.gradle 구조 (Groovy)

```groovy
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.2.0'
    id 'io.spring.dependency-management' version '1.1.4'
}

group = 'com.example'
version = '0.0.1-SNAPSHOT'

java {
    sourceCompatibility = '17'
}

configurations {
    compileOnly {
        extendsFrom annotationProcessor
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    
    runtimeOnly 'com.h2database:h2'
    
    compileOnly 'org.projectlombok:lombok'
    annotationProcessor 'org.projectlombok:lombok'
    
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}

tasks.named('test') {
    useJUnitPlatform()
}
```

### build.gradle.kts 구조 (Kotlin)

```kotlin
plugins {
    java
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
}

group = "com.example"
version = "0.0.1-SNAPSHOT"

java {
    sourceCompatibility = JavaVersion.VERSION_17
}

configurations {
    compileOnly {
        extendsFrom(configurations.annotationProcessor.get())
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    
    runtimeOnly("com.h2database:h2")
    
    compileOnly("org.projectlombok:lombok")
    annotationProcessor("org.projectlombok:lombok")
    
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.withType<Test> {
    useJUnitPlatform()
}
```

### Gradle 태스크

```bash
# 클린
./gradlew clean

# 컴파일
./gradlew compileJava

# 테스트
./gradlew test

# 빌드 (컴파일 + 테스트 + 패키징)
./gradlew build

# Spring Boot 실행
./gradlew bootRun

# 테스트 스킵하고 빌드
./gradlew build -x test

# 의존성 트리 확인
./gradlew dependencies

# 태스크 목록 확인
./gradlew tasks
```

### Gradle 디렉토리 구조

```
demo/
├── src/
│   ├── main/
│   │   ├── java/
│   │   └── resources/
│   └── test/
│       ├── java/
│       └── resources/
├── build/                   # 빌드 결과물
├── gradle/                  # Gradle Wrapper
│   └── wrapper/
├── build.gradle            # Gradle 설정 (Groovy)
├── settings.gradle         # 프로젝트 설정
└── gradlew                 # Gradle Wrapper 스크립트
```

### Gradle 장점

✅ **빠른 빌드 속도**
- 증분 빌드 지원
- 병렬 실행
- 빌드 캐시

✅ **유연한 설정**
- 프로그래밍 방식의 설정
- 복잡한 빌드 로직 구현 가능

✅ **간결한 문법**
- Groovy/Kotlin DSL
- Maven보다 짧은 설정

✅ **멀티 프로젝트 지원**
- 마이크로서비스에 적합
- 모듈 간 의존성 관리 용이

### Gradle 단점

❌ **학습 곡선**
- Maven보다 복잡
- Groovy/Kotlin 학습 필요

❌ **IDE 지원**
- Maven보다 IDE 통합이 느릴 수 있음
- 초기 임포트 시간 길 수 있음

❌ **디버깅 어려움**
- 빌드 스크립트 오류 추적 어려움

## Maven vs Gradle 비교

### 기능 비교

| 항목 | Maven | Gradle |
|------|-------|--------|
| **설정 파일** | XML (pom.xml) | Groovy/Kotlin DSL |
| **빌드 속도** | 느림 | 빠름 (2-10배) |
| **증분 빌드** | ❌ | ✅ |
| **병렬 실행** | 제한적 | 완벽 지원 |
| **학습 곡선** | 완만 | 가파름 |
| **IDE 지원** | 완벽 | 좋음 |
| **커스터마이징** | 어려움 | 쉬움 |
| **멀티 프로젝트** | 가능 | 우수 |

### 성능 비교

**빌드 시간 (중간 규모 프로젝트 기준):**

```
첫 빌드:
Maven:  45초
Gradle: 40초

증분 빌드:
Maven:  45초 (항상 전체 빌드)
Gradle: 5초  (변경된 부분만)

클린 빌드:
Maven:  50초
Gradle: 35초
```

### 의존성 표기 비교

**Maven:**
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <version>3.2.0</version>
    <scope>compile</scope>
</dependency>
```

**Gradle (Groovy):**
```groovy
implementation 'org.springframework.boot:spring-boot-starter-web:3.2.0'
```

**Gradle (Kotlin):**
```kotlin
implementation("org.springframework.boot:spring-boot-starter-web:3.2.0")
```

## 실전 사용 시나리오

### Maven을 선택해야 하는 경우

✅ **엔터프라이즈 환경**
- 회사 표준이 Maven
- 레거시 프로젝트 통합

✅ **단순한 프로젝트**
- 표준 Spring Boot 애플리케이션
- 커스텀 빌드 로직 불필요

✅ **팀 역량**
- XML에 익숙한 팀
- 안정성 우선

### Gradle을 선택해야 하는 경우

✅ **성능이 중요한 프로젝트**
- 대규모 코드베이스
- 빈번한 빌드

✅ **마이크로서비스**
- 멀티 모듈 프로젝트
- 복잡한 의존성 관리

✅ **신규 프로젝트**
- 최신 기술 스택
- 유연한 빌드 프로세스

## 변환하기

### Maven에서 Gradle로

Gradle은 자동 변환 도구를 제공합니다:

```bash
# 프로젝트 루트에서
gradle init

# 또는 Maven 프로젝트를 직접 변환
gradle init --type pom
```

### 수동 변환 가이드

**Maven pom.xml:**
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
```

**Gradle build.gradle:**
```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
}
```

## Wrapper 사용

### Maven Wrapper

```bash
# Windows
mvnw.cmd clean package

# Unix/Mac
./mvnw clean package
```

프로젝트에 Maven 설치 불필요, `.mvn/` 폴더에 포함된 버전 사용

### Gradle Wrapper

```bash
# Windows
gradlew.bat build

# Unix/Mac
./gradlew build
```

프로젝트에 Gradle 설치 불필요, `gradle/wrapper/` 폴더에 포함된 버전 사용

**장점:**
- 팀원 모두 동일한 빌드 도구 버전 사용
- CI/CD 환경에서 별도 설치 불필요
- 버전 관리에 포함

## 프로젝트별 추천

### 소규모 프로젝트 (< 10 모듈)
**Maven 추천**
- 간단한 설정
- 빠른 시작

### 중규모 프로젝트 (10-50 모듈)
**Gradle 추천**
- 빌드 속도 이점
- 유연한 구성

### 대규모 프로젝트 (50+ 모듈)
**Gradle 강력 추천**
- 증분 빌드로 시간 절약
- 멀티 프로젝트 최적화

## 다음 단계

빌드 도구를 선택했다면, 이제 의존성 관리에 대해 알아봅시다.

👉 [다음: 의존성 관리](04-dependencies.md)

## 참고 자료

- [Maven 공식 문서](https://maven.apache.org/)
- [Gradle 공식 문서](https://docs.gradle.org/)
- [Gradle vs Maven 성능 비교](https://gradle.org/maven-vs-gradle/)
- [Spring Boot with Gradle](https://docs.spring.io/spring-boot/docs/current/gradle-plugin/reference/html/)
- [Spring Boot with Maven](https://docs.spring.io/spring-boot/docs/current/maven-plugin/reference/html/)
