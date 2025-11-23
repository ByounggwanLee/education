# Spring Boot 개발 환경

VS Code에서 Spring Boot 프로젝트를 효율적으로 개발하기 위한 환경 설정과 사용법을 알아봅니다.

## 사전 준비

### 필수 설치 항목

1. **JDK 17 이상**
   ```bash
   java -version
   # openjdk version "17.0.x" 이상 확인
   ```

2. **Maven 또는 Gradle**
   ```bash
   mvn -version
   # 또는
   gradle -version
   ```

3. **필수 VS Code 확장**
   - Extension Pack for Java
   - Spring Boot Extension Pack
   - Gradle for Java (Gradle 사용 시)

## Java 개발 환경 설정

### Java Runtime 설정

`.vscode/settings.json`:
```json
{
  "java.configuration.runtimes": [
    {
      "name": "JavaSE-17",
      "path": "C:\\Program Files\\Java\\jdk-17",
      "default": true
    },
    {
      "name": "JavaSE-21",
      "path": "C:\\Program Files\\Java\\jdk-21"
    }
  ],
  "java.home": "C:\\Program Files\\Java\\jdk-17"
}
```

### Java 포맷팅 설정

```json
{
  "java.format.settings.url": "${workspaceFolder}/.vscode/java-formatter.xml",
  "java.format.settings.profile": "GoogleStyle",
  "editor.formatOnSave": true,
  "[java]": {
    "editor.defaultFormatter": "redhat.java"
  }
}
```

### Import 자동 정리

```json
{
  "java.saveActions.organizeImports": true,
  "java.completion.importOrder": [
    "java",
    "javax",
    "org",
    "com"
  ]
}
```

## Spring Boot 프로젝트 생성

### 방법 1: Spring Initializr (VS Code 내장)

1. `Ctrl+Shift+P` → "Spring Initializr: Create a Maven Project" 또는 "Create a Gradle Project"
2. 프로젝트 설정:
   - Spring Boot 버전 선택 (3.x 권장)
   - 언어: Java
   - Group Id: `com.example`
   - Artifact Id: `demo`
   - Packaging: Jar
   - Java 버전: 17

3. 의존성 선택:
   - Spring Web
   - Spring Boot DevTools
   - Lombok
   - Spring Data JPA (필요시)
   - H2 Database (개발용)

4. 프로젝트 생성 위치 선택

### 방법 2: Spring Initializr 웹사이트

1. [https://start.spring.io/](https://start.spring.io/) 접속
2. 프로젝트 설정 후 다운로드
3. VS Code에서 폴더 열기

## 프로젝트 구조 이해

### Maven 프로젝트 구조

```
demo/
├── .mvn/                    # Maven Wrapper
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/demo/
│   │   │       ├── DemoApplication.java
│   │   │       ├── controller/
│   │   │       ├── service/
│   │   │       ├── repository/
│   │   │       └── model/
│   │   └── resources/
│   │       ├── application.properties
│   │       ├── static/
│   │       └── templates/
│   └── test/
│       └── java/
│           └── com/example/demo/
├── target/                  # 빌드 출력
├── pom.xml                  # Maven 설정
└── mvnw, mvnw.cmd          # Maven Wrapper 스크립트
```

### Gradle 프로젝트 구조

```
demo/
├── gradle/                  # Gradle Wrapper
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/demo/
│   │   └── resources/
│   └── test/
│       └── java/
├── build/                   # 빌드 출력
├── build.gradle            # Gradle 빌드 스크립트
├── settings.gradle         # Gradle 설정
└── gradlew, gradlew.bat    # Gradle Wrapper 스크립트
```

## Spring Boot Dashboard

Spring Boot Extension Pack을 설치하면 Spring Boot Dashboard가 활성화됩니다.

### Dashboard 사용법

1. **Activity Bar**에서 Spring Boot 아이콘 클릭
2. 프로젝트 앱 목록 확인
3. 앱 우클릭으로 작업 실행:
   - ▶️ Start
   - ⏹️ Stop
   - 🔄 Restart
   - 🐛 Debug

### Dashboard 설정

```json
{
  "spring-boot.ls.java.home": "C:\\Program Files\\Java\\jdk-17",
  "spring-boot.ls.problem.application-properties.PROP_UNKNOWN_PROPERTY": "WARNING"
}
```

## 애플리케이션 실행

### 방법 1: Spring Boot Dashboard 사용

1. Spring Boot Dashboard 열기
2. 애플리케이션 우클릭 → "Run"

### 방법 2: Run 버튼 사용

1. `DemoApplication.java` 파일 열기
2. main 메서드 위의 "Run" 또는 "Debug" 링크 클릭

### 방법 3: 터미널 사용

**Maven:**
```bash
./mvnw spring-boot:run
```

**Gradle:**
```bash
./gradlew bootRun
```

### 방법 4: Tasks.json 설정

`.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Spring Boot App",
      "type": "shell",
      "command": "./mvnw",
      "args": ["spring-boot:run"],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "problemMatcher": [],
      "isBackground": true
    }
  ]
}
```

## 빌드 및 패키징

### Maven 빌드

```bash
# 컴파일 및 테스트
./mvnw clean package

# 테스트 건너뛰기
./mvnw clean package -DskipTests

# JAR 파일 생성 위치
# target/demo-0.0.1-SNAPSHOT.jar
```

### Gradle 빌드

```bash
# 컴파일 및 테스트
./gradlew clean build

# 테스트 건너뛰기
./gradlew clean build -x test

# JAR 파일 생성 위치
# build/libs/demo-0.0.1-SNAPSHOT.jar
```

## 설정 파일 관리

### application.properties

`src/main/resources/application.properties`:
```properties
# 서버 설정
server.port=8080
server.servlet.context-path=/api

# 데이터베이스 설정 (H2)
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=

# JPA 설정
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true

# 로깅 설정
logging.level.root=INFO
logging.level.com.example.demo=DEBUG
```

### application.yml (YAML 형식)

```yaml
server:
  port: 8080
  servlet:
    context-path: /api

spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password: 
  
  jpa:
    database-platform: org.hibernate.dialect.H2Dialect
    hibernate:
      ddl-auto: update
    show-sql: true

logging:
  level:
    root: INFO
    com.example.demo: DEBUG
```

### 프로파일별 설정

```
resources/
├── application.properties          # 공통 설정
├── application-dev.properties      # 개발 환경
├── application-prod.properties     # 운영 환경
└── application-test.properties     # 테스트 환경
```

활성 프로파일 설정:
```properties
spring.profiles.active=dev
```

## 코드 작성

### Controller 예시

```java
package com.example.demo.controller;

import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController {
    
    private final UserService userService;
    
    public UserController(UserService userService) {
        this.userService = userService;
    }
    
    @GetMapping
    public List<User> getAllUsers() {
        return userService.findAll();
    }
    
    @GetMapping("/{id}")
    public User getUserById(@PathVariable Long id) {
        return userService.findById(id);
    }
    
    @PostMapping
    public User createUser(@RequestBody User user) {
        return userService.save(user);
    }
    
    @PutMapping("/{id}")
    public User updateUser(@PathVariable Long id, @RequestBody User user) {
        return userService.update(id, user);
    }
    
    @DeleteMapping("/{id}")
    public void deleteUser(@PathVariable Long id) {
        userService.deleteById(id);
    }
}
```

### IntelliSense 활용

- **자동 완성**: `Ctrl+Space`
- **Import 자동 추가**: 클래스 이름 입력 후 `Ctrl+Space`
- **빠른 수정**: `Ctrl+.` (전구 아이콘)
- **메서드 생성**: Lombok 어노테이션 활용

### 코드 스니펫

VS Code는 Java 코드 스니펫을 제공합니다:
- `main` → main 메서드
- `sysout` → System.out.println()
- `for` → for 루프
- `foreach` → 향상된 for 루프

## 테스트 작성 및 실행

### JUnit 테스트

```java
package com.example.demo.controller;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class UserControllerTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Test
    void shouldReturnAllUsers() {
        String response = restTemplate.getForObject("/api/users", String.class);
        assertThat(response).isNotNull();
    }
}
```

### 테스트 실행

1. **Test Explorer**: Activity Bar의 플라스크 아이콘
2. 테스트 메서드 옆의 ▶️ 버튼 클릭
3. 또는 터미널에서:
   ```bash
   ./mvnw test
   # 또는
   ./gradlew test
   ```

## Hot Reload (DevTools)

Spring Boot DevTools를 사용하면 코드 변경 시 자동으로 재시작됩니다.

### DevTools 설정

`pom.xml` (Maven):
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-devtools</artifactId>
    <scope>runtime</scope>
    <optional>true</optional>
</dependency>
```

`build.gradle` (Gradle):
```gradle
dependencies {
    developmentOnly 'org.springframework.boot:spring-boot-devtools'
}
```

### 자동 빌드 활성화

```json
{
  "java.autobuild.enabled": true
}
```

코드를 저장하면 자동으로 앱이 재시작됩니다.

## 디버깅

다음 챕터에서 자세히 다룹니다.

간단한 디버깅:
1. 중단점 설정: 줄 번호 왼쪽 클릭
2. `F5` 또는 Debug 링크 클릭
3. 변수 값 확인 및 단계별 실행

## Maven/Gradle 작업

### Maven 작업 실행

1. Explorer에서 `pom.xml` 우클릭
2. "Maven" 메뉴에서 원하는 작업 선택

또는 명령 팔레트:
- `Ctrl+Shift+P` → "Maven: Execute Commands"

### Gradle 작업 실행

1. **Gradle Tasks** 뷰 열기
2. 작업 트리에서 원하는 작업 선택
3. ▶️ 버튼 클릭

## 문제 해결

### Java Language Server 오류

1. `Ctrl+Shift+P` → "Java: Clean Java Language Server Workspace"
2. VS Code 재시작

### 의존성 다운로드 실패

**Maven:**
```bash
./mvnw dependency:purge-local-repository
./mvnw clean install
```

**Gradle:**
```bash
./gradlew clean build --refresh-dependencies
```

### 포트 충돌

`application.properties`:
```properties
server.port=8081
```

## 유용한 단축키

| 단축키 | 기능 |
|--------|------|
| `Ctrl+Shift+O` | Import 구성 |
| `Alt+Shift+O` | 사용하지 않는 Import 제거 |
| `Ctrl+.` | 빠른 수정 |
| `F2` | 이름 변경 (리팩토링) |
| `Ctrl+Shift+F` | 코드 포맷팅 |
| `Alt+Shift+F` | 파일 포맷팅 |

## 다음 단계

Spring Boot 개발 환경을 설정했으니, 이제 React 개발 환경을 알아봅시다.

👉 [다음: React 개발 환경](06-react-environment.md)

## 참고 자료

- [Spring Boot in VS Code](https://code.visualstudio.com/docs/java/java-spring-boot)
- [Java in VS Code](https://code.visualstudio.com/docs/languages/java)
- [Spring Boot 공식 문서](https://spring.io/projects/spring-boot)
