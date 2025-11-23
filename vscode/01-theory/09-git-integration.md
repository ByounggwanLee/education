# Git 통합

VS Code는 강력한 Git 통합 기능을 제공하며, GitLens와 Git History 확장으로 더욱 강력해집니다.

## 기본 Git 기능

### Source Control 뷰

`Ctrl+Shift+G`로 Source Control 뷰를 엽니다.

#### 주요 영역

```
┌─────────────────────────────────┐
│  SOURCE CONTROL                 │
├─────────────────────────────────┤
│  📝 Commit Message              │
│  ✅ Commit                      │
├─────────────────────────────────┤
│  Changes (5)                    │
│    M  src/App.jsx              │
│    M  src/components/User.jsx  │
│    A  src/utils/api.js         │
│    D  src/old-file.js          │
│    ?? src/temp.txt             │
└─────────────────────────────────┘
```

#### 파일 상태 아이콘

| 아이콘 | 의미 |
|--------|------|
| `M` | Modified (수정됨) |
| `A` | Added (추가됨) |
| `D` | Deleted (삭제됨) |
| `R` | Renamed (이름 변경) |
| `C` | Copied (복사됨) |
| `U` | Untracked (추적 안 됨) |
| `??` | Untracked (추적 안 됨) |
| `!` | Ignored (무시됨) |

### 기본 Git 작업

#### 저장소 초기화

1. `Ctrl+Shift+P` → "Git: Initialize Repository"
2. 프로젝트 폴더 선택

또는 터미널:
```bash
git init
```

#### 변경 사항 스테이징

**개별 파일:**
- Source Control에서 파일 옆 "+" 버튼 클릭
- 또는 `Ctrl+Enter` (파일에 포커스)

**모든 파일:**
- "Changes" 옆 "+" 버튼 클릭

#### 커밋

1. 커밋 메시지 입력
2. `Ctrl+Enter` 또는 "✓" 버튼 클릭

**커밋 메시지 규칙 (예시):**
```
feat: 사용자 목록 조회 기능 추가

- UserController에 getAllUsers() 메서드 구현
- UserService와 Repository 연동
- API 엔드포인트 /api/users 추가
```

#### 푸시/풀

**푸시:**
- Source Control 뷰에서 "..." → "Push"
- 또는 Status Bar의 동기화 아이콘 클릭

**풀:**
- Source Control 뷰에서 "..." → "Pull"

#### 브랜치 관리

**현재 브랜치 확인:**
- Status Bar 왼쪽 하단에 표시

**브랜치 전환:**
1. Status Bar의 브랜치 이름 클릭
2. 브랜치 목록에서 선택
3. 또는 `Ctrl+Shift+P` → "Git: Checkout to..."

**새 브랜치 생성:**
1. Status Bar의 브랜치 이름 클릭
2. "+ Create new branch" 선택
3. 브랜치 이름 입력

터미널 사용:
```bash
# 새 브랜치 생성 및 전환
git checkout -b feature/user-management

# 브랜치 목록
git branch

# 브랜치 전환
git checkout main
```

### Diff 보기

#### 인라인 Diff

파일을 수정하면 에디터 왼쪽 여백에 변경 표시:
- 🟩 녹색: 추가된 줄
- 🟥 빨간색: 삭제된 줄
- 🟦 파란색: 수정된 줄

#### 나란히 비교

1. Source Control에서 변경된 파일 클릭
2. 이전 버전과 현재 버전이 나란히 표시

**단축키:**
- `Alt+F5`: 이전 변경으로 이동
- `F5`: 다음 변경으로 이동

### Git 히스토리 보기

**파일 히스토리:**
1. 파일 우클릭 → "Git: View File History"
2. 커밋 목록 표시

**커밋 비교:**
1. 커밋 선택
2. 변경 사항 확인

## GitLens 확장

GitLens는 Git 기능을 대폭 향상시키는 필수 확장입니다.

### 설치

- Extension ID: `eamodio.gitlens`

### 주요 기능

#### 1. Current Line Blame

현재 커서가 위치한 줄의 Git 정보를 인라인으로 표시합니다.

```java
public class UserService {
    // ← Git Lens: 홍길동, 2일 전 • feat: 사용자 서비스 추가
    private UserRepository userRepository;
}
```

**설정:**
```json
{
  "gitlens.currentLine.enabled": true,
  "gitlens.currentLine.format": "${author}, ${agoOrDate} • ${message}",
  "gitlens.currentLine.scrollable": true
}
```

#### 2. Code Lens

메서드와 클래스 위에 최근 변경 정보 표시

```java
// ▶ 홍길동, 2일 전 • 3 changes | ▶ 5 authors
public User findById(Long id) {
    return userRepository.findById(id).orElse(null);
}
```

**설정:**
```json
{
  "gitlens.codeLens.enabled": true,
  "gitlens.codeLens.authors.enabled": true,
  "gitlens.codeLens.recentChange.enabled": true
}
```

#### 3. File Annotations

**Blame Annotations:**
- `Ctrl+Shift+P` → "GitLens: Toggle File Blame"
- 각 줄의 커밋 정보를 여백에 표시

**Heatmap:**
- `Ctrl+Shift+P` → "GitLens: Toggle File Heatmap"
- 최근 변경된 줄을 색상으로 강조

#### 4. Side Bar Views

GitLens는 전용 사이드바 뷰를 제공합니다:

- **Commits**: 커밋 히스토리
- **File History**: 파일 변경 이력
- **Repositories**: 저장소 정보
- **Branches**: 브랜치 관리
- **Remotes**: 원격 저장소
- **Stashes**: Stash 목록
- **Tags**: 태그 목록

#### 5. Hover 정보

코드 위에 마우스를 올리면 Git 정보 표시:
- 커밋 메시지
- 작성자
- 날짜
- 변경 사항

### GitLens 명령

**유용한 명령들:**

```
GitLens: Show Commit Graph
GitLens: Search Commits
GitLens: Compare References
GitLens: Show Commit Details
GitLens: Open File on Remote
```

## Git History 확장

시각적인 Git 히스토리를 제공합니다.

### 설치

- Extension ID: `donjayamanne.githistory`

### 주요 기능

#### 1. Git Log 그래프

`Ctrl+Shift+P` → "Git: View History (git log)"

그래픽 로그 뷰:
- 브랜치 구조 시각화
- 커밋 메시지
- 작성자 및 날짜
- 파일 변경 통계

#### 2. 파일 히스토리

파일 우클릭 → "Git: View File History"

파일의 모든 변경 이력:
- 각 커밋에서의 변경 사항
- Diff 보기
- 이전 버전 복원

#### 3. 커밋 비교

두 커밋 또는 브랜치 간 차이점 비교:
1. `Ctrl+Shift+P` → "Git: Compare"
2. 비교할 대상 선택
3. 변경된 파일 목록 확인

#### 4. 브랜치 비교

```
Git: Compare Branches
```

현재 브랜치와 다른 브랜치의 차이점 확인

## 실전 Git 워크플로우

### Feature Branch 워크플로우

#### 1. 새 기능 개발 시작

```bash
# main 브랜치에서 최신 코드 가져오기
git checkout main
git pull origin main

# 새 기능 브랜치 생성
git checkout -b feature/user-profile
```

VS Code:
1. Status Bar의 브랜치 클릭
2. "+ Create new branch from..."
3. "main" 선택
4. "feature/user-profile" 입력

#### 2. 코드 작성 및 커밋

```bash
# 변경 사항 스테이징
git add src/components/UserProfile.jsx

# 커밋
git commit -m "feat: 사용자 프로필 컴포넌트 추가"
```

VS Code:
1. Source Control에서 변경 파일 스테이징
2. 커밋 메시지 입력
3. `Ctrl+Enter`로 커밋

#### 3. 원격 저장소에 푸시

```bash
git push -u origin feature/user-profile
```

VS Code:
- Source Control 뷰에서 "..." → "Push"

#### 4. Pull Request 생성

GitHub/GitLab/Bitbucket에서 Pull Request 생성

**GitHub Pull Requests 확장 사용:**
- Extension ID: `GitHub.vscode-pull-request-github`
- VS Code 내에서 PR 생성 및 리뷰 가능

### Gitflow 워크플로우

```
main (운영)
  ↑
release (릴리스)
  ↑
develop (개발)
  ↑ ↑ ↑
feature branches
```

## 충돌 해결

### 병합 충돌 발생 시

VS Code는 충돌을 시각적으로 표시합니다:

```javascript
<<<<<<< HEAD (Current Change)
const message = "Hello from main branch";
=======
const message = "Hello from feature branch";
>>>>>>> feature/new-feature (Incoming Change)
```

**해결 옵션:**
- Accept Current Change: 현재 브랜치 변경 사항 유지
- Accept Incoming Change: 병합할 브랜치 변경 사항 수용
- Accept Both Changes: 둘 다 유지
- Compare Changes: 변경 사항 비교

**수동 해결:**
1. 충돌 마커 제거
2. 원하는 코드로 수정
3. 파일 저장
4. 스테이징 및 커밋

### 3-Way Merge

`.vscode/settings.json`:
```json
{
  "git.mergeEditor": true
}
```

더 직관적인 병합 에디터 사용

## .gitignore 관리

### 자동 생성

프로젝트에 맞는 `.gitignore` 생성:

**Java/Spring Boot:**
```gitignore
# Compiled class files
*.class
target/
*.jar
*.war
*.ear

# IDE
.idea/
.vscode/
*.iml

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.bak
```

**Node.js/React:**
```gitignore
# Dependencies
node_modules/
package-lock.json
yarn.lock

# Build output
dist/
build/
.vite/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/

# OS
.DS_Store

# Logs
*.log
npm-debug.log*
```

### 이미 추적 중인 파일 제거

```bash
# 특정 파일
git rm --cached target/demo.jar

# 폴더
git rm -r --cached node_modules/

# 커밋
git commit -m "chore: .gitignore에 node_modules 추가"
```

## Git 설정

### 사용자 설정

```bash
# 전역 설정
git config --global user.name "홍길동"
git config --global user.email "hong@example.com"

# 프로젝트별 설정
git config user.name "홍길동"
git config user.email "hong@company.com"
```

### VS Code Git 설정

`.vscode/settings.json`:
```json
{
  // Git 활성화
  "git.enabled": true,
  
  // 자동 fetch
  "git.autofetch": true,
  
  // 동기화 확인 비활성화
  "git.confirmSync": false,
  
  // 빈 커밋 메시지 경고
  "git.requireGitUserConfig": true,
  
  // Diff 에디터
  "diffEditor.ignoreTrimWhitespace": false,
  "diffEditor.renderSideBySide": true,
  
  // 커밋 입력 검증
  "git.inputValidation": "always",
  
  // 미사용 추적 파일 자동 스테이징
  "git.enableSmartCommit": true,
  "git.smartCommitChanges": "all"
}
```

## Git 단축키

### 기본 단축키

| 단축키 | 기능 |
|--------|------|
| `Ctrl+Shift+G` | Source Control 열기 |
| `Ctrl+Enter` | 커밋 (메시지 입력 후) |
| `Ctrl+K Ctrl+H` | 변경 사항 취소 |
| `Alt+F5` | 이전 변경으로 이동 |
| `F5` | 다음 변경으로 이동 |

### 사용자 정의 단축키

`keybindings.json`:
```json
[
  {
    "key": "ctrl+alt+p",
    "command": "git.push"
  },
  {
    "key": "ctrl+alt+l",
    "command": "git.pull"
  },
  {
    "key": "ctrl+alt+f",
    "command": "git.fetch"
  }
]
```

## 고급 기능

### Stash

작업 중인 변경 사항을 임시 저장:

```bash
# Stash 저장
git stash save "작업 중인 기능"

# Stash 목록
git stash list

# Stash 적용
git stash apply stash@{0}

# Stash 적용 및 삭제
git stash pop
```

VS Code:
- Source Control에서 "..." → "Stash"

### Rebase

```bash
# 브랜치 rebase
git rebase main

# Interactive rebase
git rebase -i HEAD~3
```

### Cherry-pick

특정 커밋만 가져오기:

```bash
git cherry-pick <commit-hash>
```

VS Code:
1. Git History에서 커밋 우클릭
2. "Cherry-pick Commit" 선택

## 문제 해결

### Git이 느릴 때

```json
{
  "git.autorefresh": false,
  "git.decorations.enabled": false
}
```

수동으로 새로고침: `Ctrl+Shift+P` → "Git: Refresh"

### 자격 증명 관리

**Windows:**
```bash
git config --global credential.helper wincred
```

**macOS:**
```bash
git config --global credential.helper osxkeychain
```

### 대용량 파일 처리

Git LFS 사용:
```bash
git lfs install
git lfs track "*.psd"
git add .gitattributes
```

## 다음 단계

이론 학습을 완료했습니다! 이제 실습 Lab으로 넘어갑시다.

👉 [실습 시작하기](../02-practice/lab01-installation.md)

## 참고 자료

- [VS Code Git Integration](https://code.visualstudio.com/docs/sourcecontrol/overview)
- [GitLens Documentation](https://gitlens.amod.io/)
- [Git 공식 문서](https://git-scm.com/doc)
- [Pro Git 책](https://git-scm.com/book/ko/v2)
