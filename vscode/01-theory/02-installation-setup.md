# 설치 및 기본 설정

## VS Code 설치

### Windows 설치

1. **다운로드**
   - [VS Code 공식 웹사이트](https://code.visualstudio.com/) 접속
   - "Download for Windows" 버튼 클릭
   - Stable 버전 권장 (Insiders 버전은 베타 기능 포함)

2. **설치 옵션**
   ```
   ✅ Add "Open with Code" action to Windows Explorer file context menu
   ✅ Add "Open with Code" action to Windows Explorer directory context menu
   ✅ Register Code as an editor for supported file types
   ✅ Add to PATH (requires shell restart)
   ```

3. **설치 실행**
   - 다운로드한 설치 파일 실행
   - 위 옵션들을 모두 선택 (권장)
   - "Install" 클릭

### macOS 설치

1. **다운로드**
   - [VS Code 공식 웹사이트](https://code.visualstudio.com/) 접속
   - "Download for Mac" 버튼 클릭
   - Apple Silicon 또는 Intel 버전 선택

2. **설치**
   - 다운로드한 .zip 파일 압축 해제
   - Visual Studio Code.app을 Applications 폴더로 이동

3. **터미널에서 실행 설정**
   - VS Code 실행
   - `Cmd+Shift+P`로 명령 팔레트 열기
   - "Shell Command: Install 'code' command in PATH" 입력 후 실행

### Linux 설치

#### Debian/Ubuntu
```bash
# Microsoft GPG 키 추가
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/

# 저장소 추가
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'

# 설치
sudo apt update
sudo apt install code
```

#### Red Hat/Fedora/CentOS
```bash
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
sudo dnf check-update
sudo dnf install code
```

## 초기 설정

### 1. 한글 언어 팩 설치

1. `Ctrl+Shift+X`로 확장 마켓플레이스 열기
2. "Korean Language Pack" 검색
3. "Install" 클릭
4. VS Code 재시작

### 2. 테마 설정

**색상 테마 변경:**
- `Ctrl+K Ctrl+T` (Windows/Linux) 또는 `Cmd+K Cmd+T` (macOS)
- 원하는 테마 선택

**인기 테마:**
- Dark+ (기본 다크 테마)
- Light+ (기본 라이트 테마)
- One Dark Pro
- Dracula Official
- Material Theme

**아이콘 테마:**
- `Ctrl+Shift+P` → "Preferences: File Icon Theme"
- 추천: Material Icon Theme, VSCode Icons

### 3. 기본 설정

`Ctrl+,`를 눌러 설정 화면을 열고 다음 항목들을 설정합니다.

#### 편집기 설정

```json
{
  // 폰트
  "editor.fontFamily": "D2Coding, Consolas, 'Courier New', monospace",
  "editor.fontSize": 14,
  "editor.fontLigatures": true,
  
  // 들여쓰기
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "editor.detectIndentation": true,
  
  // 코드 포맷팅
  "editor.formatOnSave": true,
  "editor.formatOnPaste": false,
  
  // 자동 저장
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  
  // 줄 번호
  "editor.lineNumbers": "on",
  
  // 미니맵
  "editor.minimap.enabled": true,
  
  // 공백 표시
  "editor.renderWhitespace": "selection",
  
  // 괄호 쌍 컬러
  "editor.bracketPairColorization.enabled": true,
  
  // 들여쓰기 가이드
  "editor.guides.indentation": true
}
```

#### 터미널 설정

```json
{
  // Windows
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "terminal.integrated.fontSize": 13,
  
  // 터미널 줄 수
  "terminal.integrated.scrollback": 10000
}
```

#### 파일 설정

```json
{
  // 파일 인코딩
  "files.encoding": "utf8",
  
  // 줄바꿈 문자
  "files.eol": "\n",
  
  // 제외 파일
  "files.exclude": {
    "**/.git": true,
    "**/.DS_Store": true,
    "**/node_modules": true,
    "**/dist": true,
    "**/build": true,
    "**/.idea": true
  }
}
```

### 4. Git 설정

#### Git 설치 확인
```bash
git --version
```

Git이 설치되어 있지 않다면 [Git 공식 사이트](https://git-scm.com/)에서 설치합니다.

#### VS Code Git 설정

```json
{
  // Git 경로 (자동 감지되지 않을 경우)
  "git.path": "C:\\Program Files\\Git\\bin\\git.exe", // Windows
  
  // 자동 fetch
  "git.autofetch": true,
  
  // 커밋 확인
  "git.confirmSync": false,
  
  // Diff 에디터
  "diffEditor.ignoreTrimWhitespace": false
}
```

### 5. 개발 도구 설치

#### Node.js (React 개발용)
1. [Node.js 공식 사이트](https://nodejs.org/) 접속
2. LTS 버전 다운로드 및 설치
3. 설치 확인:
   ```bash
   node --version
   npm --version
   ```

#### Java (Spring Boot 개발용)
1. [OpenJDK](https://adoptium.net/) 또는 [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) 설치
2. JDK 17 이상 권장
3. 설치 확인:
   ```bash
   java -version
   javac -version
   ```

#### Maven (선택사항)
```bash
# Windows (Chocolatey 사용)
choco install maven

# macOS (Homebrew 사용)
brew install maven

# 확인
mvn --version
```

#### Gradle (선택사항)
```bash
# Windows (Chocolatey 사용)
choco install gradle

# macOS (Homebrew 사용)
brew install gradle

# 확인
gradle --version
```

## 워크스페이스 설정

### 폴더 열기

1. **단일 폴더 워크스페이스**
   - `Ctrl+K Ctrl+O` 또는 File → Open Folder
   - 프로젝트 폴더 선택

2. **멀티 루트 워크스페이스**
   - File → Add Folder to Workspace
   - 여러 프로젝트를 하나의 워크스페이스에서 관리

### 워크스페이스 설정 파일

프로젝트 루트에 `.vscode` 폴더를 만들어 팀 전체가 공유할 설정을 관리합니다.

```
project/
  .vscode/
    settings.json       # 워크스페이스 설정
    extensions.json     # 권장 확장 프로그램
    launch.json         # 디버그 설정
    tasks.json          # 작업 설정
```

## 설정 동기화

여러 기기에서 동일한 설정을 사용하려면:

1. `Ctrl+Shift+P` → "Settings Sync: Turn On"
2. Microsoft 또는 GitHub 계정으로 로그인
3. 동기화할 항목 선택:
   - Settings
   - Keyboard Shortcuts
   - Extensions
   - User Snippets
   - UI State

## 성능 최적화

### 대용량 프로젝트 작업 시

```json
{
  // 파일 감시 제외
  "files.watcherExclude": {
    "**/.git/objects/**": true,
    "**/node_modules/**": true,
    "**/dist/**": true,
    "**/build/**": true
  },
  
  // 검색 제외
  "search.exclude": {
    "**/node_modules": true,
    "**/bower_components": true,
    "**/dist": true,
    "**/build": true
  },
  
  // TypeScript 성능
  "typescript.tsserver.maxTsServerMemory": 4096
}
```

## 문제 해결

### VS Code가 느리게 실행되는 경우

1. **확장 프로그램 점검**
   - `Ctrl+Shift+P` → "Developer: Show Running Extensions"
   - 사용하지 않는 확장 비활성화

2. **캐시 정리**
   - 설정 폴더 정리:
     - Windows: `%APPDATA%\Code`
     - macOS: `~/Library/Application Support/Code`
     - Linux: `~/.config/Code`

3. **하드웨어 가속 비활성화**
   ```json
   {
     "disable-hardware-acceleration": true
   }
   ```

### Git이 인식되지 않는 경우

1. Git 설치 확인
2. PATH 환경 변수 확인
3. VS Code 재시작

## 다음 단계

이제 VS Code가 설치되고 기본 설정이 완료되었습니다. 다음 챕터에서는 VS Code의 사용자 인터페이스를 자세히 알아봅니다.

👉 [다음: 사용자 인터페이스 이해하기](03-user-interface.md)

## 참고 자료

- [VS Code 설치 가이드](https://code.visualstudio.com/docs/setup/setup-overview)
- [VS Code 설정 문서](https://code.visualstudio.com/docs/getstarted/settings)
- [Settings Sync](https://code.visualstudio.com/docs/editor/settings-sync)
