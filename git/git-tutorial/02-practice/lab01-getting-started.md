# 실습 1: Git 시작하기

**목표**: Git 저장소를 만들고 첫 커밋을 생성해봅니다.

**소요 시간**: 15-20분

**난이도**: ⭐ 기초

## 🎯 학습 목표

이 실습을 완료하면 다음을 할 수 있습니다:
- Git 저장소 초기화
- 파일을 스테이징 영역에 추가
- 첫 커밋 생성
- 커밋 이력 확인

## 📝 사전 준비

```bash
# Git 설치 확인
git --version

# Git 설정 확인
git config --global user.name
git config --global user.email
```

## 🚀 실습 단계

### 1단계: 프로젝트 디렉토리 생성

```bash
# 실습용 디렉토리 생성
mkdir my-first-repo
cd my-first-repo

# 현재 위치 확인
pwd  # Unix/Mac/Git Bash
cd   # Windows CMD
```

**예상 결과**: `my-first-repo` 디렉토리가 생성되고 그 안으로 이동

### 2단계: Git 저장소 초기화

```bash
# Git 저장소로 초기화
git init
```

**예상 결과**:
```
Initialized empty Git repository in /path/to/my-first-repo/.git/
```

**확인하기**:
```bash
# .git 디렉토리 확인
ls -la  # Unix/Mac/Git Bash
dir /a  # Windows CMD
```

`.git` 폴더가 생성되었으면 성공! 이 폴더에 모든 Git 정보가 저장됩니다.

### 3단계: 첫 파일 만들기

```bash
# README.md 파일 생성
echo "# My First Git Repository" > README.md

# 파일 확인
cat README.md      # Unix/Mac/Git Bash
type README.md     # Windows CMD
```

**예상 결과**:
```
# My First Git Repository
```

### 4단계: 파일 상태 확인

```bash
git status
```

**예상 결과**:
```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        README.md

nothing added to commit but untracked files present (use "git add" to track)
```

**해석**:
- `On branch main`: 현재 main 브랜치에 있음
- `Untracked files`: Git이 아직 추적하지 않는 파일
- `README.md`: 새로 생성된 파일

### 5단계: 파일 스테이징

```bash
# README.md를 스테이징 영역에 추가
git add README.md

# 다시 상태 확인
git status
```

**예상 결과**:
```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   README.md
```

**해석**:
- `Changes to be committed`: 커밋할 준비가 된 파일
- 파일이 스테이징 영역에 추가됨 (초록색으로 표시)

### 6단계: 첫 커밋 만들기

```bash
# 커밋 생성
git commit -m "Initial commit: Add README"
```

**예상 결과**:
```
[main (root-commit) a1b2c3d] Initial commit: Add README
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
```

**해석**:
- `[main (root-commit) a1b2c3d]`: main 브랜치의 첫 커밋, 커밋 해시는 a1b2c3d
- `1 file changed`: 1개 파일 변경
- `1 insertion(+)`: 1줄 추가

### 7단계: 커밋 이력 확인

```bash
# 커밋 이력 보기
git log
```

**예상 결과**:
```
commit a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0 (HEAD -> main)
Author: Your Name <your.email@example.com>
Date:   Fri Nov 22 2025 10:00:00 +0900

    Initial commit: Add README
```

**간단하게 보기**:
```bash
git log --oneline
```

**예상 결과**:
```
a1b2c3d (HEAD -> main) Initial commit: Add README
```

### 8단계: 더 많은 파일 추가해보기

```bash
# 새 파일 생성
echo "print('Hello, Git!')" > hello.py
echo "console.log('Hello, Git!');" > hello.js

# 여러 파일 한 번에 추가
git add .

# 상태 확인
git status

# 커밋
git commit -m "Add hello.py and hello.js"

# 이력 확인
git log --oneline
```

**예상 결과**:
```
b2c3d4e (HEAD -> main) Add hello.py and hello.js
a1b2c3d Initial commit: Add README
```

## ✅ 실습 확인

다음 명령어로 실습이 제대로 완료되었는지 확인하세요:

```bash
# 1. 커밋이 2개 있어야 함
git log --oneline

# 2. 파일이 3개 있어야 함
ls          # Unix/Mac/Git Bash
dir         # Windows CMD

# 3. 작업 디렉토리가 깨끗해야 함
git status
```

**성공한 경우**:
```
On branch main
nothing to commit, working tree clean
```

## 🎓 핵심 명령어 정리

| 명령어 | 설명 |
|-------|-----|
| `git init` | 현재 디렉토리를 Git 저장소로 초기화 |
| `git status` | 파일 상태 확인 |
| `git add <file>` | 파일을 스테이징 영역에 추가 |
| `git add .` | 모든 변경사항을 스테이징 |
| `git commit -m "message"` | 커밋 생성 |
| `git log` | 커밋 이력 확인 |
| `git log --oneline` | 간단한 커밋 이력 |

## 💡 추가 연습

1. **새 파일 추가하기**
   ```bash
   echo "# Project Description" > DESCRIPTION.md
   git add DESCRIPTION.md
   git commit -m "Add project description"
   ```

2. **여러 단계로 커밋하기**
   ```bash
   echo "# License" > LICENSE
   echo "# Contributors" > CONTRIBUTORS.md
   git add LICENSE
   git commit -m "Add license file"
   git add CONTRIBUTORS.md
   git commit -m "Add contributors file"
   git log --oneline
   ```

3. **상세한 로그 보기**
   ```bash
   git log --stat
   git log --patch
   ```

## ❓ 문제 해결

### Q: "not a git repository" 오류가 나요
```bash
# 현재 디렉토리에 .git 폴더가 있는지 확인
ls -la .git

# 없다면 git init 다시 실행
git init
```

### Q: 커밋 메시지를 잘못 입력했어요
```bash
# 마지막 커밋 메시지 수정
git commit --amend -m "New commit message"
```

### Q: 파일을 잘못 스테이징했어요
```bash
# 스테이징 취소
git reset HEAD <file>
```

## 🎯 다음 단계

축하합니다! 첫 Git 저장소를 만들고 커밋을 생성했습니다! 🎉

다음 실습에서는 파일을 수정하고 변경사항을 추적하는 방법을 배웁니다.

➡️ **[실습 2: 기본 작업 흐름](./lab02-basic-workflow.md)**

## 📚 관련 이론

- [Git이란?](../01-theory/01-what-is-git.md)
- [Git 작업 흐름](../01-theory/04-git-workflow.md)
- [Git 기본 명령어](../01-theory/05-basic-commands.md)
