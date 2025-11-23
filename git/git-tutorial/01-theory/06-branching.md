# Git 브랜치 관리

브랜치는 Git의 가장 강력한 기능 중 하나입니다.

## 🌿 브랜치란?

브랜치는 **독립적인 작업 공간**입니다. 메인 코드에 영향을 주지 않고 새로운 기능을 개발하거나 실험할 수 있습니다.

```
main:     O → O → O → O → O
                ↘            ↗
feature:         O → O → O
```

## 🎯 브랜치를 사용하는 이유

1. **병렬 개발**: 여러 기능을 동시에 개발
2. **안전한 실험**: 메인 코드에 영향 없이 테스트
3. **버전 관리**: 릴리스 브랜치로 버전 관리
4. **협업**: 각자의 작업 공간에서 독립적으로 작업
5. **버그 수정**: 긴급 수정을 위한 핫픽스 브랜치

## 📚 브랜치 기본 명령어

### 브랜치 목록 보기

```bash
# 로컬 브랜치 목록
git branch

# 원격 브랜치 포함
git branch -a

# 브랜치와 마지막 커밋 메시지
git branch -v

# 병합된 브랜치만
git branch --merged

# 병합 안 된 브랜치만
git branch --no-merged
```

### 브랜치 생성

```bash
# 새 브랜치 생성 (전환은 안 함)
git branch feature-login

# 특정 커밋에서 브랜치 생성
git branch feature-login abc123

# 원격 브랜치 기반으로 생성
git branch feature-login origin/develop
```

### 브랜치 전환

```bash
# 브랜치 전환 (기존 방식)
git checkout feature-login

# 브랜치 전환 (새로운 방식, Git 2.23+)
git switch feature-login

# 새 브랜치 생성하고 전환
git checkout -b feature-signup
git switch -c feature-signup  # 위와 동일

# 이전 브랜치로 전환
git checkout -
git switch -  # 위와 동일
```

### 브랜치 삭제

```bash
# 로컬 브랜치 삭제 (병합된 경우만)
git branch -d feature-login

# 강제 삭제 (병합 안 됐어도)
git branch -D feature-login

# 원격 브랜치 삭제
git push origin --delete feature-login
```

## 🔀 브랜치 병합 (Merge)

### Fast-Forward 병합

브랜치가 일직선상에 있을 때 발생합니다.

```
Before:
main:    O → O
              ↘
feature:       O → O

After:
main:    O → O → O → O
```

```bash
git checkout main
git merge feature-login
```

### 3-Way 병합

두 브랜치가 분기되었을 때 발생합니다.

```
Before:
main:    O → O → O
              ↘    ↘
feature:       O → O

After:
main:    O → O → O → M
              ↘    ↗
feature:       O → O
```

```bash
git checkout main
git merge feature-login
```

### No-Fast-Forward 병합

Fast-Forward가 가능해도 병합 커밋을 생성합니다.

```bash
git merge --no-ff feature-login
```

**사용 이유**: 브랜치 히스토리를 명확히 남기기 위해

## 🎨 브랜치 전략

### Git Flow

가장 유명한 브랜치 전략입니다.

```
main (프로덕션)
    ↓
develop (개발)
    ↓
feature/* (기능 개발)
    ↓
release/* (릴리스 준비)
    ↓
hotfix/* (긴급 수정)
```

**브랜치 설명**:

1. **main**: 프로덕션 배포용 (항상 안정적)
2. **develop**: 다음 릴리스 개발용
3. **feature/기능명**: 새 기능 개발
4. **release/버전**: 릴리스 준비
5. **hotfix/이슈**: 긴급 버그 수정

**예시**:
```bash
# 기능 개발 시작
git checkout -b feature/login develop

# 개발 완료 후 develop에 병합
git checkout develop
git merge --no-ff feature/login
git branch -d feature/login

# 릴리스 준비
git checkout -b release/1.0.0 develop

# 릴리스 완료
git checkout main
git merge --no-ff release/1.0.0
git tag -a v1.0.0

git checkout develop
git merge --no-ff release/1.0.0
```

### GitHub Flow

Git Flow보다 단순한 전략입니다.

```
main (항상 배포 가능)
    ↓
feature/* (모든 작업)
```

**워크플로우**:
1. main에서 브랜치 생성
2. 작업 후 커밋
3. Pull Request 생성
4. 코드 리뷰
5. main에 병합
6. 즉시 배포

```bash
# 작업 시작
git checkout -b feature/add-payment

# 작업 후 푸시
git push -u origin feature/add-payment

# GitHub에서 Pull Request 생성
# 리뷰 후 main에 병합
```

### Trunk-Based Development

메인 브랜치에 직접 커밋하거나 짧은 수명의 브랜치를 사용합니다.

```
main (모든 작업)
    ↓
short-lived branches (1-2일)
```

## 🔧 실전 브랜치 관리

### 브랜치 명명 규칙

**좋은 예**:
```
feature/user-authentication
feature/payment-integration
bugfix/login-error
hotfix/security-patch
release/v1.2.0
```

**나쁜 예**:
```
my-branch
test
temp
fix
```

**카테고리별 접두사**:
- `feature/`: 새 기능
- `bugfix/`: 버그 수정
- `hotfix/`: 긴급 수정
- `release/`: 릴리스
- `docs/`: 문서
- `refactor/`: 리팩토링
- `test/`: 테스트 추가

### 브랜치 작업 흐름

**1. 새 기능 개발**:
```bash
# develop에서 최신 코드 가져오기
git checkout develop
git pull origin develop

# 기능 브랜치 생성
git checkout -b feature/shopping-cart

# 작업 및 커밋
git add .
git commit -m "장바구니 기능 추가"

# 원격에 푸시
git push -u origin feature/shopping-cart

# Pull Request 생성 (GitHub/GitLab)
```

**2. 코드 리뷰 후 병합**:
```bash
# develop으로 전환
git checkout develop

# 최신 코드 가져오기
git pull origin develop

# 기능 브랜치 병합
git merge --no-ff feature/shopping-cart

# 원격에 푸시
git push origin develop

# 로컬 브랜치 삭제
git branch -d feature/shopping-cart
```

**3. 원격 브랜치 정리**:
```bash
# 원격 브랜치 삭제
git push origin --delete feature/shopping-cart

# 로컬의 원격 브랜치 참조 정리
git fetch --prune
```

## 🎯 브랜치 관리 팁

### 1. 브랜치 생명주기 짧게 유지

```bash
# ❌ 나쁜 예: 한 달 동안 작업
git checkout -b feature/everything

# ✅ 좋은 예: 작은 기능으로 분리
git checkout -b feature/login-ui
git checkout -b feature/login-validation
git checkout -b feature/login-api
```

### 2. 정기적으로 메인 브랜치 병합

```bash
# feature 브랜치에서 작업 중
git checkout feature/my-feature

# 주기적으로 develop 병합하여 충돌 최소화
git merge develop
```

### 3. 병합된 브랜치 정리

```bash
# 병합된 로컬 브랜치 목록
git branch --merged

# 일괄 삭제 (main/develop 제외)
git branch --merged | grep -v "\*\|main\|develop" | xargs -n 1 git branch -d
```

### 4. 원격 브랜치 동기화

```bash
# 삭제된 원격 브랜치 정리
git remote prune origin

# 또는
git fetch --prune
```

## 🔍 브랜치 상태 확인

### 브랜치 비교

```bash
# 두 브랜치의 차이점 보기
git diff main..feature/login

# 브랜치 간 커밋 차이
git log main..feature/login

# 그래픽으로 보기
git log --graph --oneline --all
```

### 브랜치 정보

```bash
# 브랜치의 업스트림 정보
git branch -vv

# 현재 브랜치 이름만
git branch --show-current

# 브랜치가 가리키는 커밋
git rev-parse feature/login
```

## ⚠️ 주의사항

### 1. 직접 main/develop에서 작업하지 않기

```bash
# ❌ 나쁜 예
git checkout main
# ... 직접 작업 ...
git commit -m "작업"

# ✅ 좋은 예
git checkout -b feature/my-work
# ... 작업 ...
git commit -m "작업"
```

### 2. 브랜치 전환 전 커밋 또는 스태시

```bash
# 변경사항이 있는 상태에서 브랜치 전환 시도
git checkout other-branch
# Error: Your local changes would be overwritten

# 해결 방법 1: 커밋
git add .
git commit -m "작업 중"

# 해결 방법 2: 스태시
git stash
git checkout other-branch
# ... 다른 작업 ...
git checkout original-branch
git stash pop
```

### 3. 병합 후 테스트

```bash
# 병합 후
git merge feature/login

# 테스트 실행
npm test  # 또는 적절한 테스트 명령

# 문제 없으면 푸시
git push origin develop
```

## 🛠️ 고급 기법

### 체리픽 (Cherry-pick)

특정 커밋만 가져오기:

```bash
# 다른 브랜치의 특정 커밋을 현재 브랜치에 적용
git cherry-pick abc123
```

### 브랜치 이름 변경

```bash
# 현재 브랜치 이름 변경
git branch -m new-branch-name

# 다른 브랜치 이름 변경
git branch -m old-name new-name

# 원격 브랜치도 변경
git push origin :old-name new-name
git push origin -u new-name
```

## 📊 브랜치 시각화

### 터미널에서

```bash
# 간단한 그래프
git log --graph --oneline

# 상세한 그래프
git log --graph --all --decorate --oneline

# 별칭 설정
git config --global alias.tree "log --graph --all --decorate --oneline"
git tree
```

### GUI 도구

- **gitk**: Git 기본 GUI
  ```bash
  gitk --all
  ```

- **tig**: 터미널 GUI
  ```bash
  tig
  ```

## 💡 핵심 요약

- 브랜치는 독립적인 작업 공간
- **main/develop**: 안정적인 코드
- **feature**: 새 기능 개발
- **병합 후 브랜치 삭제**로 깔끔하게 유지
- **정기적으로 메인 브랜치 병합**하여 충돌 최소화
- **명확한 브랜치 명명 규칙** 사용

---

**다음 단계**: 원격 저장소 사용하기 (07-remote-repository.md)
