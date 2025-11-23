# Git으로 협업하기

팀에서 Git을 효과적으로 사용하는 방법을 알아봅시다.

## 🤝 협업의 기본

Git을 사용한 협업은 다음 요소로 구성됩니다:

1. **원격 저장소**: 코드를 공유하는 중앙 저장소
2. **브랜치**: 독립적인 작업 공간
3. **Pull Request**: 코드 리뷰 및 병합 요청
4. **이슈 추적**: 버그, 기능 요청 관리
5. **커뮤니케이션**: 명확한 커밋 메시지와 문서

## 🔄 협업 워크플로우

### 중앙 집중식 워크플로우

가장 간단한 협업 방식입니다.

```
팀원 1: main → 작업 → commit → push → main
팀원 2: main → 작업 → commit → push → main
```

**장점**: 간단, 소규모 팀에 적합
**단점**: 충돌 가능성, 실험 어려움

```bash
# 1. 최신 코드 가져오기
git pull origin main

# 2. 작업 및 커밋
git add .
git commit -m "기능 추가"

# 3. 푸시
git push origin main
```

### Feature Branch 워크플로우

각 기능을 별도 브랜치에서 개발합니다.

```
main: ─────────────M──────────M──────
        ↘         ↗  ↘       ↗
         Feature A    Feature B
```

**장점**: 독립적 개발, 안전
**단점**: 브랜치 관리 필요

```bash
# 1. 기능 브랜치 생성
git checkout -b feature/user-profile

# 2. 작업 및 커밋
git add .
git commit -m "사용자 프로필 기능 추가"

# 3. 푸시
git push -u origin feature/user-profile

# 4. Pull Request 생성 (GitHub/GitLab)

# 5. 리뷰 후 병합

# 6. 로컬 업데이트
git checkout main
git pull origin main
git branch -d feature/user-profile
```

### Gitflow 워크플로우

대규모 프로젝트에 적합한 체계적인 방식입니다.

```
main (프로덕션)
    ↓
develop (개발)
    ↓
feature/* (기능)
release/* (릴리스)
hotfix/* (긴급수정)
```

**브랜치 역할**:

- **main**: 프로덕션 배포용 (항상 안정적)
- **develop**: 다음 릴리스 개발
- **feature/**: 새 기능 개발
- **release/**: 릴리스 준비
- **hotfix/**: 긴급 버그 수정

**워크플로우**:

```bash
# 새 기능 개발
git checkout develop
git pull origin develop
git checkout -b feature/shopping-cart

# 작업 후
git push -u origin feature/shopping-cart
# PR 생성 → develop에 병합

# 릴리스 준비
git checkout -b release/1.0.0 develop
# 버전 업데이트, 버그 수정
git checkout main
git merge release/1.0.0
git tag v1.0.0

git checkout develop
git merge release/1.0.0

# 긴급 수정
git checkout -b hotfix/security-patch main
# 수정 후
git checkout main
git merge hotfix/security-patch
git checkout develop
git merge hotfix/security-patch
```

### Forking 워크플로우

오픈소스 프로젝트에서 주로 사용합니다.

```
원본 저장소 (upstream)
    ↓ Fork
내 저장소 (origin)
    ↓ Clone
로컬 저장소
```

**워크플로우**:

```bash
# 1. Fork (GitHub에서 버튼 클릭)

# 2. Clone
git clone https://github.com/your-username/project.git
cd project

# 3. Upstream 설정
git remote add upstream https://github.com/original/project.git

# 4. 브랜치 생성 및 작업
git checkout -b feature/new-feature

# 5. 작업 후 푸시
git push origin feature/new-feature

# 6. Pull Request 생성 (GitHub에서)

# 7. 원본 저장소와 동기화
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## 📝 Pull Request (PR)

Pull Request는 협업의 핵심입니다.

### PR 생성 과정

**1. 브랜치에서 작업**:
```bash
git checkout -b feature/login
# 작업...
git push -u origin feature/login
```

**2. GitHub/GitLab에서 PR 생성**:
- "New Pull Request" 버튼 클릭
- 기본 브랜치 선택 (main 또는 develop)
- 제목과 설명 작성

**3. PR 설명 작성**:
```markdown
## 변경 사항
- 사용자 로그인 기능 구현
- JWT 토큰 인증 추가
- 로그인 페이지 UI 개선

## 테스트
- [ ] 단위 테스트 통과
- [ ] 통합 테스트 통과
- [ ] 브라우저 테스트 완료

## 스크린샷
![로그인 화면](screenshot.png)

## 관련 이슈
Closes #123
```

### 좋은 PR 작성법

**제목**:
```
✅ feat: 사용자 로그인 기능 추가
✅ fix: 결제 오류 수정
✅ docs: README 업데이트

❌ 수정
❌ 커밋
❌ PR
```

**설명 포함 사항**:
- 무엇을 변경했는지
- 왜 변경했는지
- 어떻게 테스트했는지
- 관련 이슈 번호

### 코드 리뷰

**리뷰어로서**:

```markdown
# 긍정적 피드백
👍 로그인 로직이 깔끔합니다!
💡 캐싱을 추가하면 성능이 개선될 것 같습니다.

# 개선 제안
❓ 이 함수는 어떤 경우에 실패하나요?
💭 이 부분은 별도 함수로 분리하는 게 좋을 것 같습니다.

# 필수 수정
⚠️ 보안 취약점: 비밀번호가 평문으로 저장됩니다.
🐛 edge case 처리가 누락되었습니다.
```

**작성자로서**:
```bash
# 피드백에 따라 수정
git add .
git commit -m "리뷰 피드백 반영: 비밀번호 암호화 추가"
git push origin feature/login
# PR이 자동으로 업데이트됨
```

### PR 병합

**병합 방법**:

1. **Merge Commit** (기본):
```
main: A → B → M
        ↘    ↗
feature:  C → D
```

2. **Squash and Merge**:
```
main: A → B → M (C+D 합쳐짐)
        ↘
feature:  C → D
```

3. **Rebase and Merge**:
```
main: A → B → C' → D'
```

**병합 후**:
```bash
# 로컬 업데이트
git checkout main
git pull origin main

# 기능 브랜치 삭제
git branch -d feature/login
git push origin --delete feature/login
```

## 🔀 충돌 해결

### 충돌이 발생하는 경우

```bash
git pull origin main
# Auto-merging file.txt
# CONFLICT (content): Merge conflict in file.txt
# Automatic merge failed; fix conflicts and then commit the result.
```

### 충돌 해결 과정

**1. 충돌 파일 확인**:
```bash
git status
# Unmerged paths:
#   both modified:   file.txt
```

**2. 파일 열어서 충돌 확인**:
```javascript
function calculateTotal(items) {
<<<<<<< HEAD
  // 내 변경사항
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
=======
  // 팀원의 변경사항
  return items.reduce((total, item) => total + item.amount, 0);
>>>>>>> abc123
}
```

**3. 충돌 해결**:
```javascript
// 두 변경사항을 모두 반영
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + (item.price * item.quantity || item.amount), 0);
}
```

**4. 해결 표시**:
```bash
git add file.txt
git commit -m "Merge conflict resolved"
git push origin feature-branch
```

### 충돌 최소화 전략

1. **자주 pull하기**:
```bash
# 작업 시작 전
git pull origin main

# 정기적으로
git pull origin develop
```

2. **작은 단위로 커밋**:
```bash
# ✅ 좋은 예
git commit -m "Add login button"
git commit -m "Add login validation"

# ❌ 나쁜 예
git commit -m "Complete entire login feature"
```

3. **파일 분리**:
```
# 같은 파일을 여러 명이 동시에 수정 → 충돌
# 파일을 모듈별로 분리 → 충돌 감소
```

4. **의사소통**:
```
팀원: "지금 auth.js 작업 중입니다"
나: "알겠습니다, 다른 파일 먼저 작업하겠습니다"
```

## 📊 이슈 관리

### 이슈 생성

```markdown
## 버그 리포트
**설명**: 로그인 시 에러 발생
**재현 방법**:
1. 로그인 페이지 접속
2. 이메일 입력
3. 로그인 버튼 클릭

**예상 결과**: 로그인 성공
**실제 결과**: 500 에러

**환경**: Chrome 120, Windows 11
**스크린샷**: [첨부]
```

### 이슈와 커밋 연결

```bash
# 이슈 번호를 커밋 메시지에 포함
git commit -m "fix: 로그인 에러 수정 (#123)"

# 이슈 자동 종료
git commit -m "fix: 로그인 에러 수정

Closes #123
Fixes #124"
```

### 이슈 레이블

- `bug`: 버그
- `feature`: 새 기능
- `enhancement`: 개선
- `documentation`: 문서
- `help wanted`: 도움 필요
- `good first issue`: 초보자용

## 🎯 협업 모범 사례

### 1. 명확한 커밋 메시지

```bash
# ❌ 나쁜 예
git commit -m "수정"
git commit -m "커밋"
git commit -m "작업"

# ✅ 좋은 예
git commit -m "feat: 사용자 프로필 페이지 추가"
git commit -m "fix: 로그인 시 세션 만료 버그 수정"
git commit -m "docs: API 문서 업데이트"
```

### 2. 작은 단위의 PR

```bash
# ❌ 나쁜 예: 1000줄 변경, 10개 파일
git diff
# +1000 -500 lines

# ✅ 좋은 예: 100줄 변경, 2-3개 파일
git diff
# +100 -50 lines
```

### 3. 정기적인 동기화

```bash
# 하루에 2-3번
git pull origin develop

# 작업 전
git pull origin develop

# 긴 작업 중
git fetch origin
git merge origin/develop
```

### 4. 브랜치 네이밍 규칙

```bash
# ✅ 좋은 예
feature/user-authentication
feature/payment-integration
bugfix/login-error
hotfix/security-patch
docs/api-documentation

# ❌ 나쁜 예
my-branch
test
temp
new-feature
```

### 5. 코드 리뷰 참여

**적극적으로**:
- 모든 PR 검토
- 건설적인 피드백
- 질문하고 배우기

**예의있게**:
- "이건 틀렸어" → "이 부분은 이렇게 하면 어떨까요?"
- "왜 이렇게 했어?" → "이렇게 구현한 이유가 궁금합니다"

## 🛠️ 협업 도구

### GitHub Features

```bash
# GitHub CLI 설치
# https://cli.github.com/

# PR 생성
gh pr create --title "로그인 기능" --body "설명"

# PR 목록
gh pr list

# PR 체크아웃
gh pr checkout 123

# PR 병합
gh pr merge 123
```

### Git Hooks

`.git/hooks/pre-commit`:
```bash
#!/bin/sh
# 커밋 전 테스트 실행
npm test
```

`.git/hooks/pre-push`:
```bash
#!/bin/sh
# 푸시 전 린트 검사
npm run lint
```

### CI/CD 통합

`.github/workflows/ci.yml`:
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: npm test
      - name: Run lint
        run: npm run lint
```

## 📋 협업 체크리스트

**작업 시작 전**:
- [ ] 최신 코드 pull
- [ ] 이슈 확인 및 할당
- [ ] 브랜치 생성

**작업 중**:
- [ ] 자주 커밋
- [ ] 명확한 커밋 메시지
- [ ] 정기적으로 동기화

**작업 완료 후**:
- [ ] 테스트 실행
- [ ] PR 생성
- [ ] 설명 작성
- [ ] 코드 리뷰 대응

**병합 후**:
- [ ] 로컬 업데이트
- [ ] 브랜치 삭제
- [ ] 이슈 종료

## 💡 팀 규칙 예시

### 커밋 메시지 규칙

```
타입(스코프): 제목

본문

관련 이슈
```

**타입**:
- `feat`: 새 기능
- `fix`: 버그 수정
- `docs`: 문서
- `style`: 포맷팅
- `refactor`: 리팩토링
- `test`: 테스트
- `chore`: 기타

### PR 규칙

- PR 크기: 500줄 이하
- 리뷰어: 최소 2명
- 승인 후 24시간 내 병합
- Squash merge 사용
- 브랜치는 작성자가 삭제

### 브랜치 규칙

- `main`: 배포용 (보호됨)
- `develop`: 개발용
- `feature/*`: 새 기능
- `bugfix/*`: 버그 수정
- `hotfix/*`: 긴급 수정

## 🚨 흔한 협업 실수

### 1. main에 직접 푸시

```bash
# ❌ 절대 하지 마세요
git checkout main
git commit -m "수정"
git push origin main

# ✅ 올바른 방법
git checkout -b feature/my-work
git commit -m "수정"
git push origin feature/my-work
# PR 생성
```

### 2. 강제 푸시 남용

```bash
# ❌ 공유 브랜치에서 절대 금지
git push -f origin main

# ✅ 자신의 feature 브랜치에서만
git push -f origin feature/my-work
```

### 3. 대용량 파일 커밋

```bash
# ❌ 나쁜 예
git add video.mp4  # 500MB

# ✅ .gitignore에 추가
echo "*.mp4" >> .gitignore
```

### 4. 민감 정보 커밋

```bash
# ❌ 절대 금지
git add .env  # API 키, 비밀번호 포함

# ✅ .gitignore에 추가
echo ".env" >> .gitignore
```

---

**다음 단계**: 실습 시작하기 (02-practice/)
