# 필수 확장 프로그램

VS Code의 진정한 힘은 확장 프로그램 생태계에 있습니다. 프로젝트 개발에 필요한 필수 확장 프로그램을 소개합니다.

## 확장 프로그램 설치 방법

### UI에서 설치

1. `Ctrl+Shift+X`로 Extensions 뷰 열기
2. 검색창에 확장 프로그램 이름 입력
3. "Install" 버튼 클릭

### 명령줄에서 설치

```bash
code --install-extension <extension-id>
```

### 팀 전체 권장 확장 설정

프로젝트 루트에 `.vscode/extensions.json` 파일 생성:

```json
{
  "recommendations": [
    "vscjava.vscode-java-pack",
    "vmware.vscode-spring-boot",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "eamodio.gitlens"
  ]
}
```

## 범용 필수 확장

### 1. Korean Language Pack (한국어 팩)
- **ID**: `MS-CEINTL.vscode-language-pack-ko`
- **설명**: VS Code 인터페이스를 한글로 변경
- **필수도**: ⭐⭐⭐⭐⭐

### 2. GitLens
- **ID**: `eamodio.gitlens`
- **설명**: Git을 슈퍼차지하는 최고의 Git 확장
- **주요 기능**:
  - 각 줄의 Git blame 정보 표시
  - 파일 및 줄 히스토리 조회
  - 커밋 검색 및 비교
  - 저장소 시각화
- **필수도**: ⭐⭐⭐⭐⭐

```json
{
  "gitlens.hovers.currentLine.over": "line",
  "gitlens.currentLine.enabled": true,
  "gitlens.codeLens.enabled": true
}
```

### 3. Git History
- **ID**: `donjayamanne.githistory`
- **설명**: Git 로그, 파일 히스토리, 브랜치 비교
- **주요 기능**:
  - 그래픽 Git 로그
  - 파일 히스토리 조회
  - 브랜치 및 커밋 비교
- **필수도**: ⭐⭐⭐⭐

### 4. Prettier - Code formatter
- **ID**: `esbenp.prettier-vscode`
- **설명**: 코드 자동 포맷팅
- **지원 언어**: JavaScript, TypeScript, JSON, CSS, HTML, Markdown 등
- **필수도**: ⭐⭐⭐⭐⭐

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

### 5. ESLint
- **ID**: `dbaeumer.vscode-eslint`
- **설명**: JavaScript/TypeScript 린팅
- **필수도**: ⭐⭐⭐⭐⭐

```json
{
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],
  "eslint.codeActionsOnSave.mode": "all",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

### 6. Path Intellisense
- **ID**: `christian-kohler.path-intellisense`
- **설명**: 파일 경로 자동완성
- **필수도**: ⭐⭐⭐⭐

### 7. Auto Rename Tag
- **ID**: `formulahendry.auto-rename-tag`
- **설명**: HTML/XML 태그 자동 이름 변경
- **필수도**: ⭐⭐⭐⭐

### 8. Bracket Pair Colorizer 2 (내장 기능)
- VS Code 1.60 이후 내장 기능으로 제공
- 설정만 활성화:

```json
{
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": "active"
}
```

### 9. Error Lens
- **ID**: `usernamehw.errorlens`
- **설명**: 에러와 경고를 인라인으로 강조 표시
- **필수도**: ⭐⭐⭐⭐

### 10. Todo Tree
- **ID**: `Gruntfuggly.todo-tree`
- **설명**: TODO, FIXME 등의 주석을 추적하고 표시
- **필수도**: ⭐⭐⭐

```json
{
  "todo-tree.general.tags": [
    "TODO",
    "FIXME",
    "NOTE",
    "BUG",
    "HACK"
  ],
  "todo-tree.highlights.defaultHighlight": {
    "icon": "alert",
    "type": "text"
  }
}
```

## Java / Spring Boot 개발 필수 확장

### 1. Extension Pack for Java
- **ID**: `vscjava.vscode-java-pack`
- **설명**: Java 개발을 위한 확장 팩
- **포함 내용**:
  - Language Support for Java
  - Debugger for Java
  - Test Runner for Java
  - Maven for Java
  - Project Manager for Java
  - Visual Studio IntelliCode
- **필수도**: ⭐⭐⭐⭐⭐

### 2. Spring Boot Extension Pack
- **ID**: `vmware.vscode-spring-boot`
- **설명**: Spring Boot 개발 도구 모음
- **포함 내용**:
  - Spring Boot Tools
  - Spring Boot Dashboard
  - Spring Initializr Java Support
- **필수도**: ⭐⭐⭐⭐⭐

```json
{
  "java.configuration.updateBuildConfiguration": "automatic",
  "java.compile.nullAnalysis.mode": "automatic",
  "spring-boot.ls.problem.boot2": "WARNING"
}
```

### 3. Gradle for Java
- **ID**: `vscjava.vscode-gradle`
- **설명**: Gradle 프로젝트 지원
- **필수도**: ⭐⭐⭐⭐⭐ (Gradle 사용 시)

### 4. Lombok Annotations Support
- **ID**: `vscjava.vscode-lombok`
- **설명**: Lombok 어노테이션 지원
- **필수도**: ⭐⭐⭐⭐ (Lombok 사용 시)

### 5. SonarLint
- **ID**: `SonarSource.sonarlint-vscode`
- **설명**: 코드 품질 및 보안 이슈 감지
- **필수도**: ⭐⭐⭐⭐

## JavaScript / React 개발 필수 확장

### 1. ES7+ React/Redux/React-Native snippets
- **ID**: `dsznajder.es7-react-js-snippets`
- **설명**: React 코드 스니펫
- **주요 스니펫**:
  - `rafce` → React Arrow Function Component Export
  - `useS` → useState Hook
  - `useE` → useEffect Hook
- **필수도**: ⭐⭐⭐⭐⭐

### 2. Vite
- **ID**: `antfu.vite`
- **설명**: Vite 프로젝트 지원
- **필수도**: ⭐⭐⭐⭐ (Vite 사용 시)

### 3. CSS Modules
- **ID**: `clinyong.vscode-css-modules`
- **설명**: CSS Modules 자동완성
- **필수도**: ⭐⭐⭐

### 4. Tailwind CSS IntelliSense
- **ID**: `bradlc.vscode-tailwindcss`
- **설명**: Tailwind CSS 자동완성 및 문법 검사
- **필수도**: ⭐⭐⭐⭐ (Tailwind 사용 시)

### 5. PostCSS Language Support
- **ID**: `csstools.postcss`
- **설명**: PostCSS 문법 지원
- **필수도**: ⭐⭐⭐

## 디버깅 및 개발 도구

### 1. Remote Development
- **ID**: `ms-vscode-remote.vscode-remote-extensionpack`
- **설명**: 원격 개발 확장 팩
- **포함 내용**:
  - Remote - SSH
  - Remote - Containers
  - Remote - WSL
- **필수도**: ⭐⭐⭐⭐⭐ (원격 개발 시)

### 2. REST Client
- **ID**: `humao.rest-client`
- **설명**: HTTP 요청을 파일에서 직접 실행
- **필수도**: ⭐⭐⭐⭐

**사용 예시:**
```http
### GET 요청
GET http://localhost:8080/api/users HTTP/1.1

### POST 요청
POST http://localhost:8080/api/users HTTP/1.1
Content-Type: application/json

{
  "name": "홍길동",
  "email": "hong@example.com"
}
```

### 3. Thunder Client
- **ID**: `rangav.vscode-thunder-client`
- **설명**: 가벼운 REST API 클라이언트 (Postman 대안)
- **필수도**: ⭐⭐⭐⭐

### 4. Docker
- **ID**: `ms-azuretools.vscode-docker`
- **설명**: Docker 컨테이너 관리
- **필수도**: ⭐⭐⭐⭐

## 생산성 향상 도구

### 1. Live Share
- **ID**: `ms-vsliveshare.vsliveshare`
- **설명**: 실시간 협업 코딩
- **주요 기능**:
  - 코드 공유
  - 공동 디버깅
  - 터미널 공유
- **필수도**: ⭐⭐⭐⭐

### 2. Project Manager
- **ID**: `alefragnani.project-manager`
- **설명**: 여러 프로젝트 빠르게 전환
- **필수도**: ⭐⭐⭐⭐

### 3. Bookmarks
- **ID**: `alefragnani.Bookmarks`
- **설명**: 코드에 북마크 설정
- **필수도**: ⭐⭐⭐

### 4. Code Spell Checker
- **ID**: `streetsidesoftware.code-spell-checker`
- **설명**: 스펠링 체크
- **필수도**: ⭐⭐⭐

## 테마 및 아이콘

### 추천 테마

1. **One Dark Pro**
   - ID: `zhuangtongfa.Material-theme`
   - 가장 인기 있는 다크 테마

2. **Material Theme**
   - ID: `Equinusocio.vsc-material-theme`
   - 다양한 색상 변형 제공

3. **Dracula Official**
   - ID: `dracula-theme.theme-dracula`
   - 눈이 편한 다크 테마

### 추천 아이콘 테마

1. **Material Icon Theme**
   - ID: `PKief.material-icon-theme`
   - 가장 인기 있는 아이콘 테마

2. **vscode-icons**
   - ID: `vscode-icons-team.vscode-icons`
   - 풍부한 아이콘 세트

## 확장 프로그램 관리

### 워크스페이스별 활성화/비활성화

1. 확장 프로그램 우클릭
2. "Enable (Workspace)" 또는 "Disable (Workspace)" 선택

### 확장 프로그램 설정 동기화

```json
{
  "settingsSync.ignoredExtensions": [
    "ms-vscode-remote.remote-ssh" // 동기화 제외할 확장
  ]
}
```

### 성능 영향 확인

1. `Ctrl+Shift+P` → "Developer: Show Running Extensions"
2. 각 확장의 활성화 시간과 메모리 사용량 확인
3. 느린 확장은 비활성화 고려

## 확장 프로그램 추천 팁

### 필수 vs 선택

- **반드시 설치**: Java Pack, Spring Boot, GitLens, Prettier, ESLint
- **프로젝트에 따라**: Gradle/Maven, Tailwind CSS, Docker
- **개인 취향**: 테마, 아이콘, 북마크 도구

### 너무 많은 확장 설치 주의

- 확장이 많을수록 시작 속도 저하
- 필요한 확장만 설치
- 사용하지 않는 확장은 비활성화 또는 제거

### 프로젝트별 확장 추천 파일 작성

팀원들이 일관된 개발 환경을 유지하도록 `.vscode/extensions.json` 파일을 버전 관리에 포함하세요.

## 다음 단계

필수 확장 프로그램을 설치했다면, 이제 Spring Boot 개발 환경을 설정해봅시다.

👉 [다음: Spring Boot 개발 환경](05-springboot-environment.md)

## 참고 자료

- [VS Code Marketplace](https://marketplace.visualstudio.com/vscode)
- [확장 프로그램 가이드](https://code.visualstudio.com/docs/editor/extension-marketplace)
