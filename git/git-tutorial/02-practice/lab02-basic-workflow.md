# 실습 2: 기본 작업 흐름

**목표**: 파일을 수정하고 변경사항을 추적하는 Git의 기본 작업 흐름을 익힙니다.

**소요 시간**: 20-25분

**난이도**: ⭐ 기초

## 🎯 학습 목표

이 실습을 완료하면 다음을 할 수 있습니다:
- 파일 수정 및 변경사항 확인
- 선택적으로 파일 스테이징
- 의미 있는 커밋 메시지 작성
- 파일 삭제 및 이름 변경
- 변경사항 되돌리기

## 📝 사전 준비

실습 1을 완료했거나, 아래 명령어로 시작 환경을 만듭니다:

```bash
mkdir git-workflow-practice
cd git-workflow-practice
git init
echo "# Git Workflow Practice" > README.md
git add README.md
git commit -m "Initial commit"
```

## 🚀 실습 단계

### 1단계: 파일 수정하기

```bash
# README.md에 내용 추가
echo "" >> README.md
echo "This project demonstrates Git workflow." >> README.md
echo "" >> README.md
echo "## Features" >> README.md
echo "- Version control" >> README.md
echo "- Collaboration" >> README.md

# 파일 내용 확인
cat README.md      # Unix/Mac/Git Bash
type README.md     # Windows CMD
```

**상태 확인**:
```bash
git status
```

**예상 결과**:
```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
```

### 2단계: 변경사항 자세히 보기

```bash
# 변경사항 확인
git diff
```

**예상 결과**:
```diff
diff --git a/README.md b/README.md
index 1234567..abcdefg 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,7 @@
 # Git Workflow Practice
+
+This project demonstrates Git workflow.
+
+## Features
+- Version control
+- Collaboration
```

**해석**:
- `---` : 변경 전 파일
- `+++` : 변경 후 파일
- `+` : 추가된 줄 (초록색)
- `-` : 삭제된 줄 (빨간색, 이 경우는 없음)

### 3단계: 변경사항 스테이징 및 커밋

```bash
# 스테이징
git add README.md

# 스테이징된 변경사항 확인
git diff --staged

# 커밋
git commit -m "Update README with project description"

# 이력 확인
git log --oneline
```

### 4단계: 여러 파일 동시에 작업하기

```bash
# 새 파일들 생성
echo "def greet(name):" > utils.py
echo "    return f'Hello, {name}!'" >> utils.py

echo "def add(a, b):" > math_utils.py
echo "    return a + b" >> math_utils.py

echo "# TODO List" > TODO.md
echo "- [ ] Implement feature A" >> TODO.md
echo "- [ ] Write tests" >> TODO.md

# 상태 확인
git status
```

**예상 결과**:
```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        TODO.md
        math_utils.py
        utils.py
```

### 5단계: 선택적 스테이징

일부 파일만 선택해서 커밋할 수 있습니다.

```bash
# Python 파일만 스테이징
git add *.py

# 상태 확인
git status
```

**예상 결과**:
```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   math_utils.py
        new file:   utils.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        TODO.md
```

```bash
# Python 파일들 커밋
git commit -m "Add utility functions"

# TODO.md 따로 커밋
git add TODO.md
git commit -m "Add TODO list"

# 전체 이력 확인
git log --oneline
```

### 6단계: 파일 수정 및 추적

```bash
# utils.py 수정
echo "" >> utils.py
echo "def farewell(name):" >> utils.py
echo "    return f'Goodbye, {name}!'" >> utils.py

# README.md도 수정
echo "- Easy to use" >> README.md

# 상태 확인
git status
```

**예상 결과**:
```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md
        modified:   utils.py
```

**변경사항 확인**:
```bash
# 전체 변경사항
git diff

# 특정 파일만
git diff utils.py
```

### 7단계: 부분적 스테이징 및 커밋

```bash
# utils.py만 스테이징
git add utils.py
git status

# 커밋
git commit -m "Add farewell function to utils"

# README.md 스테이징 및 커밋
git add README.md
git commit -m "Add feature to README"
```

### 8단계: 파일 이름 변경

```bash
# Git 명령어로 이름 변경
git mv math_utils.py calculator.py

# 상태 확인
git status
```

**예상 결과**:
```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        renamed:    math_utils.py -> calculator.py
```

```bash
# 커밋
git commit -m "Rename math_utils.py to calculator.py"
```

### 9단계: 파일 삭제

```bash
# Git 명령어로 파일 삭제
git rm TODO.md

# 상태 확인
git status
```

**예상 결과**:
```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        deleted:    TODO.md
```

```bash
# 커밋
git commit -m "Remove TODO.md"

# 최종 이력 확인
git log --oneline --all --graph
```

### 10단계: 변경사항 되돌리기

#### 작업 디렉토리 변경사항 취소

```bash
# README.md에 실수로 내용 추가
echo "This is a mistake" >> README.md

# 변경사항 확인
git diff README.md

# 변경사항 취소 (복구 불가능하므로 주의!)
git restore README.md

# 확인
git diff README.md
# (아무것도 표시되지 않음 = 변경사항이 없음)
```

#### 스테이징 취소

```bash
# 파일 수정
echo "print('test')" > test.py

# 스테이징
git add test.py

# 상태 확인
git status

# 스테이징 취소
git restore --staged test.py

# 상태 재확인
git status
```

**예상 결과**:
```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        test.py
```

#### 파일 삭제 후 복구

```bash
# test.py 삭제
rm test.py

# 복구 (아직 커밋 안 했으므로 불가능)
# 대신 새로 만들기
```

## 🎓 핵심 명령어 정리

| 명령어 | 설명 |
|-------|-----|
| `git diff` | 작업 디렉토리의 변경사항 확인 |
| `git diff --staged` | 스테이징된 변경사항 확인 |
| `git diff <file>` | 특정 파일의 변경사항 확인 |
| `git add <file>` | 특정 파일 스테이징 |
| `git add *.py` | 패턴에 맞는 파일 스테이징 |
| `git mv <old> <new>` | 파일 이름 변경 |
| `git rm <file>` | 파일 삭제 |
| `git restore <file>` | 작업 디렉토리 변경사항 취소 |
| `git restore --staged <file>` | 스테이징 취소 |

## 📊 작업 흐름 요약

```
[작업 디렉토리]      →(git add)→      [스테이징 영역]      →(git commit)→      [저장소]
    수정됨                                 커밋 대기                              커밋됨
      ↑                                       ↑
      |                                       |
  (git restore)                      (git restore --staged)
```

## ✅ 실습 확인

```bash
# 1. 여러 개의 커밋이 있어야 함
git log --oneline

# 2. 최소 다음 파일들이 있어야 함
ls
# README.md, utils.py, calculator.py

# 3. 작업 디렉토리가 깨끗해야 함
git status
```

## 💡 추가 연습

### 연습 1: 좋은 커밋 메시지 작성

```bash
# 새 기능 추가
echo "def multiply(a, b):" >> calculator.py
echo "    return a * b" >> calculator.py

# 상세한 커밋 메시지 (에디터 열림)
git add calculator.py
git commit
```

에디터에서:
```
Add multiply function to calculator

- Implements multiplication operation
- Takes two parameters
- Returns their product
```

### 연습 2: 여러 변경사항을 논리적으로 분리

```bash
# 두 파일 수정
echo "def subtract(a, b):" >> calculator.py
echo "    return a - b" >> calculator.py

echo "## Installation" >> README.md
echo "pip install -r requirements.txt" >> README.md

# 각각 따로 커밋
git add calculator.py
git commit -m "Add subtract function"

git add README.md
git commit -m "Add installation instructions"
```

### 연습 3: 인터랙티브 스테이징

```bash
# 파일의 일부만 스테이징 (고급)
git add -p utils.py
```

## ❓ 문제 해결

### Q: `git diff`에서 아무것도 안 보여요
```bash
# 이미 스테이징했을 수 있음
git diff --staged
```

### Q: 실수로 파일을 삭제했어요
```bash
# 아직 커밋 안 한 경우
git restore <file>

# 이미 커밋한 경우
git checkout HEAD <file>
```

### Q: 커밋을 잘못했어요
```bash
# 마지막 커밋 수정 (아직 푸시 안 한 경우)
git commit --amend
```

## 🎯 다음 단계

기본 작업 흐름을 마스터했습니다! 🎉

다음 실습에서는 브랜치를 사용해서 독립적인 작업 공간을 만드는 방법을 배웁니다.

➡️ **[실습 3: 브랜치 사용하기](./lab03-branching.md)**

## 📚 관련 이론

- [Git 작업 흐름](../01-theory/04-git-workflow.md)
- [Git 기본 명령어](../01-theory/05-basic-commands.md)
