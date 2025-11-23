# Git 기본 설정

Git을 처음 사용하기 전에 기본 설정이 필요합니다.

## 🎯 필수 설정

### 1. 사용자 정보 설정

Git은 모든 커밋에 작성자 정보를 기록합니다.

```bash
# 사용자 이름 설정
git config --global user.name "홍길동"

# 이메일 주소 설정
git config --global user.email "hong@example.com"
```

**중요**: 이메일 주소는 GitHub/GitLab 계정과 동일하게 설정하세요!

### 2. 설정 확인

```bash
# 전체 설정 보기
git config --list

# 특정 설정 확인
git config user.name
git config user.email
```

## ⚙️ 추가 설정 (권장)

### 기본 에디터 설정

커밋 메시지 작성 시 사용할 에디터를 지정합니다.

```bash
# Visual Studio Code
git config --global core.editor "code --wait"

# Vim
git config --global core.editor "vim"

# Nano
git config --global core.editor "nano"

# Notepad (Windows)
git config --global core.editor "notepad"
```

### 기본 브랜치 이름 설정

```bash
# 'main'을 기본 브랜치로 설정 (GitHub 표준)
git config --global init.defaultBranch main
```

### 줄바꿈 문자 처리

운영체제별로 줄바꿈 문자가 다릅니다:
- Windows: CRLF (`\r\n`)
- macOS/Linux: LF (`\n`)

```bash
# Windows
git config --global core.autocrlf true

# macOS/Linux
git config --global core.autocrlf input
```

### 컬러 출력 활성화

```bash
git config --global color.ui auto
```

### 자격증명 저장 (선택)

매번 비밀번호를 입력하지 않도록 자격증명을 저장할 수 있습니다.

```bash
# Windows (자격 증명 관리자 사용)
git config --global credential.helper wincred

# macOS (Keychain 사용)
git config --global credential.helper osxkeychain

# Linux (메모리에 15분간 캐시)
git config --global credential.helper cache

# Linux (영구 저장 - 주의: 평문으로 저장됨)
git config --global credential.helper store
```

## 📝 설정 파일 위치

Git 설정은 3가지 레벨로 관리됩니다:

### 1. System (시스템 전체)
```bash
# 설정 위치: /etc/gitconfig (Linux/macOS)
git config --system <key> <value>
```

### 2. Global (사용자)
```bash
# 설정 위치:
# - Windows: C:\Users\<사용자>\.gitconfig
# - macOS/Linux: ~/.gitconfig
git config --global <key> <value>
```

### 3. Local (저장소별)
```bash
# 설정 위치: <저장소>/.git/config
git config --local <key> <value>
```

**우선순위**: Local > Global > System

## 🔍 설정 파일 직접 편집

텍스트 에디터로 설정 파일을 직접 편집할 수도 있습니다.

```bash
# Global 설정 파일 열기
git config --global --edit
```

**예시 (.gitconfig)**:
```ini
[user]
    name = 홍길동
    email = hong@example.com
    
[core]
    editor = code --wait
    autocrlf = true
    
[init]
    defaultBranch = main
    
[color]
    ui = auto
    
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
```

## 🎨 유용한 별칭(Alias) 설정

자주 사용하는 명령어를 짧게 줄일 수 있습니다.

```bash
# 기본 별칭
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit

# 고급 별칭
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual 'log --graph --oneline --all'
```

**사용 예시**:
```bash
# 기존 명령어
git status

# 별칭 사용
git st
```

## ✅ 설정 완료 체크리스트

설정이 제대로 되었는지 확인하세요:

```bash
# 사용자 정보 확인
git config user.name
git config user.email

# 전체 설정 보기
git config --list
```

**필수 확인 항목**:
- [ ] user.name 설정됨
- [ ] user.email 설정됨
- [ ] core.autocrlf 설정됨 (Windows: true, Mac/Linux: input)
- [ ] init.defaultBranch 설정됨 (main 권장)

## 🔧 설정 초기화 및 삭제

### 특정 설정 삭제
```bash
git config --global --unset user.name
```

### 섹션 전체 삭제
```bash
git config --global --remove-section alias
```

### 설정 파일 위치 확인
```bash
git config --list --show-origin
```

## 💡 실전 팁

### 회사/개인 프로젝트 구분

Global과 Local 설정을 활용해 회사와 개인 이메일을 구분할 수 있습니다:

```bash
# Global (개인)
git config --global user.email "personal@example.com"

# 회사 프로젝트 디렉토리에서 (Local)
cd /path/to/company/project
git config --local user.email "work@company.com"
```

### 여러 GitHub 계정 사용

각 저장소마다 다른 계정을 사용하려면 Local 설정을 활용하세요:

```bash
# 저장소마다 설정
cd project1
git config --local user.email "account1@example.com"

cd ../project2
git config --local user.email "account2@example.com"
```

## 📋 기본 설정 템플릿

처음 Git을 설정하는 초보자를 위한 완전한 설정:

```bash
# 필수 설정
git config --global user.name "당신의 이름"
git config --global user.email "your.email@example.com"

# 권장 설정
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
git config --global color.ui auto

# Windows 사용자
git config --global core.autocrlf true

# macOS/Linux 사용자
git config --global core.autocrlf input

# 유용한 별칭
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --graph --oneline --decorate --all"
```

---

**다음 단계**: Git 작업 흐름 이해하기 (04-git-workflow.md)
