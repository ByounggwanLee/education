# VS Code란 무엇인가?

## 개요

Visual Studio Code(VS Code)는 Microsoft에서 개발한 무료 오픈소스 코드 에디터입니다. 가볍고 빠르면서도 강력한 기능을 제공하여 전 세계 개발자들이 가장 많이 사용하는 개발 도구입니다.

## 주요 특징

### 1. 크로스 플랫폼 지원

- **Windows, macOS, Linux** 모두 지원
- 동일한 사용자 경험 제공
- 설정 동기화 기능으로 여러 기기에서 일관된 환경 유지

### 2. 가볍고 빠른 성능

- 빠른 실행 속도
- 적은 메모리 사용량
- 대용량 파일도 원활하게 처리

### 3. 풍부한 확장 프로그램 생태계

- 수만 개의 확장 프로그램 제공
- 다양한 프로그래밍 언어 지원
- 개발 워크플로우 맞춤 설정 가능

### 4. 내장 기능

- **IntelliSense**: 지능형 코드 완성
- **디버깅**: 강력한 디버깅 도구
- **Git 통합**: 버전 관리 기능 내장
- **터미널**: 통합 터미널 제공
- **확장성**: 거의 모든 개발 언어와 프레임워크 지원

## VS Code vs 다른 IDE 비교

### VS Code의 장점

| 특징 | VS Code | IntelliJ IDEA | Eclipse |
|------|---------|---------------|---------|
| 무료 | ✅ | ⚠️ (Community만) | ✅ |
| 가벼움 | ✅ | ❌ | ❌ |
| 빠른 시작 | ✅ | ❌ | ❌ |
| 확장성 | ✅ | ✅ | ✅ |
| 다중 언어 지원 | ✅ | ⚠️ (제한적) | ⚠️ (제한적) |

### 언제 VS Code를 사용해야 하나?

✅ **VS Code가 적합한 경우:**
- 여러 프로그래밍 언어를 사용하는 프로젝트
- 프론트엔드 개발 (JavaScript, TypeScript, React 등)
- 경량화된 개발 환경이 필요한 경우
- 빠른 파일 편집이 필요한 경우
- 마이크로서비스 아키텍처 개발

⚠️ **다른 IDE가 더 나을 수 있는 경우:**
- 대규모 Java 엔터프라이즈 애플리케이션 (IntelliJ IDEA)
- 복잡한 리팩토링이 자주 필요한 경우 (IntelliJ IDEA)
- Android 앱 개발 (Android Studio)

## 프로젝트 개발에서 VS Code의 역할

### Spring Boot 개발
- Java Extension Pack으로 강력한 Java 개발 지원
- Maven/Gradle 통합
- Spring Boot 전용 확장 프로그램
- 디버깅 및 테스트 실행 지원

### React 개발
- 최고의 JavaScript/TypeScript 지원
- JSX/TSX 문법 지원
- ESLint, Prettier 통합
- Vite 개발 서버 통합

### Git 통합
- 기본 Git 기능 내장
- GitLens로 강력한 Git 시각화
- Git History로 변경 이력 추적
- Pull Request 관리

## 핵심 개념

### 워크스페이스 (Workspace)

- 프로젝트 폴더를 여는 단위
- 워크스페이스별 설정 가능
- 멀티 루트 워크스페이스 지원

### 확장 프로그램 (Extensions)

- VS Code의 기능을 확장하는 플러그인
- Marketplace에서 설치
- 프로젝트별 추천 확장 설정 가능

### 설정 (Settings)

- 사용자 설정: 모든 프로젝트에 적용
- 워크스페이스 설정: 특정 프로젝트에만 적용
- JSON 또는 UI로 관리

### 명령 팔레트 (Command Palette)

- 모든 명령을 검색하고 실행
- 단축키: `Ctrl+Shift+P` (Windows/Linux) 또는 `Cmd+Shift+P` (macOS)

## VS Code의 철학

1. **코드 중심**: 코드 작성에 집중할 수 있는 깔끔한 인터페이스
2. **확장성**: 필요한 기능만 추가하여 사용
3. **개방성**: 오픈소스로 투명하게 개발
4. **커뮤니티**: 활발한 커뮤니티와 생태계

## 다음 단계

다음 챕터에서는 VS Code를 설치하고 기본 설정을 진행합니다.

👉 [다음: 설치 및 기본 설정](02-installation-setup.md)

## 참고 자료

- [VS Code 공식 웹사이트](https://code.visualstudio.com/)
- [VS Code 문서](https://code.visualstudio.com/docs)
- [VS Code GitHub](https://github.com/microsoft/vscode)
