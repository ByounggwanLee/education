# 원격 디버깅

원격 서버나 컨테이너에서 실행 중인 애플리케이션을 VS Code에서 디버깅하는 방법을 알아봅니다.

## 원격 디버깅이란?

로컬이 아닌 다른 환경(원격 서버, Docker 컨테이너, 클라우드 등)에서 실행되는 애플리케이션을 디버깅하는 기술입니다.

### 사용 사례

- 로컬과 다른 운영 환경에서 발생하는 버그 디버깅
- Docker 컨테이너 내 애플리케이션 디버깅
- 개발 서버에서 실행 중인 애플리케이션 디버깅
- 클라우드 환경 디버깅

## Java 원격 디버깅

### JDWP (Java Debug Wire Protocol)

Java 애플리케이션 원격 디버깅을 위한 표준 프로토콜입니다.

### Spring Boot 원격 디버그 설정

#### 1. 원격 서버 설정

**애플리케이션 실행 시 디버그 옵션 추가:**

```bash
# Maven
./mvnw spring-boot:run -Dspring-boot.run.jvmArguments="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"

# Gradle
./gradlew bootRun --debug-jvm

# JAR 직접 실행
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005 \
     -jar target/demo-0.0.1-SNAPSHOT.jar
```

**JVM 옵션 설명:**
- `transport=dt_socket`: 소켓 통신 사용
- `server=y`: 디버거 연결 대기
- `suspend=n`: 디버거 연결 전에도 실행 (y로 설정하면 연결 대기)
- `address=*:5005`: 모든 인터페이스에서 5005 포트로 대기

#### 2. VS Code 설정

`.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "java",
      "name": "Remote Debug (Attach)",
      "request": "attach",
      "hostName": "localhost",
      "port": 5005
    },
    {
      "type": "java",
      "name": "Remote Debug (Server)",
      "request": "attach",
      "hostName": "192.168.1.100",
      "port": 5005
    }
  ]
}
```

#### 3. 디버깅 시작

1. 원격 서버에서 애플리케이션 실행 (디버그 모드)
2. VS Code에서 `F5` 눌러 디버거 연결
3. 로컬 코드에 중단점 설정
4. 원격 애플리케이션이 중단점에 도달하면 디버깅 가능

### application.properties 설정

**개발 환경 전용 프로파일:**

`application-dev.properties`:
```properties
# 원격 디버그 포트
debug.port=5005

# 로깅 레벨 상세화
logging.level.com.example.demo=DEBUG
logging.level.org.springframework.web=DEBUG
```

### Docker 컨테이너 내 Spring Boot 디버깅

#### Dockerfile

```dockerfile
FROM openjdk:17-jdk-slim

# 디버그 포트 노출
EXPOSE 8080 5005

COPY target/demo-0.0.1-SNAPSHOT.jar app.jar

# 디버그 옵션 포함하여 실행
ENTRYPOINT ["java", \
            "-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005", \
            "-jar", "/app.jar"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8080:8080"
      - "5005:5005"  # 디버그 포트
    environment:
      - SPRING_PROFILES_ACTIVE=dev
    volumes:
      - ./target:/app/target
```

#### VS Code 설정

```json
{
  "type": "java",
  "name": "Attach to Docker",
  "request": "attach",
  "hostName": "localhost",
  "port": 5005,
  "projectName": "demo"
}
```

## Node.js / React 원격 디버깅

### Node.js 원격 디버그 설정

#### 1. 원격 서버에서 Node.js 실행

```bash
# 디버그 모드로 실행
node --inspect=0.0.0.0:9229 server.js

# 또는 특정 호스트에서만
node --inspect=127.0.0.1:9229 server.js

# nodemon과 함께
nodemon --inspect=0.0.0.0:9229 server.js
```

#### 2. VS Code 설정

`.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to Remote Node",
      "address": "192.168.1.100",
      "port": 9229,
      "localRoot": "${workspaceFolder}",
      "remoteRoot": "/app",
      "sourceMaps": true
    }
  ]
}
```

### React 앱 원격 디버깅

#### Chrome 원격 디버깅

**Chrome을 디버그 포트로 실행:**

Windows:
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

macOS:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

#### VS Code 설정

```json
{
  "type": "chrome",
  "request": "attach",
  "name": "Attach to Chrome",
  "port": 9222,
  "urlFilter": "http://localhost:3000/*",
  "webRoot": "${workspaceFolder}/src"
}
```

## SSH를 통한 원격 개발

### Remote - SSH 확장 사용

VS Code의 Remote - SSH 확장을 사용하면 원격 서버에서 직접 개발할 수 있습니다.

#### 1. 확장 설치

- Extension ID: `ms-vscode-remote.remote-ssh`

#### 2. SSH 설정

**SSH 구성 파일 생성/편집:**

`~/.ssh/config` (Windows: `C:\Users\[사용자]\.ssh\config`):
```
Host dev-server
    HostName 192.168.1.100
    User developer
    Port 22
    IdentityFile ~/.ssh/id_rsa
```

#### 3. 원격 서버 연결

1. `Ctrl+Shift+P` → "Remote-SSH: Connect to Host"
2. 구성한 호스트 선택 또는 직접 입력
3. 새 VS Code 창이 원격 서버에 연결됨

#### 4. 원격 서버에서 디버깅

연결 후에는 로컬과 동일하게 디버깅:
- 확장 프로그램 설치
- 프로젝트 열기
- launch.json 설정
- 디버깅 시작

### 장점

- 원격 서버의 파일 시스템에 직접 접근
- 원격 터미널 사용
- 원격 확장 프로그램 실행
- 네트워크 지연 없는 빠른 개발

## Docker 컨테이너에서 개발

### Remote - Containers 확장

- Extension ID: `ms-vscode-remote.remote-containers`

#### devcontainer.json 설정

`.devcontainer/devcontainer.json`:
```json
{
  "name": "Spring Boot Development",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
  
  // 포트 포워딩
  "forwardPorts": [8080, 5005],
  
  // VS Code 설정
  "settings": {
    "java.home": "/usr/lib/jvm/java-17-openjdk",
    "terminal.integrated.shell.linux": "/bin/bash"
  },
  
  // 확장 프로그램
  "extensions": [
    "vscjava.vscode-java-pack",
    "vmware.vscode-spring-boot"
  ],
  
  // 컨테이너 생성 후 실행할 명령
  "postCreateCommand": "./mvnw clean install",
  
  // 사용자 설정
  "remoteUser": "developer"
}
```

#### 컨테이너에서 열기

1. `Ctrl+Shift+P` → "Remote-Containers: Open Folder in Container"
2. 프로젝트 폴더 선택
3. 컨테이너 빌드 및 연결
4. 컨테이너 내에서 개발 및 디버깅

## 포트 포워딩

### SSH 터널링

로컬에서 원격 서버의 포트에 접근:

```bash
# 로컬 5005 포트를 원격 서버 5005 포트로 포워딩
ssh -L 5005:localhost:5005 user@remote-server

# 백그라운드 실행
ssh -fN -L 5005:localhost:5005 user@remote-server
```

이후 `localhost:5005`로 디버거 연결

### VS Code 자동 포트 포워딩

Remote - SSH 연결 시 자동으로 포트 포워딩:

```json
{
  "remote.SSH.defaultForwardedPorts": [
    {
      "localPort": 8080,
      "remotePort": 8080,
      "name": "Application"
    },
    {
      "localPort": 5005,
      "remotePort": 5005,
      "name": "Debug"
    }
  ]
}
```

## 소스 맵 설정

원격 코드와 로컬 코드의 경로 매핑

### Java

```json
{
  "type": "java",
  "request": "attach",
  "hostName": "localhost",
  "port": 5005,
  "sourceRoots": [
    "${workspaceFolder}/src/main/java"
  ]
}
```

### Node.js

```json
{
  "type": "node",
  "request": "attach",
  "port": 9229,
  "localRoot": "${workspaceFolder}",
  "remoteRoot": "/app",
  "sourceMaps": true,
  "outFiles": [
    "${workspaceFolder}/dist/**/*.js"
  ]
}
```

## 보안 고려사항

### 1. 디버그 포트 노출 주의

- 운영 환경에서는 디버그 모드 비활성화
- 방화벽 규칙으로 디버그 포트 제한
- VPN이나 SSH 터널을 통해서만 접근

### 2. 인증 설정

일부 디버거는 인증 토큰 지원:

```bash
# Node.js
node --inspect=0.0.0.0:9229 --inspect-brk server.js
```

### 3. 네트워크 세그먼트 분리

- 개발 서버와 운영 서버 분리
- 디버그 포트는 내부 네트워크에만 노출

## 문제 해결

### 연결 실패

**원인:**
- 방화벽 차단
- 잘못된 포트 번호
- 원격 애플리케이션이 실행 중이 아님

**해결:**
```bash
# 포트 열려있는지 확인
netstat -an | grep 5005

# 원격 서버에서 포트 테스트
telnet remote-server 5005
```

### 중단점이 작동하지 않음

**원인:**
- 소스 코드 버전 불일치
- 소스 맵 경로 오류
- 컴파일된 코드가 최신이 아님

**해결:**
- 원격 서버의 코드를 최신으로 업데이트
- 로컬 코드와 원격 코드 동기화
- 소스 맵 경로 확인

### 성능 저하

**원인:**
- 네트워크 지연
- 과도한 중단점

**해결:**
- 조건부 중단점 사용
- 로그 포인트로 대체
- SSH 압축 활성화: `ssh -C`

## 실전 팁

### 1. 개발 환경별 launch 구성 분리

```json
{
  "configurations": [
    {
      "name": "Local Debug",
      "type": "java",
      "request": "launch",
      "mainClass": "..."
    },
    {
      "name": "Dev Server Debug",
      "type": "java",
      "request": "attach",
      "hostName": "dev.example.com",
      "port": 5005
    },
    {
      "name": "Docker Debug",
      "type": "java",
      "request": "attach",
      "hostName": "localhost",
      "port": 5005
    }
  ]
}
```

### 2. 자동 재연결 스크립트

```bash
#!/bin/bash
# reconnect-debug.sh

while true; do
  ssh -fN -L 5005:localhost:5005 dev-server
  sleep 5
done
```

### 3. 디버그 전용 프로파일 사용

`application-remote-debug.properties`:
```properties
# 더 상세한 로깅
logging.level.root=DEBUG

# 디버그 정보 포함
server.error.include-stacktrace=always
server.error.include-message=always
```

## 다음 단계

원격 디버깅을 마스터했다면, 이제 Git 통합 기능을 알아봅시다.

👉 [다음: Git 통합](09-git-integration.md)

## 참고 자료

- [Remote Development with VS Code](https://code.visualstudio.com/docs/remote/remote-overview)
- [Java Debugging](https://code.visualstudio.com/docs/java/java-debugging)
- [Node.js Debugging](https://code.visualstudio.com/docs/nodejs/nodejs-debugging)
- [Docker in VS Code](https://code.visualstudio.com/docs/containers/overview)
