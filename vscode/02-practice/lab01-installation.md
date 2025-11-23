# Lab 1: VS Code 설치 및 설정

VS Code를 설치하고 프로젝트 개발을 위한 기본 환경을 설정합니다.

**소요 시간**: 30-40분  
**난이도**: ⭐ 초급

## 학습 목표

- [ ] VS Code 설치
- [ ] 한글 언어 팩 설치
- [ ] 기본 설정 구성
- [ ] 필수 확장 프로그램 설치
- [ ] JDK 및 Node.js 설정 확인

## 사전 준비

- 인터넷 연결
- 관리자 권한 (설치용)

## 실습 1: VS Code 설치

### Windows

1. **다운로드**
   - [VS Code 공식 사이트](https://code.visualstudio.com/) 접속
   - "Download for Windows" 클릭
   - `VSCodeUserSetup-x64-{version}.exe` 다운로드

2. **설치**
   - 다운로드한 파일 실행
   - 라이선스 동의
   - 설치 옵션 선택:
     ```
     ✅ Add "Open with Code" action to Windows Explorer file context menu
     ✅ Add "Open with Code" action to Windows Explorer directory context menu
     ✅ Register Code as an editor for supported file types
     ✅ Add to PATH
     ```
   - "Install" 클릭

3. **설치 확인**
   - VS Code 실행
   - `Ctrl+Shift+P` → "About" 입력 → 버전 확인

### 터미널에서 VS Code 확인

```bash
# 버전 확인
code --version

# 현재 디렉토리를 VS Code로 열기
code .
```

✅ **체크포인트**: VS Code가 정상적으로 실행되고 버전 정보가 표시됨

## 실습 2: 한글 언어 팩 설치

1. **Extensions 뷰 열기**
   - `Ctrl+Shift+X` 누르기

2. **Korean Language Pack 검색**
   - 검색창에 "Korean Language Pack" 입력
   - "Korean Language Pack for Visual Studio Code" 선택

3. **설치**
   - "Install" 버튼 클릭
   - VS Code 재시작 메시지 확인 시 "Restart" 클릭

4. **언어 변경 확인**
   - VS Code 재시작 후 메뉴가 한글로 표시되는지 확인

✅ **체크포인트**: VS Code 인터페이스가 한글로 표시됨

## 실습 3: 기본 설정 구성

### 설정 파일 열기

1. **설정 UI 열기**
   - `Ctrl+,` (쉼표) 누르기
   - 또는 파일 → 기본 설정 → 설정

2. **JSON 설정 파일 열기**
   - 설정 창 오른쪽 상단의 파일 아이콘 클릭
   - 또는 `Ctrl+Shift+P` → "Preferences: Open User Settings (JSON)"

### 추천 설정 입력

`settings.json`에 다음 내용 추가:

```json
{
  // 편집기 설정
  "editor.fontSize": 14,
  "editor.fontFamily": "D2Coding, Consolas, 'Courier New', monospace",
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "editor.formatOnSave": true,
  "editor.minimap.enabled": true,
  "editor.lineNumbers": "on",
  "editor.renderWhitespace": "selection",
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.indentation": true,
  
  // 파일 설정
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "files.encoding": "utf8",
  "files.eol": "\n",
  
  // 터미널 설정
  "terminal.integrated.fontSize": 13,
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  
  // Git 설정
  "git.autofetch": true,
  "git.confirmSync": false
}
```

3. **파일 저장**
   - `Ctrl+S`

✅ **체크포인트**: 설정 파일이 저장되고 에디터 모양이 변경됨

## 실습 4: 테마 및 아이콘 설정

### 색상 테마 변경

1. **테마 선택 창 열기**
   - `Ctrl+K Ctrl+T` (K 누른 상태에서 T)
   - 또는 `Ctrl+Shift+P` → "Preferences: Color Theme"

2. **테마 선택**
   - 화살표 키로 이동하며 미리보기
   - Enter로 선택
   - 추천: "Dark+ (기본 다크)" 또는 "Light+ (기본 라이트)"

### 파일 아이콘 테마 설치

1. **Material Icon Theme 설치**
   - `Ctrl+Shift+X`
   - "Material Icon Theme" 검색
   - "Install" 클릭

2. **아이콘 테마 적용**
   - `Ctrl+Shift+P` → "Preferences: File Icon Theme"
   - "Material Icon Theme" 선택

✅ **체크포인트**: 선택한 테마가 적용되고 파일 아이콘이 표시됨

## 실습 5: 필수 확장 프로그램 설치

### 범용 확장

다음 확장을 검색하여 설치하세요 (`Ctrl+Shift+X`):

1. **GitLens — Git supercharged**
   - ID: `eamodio.gitlens`
   - Git 기능 강화

2. **Git History**
   - ID: `donjayamanne.githistory`
   - Git 히스토리 시각화

3. **Prettier - Code formatter**
   - ID: `esbenp.prettier-vscode`
   - 코드 포맷터

4. **ESLint**
   - ID: `dbaeumer.vscode-eslint`
   - JavaScript 린터

5. **Path Intellisense**
   - ID: `christian-kohler.path-intellisense`
   - 파일 경로 자동완성

### Java 개발 확장

6. **Extension Pack for Java**
   - ID: `vscjava.vscode-java-pack`
   - Java 개발 도구 모음

7. **Spring Boot Extension Pack**
   - ID: `vmware.vscode-spring-boot`
   - Spring Boot 도구

8. **Gradle for Java** (Gradle 사용 시)
   - ID: `vscjava.vscode-gradle`
   - Gradle 지원

### JavaScript/React 확장

9. **ES7+ React/Redux/React-Native snippets**
   - ID: `dsznajder.es7-react-js-snippets`
   - React 코드 스니펫

10. **Auto Rename Tag**
    - ID: `formulahendry.auto-rename-tag`
    - HTML 태그 자동 이름 변경

### 설치 명령 (선택사항)

터미널에서 일괄 설치:

```bash
code --install-extension eamodio.gitlens
code --install-extension donjayamanne.githistory
code --install-extension esbenp.prettier-vscode
code --install-extension dbaeumer.vscode-eslint
code --install-extension christian-kohler.path-intellisense
code --install-extension vscjava.vscode-java-pack
code --install-extension vmware.vscode-spring-boot
code --install-extension vscjava.vscode-gradle
code --install-extension dsznajder.es7-react-js-snippets
code --install-extension formulahendry.auto-rename-tag
```

✅ **체크포인트**: 모든 확장이 설치되고 "설치됨" 상태로 표시됨

## 실습 6: JDK 설정 확인

### JDK 설치 확인

1. **터미널 열기**
   - ``Ctrl+` `` (백틱)

2. **Java 버전 확인**
   ```bash
   java -version
   javac -version
   ```

3. **출력 예시**
   ```
   openjdk version "17.0.8" 2023-07-18
   OpenJDK Runtime Environment (build 17.0.8+7)
   OpenJDK 64-Bit Server VM (build 17.0.8+7, mixed mode, sharing)
   ```

### VS Code에 JDK 경로 설정

1. **설정 파일 열기**
   - `Ctrl+,` → "java home" 검색

2. **Java: Home 설정**
   - "settings.json에서 편집" 클릭
   - 다음 추가:
   ```json
   {
     "java.home": "C:\\Program Files\\Java\\jdk-17",
     "java.configuration.runtimes": [
       {
         "name": "JavaSE-17",
         "path": "C:\\Program Files\\Java\\jdk-17",
         "default": true
       }
     ]
   }
   ```
   - 실제 JDK 설치 경로로 변경

✅ **체크포인트**: Java 버전이 표시되고 VS Code가 JDK를 인식함

## 실습 7: Node.js 설정 확인

### Node.js 설치 확인

1. **터미널에서 확인**
   ```bash
   node --version
   npm --version
   ```

2. **출력 예시**
   ```
   v18.17.1
   9.8.1
   ```

### NPM 글로벌 패키지 경로 설정 (선택사항)

```bash
# 현재 글로벌 경로 확인
npm config get prefix

# Windows에서 권장 경로
npm config set prefix "C:\Users\[사용자이름]\AppData\Roaming\npm"
```

✅ **체크포인트**: Node.js와 npm 버전이 표시됨

## 실습 8: 워크스페이스 설정

### 실습용 폴더 생성

1. **탐색기에서 폴더 생성**
   - `C:\workspace\vscode-practice` (Windows)
   - `~/workspace/vscode-practice` (macOS/Linux)

2. **VS Code에서 폴더 열기**
   - 파일 → 폴더 열기 (또는 `Ctrl+K Ctrl+O`)
   - 생성한 폴더 선택

### 워크스페이스 권장 확장 설정

1. **`.vscode` 폴더 생성**
   - Explorer에서 새 폴더 아이콘 클릭
   - `.vscode` 입력

2. **`extensions.json` 파일 생성**
   - `.vscode` 폴더에서 새 파일 생성
   - `extensions.json` 파일명 입력

3. **내용 작성**
   ```json
   {
     "recommendations": [
       "vscjava.vscode-java-pack",
       "vmware.vscode-spring-boot",
       "dsznajder.es7-react-js-snippets",
       "dbaeumer.vscode-eslint",
       "esbenp.prettier-vscode",
       "eamodio.gitlens",
       "donjayamanne.githistory"
     ]
   }
   ```

4. **저장**: `Ctrl+S`

✅ **체크포인트**: `.vscode/extensions.json` 파일이 생성됨

## 실습 9: 단축키 테스트

다음 단축키를 실제로 사용해보세요:

### 파일 관리
- `Ctrl+N`: 새 파일
- `Ctrl+S`: 저장
- `Ctrl+W`: 탭 닫기
- `Ctrl+P`: 파일 빠르게 열기

### 편집
- `Ctrl+C`: 복사 (선택 없으면 전체 줄)
- `Ctrl+X`: 잘라내기 (선택 없으면 전체 줄)
- `Ctrl+V`: 붙여넣기
- `Alt+↑/↓`: 줄 이동
- `Shift+Alt+↓`: 줄 복사

### 뷰 전환
- `Ctrl+B`: 사이드바 토글
- `Ctrl+J`: 패널 토글
- ``Ctrl+` ``: 터미널 토글
- `Ctrl+Shift+E`: Explorer
- `Ctrl+Shift+G`: Source Control
- `Ctrl+Shift+X`: Extensions

### 명령 팔레트
- `Ctrl+Shift+P`: 모든 명령 표시
- `Ctrl+P`: 파일로 이동

✅ **체크포인트**: 모든 단축키가 정상 작동함

## 실습 10: 설정 동기화 (선택사항)

여러 컴퓨터에서 동일한 설정을 사용하려면:

1. **설정 동기화 켜기**
   - 왼쪽 하단 계정 아이콘 클릭
   - "설정 동기화 켜기..." 선택

2. **로그인**
   - Microsoft 또는 GitHub 계정 선택
   - 로그인 진행

3. **동기화 항목 선택**
   - 설정
   - 키보드 단축키
   - 확장
   - 사용자 스니펫
   - UI 상태

4. **동기화 시작**
   - "로그인 및 켜기" 클릭

✅ **체크포인트**: 설정 동기화가 활성화됨

## 확인 문제

### 문제 1: 버전 확인
VS Code, Java, Node.js의 버전을 각각 확인하고 기록하세요.

**답안:**
```bash
code --version
java -version
node --version
```

### 문제 2: 확장 프로그램
설치한 확장 프로그램 목록을 확인하세요.

**방법:**
- Extensions 뷰 (`Ctrl+Shift+X`)
- "설치됨" 필터 선택

### 문제 3: 단축키 실습
다음 작업을 단축키만으로 수행하세요:
1. 새 파일 만들기
2. "Hello VS Code" 입력
3. 저장 (파일명: test.txt)
4. 터미널 열기
5. Explorer로 전환

**답안:**
1. `Ctrl+N`
2. (타이핑)
3. `Ctrl+S` → test.txt 입력 → Enter
4. ``Ctrl+` ``
5. `Ctrl+Shift+E`

## 문제 해결

### 확장 설치 실패
- 인터넷 연결 확인
- VS Code 재시작
- 프록시 설정 확인

### JDK/Node.js 인식 안 됨
- PATH 환경 변수 확인
- VS Code 재시작
- 설정에서 경로 수동 지정

### 한글 언어 팩 적용 안 됨
- VS Code 완전히 종료 후 재시작
- `Ctrl+Shift+P` → "Configure Display Language" → "ko" 선택

## 다음 단계

VS Code 설치 및 기본 설정이 완료되었습니다. 이제 Spring Boot 프로젝트를 시작해봅시다!

👉 [Lab 2: Spring Boot 프로젝트 시작하기](lab02-springboot-project.md)

## 참고 자료

- [VS Code 설정 가이드](https://code.visualstudio.com/docs/getstarted/settings)
- [확장 프로그램 마켓플레이스](https://marketplace.visualstudio.com/vscode)
- [단축키 참조 (Windows)](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf)
