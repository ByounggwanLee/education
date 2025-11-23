# 실습 3: 브랜치 사용하기

**목표**: Git 브랜치를 생성하고 병합하는 방법을 익힙니다.

**소요 시간**: 25-30분

**난이도**: ⭐⭐ 중급

## 🎯 학습 목표

이 실습을 완료하면 다음을 할 수 있습니다:
- 브랜치 생성 및 전환
- 브랜치에서 독립적으로 작업
- Fast-forward 병합
- 3-way 병합
- 브랜치 삭제

## 📝 사전 준비

새로운 프로젝트로 시작합니다:

```bash
mkdir branch-practice
cd branch-practice
git init
echo "# Branch Practice Project" > README.md
git add README.md
git commit -m "Initial commit"
```

## 🚀 실습 단계

### 1단계: 브랜치 확인 및 이해

```bash
# 현재 브랜치 확인
git branch
```

**예상 결과**:
```
* main
```

`*` 표시는 현재 브랜치를 나타냅니다.

```bash
# 더 많은 정보 보기
git branch -v

# 커밋 이력과 함께 보기
git log --oneline --graph --all
```

### 2단계: 첫 브랜치 생성

```bash
# feature-login 브랜치 생성
git branch feature-login

# 브랜치 목록 확인
git branch
```

**예상 결과**:
```
  feature-login
* main
```

아직 main 브랜치에 있습니다 (`*`가 main에 있음).

### 3단계: 브랜치 전환

```bash
# feature-login 브랜치로 전환
git checkout feature-login

# 또는 최신 명령어
git switch feature-login

# 현재 브랜치 확인
git branch
```

**예상 결과**:
```
* feature-login
  main
```

**Tip**: 브랜치 생성과 전환을 동시에:
```bash
git checkout -b feature-signup
# 또는
git switch -c feature-signup
```

### 4단계: 브랜치에서 작업하기

```bash
# 현재 브랜치 확인 (feature-login이어야 함)
git branch

# 로그인 기능 파일 생성
echo "def login(username, password):" > login.py
echo "    # TODO: Implement login logic" >> login.py
echo "    return True" >> login.py

# 스테이징 및 커밋
git add login.py
git commit -m "Add login function skeleton"

# README 업데이트
echo "" >> README.md
echo "## Features" >> README.md
echo "- User Login" >> README.md

git add README.md
git commit -m "Update README with login feature"

# 브랜치의 커밋 이력 확인
git log --oneline
```

### 5단계: main 브랜치와 비교

```bash
# main 브랜치로 전환
git switch main

# 파일 확인
ls
cat README.md
```

**확인사항**:
- `login.py` 파일이 없음
- README.md에 "Features" 섹션이 없음

```bash
# main 브랜치의 이력
git log --oneline

# 브랜치 간 차이 확인
git log --oneline --graph --all
```

**예상 결과**:
```
* b2c3d4e (feature-login) Update README with login feature
* a1b2c3d Add login function skeleton
* 1234567 (HEAD -> main) Initial commit
```

### 6단계: Fast-forward 병합

main 브랜치에 feature-login 브랜치를 병합합니다.

```bash
# main 브랜치에 있는지 확인
git branch

# feature-login 브랜치 병합
git merge feature-login
```

**예상 결과**:
```
Updating 1234567..b2c3d4e
Fast-forward
 README.md | 3 +++
 login.py  | 3 +++
 2 files changed, 6 insertions(+)
 create mode 100644 login.py
```

**Fast-forward**란?
- main 브랜치가 그대로고 feature-login만 앞으로 나간 경우
- main을 그냥 feature-login으로 이동시킴
- 새로운 병합 커밋이 생성되지 않음

```bash
# 파일 확인
ls
cat README.md

# 이력 확인
git log --oneline --graph
```

### 7단계: 브랜치 삭제

```bash
# 병합된 브랜치 삭제
git branch -d feature-login

# 브랜치 목록 확인
git branch
```

**예상 결과**:
```
* main
```

### 8단계: 3-way 병합 실습

이번에는 main과 feature 브랜치가 모두 변경된 상황을 만듭니다.

```bash
# feature-signup 브랜치 생성 및 전환
git switch -c feature-signup

# 회원가입 기능 추가
echo "def signup(username, password, email):" > signup.py
echo "    # TODO: Implement signup logic" >> signup.py
echo "    return True" >> signup.py

git add signup.py
git commit -m "Add signup function"

# main으로 돌아가기
git switch main

# main에서도 작업
echo "## Installation" >> README.md
echo "pip install -r requirements.txt" >> README.md

git add README.md
git commit -m "Add installation instructions"

# 브랜치 상황 확인
git log --oneline --graph --all
```

**예상 결과**:
```
* c3d4e5f (HEAD -> main) Add installation instructions
| * d4e5f6g (feature-signup) Add signup function
|/
* b2c3d4e Update README with login feature
* a1b2c3d Add login function skeleton
* 1234567 Initial commit
```

### 9단계: 3-way 병합 수행

```bash
# main 브랜치에서 feature-signup 병합
git merge feature-signup
```

**예상 결과** (에디터가 열림):
```
Merge branch 'feature-signup'

# Please enter a commit message to explain why this merge is necessary
```

저장하고 닫으면:
```
Merge made by the 'recursive' strategy.
 signup.py | 3 +++
 1 file changed, 3 insertions(+)
 create mode 100644 signup.py
```

```bash
# 이력 확인
git log --oneline --graph --all
```

**예상 결과**:
```
*   e5f6g7h (HEAD -> main) Merge branch 'feature-signup'
|\
| * d4e5f6g (feature-signup) Add signup function
* | c3d4e5f Add installation instructions
|/
* b2c3d4e Update README with login feature
* a1b2c3d Add login function skeleton
* 1234567 Initial commit
```

**3-way 병합**이란?
- 두 브랜치가 각각 다른 방향으로 진행된 경우
- 공통 조상, 브랜치 A, 브랜치 B를 비교해서 병합
- 새로운 병합 커밋이 생성됨

### 10단계: 여러 브랜치 동시 작업

```bash
# 여러 기능 브랜치 생성
git switch -c feature-profile
echo "def get_profile(user_id):" > profile.py
echo "    return {}" >> profile.py
git add profile.py
git commit -m "Add profile function"

git switch main
git switch -c feature-settings
echo "def update_settings(user_id, settings):" > settings.py
echo "    pass" >> settings.py
git add settings.py
git commit -m "Add settings function"

git switch main
git switch -c bugfix-login
echo "    # Fixed: Add password validation" >> login.py
git add login.py
git commit -m "Fix login validation"

# 모든 브랜치 확인
git branch

# 전체 구조 보기
git log --oneline --graph --all
```

### 11단계: 순차적 병합

```bash
# main으로 전환
git switch main

# bugfix부터 병합 (우선순위가 높음)
git merge bugfix-login
git branch -d bugfix-login

# feature 브랜치들 병합
git merge feature-profile
git branch -d feature-profile

git merge feature-settings
git branch -d feature-settings

# 최종 상태 확인
git log --oneline --graph
git branch
```

## 🎓 핵심 명령어 정리

| 명령어 | 설명 |
|-------|-----|
| `git branch` | 브랜치 목록 확인 |
| `git branch <name>` | 새 브랜치 생성 |
| `git branch -d <name>` | 브랜치 삭제 |
| `git switch <name>` | 브랜치 전환 (최신) |
| `git switch -c <name>` | 브랜치 생성 및 전환 |
| `git checkout <name>` | 브랜치 전환 (구버전) |
| `git checkout -b <name>` | 브랜치 생성 및 전환 |
| `git merge <branch>` | 현재 브랜치에 병합 |
| `git log --graph --all` | 브랜치 그래프 보기 |

## 📊 병합 유형 비교

### Fast-forward 병합
```
main:     A → B
               ↓
feature:       B → C → D

병합 후:
main:     A → B → C → D
```

### 3-way 병합
```
main:     A → B → C
               ↓     ↘
feature:       B → D → E (merge)

병합 후:
main:     A → B → C → E (merge commit)
                  ↘   ↗
feature:            D
```

## ✅ 실습 확인

```bash
# 1. main 브랜치만 남아있어야 함
git branch

# 2. 여러 파일이 있어야 함
ls
# README.md, login.py, signup.py, profile.py, settings.py

# 3. 병합 커밋이 포함된 이력
git log --oneline --graph
```

## 💡 추가 연습

### 연습 1: 브랜치 이름 규칙 연습

```bash
git switch -c feature/user-authentication
git switch -c bugfix/login-error
git switch -c hotfix/security-patch
git branch
```

### 연습 2: 브랜치에서 여러 커밋

```bash
git switch -c feature-admin
echo "admin.py" > admin.py
git add admin.py
git commit -m "Add admin module"

echo "# Admin functions" > admin.py
git add admin.py
git commit -m "Update admin module"

git log --oneline
git switch main
```

### 연습 3: 브랜치 비교

```bash
# 두 브랜치 간 차이 확인
git diff main feature-admin

# 커밋 차이 확인
git log main..feature-admin
```

## ❓ 문제 해결

### Q: 브랜치를 삭제할 수 없어요
```bash
# 병합되지 않은 브랜치는 -d로 삭제 불가
git branch -d feature-x
# error: The branch 'feature-x' is not fully merged.

# 강제 삭제
git branch -D feature-x
```

### Q: 어느 브랜치에 있는지 모르겠어요
```bash
git branch
# 또는
git status
```

### Q: 잘못된 브랜치에서 작업했어요
```bash
# 아직 커밋 안 한 경우
git stash
git switch correct-branch
git stash pop
```

## 🎯 다음 단계

브랜치를 자유자재로 다룰 수 있게 되었습니다! 🎉

다음 실습에서는 GitHub에 코드를 올리고 원격 저장소를 사용하는 방법을 배웁니다.

➡️ **[실습 4: 원격 저장소 사용하기](./lab04-remote-repository.md)**

## 📚 관련 이론

- [Git 브랜치 관리](../01-theory/06-branching.md)
- [Git 작업 흐름](../01-theory/04-git-workflow.md)
