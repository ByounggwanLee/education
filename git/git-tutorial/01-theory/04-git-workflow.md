# Git 작업 흐름

Git의 작업 흐름을 이해하는 것은 매우 중요합니다.

## 🔄 Git의 세 가지 상태

Git 파일은 세 가지 주요 상태를 가집니다:

```
작업 디렉토리     스테이징 영역      로컬 저장소       원격 저장소
(Working Dir)    (Staging Area)   (Local Repo)    (Remote Repo)
    📝               📦               💾              ☁️
    |                |                |               |
    |   git add      |   git commit   |   git push    |
    |--------------> |--------------> |-------------> |
    |                |                |               |
    |   수정 파일      |   커밋 대기     |   커밋된 내용   |   공유된 내용  |
```

### 1. 작업 디렉토리 (Working Directory)
- 실제로 파일을 편집하는 공간
- 프로젝트의 현재 작업 상태

### 2. 스테이징 영역 (Staging Area / Index)
- 다음 커밋에 포함될 변경사항을 준비하는 공간
- 커밋할 파일을 선택적으로 추가
- "무대에 올린다"는 의미

### 3. 로컬 저장소 (Repository)
- 커밋된 모든 변경 이력이 저장되는 곳
- `.git` 디렉토리

### 4. 원격 저장소 (Remote Repository)
- GitHub, GitLab 등 서버에 있는 저장소
- 팀원들과 코드를 공유

## 📊 파일의 상태

Git에서 파일은 다음 상태 중 하나입니다:

```
Untracked (추적 안 됨)
    ↓ git add
Tracked (추적됨)
    ├─ Unmodified (수정 안 됨)
    ├─ Modified (수정됨)
    └─ Staged (스테이징됨)
```

### Untracked (추적 안 됨)
- Git이 관리하지 않는 새 파일
- `.gitignore`에 명시된 파일

### Tracked (추적됨)
파일이 Git의 관리 대상일 때:

1. **Unmodified**: 변경사항 없음
2. **Modified**: 파일 수정됨, 아직 스테이징 안 됨
3. **Staged**: 스테이징되어 커밋 대기 중

## 🎯 기본 워크플로우

### 1단계: 저장소 초기화 또는 복제

**새 프로젝트 시작**:
```bash
git init
```

**기존 프로젝트 복제**:
```bash
git clone <저장소 URL>
```

### 2단계: 파일 작업

```bash
# 새 파일 생성 또는 기존 파일 수정
echo "Hello World" > README.md
```

### 3단계: 변경사항 스테이징

```bash
# 특정 파일 스테이징
git add README.md

# 모든 변경사항 스테이징
git add .
```

### 4단계: 커밋

```bash
# 커밋 (변경사항 저장)
git commit -m "커밋 메시지"
```

### 5단계: 원격 저장소에 푸시

```bash
# 원격 저장소로 업로드
git push origin main
```

## 🔍 상태 확인

언제든지 현재 상태를 확인할 수 있습니다:

```bash
# 작업 디렉토리 상태 확인
git status

# 변경 내용 상세 보기
git diff

# 커밋 히스토리 보기
git log
```

## 📝 실제 작업 시나리오

### 시나리오 1: 새 기능 추가

```bash
# 1. 파일 수정
echo "새 기능 코드" >> feature.js

# 2. 상태 확인
git status
# 출력: Changes not staged for commit

# 3. 스테이징
git add feature.js

# 4. 상태 재확인
git status
# 출력: Changes to be committed

# 5. 커밋
git commit -m "새 기능 추가"

# 6. 원격 저장소에 푸시
git push origin main
```

### 시나리오 2: 여러 파일 작업

```bash
# 여러 파일 수정
echo "Header" > header.html
echo "Footer" > footer.html
echo "Styles" > style.css

# 선택적으로 스테이징
git add header.html footer.html

# 커밋
git commit -m "헤더와 푸터 추가"

# 나머지 파일 추가
git add style.css
git commit -m "스타일 추가"
```

### 시나리오 3: 실수로 스테이징한 경우

```bash
# 파일을 실수로 스테이징
git add wrong_file.txt

# 스테이징 취소
git reset HEAD wrong_file.txt

# 또는 Git 2.23 이상
git restore --staged wrong_file.txt
```

## 🌊 전체 워크플로우 예시

```bash
# 1. 저장소 복제
git clone https://github.com/username/project.git
cd project

# 2. 브랜치 생성 (선택사항)
git checkout -b feature-login

# 3. 파일 작업
# ... 코드 작성 ...

# 4. 상태 확인
git status

# 5. 변경사항 스테이징
git add .

# 6. 커밋
git commit -m "로그인 기능 구현"

# 7. 원격 저장소에 푸시
git push origin feature-login

# 8. GitHub에서 Pull Request 생성
# ... 웹 브라우저에서 작업 ...

# 9. 메인 브랜치로 전환
git checkout main

# 10. 최신 변경사항 가져오기
git pull origin main
```

## ⚡ 빠른 명령어 조합

### 스테이징과 커밋 동시에

```bash
# 추적 중인 파일만 (새 파일 제외)
git commit -am "커밋 메시지"
```

### 마지막 커밋 수정

```bash
# 커밋 메시지만 수정
git commit --amend -m "새로운 커밋 메시지"

# 파일 추가하고 커밋 수정
git add forgotten_file.txt
git commit --amend --no-edit
```

## 🎨 작업 흐름 다이어그램

```
┌─────────────────────┐
│   원격 저장소 (GitHub) │
└──────────┬──────────┘
           │
    git clone/pull
           │
           ↓
┌──────────────────────┐
│    로컬 저장소 (.git)  │
└──────────┬───────────┘
           │
      git commit
           │
           ↑
┌──────────┴───────────┐
│   스테이징 영역 (Index) │
└──────────┬───────────┘
           │
       git add
           │
           ↑
┌──────────┴───────────┐
│   작업 디렉토리 (파일들) │
└──────────────────────┘
```

## 🔄 일반적인 작업 사이클

```
1. 파일 수정 (Working Directory)
    ↓
2. git status (상태 확인)
    ↓
3. git add (Staging)
    ↓
4. git status (스테이징 확인)
    ↓
5. git commit (Repository)
    ↓
6. git push (Remote)
    ↓
7. 반복...
```

## 💡 중요한 원칙

### 1. 자주 커밋하기
- 작은 단위로 자주 커밋
- 의미 있는 단위로 분리

### 2. 명확한 커밋 메시지
- 무엇을 변경했는지 명확히 작성
- 미래의 자신과 팀원을 위해

### 3. 푸시 전에 풀(pull)하기
- 충돌 방지
- 최신 상태 유지

### 4. 테스트 후 커밋
- 동작하는 코드만 커밋
- 빌드 오류가 없는지 확인

## 📋 체크리스트: 코드 작업 시

- [ ] `git status`로 현재 상태 확인
- [ ] 필요한 파일만 `git add`로 스테이징
- [ ] 의미 있는 메시지로 `git commit`
- [ ] `git push` 전에 `git pull`로 최신 상태 확인
- [ ] 충돌 발생 시 해결 후 다시 커밋

## 🚨 주의사항

### 하지 말아야 할 것

❌ 큰 바이너리 파일 커밋 (이미지, 동영상 등)
❌ 민감한 정보 커밋 (비밀번호, API 키)
❌ 의미 없는 커밋 메시지 ("수정", "커밋")
❌ 동작하지 않는 코드 커밋
❌ 여러 기능을 한 커밋에 포함

### 해야 할 것

✅ `.gitignore` 파일 작성
✅ 논리적 단위로 커밋 분리
✅ 명확한 커밋 메시지 작성
✅ 정기적으로 푸시
✅ 코드 리뷰 활용

---

**다음 단계**: 기본 명령어 배우기 (05-basic-commands.md)
