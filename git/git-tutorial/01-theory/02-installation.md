# Git 설치

Git을 사용하기 위해 먼저 설치가 필요합니다.

## 💻 운영체제별 설치 방법

### Windows

#### 방법 1: Git for Windows (권장)

1. **다운로드**
   - 공식 사이트 접속: https://git-scm.com/download/win
   - 자동으로 최신 버전 다운로드 시작

2. **설치 과정**
   - 실행 파일(Git-x.xx.x-64-bit.exe) 실행
   - 설치 옵션 선택:
     - ✅ **Git Bash Here**: 탐색기에서 Git Bash 열기 (권장)
     - ✅ **Git GUI Here**: GUI 도구 사용
     - ✅ **기본 에디터**: VS Code 또는 선호하는 에디터 선택
     - ✅ **PATH 설정**: Git from the command line and also from 3rd-party software (권장)
     - ✅ **Line ending 변환**: Checkout Windows-style, commit Unix-style (권장)

3. **설치 확인**
   ```cmd
   git --version
   ```
   출력 예시: `git version 2.43.0.windows.1`

#### 방법 2: Winget (Windows 10/11)
```cmd
winget install Git.Git
```

#### 방법 3: Chocolatey
```cmd
choco install git
```

### macOS

#### 방법 1: Homebrew (권장)
```bash
brew install git
```

#### 방법 2: 공식 설치 파일
1. https://git-scm.com/download/mac 접속
2. dmg 파일 다운로드 및 설치

#### 방법 3: Xcode Command Line Tools
```bash
xcode-select --install
```

### Linux

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install git
```

#### Fedora/RHEL/CentOS
```bash
sudo dnf install git
# 또는
sudo yum install git
```

#### Arch Linux
```bash
sudo pacman -S git
```

## ✅ 설치 확인

터미널에서 다음 명령어를 실행하세요:

```bash
git --version
```

**예상 출력**:
```
git version 2.43.0
```

버전 정보가 표시되면 설치 성공입니다!

## 🛠️ GUI 도구 (선택사항)

명령줄이 익숙하지 않다면 GUI 도구를 사용할 수 있습니다:

### 추천 GUI 도구

1. **GitHub Desktop**
   - https://desktop.github.com/
   - 초보자 친화적
   - GitHub와 완벽한 통합

2. **Sourcetree**
   - https://www.sourcetreeapp.com/
   - 무료, 강력한 기능
   - Windows/macOS 지원

3. **GitKraken**
   - https://www.gitkraken.com/
   - 세련된 인터페이스
   - 다양한 기능

4. **VS Code (통합)**
   - Visual Studio Code에 Git 기능 내장
   - 별도 설치 불필요

### Git Bash vs CMD vs PowerShell (Windows)

**Git Bash** (권장)
- Linux 스타일 명령어 사용
- Git과 함께 설치
- 튜토리얼과 문서가 대부분 Bash 기반

**CMD/PowerShell**
- Windows 기본 터미널
- Git 명령어는 동일하게 작동
- Windows 명령어와 혼용 가능

## 🔧 기본 설정 준비

설치가 완료되었으면 다음 단계는 Git 기본 설정입니다.

**필수 설정 항목**:
- 사용자 이름
- 이메일 주소
- 기본 에디터
- 줄바꿈 처리

## 📋 설치 문제 해결

### Windows: 'git' is not recognized

**원인**: PATH 환경변수에 Git이 없음

**해결**:
1. Git 재설치 시 PATH 옵션 선택
2. 또는 수동으로 PATH 추가:
   - 시스템 환경 변수 편집
   - Path에 `C:\Program Files\Git\cmd` 추가

### macOS: xcrun: error

**원인**: Xcode Command Line Tools 미설치

**해결**:
```bash
xcode-select --install
```

### Linux: Permission denied

**원인**: 관리자 권한 필요

**해결**:
```bash
sudo apt install git  # sudo 사용
```

## 💡 설치 후 체크리스트

- [ ] Git 설치 완료
- [ ] `git --version` 명령어 실행 성공
- [ ] 터미널/Git Bash 사용 가능
- [ ] (선택) GUI 도구 설치

---

**다음 단계**: Git 기본 설정 (03-basic-config.md)
