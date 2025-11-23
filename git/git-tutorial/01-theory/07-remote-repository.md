# 원격 저장소

원격 저장소를 통해 코드를 공유하고 협업할 수 있습니다.

## 🌐 원격 저장소란?

원격 저장소는 네트워크상의 Git 저장소입니다. GitHub, GitLab, Bitbucket 등의 플랫폼에서 호스팅됩니다.

```
로컬 저장소 (내 컴퓨터)  ↔  원격 저장소 (GitHub/GitLab)
```

## 🎯 원격 저장소의 역할

1. **백업**: 코드를 안전하게 보관
2. **협업**: 팀원들과 코드 공유
3. **배포**: CI/CD를 통한 자동 배포
4. **오픈소스**: 전 세계와 코드 공유
5. **포트폴리오**: 개발 이력 관리

## 🔗 주요 플랫폼

### GitHub
- **특징**: 가장 큰 개발자 커뮤니티
- **URL**: https://github.com
- **장점**: 오픈소스 생태계, GitHub Actions
- **무료**: 무제한 Public/Private 저장소

### GitLab
- **특징**: CI/CD 통합, 자체 호스팅 가능
- **URL**: https://gitlab.com
- **장점**: 강력한 DevOps 기능
- **무료**: 무제한 저장소, CI/CD

### Bitbucket
- **특징**: Atlassian 제품과 통합
- **URL**: https://bitbucket.org
- **장점**: Jira 통합
- **무료**: 5명까지 무료

## 📝 원격 저장소 관리

### 원격 저장소 확인

```bash
# 등록된 원격 저장소 목록
git remote

# 상세 정보 (URL 포함)
git remote -v

# 출력 예시:
# origin  https://github.com/username/repo.git (fetch)
# origin  https://github.com/username/repo.git (push)
```

### 원격 저장소 추가

```bash
# 원격 저장소 추가
git remote add origin https://github.com/username/repo.git

# 여러 원격 저장소 추가
git remote add upstream https://github.com/original/repo.git

# 확인
git remote -v
```

### 원격 저장소 URL 변경

```bash
# URL 변경
git remote set-url origin https://github.com/username/new-repo.git

# SSH로 변경
git remote set-url origin git@github.com:username/repo.git
```

### 원격 저장소 삭제

```bash
# 원격 저장소 제거
git remote remove origin

# 또는
git remote rm origin
```

### 원격 저장소 이름 변경

```bash
# origin을 upstream으로 변경
git remote rename origin upstream
```

## 📥 원격에서 가져오기

### git clone - 저장소 복제

```bash
# HTTPS로 복제
git clone https://github.com/username/repo.git

# SSH로 복제
git clone git@github.com:username/repo.git

# 특정 폴더로 복제
git clone https://github.com/username/repo.git my-folder

# 특정 브랜치만 복제
git clone -b develop https://github.com/username/repo.git

# 얕은 복제 (최근 커밋만)
git clone --depth 1 https://github.com/username/repo.git
```

### git fetch - 변경사항 가져오기 (병합 안 함)

```bash
# origin의 모든 브랜치 가져오기
git fetch origin

# 특정 브랜치만 가져오기
git fetch origin main

# 모든 원격 저장소에서 가져오기
git fetch --all

# 원격 브랜치 정보 업데이트
git fetch --prune
```

**fetch 특징**:
- 로컬 파일은 변경하지 않음
- 원격 변경사항만 확인
- 안전하게 검토 가능

### git pull - 가져오기 + 병합

```bash
# 현재 브랜치에 원격 변경사항 병합
git pull origin main

# fetch + merge와 동일
git fetch origin main
git merge origin/main

# Rebase로 가져오기
git pull --rebase origin main

# 모든 브랜치 가져오기
git pull --all
```

**pull = fetch + merge**

### fetch vs pull

```
Fetch:
로컬: A → B
       ↓
원격: A → B → C
       ↓
가져온 후:
로컬: A → B
원격: A → B → C (로컬에 저장만 됨)

Pull:
로컬: A → B → D (C와 병합)
       ↓
원격: A → B → C
```

## 📤 원격에 보내기

### git push - 원격에 업로드

```bash
# 기본 푸시
git push origin main

# 처음 푸시 시 (upstream 설정)
git push -u origin main
git push --set-upstream origin main

# 이후부터는 간단히
git push

# 모든 브랜치 푸시
git push --all origin

# 태그 푸시
git push --tags

# 특정 태그 푸시
git push origin v1.0.0

# 강제 푸시 (주의!)
git push -f origin main

# 안전한 강제 푸시
git push --force-with-lease origin main
```

### upstream 설정

```bash
# 브랜치를 원격 브랜치와 연결
git push -u origin feature-login

# 이후부터는 간단히
git push
git pull
```

### 브랜치 푸시 및 삭제

```bash
# 새 브랜치 푸시
git push origin feature-payment

# 원격 브랜치 삭제
git push origin --delete feature-payment

# 또는
git push origin :feature-payment
```

## 🌿 원격 브랜치 작업

### 원격 브랜치 확인

```bash
# 원격 브랜치 목록
git branch -r

# 모든 브랜치 (로컬 + 원격)
git branch -a

# 원격 브랜치 상세 정보
git remote show origin
```

### 원격 브랜치 체크아웃

```bash
# 원격 브랜치를 로컬로 가져오기
git checkout -b feature-login origin/feature-login

# 또는 (Git 2.23+)
git switch -c feature-login origin/feature-login

# 또는 간단히 (같은 이름으로)
git checkout feature-login
```

### 원격 브랜치 추적

```bash
# 현재 브랜치가 추적하는 원격 브랜치 확인
git branch -vv

# 출력 예시:
# * main    abc123 [origin/main] Latest commit
#   feature def456 [origin/feature: ahead 2] Feature work

# 추적 브랜치 설정
git branch --set-upstream-to=origin/main main

# 또는
git branch -u origin/main main
```

## 🔄 협업 워크플로우

### Fork & Pull Request

오픈소스 프로젝트에서 흔히 사용합니다.

**1. Fork**:
- GitHub에서 원본 저장소를 자신의 계정으로 복사

**2. Clone**:
```bash
# 자신의 Fork를 로컬로 복제
git clone https://github.com/your-username/repo.git
cd repo
```

**3. Upstream 설정**:
```bash
# 원본 저장소를 upstream으로 추가
git remote add upstream https://github.com/original/repo.git

# 확인
git remote -v
# origin    https://github.com/your-username/repo.git
# upstream  https://github.com/original/repo.git
```

**4. 브랜치 생성 및 작업**:
```bash
# 최신 코드 가져오기
git fetch upstream
git checkout main
git merge upstream/main

# 새 브랜치에서 작업
git checkout -b feature-new

# 작업 후 커밋
git add .
git commit -m "새 기능 추가"
```

**5. Push & Pull Request**:
```bash
# 자신의 Fork에 푸시
git push origin feature-new

# GitHub에서 Pull Request 생성
```

**6. 동기화 유지**:
```bash
# 주기적으로 원본 저장소와 동기화
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 공동 저장소에서 작업

팀 프로젝트에서 사용합니다.

**1. Clone**:
```bash
git clone https://github.com/team/project.git
cd project
```

**2. 브랜치에서 작업**:
```bash
# 최신 코드 가져오기
git pull origin main

# 새 브랜치 생성
git checkout -b feature-payment

# 작업 및 커밋
git add .
git commit -m "결제 기능 구현"

# 푸시
git push -u origin feature-payment
```

**3. Pull Request & 코드 리뷰**:
- GitHub/GitLab에서 PR 생성
- 팀원들이 코드 리뷰
- 필요시 수정 후 다시 푸시

**4. 병합**:
```bash
# main으로 전환
git checkout main

# 최신 상태로 업데이트
git pull origin main

# 기능 브랜치 병합
git merge --no-ff feature-payment

# 푸시
git push origin main

# 브랜치 정리
git branch -d feature-payment
git push origin --delete feature-payment
```

## 🔐 인증 방법

### HTTPS 인증

```bash
# 저장소 클론 (HTTPS)
git clone https://github.com/username/repo.git

# 푸시 시 사용자명과 비밀번호 입력 요구
# (GitHub는 Personal Access Token 사용)
```

**Personal Access Token 생성** (GitHub):
1. Settings → Developer settings → Personal access tokens
2. Generate new token
3. repo 권한 선택
4. 생성된 토큰을 비밀번호 대신 사용

### SSH 인증

```bash
# SSH 키 생성
ssh-keygen -t ed25519 -C "your.email@example.com"

# 공개키 복사 (Windows)
type %USERPROFILE%\.ssh\id_ed25519.pub

# GitHub에 SSH 키 등록
# Settings → SSH and GPG keys → New SSH key

# SSH로 클론
git clone git@github.com:username/repo.git
```

**SSH 장점**:
- 비밀번호 입력 불필요
- 더 안전
- 자동화에 유리

## 📊 원격 저장소 정보 확인

### 원격 저장소 상세 정보

```bash
# 원격 저장소의 모든 정보
git remote show origin

# 출력 예시:
# * remote origin
#   Fetch URL: https://github.com/username/repo.git
#   Push  URL: https://github.com/username/repo.git
#   HEAD branch: main
#   Remote branches:
#     main    tracked
#     develop tracked
#   Local branches configured for 'git pull':
#     main    merges with remote main
#     develop merges with remote develop
```

### 원격 브랜치와 로컬 브랜치 비교

```bash
# 로컬이 원격보다 몇 커밋 앞서/뒤처졌는지
git status

# 출력 예시:
# Your branch is ahead of 'origin/main' by 2 commits.
# Your branch is behind 'origin/main' by 1 commit.

# 상세 비교
git log origin/main..main  # 로컬이 앞선 커밋
git log main..origin/main  # 원격이 앞선 커밋
```

## 🚨 자주 발생하는 문제

### 1. Push 거부: non-fast-forward

**에러**:
```
! [rejected] main -> main (non-fast-forward)
```

**원인**: 원격에 로컬에 없는 커밋이 있음

**해결**:
```bash
# 1. pull로 원격 변경사항 병합
git pull origin main

# 2. 충돌 해결 (있다면)

# 3. 다시 푸시
git push origin main
```

### 2. 충돌 (Conflict)

**pull 시 충돌 발생**:
```bash
git pull origin main
# Auto-merging file.txt
# CONFLICT (content): Merge conflict in file.txt
```

**해결**:
```bash
# 1. 충돌 파일 확인
git status

# 2. 파일 편집 (충돌 마커 제거)
# <<<<<<< HEAD
# 내 변경사항
# =======
# 원격의 변경사항
# >>>>>>> abc123

# 3. 충돌 해결 표시
git add file.txt

# 4. 병합 완료
git commit -m "충돌 해결"

# 5. 푸시
git push origin main
```

### 3. 원격 브랜치 추적 오류

**에러**:
```
There is no tracking information for the current branch.
```

**해결**:
```bash
# 추적 브랜치 설정
git branch --set-upstream-to=origin/main main

# 또는 푸시 시 설정
git push -u origin main
```

### 4. 강제 푸시 필요

**상황**: 로컬 히스토리를 재작성한 경우

```bash
# 일반 푸시 실패
git push origin main
# ! [rejected] main -> main (non-fast-forward)

# 강제 푸시 (주의!)
git push --force-with-lease origin main
```

**주의**: 팀 작업 시 강제 푸시는 매우 조심해야 합니다!

## 💡 모범 사례

### 1. 자주 Pull하기

```bash
# 작업 시작 전
git pull origin main

# 정기적으로
git pull origin main
```

### 2. 작은 단위로 자주 Push

```bash
# 기능 완성 시마다
git push origin feature-branch
```

### 3. 브랜치에서 작업

```bash
# ❌ main에서 직접 작업
git checkout main
# ... 작업 ...

# ✅ 브랜치에서 작업
git checkout -b feature/my-work
# ... 작업 ...
```

### 4. Pull Request 활용

- 코드 리뷰 받기
- CI/CD 자동 테스트
- 팀원들과 소통

### 5. .gitignore 작성

```bash
# .gitignore 파일 생성
echo "node_modules/" >> .gitignore
echo ".env" >> .gitignore
echo "*.log" >> .gitignore
```

## 📋 원격 저장소 체크리스트

- [ ] 원격 저장소 추가 (`git remote add`)
- [ ] SSH 키 또는 Access Token 설정
- [ ] 첫 푸시 시 `-u` 옵션 사용
- [ ] 작업 전 최신 코드 pull
- [ ] 브랜치에서 작업
- [ ] Pull Request로 병합
- [ ] 병합 후 브랜치 삭제

---

**다음 단계**: 협업하기 (08-collaboration.md)
