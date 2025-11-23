# Git 기본 명령어

Git의 핵심 명령어들을 배워봅시다.

## 📁 저장소 초기화 및 복제

### git init - 새 저장소 만들기

```bash
# 현재 디렉토리를 Git 저장소로 초기화
git init

# 특정 디렉토리를 저장소로 초기화
git init my-project
```

**결과**: `.git` 폴더가 생성되며 Git 저장소가 됩니다.

### git clone - 원격 저장소 복제

```bash
# HTTPS로 복제
git clone https://github.com/username/repository.git

# SSH로 복제
git clone git@github.com:username/repository.git

# 다른 폴더 이름으로 복제
git clone https://github.com/username/repository.git my-folder

# 특정 브랜치만 복제
git clone -b develop https://github.com/username/repository.git
```

## 📊 상태 확인

### git status - 현재 상태 보기

```bash
# 상세한 상태 보기
git status

# 간단한 상태 보기
git status -s
```

**출력 예시**:
```
On branch main
Changes not staged for commit:
  modified:   file1.txt

Untracked files:
  newfile.txt
```

### git diff - 변경사항 비교

```bash
# 작업 디렉토리와 스테이징 영역 비교
git diff

# 스테이징 영역과 마지막 커밋 비교
git diff --staged
git diff --cached  # 위와 동일

# 특정 파일만 비교
git diff file1.txt

# 두 커밋 비교
git diff commit1 commit2
```

### git log - 커밋 히스토리 보기

```bash
# 기본 로그
git log

# 한 줄로 보기
git log --oneline

# 그래프로 보기
git log --graph --oneline --all

# 최근 n개 커밋만
git log -n 5

# 특정 파일의 히스토리
git log -- file1.txt

# 작성자로 필터링
git log --author="홍길동"

# 날짜로 필터링
git log --since="2024-01-01" --until="2024-12-31"
```

## 📝 기본 워크플로우 명령어

### git add - 스테이징 영역에 추가

```bash
# 특정 파일 추가
git add file1.txt

# 여러 파일 추가
git add file1.txt file2.txt

# 모든 변경사항 추가
git add .
git add -A  # 위와 동일

# 특정 패턴의 파일 추가
git add *.js

# 대화형 모드
git add -i

# 파일의 일부만 추가
git add -p file1.txt
```

### git commit - 변경사항 커밋

```bash
# 커밋 메시지와 함께 커밋
git commit -m "커밋 메시지"

# 상세한 메시지 작성 (에디터 열림)
git commit

# 스테이징과 커밋 동시에 (추적 중인 파일만)
git commit -am "커밋 메시지"

# 마지막 커밋 수정
git commit --amend -m "수정된 커밋 메시지"

# 빈 커밋 (변경사항 없이)
git commit --allow-empty -m "Empty commit"
```

**좋은 커밋 메시지 작성법**:
```
타입: 제목 (50자 이내)

본문 (선택사항, 72자마다 줄바꿈)
- 무엇을 변경했는지
- 왜 변경했는지

Fixes #123
```

**타입 예시**:
- `feat`: 새 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅
- `refactor`: 리팩토링
- `test`: 테스트 추가
- `chore`: 빌드, 설정 변경

## 🔄 변경사항 취소

### git restore - 파일 복원

```bash
# 작업 디렉토리의 변경사항 취소 (Git 2.23+)
git restore file1.txt

# 스테이징 취소
git restore --staged file1.txt

# 모든 파일 복원
git restore .
```

### git reset - 커밋 취소

```bash
# 스테이징 취소 (파일은 유지)
git reset HEAD file1.txt

# 마지막 커밋 취소 (변경사항은 유지)
git reset --soft HEAD~1

# 마지막 커밋 취소 (변경사항 스테이징 해제)
git reset --mixed HEAD~1
git reset HEAD~1  # 위와 동일 (기본값)

# 마지막 커밋 완전히 삭제 (주의!)
git reset --hard HEAD~1

# 특정 커밋으로 이동
git reset --hard commit-hash
```

**주의**: `--hard`는 변경사항을 완전히 삭제합니다!

### git revert - 안전한 커밋 취소

```bash
# 특정 커밋을 되돌리는 새 커밋 생성
git revert commit-hash

# 최근 커밋 되돌리기
git revert HEAD

# 여러 커밋 되돌리기
git revert HEAD~3..HEAD
```

**reset vs revert**:
- `reset`: 히스토리를 삭제 (로컬에서만 사용)
- `revert`: 새 커밋을 생성 (원격에서도 안전)

## 🌿 브랜치 명령어

### git branch - 브랜치 관리

```bash
# 브랜치 목록 보기
git branch

# 모든 브랜치 보기 (원격 포함)
git branch -a

# 새 브랜치 생성
git branch feature-login

# 브랜치 삭제
git branch -d feature-login

# 강제 삭제
git branch -D feature-login

# 브랜치 이름 변경
git branch -m old-name new-name
```

### git checkout - 브랜치 전환

```bash
# 기존 브랜치로 전환
git checkout feature-login

# 새 브랜치 생성하고 전환
git checkout -b feature-signup

# 이전 브랜치로 전환
git checkout -

# 특정 커밋으로 이동
git checkout commit-hash

# 특정 파일만 이전 버전으로 복원
git checkout commit-hash -- file1.txt
```

### git switch - 브랜치 전환 (Git 2.23+)

```bash
# 브랜치 전환
git switch feature-login

# 새 브랜치 생성하고 전환
git switch -c feature-signup

# 이전 브랜치로 전환
git switch -
```

### git merge - 브랜치 병합

```bash
# 현재 브랜치에 다른 브랜치 병합
git merge feature-login

# 커밋 메시지와 함께 병합
git merge feature-login -m "Login 기능 병합"

# Fast-forward 없이 병합
git merge --no-ff feature-login

# 병합 취소
git merge --abort
```

## ☁️ 원격 저장소 명령어

### git remote - 원격 저장소 관리

```bash
# 원격 저장소 목록
git remote

# 상세 정보
git remote -v

# 원격 저장소 추가
git remote add origin https://github.com/username/repo.git

# 원격 저장소 URL 변경
git remote set-url origin https://github.com/username/new-repo.git

# 원격 저장소 삭제
git remote remove origin

# 원격 저장소 이름 변경
git remote rename origin upstream
```

### git fetch - 원격 변경사항 가져오기

```bash
# 모든 원격 브랜치 정보 가져오기
git fetch origin

# 특정 브랜치만 가져오기
git fetch origin main

# 모든 원격 저장소에서 가져오기
git fetch --all
```

### git pull - 가져오기 + 병합

```bash
# 현재 브랜치에 원격 변경사항 병합
git pull origin main

# Rebase로 가져오기
git pull --rebase origin main

# 모든 원격 변경사항 가져오기
git pull --all
```

**pull = fetch + merge**

### git push - 원격에 업로드

```bash
# 원격 저장소에 푸시
git push origin main

# 현재 브랜치를 같은 이름으로 푸시
git push origin HEAD

# 새 브랜치를 원격에 푸시
git push -u origin feature-login

# 모든 브랜치 푸시
git push --all origin

# 태그 푸시
git push --tags

# 강제 푸시 (주의!)
git push -f origin main

# 안전한 강제 푸시
git push --force-with-lease origin main
```

## 🏷️ 태그 명령어

### git tag - 버전 태그

```bash
# 태그 목록
git tag

# 태그 생성 (Lightweight)
git tag v1.0.0

# 주석이 있는 태그 (Annotated)
git tag -a v1.0.0 -m "버전 1.0.0 릴리스"

# 특정 커밋에 태그
git tag v1.0.0 commit-hash

# 태그 삭제
git tag -d v1.0.0

# 원격 태그 삭제
git push origin --delete v1.0.0

# 태그 푸시
git push origin v1.0.0

# 모든 태그 푸시
git push origin --tags

# 태그 정보 보기
git show v1.0.0
```

## 🔍 검색 및 조회

### git grep - 파일 내용 검색

```bash
# 모든 파일에서 검색
git grep "검색어"

# 줄 번호 표시
git grep -n "검색어"

# 파일명만 표시
git grep -l "검색어"
```

### git show - 커밋 상세 보기

```bash
# 마지막 커밋 보기
git show

# 특정 커밋 보기
git show commit-hash

# 특정 파일의 특정 버전 보기
git show commit-hash:path/to/file
```

## 🧹 정리 명령어

### git clean - 추적되지 않는 파일 삭제

```bash
# 삭제될 파일 미리보기
git clean -n

# 파일 삭제
git clean -f

# 디렉토리까지 삭제
git clean -fd

# .gitignore 파일도 삭제
git clean -fx
```

### git gc - 저장소 최적화

```bash
# 가비지 컬렉션 실행
git gc

# 더 공격적인 최적화
git gc --aggressive
```

## 💡 유용한 조합

### 작업 흐름

```bash
# 1. 최신 코드 가져오기
git pull origin main

# 2. 새 브랜치에서 작업
git checkout -b feature-new

# 3. 작업 후 커밋
git add .
git commit -m "새 기능 추가"

# 4. 원격에 푸시
git push -u origin feature-new
```

### 실수 복구

```bash
# 스테이징 취소
git restore --staged .

# 작업 디렉토리 변경사항 취소
git restore .

# 마지막 커밋 수정
git commit --amend
```

## 📋 자주 사용하는 명령어 요약

| 명령어 | 설명 |
|--------|------|
| `git status` | 현재 상태 확인 |
| `git add .` | 모든 변경사항 스테이징 |
| `git commit -m "메시지"` | 커밋 |
| `git push` | 원격에 업로드 |
| `git pull` | 원격에서 가져오기 |
| `git checkout -b 브랜치명` | 새 브랜치 생성 및 전환 |
| `git merge 브랜치명` | 브랜치 병합 |
| `git log --oneline` | 커밋 히스토리 |
| `git diff` | 변경사항 비교 |

## 🆘 도움말

```bash
# 전체 명령어 목록
git help

# 특정 명령어 도움말
git help commit
git commit --help

# 간단한 도움말
git commit -h
```

---

**다음 단계**: 브랜치 관리 (06-branching.md)
