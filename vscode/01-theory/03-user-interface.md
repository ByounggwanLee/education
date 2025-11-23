# 사용자 인터페이스 이해하기

VS Code의 UI는 효율적인 코드 작성을 위해 설계되었습니다. 각 영역의 역할을 이해하면 생산성을 크게 향상시킬 수 있습니다.

## 기본 레이아웃

```
┌─────────────────────────────────────────────────────────┐
│  Title Bar (제목 표시줄)                                │
├─────────────────────────────────────────────────────────┤
│  Menu Bar (메뉴 바) - 선택적                            │
├───┬─────────────────────────────────────────────┬───────┤
│   │  Editor Group (에디터 그룹)                │       │
│ A │  ┌─────────────────────────────────┐       │   P   │
│ c │  │  Tab 1 │ Tab 2 │ Tab 3        │       │   a   │
│ t │  ├─────────────────────────────────┤       │   n   │
│ i │  │                                 │       │   e   │
│ v │  │                                 │       │   l   │
│ i │  │      Code Editor                │       │       │
│ t │  │      (코드 에디터)              │       │       │
│ y │  │                                 │       │       │
│   │  │                                 │       │       │
│ B │  └─────────────────────────────────┘       │       │
│ a │                                             │       │
│ r │                                             │       │
├───┴─────────────────────────────────────────────┴───────┤
│  Status Bar (상태 표시줄)                                │
└─────────────────────────────────────────────────────────┘
```

## 주요 UI 영역

### 1. Activity Bar (활동 표시줄) - 왼쪽

가장 왼쪽에 위치한 수직 바로, 주요 뷰를 전환합니다.

#### 기본 아이콘

| 아이콘 | 기능 | 단축키 |
|-------|------|-------|
| 📁 | **Explorer** - 파일 탐색기 | `Ctrl+Shift+E` |
| 🔍 | **Search** - 전체 검색 | `Ctrl+Shift+F` |
| 🔀 | **Source Control** - Git 관리 | `Ctrl+Shift+G` |
| ▶️ | **Run and Debug** - 디버깅 | `Ctrl+Shift+D` |
| 📦 | **Extensions** - 확장 프로그램 | `Ctrl+Shift+X` |

#### Activity Bar 사용자 정의

- 아이콘 우클릭 → 순서 변경 또는 숨기기
- 확장 프로그램이 추가 아이콘을 제공할 수 있음

### 2. Side Bar (사이드 바) - Activity Bar 오른쪽

Activity Bar에서 선택한 뷰가 표시되는 영역입니다.

#### Explorer (탐색기)
- **폴더 트리**: 프로젝트 파일 구조
- **Outline**: 현재 파일의 심볼 구조
- **Timeline**: 파일 변경 이력

#### Search (검색)
- 전체 텍스트 검색 및 바꾸기
- 정규식 지원
- 특정 파일 포함/제외

#### Source Control (소스 제어)
- 변경된 파일 목록
- 커밋 메시지 작성
- 브랜치 관리

### 3. Editor (에디터) - 중앙

코드를 작성하는 주요 작업 영역입니다.

#### Editor Groups (에디터 그룹)

**분할 레이아웃:**
- 수평 분할: `Ctrl+\`
- 수직 분할: `Ctrl+K Ctrl+\`
- 최대 3x3 그리드까지 분할 가능

**그룹 간 이동:**
- `Ctrl+1`, `Ctrl+2`, `Ctrl+3`: 그룹으로 이동
- `Ctrl+K Ctrl+←/→`: 이전/다음 그룹으로 이동

#### Tabs (탭)

**탭 관리:**
- `Ctrl+Tab`: 열린 파일 간 전환
- `Ctrl+W`: 현재 탭 닫기
- `Ctrl+K W`: 모든 탭 닫기
- `Ctrl+K Ctrl+W`: 다른 탭 모두 닫기

**탭 고정:**
- 탭 우클릭 → "Pin Tab" (📌 아이콘 표시)
- 고정된 탭은 자동으로 닫히지 않음

#### Breadcrumbs (경로 탐색)

에디터 상단에 파일 경로와 심볼 계층 구조를 표시합니다.

```json
{
  "breadcrumbs.enabled": true,
  "breadcrumbs.filePath": "on",
  "breadcrumbs.symbolPath": "on"
}
```

### 4. Panel (패널) - 하단

추가 정보와 도구를 표시하는 영역입니다.

#### 주요 패널

| 패널 | 기능 | 단축키 |
|------|------|-------|
| **Terminal** | 통합 터미널 | ``Ctrl+` `` |
| **Problems** | 오류 및 경고 | `Ctrl+Shift+M` |
| **Output** | 확장 및 작업 출력 | `Ctrl+Shift+U` |
| **Debug Console** | 디버그 콘솔 | `Ctrl+Shift+Y` |

**패널 제어:**
- `Ctrl+J`: 패널 토글 (보이기/숨기기)
- 패널 크기 조정: 경계선 드래그
- 패널 위치 변경: 우클릭 → "Move Panel"

#### 통합 터미널

**여러 터미널 사용:**
- 새 터미널: ``Ctrl+Shift+` ``
- 터미널 간 전환: 드롭다운 메뉴 사용
- 터미널 분할: 분할 아이콘 클릭

**터미널 프로필:**
```json
{
  "terminal.integrated.profiles.windows": {
    "PowerShell": {
      "source": "PowerShell",
      "icon": "terminal-powershell"
    },
    "Command Prompt": {
      "path": "cmd.exe",
      "icon": "terminal-cmd"
    },
    "Git Bash": {
      "source": "Git Bash",
      "icon": "terminal-bash"
    }
  }
}
```

### 5. Status Bar (상태 표시줄) - 하단

현재 상태 정보와 빠른 작업을 제공합니다.

#### 왼쪽 정보

| 항목 | 설명 |
|------|------|
| 🔀 브랜치 | 현재 Git 브랜치 (클릭하여 변경) |
| 🔄 동기화 | Git 동기화 상태 |
| ❌ 오류 | 오류 개수 |
| ⚠️ 경고 | 경고 개수 |

#### 오른쪽 정보

| 항목 | 설명 |
|------|------|
| 줄:열 | 커서 위치 |
| Spaces/Tab | 들여쓰기 설정 |
| UTF-8 | 파일 인코딩 |
| LF/CRLF | 줄바꿈 문자 |
| 언어 모드 | 파일 언어 (클릭하여 변경) |

## 명령 팔레트 (Command Palette)

모든 명령에 접근할 수 있는 강력한 도구입니다.

### 사용법

- `Ctrl+Shift+P` 또는 `F1`: 명령 팔레트 열기
- 명령 이름 입력하여 검색
- 화살표 키로 선택, Enter로 실행

### 주요 명령

```
> Preferences: Open Settings (UI)
> Preferences: Open Keyboard Shortcuts
> File: Revert File
> View: Toggle Terminal
> Git: Clone
> Extensions: Install Extensions
```

### 빠른 열기 (Quick Open)

- `Ctrl+P`: 파일 빠르게 열기
- 파일 이름 입력하여 검색
- 퍼지 검색 지원 (예: "ucmd" → "user-commands.md")

#### 추가 기능

| 접두사 | 기능 | 예시 |
|-------|------|------|
| 없음 | 파일 열기 | `app.js` |
| `@` | 심볼로 이동 | `@getUserData` |
| `@:` | 그룹화된 심볼 | `@:` |
| `#` | 워크스페이스 심볼 | `#UserModel` |
| `:` | 줄로 이동 | `:42` |
| `>` | 명령 실행 | `>format` |

## 제스처와 단축키

### 에디터 제스처

| 동작 | 결과 |
|------|------|
| `Ctrl+클릭` | 정의로 이동 |
| `Alt+클릭` | 다중 커서 추가 |
| `Shift+Alt+드래그` | 열 선택 (Box Selection) |
| `Ctrl+D` | 단어 선택 (반복하면 다중 선택) |

### 필수 단축키

#### 파일 관리
- `Ctrl+N`: 새 파일
- `Ctrl+O`: 파일 열기
- `Ctrl+S`: 저장
- `Ctrl+Shift+S`: 다른 이름으로 저장
- `Ctrl+K S`: 모두 저장

#### 편집
- `Ctrl+X`: 잘라내기 (선택 없으면 전체 줄)
- `Ctrl+C`: 복사 (선택 없으면 전체 줄)
- `Ctrl+V`: 붙여넣기
- `Ctrl+Z`: 실행 취소
- `Ctrl+Y`: 다시 실행

#### 탐색
- `Ctrl+G`: 줄로 이동
- `Ctrl+P`: 파일 빠르게 열기
- `F12`: 정의로 이동
- `Alt+F12`: 정의 미리보기
- `Shift+F12`: 참조 찾기

## 사용자 정의

### UI 밀도 조정

```json
{
  // 탭 크기
  "workbench.editor.tabSizing": "shrink", // "fit" | "shrink"
  
  // Activity Bar 위치
  "workbench.activityBar.location": "default", // "default" | "top" | "bottom" | "hidden"
  
  // 사이드바 위치
  "workbench.sideBar.location": "left", // "left" | "right"
  
  // Zen Mode (집중 모드)
  "zenMode.fullScreen": false,
  "zenMode.centerLayout": true
}
```

### 작업 영역 최대화

**Zen Mode (집중 모드):**
- `Ctrl+K Z`: Zen Mode 토글
- 불필요한 UI 요소 모두 숨김
- `Esc` 두 번 눌러 종료

**전체 화면:**
- `F11`: 전체 화면 토글

**UI 요소 토글:**
- `Ctrl+B`: 사이드바 토글
- `Ctrl+J`: 패널 토글
- Menu Bar 숨기기: `Alt` 키로 임시 표시

## 접근성 기능

### 화면 확대/축소

- `Ctrl++`: 확대
- `Ctrl+-`: 축소
- `Ctrl+0`: 초기화

### 고대비 테마

```json
{
  "workbench.colorTheme": "Default High Contrast"
}
```

### 스크린 리더

VS Code는 NVDA, JAWS 등의 스크린 리더를 지원합니다.

## 다음 단계

이제 VS Code의 UI를 이해했으니, 다음 챕터에서는 필수 확장 프로그램을 알아봅니다.

👉 [다음: 필수 확장 프로그램](04-essential-extensions.md)

## 참고 자료

- [VS Code UI 가이드](https://code.visualstudio.com/docs/getstarted/userinterface)
- [단축키 참조](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf)
