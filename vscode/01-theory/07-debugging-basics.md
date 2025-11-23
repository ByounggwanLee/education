# 디버깅 기초

VS Code의 강력한 디버깅 기능을 활용하여 효율적으로 버그를 찾고 수정하는 방법을 알아봅니다.

## 디버깅 기본 개념

### 디버거란?

프로그램 실행을 제어하고 변수 값을 검사하며, 코드 실행 흐름을 추적할 수 있는 도구입니다.

### VS Code 디버깅의 장점

- 통합 환경에서 코드 작성과 디버깅
- 시각적 변수 검사
- 조건부 중단점
- 로그 포인트
- 다중 세션 디버깅

## 디버깅 UI 이해

### Run and Debug 뷰

`Ctrl+Shift+D`로 디버그 뷰를 엽니다.

```
┌─────────────────────────────────┐
│  ▶️ RUN AND DEBUG               │
├─────────────────────────────────┤
│  Variables (변수)               │
│  - Local                        │
│  - Global                       │
│                                 │
│  Watch (감시)                   │
│  - 표현식 추가                  │
│                                 │
│  Call Stack (호출 스택)         │
│  - 현재 실행 위치               │
│                                 │
│  Breakpoints (중단점)           │
│  - 설정된 중단점 목록           │
└─────────────────────────────────┘
```

### 디버그 툴바

프로그램 실행 중 상단에 표시되는 제어 버튼들:

| 아이콘 | 단축키 | 기능 |
|--------|--------|------|
| ▶️ | `F5` | Continue (계속 실행) |
| ⏸️ | `F6` | Pause (일시 정지) |
| ⟳ | `Ctrl+Shift+F5` | Restart (재시작) |
| ⏹️ | `Shift+F5` | Stop (중지) |
| ⤵️ | `F10` | Step Over (한 단계 실행) |
| ⬇️ | `F11` | Step Into (들어가기) |
| ⬆️ | `Shift+F11` | Step Out (나가기) |

## 중단점 (Breakpoints)

### 중단점 설정

**일반 중단점:**
- 줄 번호 왼쪽 여백 클릭
- 빨간 점이 표시됨
- 다시 클릭하면 제거

**단축키:**
- `F9`: 현재 줄에 중단점 토글

### 조건부 중단점

특정 조건에서만 실행을 멈춥니다.

1. 줄 번호 여백 우클릭
2. "Add Conditional Breakpoint" 선택
3. 조건 입력

**예시:**
```javascript
// i가 50일 때만 중단
i === 50

// users 배열 길이가 10 이상일 때 중단
users.length >= 10

// 특정 사용자 ID일 때만 중단
user.id === '12345'
```

### 로그 포인트 (Logpoints)

코드 실행을 멈추지 않고 콘솔에 로그만 출력합니다.

1. 줄 번호 여백 우클릭
2. "Add Logpoint" 선택
3. 로그 메시지 입력

**예시:**
```javascript
// 변수 값 출력
User: {user.name}, Age: {user.age}

// 표현식 평가
Sum: {numbers.reduce((a, b) => a + b, 0)}
```

### Hit Count 중단점

중단점에 도달한 횟수를 기준으로 중단합니다.

**예시:**
```
> 5        // 5번 초과 시
== 10      // 정확히 10번째
% 2 == 0   // 짝수 번째마다
```

## launch.json 설정

디버그 구성 파일입니다.

### 생성 방법

1. Run and Debug 뷰 열기
2. "create a launch.json file" 클릭
3. 환경 선택 (Java, Node.js 등)

`.vscode/launch.json` 파일이 생성됩니다.

### Java (Spring Boot) 디버그 설정

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "java",
      "name": "Debug Spring Boot App",
      "request": "launch",
      "mainClass": "com.example.demo.DemoApplication",
      "projectName": "demo",
      "args": "",
      "vmArgs": "-Dspring.profiles.active=dev"
    },
    {
      "type": "java",
      "name": "Debug Current File",
      "request": "launch",
      "mainClass": "${file}"
    }
  ]
}
```

### Node.js (React) 디버그 설정

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch Chrome",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/src",
      "sourceMapPathOverrides": {
        "webpack:///src/*": "${webRoot}/*"
      }
    },
    {
      "name": "Attach to Chrome",
      "type": "chrome",
      "request": "attach",
      "port": 9222,
      "webRoot": "${workspaceFolder}/src"
    }
  ]
}
```

## Java 애플리케이션 디버깅

### Spring Boot 애플리케이션 디버그

1. **중단점 설정**
   - Controller, Service, Repository 메서드에 설정

2. **디버그 시작**
   - `DemoApplication.java`에서 `F5`
   - 또는 Spring Boot Dashboard에서 Debug 버튼

3. **변수 검사**
   ```java
   @GetMapping("/{id}")
   public User getUserById(@PathVariable Long id) {
       // 여기에 중단점 설정
       User user = userService.findById(id);  // user 변수 검사
       return user;
   }
   ```

### 조건부 중단점 활용

```java
@GetMapping
public List<User> getUsers(@RequestParam(required = false) String name) {
    // name이 null이 아닐 때만 중단
    // 조건: name != null
    List<User> users = userService.findByName(name);
    return users;
}
```

### 표현식 평가

Debug Console에서 실시간으로 표현식 평가:
```java
// 변수 값 확인
user.getName()

// 메서드 호출
userService.count()

// 복잡한 표현식
users.stream().filter(u -> u.getAge() > 30).count()
```

## JavaScript/React 디버깅

### Chrome DevTools 연동

**필요한 확장:**
- Debugger for Chrome (또는 Debugger for Microsoft Edge)

**설정:**
```json
{
  "name": "Launch Chrome for React",
  "type": "chrome",
  "request": "launch",
  "url": "http://localhost:3000",
  "webRoot": "${workspaceFolder}/src"
}
```

### 브라우저에서 디버깅

1. 개발 서버 시작: `npm run dev`
2. VS Code에서 `F5` 눌러 브라우저 실행
3. VS Code에서 설정한 중단점에서 멈춤

### React 컴포넌트 디버깅

```jsx
const UserList = () => {
  const [users, setUsers] = useState([])
  
  useEffect(() => {
    // 여기에 중단점 설정
    fetchUsers()
  }, [])
  
  const fetchUsers = async () => {
    // 여기에 중단점 설정
    const response = await fetch('/api/users')
    const data = await response.json()
    // data 변수 검사
    setUsers(data)
  }
  
  return (
    <div>
      {users.map(user => (
        // 여기에 중단점 설정하여 user 객체 검사
        <li key={user.id}>{user.name}</li>
      ))}
    </div>
  )
}
```

### Console Logging 대신 디버거 사용

❌ **좋지 않은 방법:**
```javascript
console.log('users:', users)
console.log('user.name:', user.name)
```

✅ **좋은 방법:**
- 중단점 설정
- Variables 패널에서 변수 검사
- Watch 표현식으로 관심 있는 값 추적

## 디버그 세션 제어

### Step Over (F10)

현재 줄을 실행하고 다음 줄로 이동 (함수 내부로 들어가지 않음)

```java
public void processUser(User user) {
    validateUser(user);     // F10: 이 함수를 실행하고 다음 줄로
    saveUser(user);         // 여기로 이동
    sendNotification(user); // F10으로 계속 진행
}
```

### Step Into (F11)

함수 내부로 들어가서 디버깅

```java
public void processUser(User user) {
    validateUser(user);  // F11: validateUser() 내부로 들어감
}

private void validateUser(User user) {
    // 이 함수의 첫 줄로 이동
    if (user.getName() == null) {
        throw new IllegalArgumentException();
    }
}
```

### Step Out (Shift+F11)

현재 함수를 끝까지 실행하고 호출한 곳으로 돌아감

```java
private void validateUser(User user) {
    if (user.getName() == null) {
        // Shift+F11: 이 함수를 끝까지 실행
    }
}
// 여기로 돌아옴
```

## Variables 패널 활용

### 변수 값 변경

디버그 중 변수 값을 임시로 변경할 수 있습니다:

1. Variables 패널에서 변수 우클릭
2. "Set Value" 선택
3. 새로운 값 입력

### 변수 복사

- 변수 우클릭 → "Copy Value"
- 변수의 JSON 표현을 클립보드에 복사

## Watch 표현식

관심 있는 표현식을 추적합니다.

### Watch 추가

1. Watch 섹션에서 "+" 버튼 클릭
2. 표현식 입력

**유용한 Watch 표현식:**
```javascript
// JavaScript
users.length
users.filter(u => u.active).length
Object.keys(state)

// Java
users.size()
users.stream().filter(u -> u.isActive()).count()
```

## Call Stack

함수 호출 순서를 보여줍니다.

```
Call Stack:
  processUser (line 45)
  createUser (line 28)
  handleSubmit (line 15)
  main (line 10)
```

스택의 각 프레임을 클릭하면 해당 시점의 변수를 볼 수 있습니다.

## 디버그 콘솔

### 표현식 평가

Debug Console에서 코드를 실행할 수 있습니다:

```javascript
// 변수 확인
> user
{ id: 1, name: "홍길동", age: 30 }

// 메서드 호출
> user.getName()
"홍길동"

// 새로운 변수 생성 및 테스트
> const total = users.reduce((sum, u) => sum + u.age, 0)
```

### REPL 모드

디버그 콘솔은 Read-Eval-Print Loop로 작동합니다:
- 표현식 입력
- 즉시 평가
- 결과 출력

## 예외 처리 디버깅

### 예외 발생 시 중단

```json
{
  "configurations": [
    {
      "type": "java",
      "name": "Debug",
      "request": "launch",
      "mainClass": "...",
      "stopOnEntry": false,
      "exceptionBreakpoints": {
        "uncaught": true,
        "caught": false
      }
    }
  ]
}
```

### 예외 중단점 설정

1. Breakpoints 패널에서 "+" 버튼
2. "Exception Breakpoint" 선택
3. 예외 타입 선택

## 다중 세션 디버깅

동시에 여러 애플리케이션을 디버그할 수 있습니다.

### Compound 설정

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Backend",
      "type": "java",
      "request": "launch",
      "mainClass": "com.example.demo.DemoApplication"
    },
    {
      "name": "Debug Frontend",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000"
    }
  ],
  "compounds": [
    {
      "name": "Full Stack Debug",
      "configurations": ["Debug Backend", "Debug Frontend"]
    }
  ]
}
```

Run and Debug 뷰에서 "Full Stack Debug" 선택하면 백엔드와 프론트엔드를 동시에 디버그할 수 있습니다.

## 디버깅 팁

### 1. 로그 포인트 활용

코드를 멈추지 않고 로그만 출력하여 성능 영향 최소화

### 2. 조건부 중단점으로 특정 케이스만 디버그

루프에서 특정 값만 검사

### 3. Watch 표현식으로 복잡한 상태 추적

계산된 값이나 집계 결과를 실시간 모니터링

### 4. Call Stack으로 호출 경로 파악

버그가 어디서 시작되었는지 추적

### 5. Debug Console에서 빠른 테스트

코드를 수정하지 않고 다양한 시나리오 테스트

## 성능 고려사항

### 중단점이 많을 때

- 사용하지 않는 중단점 비활성화
- Breakpoints 패널에서 체크박스 해제

### 조건부 중단점 비용

- 복잡한 조건은 성능에 영향
- 필요한 경우에만 사용

## 다음 단계

기본 디버깅을 마스터했다면, 이제 원격 디버깅을 알아봅시다.

👉 [다음: 원격 디버깅](08-remote-debugging.md)

## 참고 자료

- [VS Code 디버깅 가이드](https://code.visualstudio.com/docs/editor/debugging)
- [Java 디버깅](https://code.visualstudio.com/docs/java/java-debugging)
- [Node.js 디버깅](https://code.visualstudio.com/docs/nodejs/nodejs-debugging)
