# 실습 4: 원격 저장소 사용하기

**목표**: GitHub에 저장소를 생성하고 로컬 저장소와 연결하여 코드를 공유합니다.

**소요 시간**: 25-30분

**난이도**: ⭐⭐ 중급

## 🎯 학습 목표

이 실습을 완료하면 다음을 할 수 있습니다:
- GitHub에 저장소 생성
- 로컬과 원격 저장소 연결
- 코드 푸시(push)
- 코드 클론(clone)
- 코드 풀(pull)
- 원격 브랜치 관리

## 📝 사전 준비

### 1. GitHub 계정
- https://github.com 에서 계정 생성
- 이메일 인증 완료

### 2. Git 설정 확인
```bash
git config --global user.name
git config --global user.email
```

이메일은 GitHub 계정과 동일해야 합니다!

### 3. 로컬 저장소 준비
```bash
mkdir remote-practice
cd remote-practice
git init
echo "# Remote Repository Practice" > README.md
git add README.md
git commit -m "Initial commit"
```

## 🚀 실습 단계

### 1단계: GitHub에 저장소 생성

#### 웹 브라우저에서:

1. **GitHub 로그인**
   - https://github.com 접속
   - 로그인

2. **새 저장소 만들기**
   - 우측 상단 `+` 클릭 → `New repository`
   - 또는 https://github.com/new 직접 접속

3. **저장소 설정**
   ```
   Repository name: remote-practice
   Description: Git remote repository practice
   Public ✓ (또는 Private)
   ✗ Add a README file (이미 로컬에 있으므로 체크 안 함)
   ✗ Add .gitignore
   ✗ Choose a license
   ```

4. **Create repository 클릭**

5. **화면에 나타난 명령어 확인**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/remote-practice.git
   git branch -M main
   git push -u origin main
   ```

### 2단계: 로컬과 원격 저장소 연결

```bash
# 원격 저장소 추가 (YOUR_USERNAME을 본인 계정으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/remote-practice.git

# 원격 저장소 확인
git remote -v
```

**예상 결과**:
```
origin  https://github.com/YOUR_USERNAME/remote-practice.git (fetch)
origin  https://github.com/YOUR_USERNAME/remote-practice.git (push)
```

**origin**이란?
- 원격 저장소의 기본 이름
- 다른 이름도 가능하지만 관례적으로 origin 사용

### 3단계: 첫 푸시(Push)

```bash
# main 브랜치로 이름 변경 (필요시)
git branch -M main

# 원격 저장소에 푸시
git push -u origin main
```

**GitHub 인증** 창이 나타나면:
- **Windows**: GitHub 로그인 창 → 로그인
- **Mac/Linux**: Token 또는 SSH 키 필요

**예상 결과**:
```
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Writing objects: 100% (3/3), 250 bytes | 250.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To https://github.com/YOUR_USERNAME/remote-practice.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**`-u` 옵션**이란?
- `--set-upstream`의 약자
- 로컬 브랜치와 원격 브랜치를 연결
- 이후부터는 `git push`만 입력해도 됨

#### 브라우저에서 확인
- GitHub 저장소 새로고침
- README.md 파일이 보여야 함

### 4단계: 추가 작업 및 푸시

```bash
# 새 파일 생성
echo "def hello():" > app.py
echo "    print('Hello, GitHub!')" >> app.py

# 커밋
git add app.py
git commit -m "Add hello function"

# 푸시 (이번엔 -u 불필요)
git push
```

**예상 결과**:
```
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 8 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 312 bytes | 312.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To https://github.com/YOUR_USERNAME/remote-practice.git
   a1b2c3d..e4f5g6h  main -> main
```

#### 브라우저에서 확인
- 새로고침하면 app.py 파일이 추가됨
- 커밋 메시지도 보임

### 5단계: 브랜치 푸시

```bash
# 새 브랜치 생성
git switch -c feature-greeting

# 작업
echo "" >> app.py
echo "def goodbye():" >> app.py
echo "    print('Goodbye!')" >> app.py

git add app.py
git commit -m "Add goodbye function"

# 브랜치 푸시
git push -u origin feature-greeting
```

**예상 결과**:
```
Total 3 (delta 1), reused 0 (delta 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
remote:
remote: Create a pull request for 'feature-greeting' on GitHub by visiting:
remote:      https://github.com/YOUR_USERNAME/remote-practice/pull/new/feature-greeting
remote:
To https://github.com/YOUR_USERNAME/remote-practice.git
 * [new branch]      feature-greeting -> feature-greeting
Branch 'feature-greeting' set up to track remote branch 'feature-greeting' from 'origin'.
```

#### 브라우저에서 확인
- 브랜치 드롭다운에서 `feature-greeting` 선택 가능
- "Compare & pull request" 버튼이 나타남

### 6단계: 저장소 클론하기

다른 위치에서 저장소를 복제해봅시다.

```bash
# 부모 디렉토리로 이동
cd ..

# 저장소 클론
git clone https://github.com/YOUR_USERNAME/remote-practice.git remote-practice-clone

# 클론된 디렉토리로 이동
cd remote-practice-clone

# 내용 확인
ls
git log --oneline
git branch -a
```

**예상 결과**:
```
* e4f5g6h (HEAD -> main, origin/main, origin/HEAD) Add hello function
* a1b2c3d Initial commit
```

**클론의 특징**:
- 전체 이력 복제
- 원격 저장소 자동 설정 (origin)
- main 브랜치만 체크아웃 (다른 브랜치는 존재하지만 안 보임)

### 7단계: 원격 브랜치 확인 및 체크아웃

```bash
# 모든 브랜치 보기 (원격 포함)
git branch -a
```

**예상 결과**:
```
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/feature-greeting
  remotes/origin/main
```

```bash
# 원격 브랜치 체크아웃
git switch feature-greeting
# 또는
git checkout -b feature-greeting origin/feature-greeting

# 확인
git branch
```

### 8단계: Pull 실습

두 개의 저장소에서 작업하는 상황을 만들어봅시다.

#### 원본 저장소에서 작업
```bash
# 원본 저장소로 돌아가기
cd ../remote-practice

# main 브랜치로 전환
git switch main

# 변경 작업
echo "## Features" >> README.md
echo "- Hello function" >> README.md

git add README.md
git commit -m "Update README with features"

# 푸시
git push
```

#### 클론 저장소에서 풀
```bash
# 클론 저장소로 이동
cd ../remote-practice-clone

# main 브랜치 확인
git switch main

# 원격 저장소의 변경사항 가져오기
git pull
```

**예상 결과**:
```
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 1), reused 3 (delta 1), pack-reused 0
Unpacking objects: 100% (3/3), done.
From https://github.com/YOUR_USERNAME/remote-practice
   e4f5g6h..f6g7h8i  main       -> origin/main
Updating e4f5g6h..f6g7h8i
Fast-forward
 README.md | 2 ++
 1 file changed, 2 insertions(+)
```

```bash
# README 확인
cat README.md
```

### 9단계: Fetch vs Pull 이해하기

```bash
# 원본 저장소에서 또 다른 변경
cd ../remote-practice
echo "- Goodbye function" >> README.md
git add README.md
git commit -m "Add goodbye to features"
git push

# 클론 저장소로 돌아가기
cd ../remote-practice-clone

# Fetch만 실행 (다운로드만, 병합은 안 함)
git fetch origin

# 로컬과 원격 비교
git log --oneline --graph --all
```

**예상 결과**:
```
* g7h8i9j (origin/main) Add goodbye to features
* f6g7h8i (HEAD -> main) Update README with features
* e4f5g6h Add hello function
* a1b2c3d Initial commit
```

```bash
# 아직 로컬에는 반영 안 됨
cat README.md

# 이제 병합
git merge origin/main
# 또는 처음부터 pull (fetch + merge)
git pull

# 확인
cat README.md
```

**Fetch vs Pull**:
- `git fetch`: 원격 변경사항 다운로드만
- `git pull`: fetch + merge (다운로드 + 병합)

### 10단계: 원격 브랜치 삭제

```bash
# 원본 저장소로 이동
cd ../remote-practice

# 로컬에서 브랜치 병합 후 삭제
git switch main
git merge feature-greeting
git push

git branch -d feature-greeting

# 원격 브랜치도 삭제
git push origin --delete feature-greeting

# 확인
git branch -a
```

#### 브라우저에서 확인
- `feature-greeting` 브랜치가 사라짐

## 🎓 핵심 명령어 정리

| 명령어 | 설명 |
|-------|-----|
| `git remote add origin <url>` | 원격 저장소 추가 |
| `git remote -v` | 원격 저장소 목록 확인 |
| `git push -u origin main` | 처음 푸시 (upstream 설정) |
| `git push` | 푸시 (upstream 설정 후) |
| `git clone <url>` | 저장소 복제 |
| `git pull` | fetch + merge |
| `git fetch` | 원격 변경사항 다운로드만 |
| `git push origin --delete <branch>` | 원격 브랜치 삭제 |
| `git branch -a` | 모든 브랜치 보기 |

## 📊 원격 저장소 작업 흐름

```
로컬 저장소                    원격 저장소 (GitHub)
[main] ─────(push)────────→ [origin/main]
  ↑                              ↓
  └────────(pull)───────────────┘
           (fetch + merge)
```

## ✅ 실습 확인

```bash
# 1. 원격 저장소 설정 확인
git remote -v

# 2. 최신 상태 확인
git status

# 3. 원격과 로컬이 동기화되었는지 확인
git log --oneline
```

브라우저에서도 확인:
- 모든 커밋이 GitHub에 표시됨
- 파일들이 정확히 표시됨

## 💡 추가 연습

### 연습 1: SSH 키 설정 (권장)

HTTPS 대신 SSH를 사용하면 매번 인증하지 않아도 됩니다.

```bash
# SSH 키 생성 (이미 있다면 생략)
ssh-keygen -t ed25519 -C "your_email@example.com"

# 공개키 복사 (Windows Git Bash)
cat ~/.ssh/id_ed25519.pub

# GitHub에 등록
# Settings → SSH and GPG keys → New SSH key
```

원격 URL 변경:
```bash
git remote set-url origin git@github.com:YOUR_USERNAME/remote-practice.git
git remote -v
```

### 연습 2: .gitignore 추가

```bash
# .gitignore 파일 생성
echo "__pycache__/" > .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
echo "venv/" >> .gitignore

git add .gitignore
git commit -m "Add .gitignore"
git push
```

### 연습 3: 여러 원격 저장소

```bash
# 다른 원격 저장소 추가 가능
git remote add backup https://github.com/ANOTHER_USER/repo.git
git remote -v
```

## ❓ 문제 해결

### Q: 푸시가 거부됩니다 (rejected)
```bash
# 원격에 새 커밋이 있는 경우
git pull --rebase origin main
git push
```

### Q: 인증 실패 (Authentication failed)
```bash
# Personal Access Token 사용 (2021년 8월 이후)
# GitHub Settings → Developer settings → Personal access tokens
# Token 생성 후 비밀번호 대신 사용
```

### Q: 원격 저장소 URL 변경
```bash
git remote set-url origin <new-url>
git remote -v
```

### Q: 로컬과 원격이 달라서 pull이 안 돼요
```bash
# 관련 없는 이력을 허용
git pull origin main --allow-unrelated-histories
```

## 🎯 다음 단계

원격 저장소 사용법을 익혔습니다! 🎉

다음 실습에서는 GitHub의 Pull Request를 사용해서 협업하는 방법을 배웁니다.

➡️ **[실습 5: Pull Request 만들기](./lab05-pull-request.md)**

## 📚 관련 이론

- [원격 저장소](../01-theory/07-remote-repository.md)
- [Git으로 협업하기](../01-theory/08-collaboration.md)
