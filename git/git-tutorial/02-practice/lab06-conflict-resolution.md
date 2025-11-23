# 실습 6: 충돌 해결하기

**목표**: Git에서 발생하는 충돌(Conflict)을 이해하고 해결하는 방법을 배웁니다.

**소요 시간**: 30-35분

**난이도**: ⭐⭐⭐ 고급

## 🎯 학습 목표

이 실습을 완료하면 다음을 할 수 있습니다:
- 충돌이 발생하는 상황 이해
- 병합 충돌 해결
- 리베이스 충돌 해결
- 충돌 해결 도구 사용
- 충돌 예방 전략

## 📝 충돌이란?

**충돌(Conflict)**은 Git이 자동으로 병합할 수 없을 때 발생합니다.

일반적인 충돌 상황:
- 같은 파일의 같은 줄을 서로 다르게 수정
- 한쪽에서 파일을 삭제하고 다른 쪽에서 수정
- 두 브랜치에서 같은 이름의 파일을 다르게 생성

## 🚀 실습 단계

### 1단계: 실습 환경 준비

```bash
# 새 프로젝트 생성
mkdir conflict-practice
cd conflict-practice
git init

# 초기 파일 생성
cat > greeting.py << 'EOF'
def greet(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("World"))
EOF

git add greeting.py
git commit -m "Initial commit with greeting function"
```

### 2단계: 충돌 상황 만들기

#### main 브랜치에서 작업
```bash
# main 브랜치에서 수정
cat > greeting.py << 'EOF'
def greet(name):
    return f"안녕하세요, {name}님!"

if __name__ == "__main__":
    print(greet("World"))
EOF

git add greeting.py
git commit -m "Change greeting to Korean"

# 현재 상태 확인
git log --oneline
```

#### feature 브랜치에서 작업
```bash
# 첫 커밋으로 돌아가서 브랜치 생성
git checkout -b feature-formal HEAD~1

# 같은 부분을 다르게 수정
cat > greeting.py << 'EOF'
def greet(name):
    return f"Good day, {name}!"

if __name__ == "__main__":
    print(greet("World"))
EOF

git add greeting.py
git commit -m "Change greeting to formal English"

# 브랜치 구조 확인
git log --oneline --graph --all
```

**예상 결과**:
```
* b2c3d4e (feature-formal) Change greeting to formal English
| * a1b2c3d (HEAD -> main) Change greeting to Korean
|/
* 1234567 Initial commit with greeting function
```

### 3단계: 충돌 발생시키기

```bash
# main 브랜치로 전환
git switch main

# feature-formal 브랜치 병합 시도
git merge feature-formal
```

**예상 결과** (충돌 발생!):
```
Auto-merging greeting.py
CONFLICT (content): Merge conflict in greeting.py
Automatic merge failed; fix conflicts and then commit the result.
```

### 4단계: 충돌 확인

```bash
# 상태 확인
git status
```

**예상 결과**:
```
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   greeting.py

no changes added to commit (use "git add" and/or "git commit -a")
```

```bash
# 충돌 내용 확인
cat greeting.py
```

**예상 결과**:
```python
def greet(name):
<<<<<<< HEAD
    return f"안녕하세요, {name}님!"
=======
    return f"Good day, {name}!"
>>>>>>> feature-formal

if __name__ == "__main__":
    print(greet("World"))
```

**충돌 마커 설명**:
- `<<<<<<< HEAD`: 현재 브랜치(main)의 내용 시작
- `=======`: 구분선
- `>>>>>>> feature-formal`: 병합하려는 브랜치의 내용 끝

### 5단계: 수동으로 충돌 해결

#### 방법 1: 텍스트 에디터로 직접 수정

```bash
# greeting.py를 다음과 같이 수정
cat > greeting.py << 'EOF'
def greet(name, language="en"):
    if language == "ko":
        return f"안녕하세요, {name}님!"
    elif language == "en-formal":
        return f"Good day, {name}!"
    else:
        return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("World"))
    print(greet("World", "ko"))
    print(greet("World", "en-formal"))
EOF

# 충돌 마커가 모두 제거되었는지 확인
cat greeting.py
```

### 6단계: 충돌 해결 완료

```bash
# 해결된 파일을 스테이징
git add greeting.py

# 상태 확인
git status
```

**예상 결과**:
```
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:
        modified:   greeting.py
```

```bash
# 병합 커밋 생성
git commit -m "Merge feature-formal: Support multiple languages"

# 이력 확인
git log --oneline --graph
```

**예상 결과**:
```
*   d4e5f6g (HEAD -> main) Merge feature-formal: Support multiple languages
|\
| * b2c3d4e (feature-formal) Change greeting to formal English
* | a1b2c3d Change greeting to Korean
|/
* 1234567 Initial commit with greeting function
```

### 7단계: 여러 파일 충돌 해결

```bash
# 새로운 시나리오
git switch -c feature-extended HEAD~1

# 여러 파일 수정
echo "# Welcome Module" > welcome.py
echo "def welcome():" >> welcome.py
echo '    return "Welcome!"' >> welcome.py

cat > greeting.py << 'EOF'
def greet(name):
    return f"Greetings, {name}!"

def farewell(name):
    return f"Goodbye, {name}!"

if __name__ == "__main__":
    print(greet("World"))
EOF

git add welcome.py greeting.py
git commit -m "Add welcome module and farewell function"

# main으로 돌아가기
git switch main

# 충돌 발생시키기
git merge feature-extended
```

**예상 결과**:
```
CONFLICT (content): Merge conflict in greeting.py
```

```bash
# 충돌 해결
cat > greeting.py << 'EOF'
def greet(name, language="en"):
    if language == "ko":
        return f"안녕하세요, {name}님!"
    elif language == "en-formal":
        return f"Good day, {name}!"
    else:
        return f"Hello, {name}!"

def farewell(name):
    return f"Goodbye, {name}!"

if __name__ == "__main__":
    print(greet("World"))
    print(greet("World", "ko"))
    print(greet("World", "en-formal"))
    print(farewell("World"))
EOF

git add greeting.py
git commit -m "Merge feature-extended: Add farewell and welcome"
```

### 8단계: VS Code를 사용한 충돌 해결

VS Code는 충돌 해결을 위한 GUI를 제공합니다.

```bash
# 새 충돌 상황 만들기
git switch -c feature-vscode HEAD~2

cat > greeting.py << 'EOF'
def greet(name):
    message = f"Hi there, {name}!"
    return message

if __name__ == "__main__":
    print(greet("World"))
EOF

git add greeting.py
git commit -m "Change greeting style"

git switch main
git merge feature-vscode
# 충돌 발생!

# VS Code로 열기
code greeting.py
```

**VS Code에서**:
- 충돌된 파일에 다음 버튼들이 표시됨:
  - `Accept Current Change`: 현재 브랜치 내용 선택
  - `Accept Incoming Change`: 병합하려는 브랜치 내용 선택
  - `Accept Both Changes`: 둘 다 포함
  - `Compare Changes`: 차이점 비교

원하는 옵션 선택 후:
```bash
git add greeting.py
git commit -m "Merge feature-vscode"
```

### 9단계: 병합 중단하기

충돌 해결이 복잡할 때는 병합을 취소할 수 있습니다.

```bash
# 새 충돌 상황
git switch -c feature-complex HEAD~1

cat > greeting.py << 'EOF'
# This is a complex change
def greet(name):
    return "This is complicated"
EOF

git add greeting.py
git commit -m "Complex change"

git switch main
git merge feature-complex
# 충돌!

# 병합 중단
git merge --abort

# 상태 확인 (원래대로 돌아감)
git status
```

### 10단계: 충돌 해결 도구 사용

```bash
# Git의 mergetool 설정
git config --global merge.tool vimdiff
# 또는
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# 충돌 발생시
git merge feature-complex

# mergetool 실행
git mergetool
```

## 🎓 충돌 해결 전략

### 1. 충돌 예방

```bash
# 자주 pull/merge 하기
git pull origin main  # 매일 또는 작업 시작 전

# 작은 단위로 커밋
# → 충돌 범위가 작아짐

# 다른 파일/모듈 작업
# → 충돌 가능성 감소
```

### 2. 충돌 최소화

```bash
# Rebase 사용 (선형 히스토리 유지)
git fetch origin
git rebase origin/main

# Feature 브랜치를 최신 상태로 유지
git switch feature-branch
git merge main  # 또는 git rebase main
```

### 3. 충돌 해결 체크리스트

```
□ 충돌 파일 모두 확인
□ 충돌 마커(<<<, ===, >>>) 모두 제거
□ 코드가 논리적으로 올바른지 확인
□ 테스트 실행
□ git add로 해결 표시
□ 커밋 완료
```

## 🎓 핵심 명령어 정리

| 명령어 | 설명 |
|-------|-----|
| `git merge <branch>` | 브랜치 병합 |
| `git merge --abort` | 병합 취소 |
| `git status` | 충돌 파일 확인 |
| `git diff` | 충돌 내용 상세 확인 |
| `git add <file>` | 충돌 해결 표시 |
| `git commit` | 병합 완료 |
| `git mergetool` | 충돌 해결 도구 실행 |
| `git log --merge` | 충돌 관련 커밋 보기 |

## 📊 충돌 해결 프로세스

```
1. 병합 시도
   ↓
2. 충돌 발생
   ↓
3. 충돌 파일 확인 (git status)
   ↓
4. 파일 편집 (충돌 해결)
   ↓
5. 충돌 마커 제거
   ↓
6. 테스트
   ↓
7. git add (해결 표시)
   ↓
8. git commit (병합 완료)
```

## ✅ 실습 확인

```bash
# 1. 충돌이 모두 해결되었는지 확인
git status
# "nothing to commit, working tree clean"

# 2. 병합 이력 확인
git log --oneline --graph --all

# 3. 코드가 정상 작동하는지 확인
python greeting.py
```

## 💡 실전 팁

### Tip 1: 충돌 미리보기
```bash
# 병합하기 전에 충돌 확인
git merge --no-commit --no-ff feature-branch
git diff --cached

# 취소
git merge --abort
```

### Tip 2: 한쪽 변경사항 전체 선택
```bash
# 충돌 시 현재 브랜치 우선
git checkout --ours greeting.py
git add greeting.py

# 또는 병합하는 브랜치 우선
git checkout --theirs greeting.py
git add greeting.py
```

### Tip 3: 충돌 히스토리 보기
```bash
git log --merge -p greeting.py
```

## 🔄 추가 연습

### 연습 1: 3-way 충돌
```bash
# 3개 브랜치에서 같은 파일 수정 후 순차 병합
git switch -c feature-1
# ... 수정 ...
git switch main
git merge feature-1

git switch -c feature-2 HEAD~1
# ... 충돌나는 수정 ...
git switch main
git merge feature-2  # 충돌!
```

### 연습 2: 바이너리 파일 충돌
```bash
# 이미지 등 바이너리 파일은 자동 병합 불가
# 한쪽을 선택해야 함
git checkout --ours image.png
# 또는
git checkout --theirs image.png
```

### 연습 3: 리베이스 충돌
```bash
git rebase main
# 충돌 발생 시
# ... 해결 ...
git add .
git rebase --continue
# 또는 중단: git rebase --abort
```

## ❓ 문제 해결

### Q: 충돌 마커를 잊고 커밋했어요
```bash
# 다시 수정
vi greeting.py  # 충돌 마커 제거
git add greeting.py
git commit --amend
```

### Q: 어느 버전이 맞는지 모르겠어요
```bash
# 양쪽 비교
git show :1:greeting.py  # 공통 조상
git show :2:greeting.py  # 현재 브랜치
git show :3:greeting.py  # 병합하는 브랜치
```

### Q: 충돌이 너무 복잡해요
```bash
# 병합 취소하고 다시 시도
git merge --abort

# 파일 단위로 선택
git checkout --ours .
# 또는
git checkout --theirs .
```

## 🎯 다음 단계

충돌 해결 방법을 마스터했습니다! 🎉

다음 실습에서는 실제 팀 프로젝트 시나리오에서 Git을 사용하는 방법을 배웁니다.

➡️ **[실습 7: 프로젝트 협업](./lab07-team-project.md)**

## 📚 관련 이론

- [Git 브랜치 관리](../01-theory/06-branching.md)
- [Git으로 협업하기](../01-theory/08-collaboration.md)
