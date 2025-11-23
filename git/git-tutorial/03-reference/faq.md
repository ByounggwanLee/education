# Git FAQ (자주 묻는 질문)

Git 사용 중 자주 발생하는 질문과 답변입니다.

## 🎯 기초 개념

### Q1: Git과 GitHub의 차이는 무엇인가요?

**A:** 
- **Git**: 버전 관리 시스템 (소프트웨어)
- **GitHub**: Git 저장소 호스팅 서비스 (웹사이트)

```
Git (로컬)          GitHub (원격)
  저장소    ←→    저장소 + 협업 기능
                  (PR, Issues, Wiki 등)
```

비유: Git은 문서 작성 프로그램, GitHub는 구글 드라이브

### Q2: Commit, Push, Pull의 차이가 뭔가요?

**A:**
- **Commit**: 로컬 저장소에 변경사항 저장
- **Push**: 로컬 → 원격으로 업로드
- **Pull**: 원격 → 로컬로 다운로드 + 병합

```bash
# 작업 흐름
git add .           # 스테이징
git commit -m "msg" # 로컬에 저장
git push            # 원격에 업로드

# 다른 컴퓨터나 팀원의 변경사항 가져오기
git pull            # 원격에서 다운로드 + 병합
```

### Q3: HEAD가 무엇인가요?

**A:** HEAD는 현재 체크아웃된 커밋을 가리키는 포인터입니다.

```bash
# 보통은 브랜치를 가리킴
HEAD → main → 최신 커밋

# 특정 커밋을 체크아웃하면 "detached HEAD"
HEAD → 특정 커밋
```

## 📝 커밋 관련

### Q4: 좋은 커밋 메시지는 어떻게 작성하나요?

**A:** 

```bash
# ✅ 좋은 예
git commit -m "Add user authentication feature"
git commit -m "Fix memory leak in data processor"
git commit -m "Update README with installation steps"

# ❌ 나쁜 예
git commit -m "fix"
git commit -m "update"
git commit -m "various changes"
```

**작성 규칙**:
1. 첫 줄은 50자 이내로 요약
2. 동사로 시작 (Add, Fix, Update, Remove 등)
3. 현재형 사용 ("Added" ❌, "Add" ✅)
4. 상세 설명이 필요하면 빈 줄 후 추가

```bash
# 상세 커밋 메시지
git commit -m "Add user authentication

- Implement JWT-based authentication
- Add login and registration endpoints
- Include password hashing with bcrypt
- Add tests for auth endpoints"
```

### Q5: 마지막 커밋을 수정하고 싶어요

**A:**

```bash
# 커밋 메시지만 수정
git commit --amend -m "New message"

# 파일을 추가하고 싶을 때
git add forgotten_file.txt
git commit --amend --no-edit

# ⚠️ 주의: 이미 푸시한 커밋은 수정하면 안 됨!
```

### Q6: 여러 커밋을 하나로 합치고 싶어요

**A:**

```bash
# 최근 3개 커밋 합치기
git rebase -i HEAD~3

# 에디터에서:
pick abc1234 First commit
squash def5678 Second commit
squash ghi9012 Third commit

# 저장 후 커밋 메시지 수정
```

## 🌿 브랜치 관련

### Q7: 브랜치를 언제 만들어야 하나요?

**A:** 

- ✅ 새 기능 개발
- ✅ 버그 수정
- ✅ 실험적인 코드
- ✅ 코드 리뷰가 필요한 작업

```bash
# Feature
git switch -c feature/user-profile

# Bugfix
git switch -c bugfix/login-error

# Hotfix
git switch -c hotfix/security-patch

# Experiment
git switch -c experiment/new-algorithm
```

### Q8: 잘못된 브랜치에서 작업했어요!

**A:**

```bash
# 아직 커밋하지 않은 경우
git stash
git switch correct-branch
git stash pop

# 이미 커밋한 경우
git log --oneline  # 커밋 해시 확인
git switch correct-branch
git cherry-pick <commit-hash>

# 원래 브랜치에서 커밋 제거 (선택사항)
git switch wrong-branch
git reset --hard HEAD~1
```

### Q9: 브랜치 이름을 변경하고 싶어요

**A:**

```bash
# 로컬 브랜치 이름 변경
git branch -m old-name new-name

# 현재 브랜치 이름 변경
git branch -m new-name

# 원격 브랜치도 변경
git push origin :old-name new-name
git push origin -u new-name
```

## 🔄 병합 및 충돌

### Q10: Fast-forward와 3-way merge의 차이는?

**A:**

**Fast-forward**:
```
main:     A → B
               ↓
feature:       B → C → D

병합 후:  A → B → C → D (main)
```

**3-way merge**:
```
main:     A → B → C
               ↓     ↘
feature:       B → D → M (merge commit)

병합 후:  A → B → C → M (main)
                  ↘   ↗
                    D
```

```bash
# Fast-forward 방지 (명시적 병합 커밋 생성)
git merge --no-ff feature-branch
```

### Q11: 충돌이 무서워요. 어떻게 하나요?

**A:** 충돌은 자연스러운 현상입니다! 단계별로 해결하세요.

```bash
# 1. 충돌 확인
git status

# 2. 충돌 파일 열기
code conflicted_file.py

# 3. 충돌 마커 찾기
<<<<<<< HEAD
현재 브랜치의 코드
=======
병합하려는 브랜치의 코드
>>>>>>> feature-branch

# 4. 마커 제거하고 올바른 코드 작성
원하는 최종 코드

# 5. 해결 표시
git add conflicted_file.py

# 6. 병합 완료
git commit
```

**팁**: 충돌 예방법
```bash
# 자주 pull/merge 하기
git pull origin main  # 매일

# 작은 단위로 자주 커밋
# 다른 파일에서 작업하기
```

### Q12: 병합을 취소하고 싶어요

**A:**

```bash
# 병합 진행 중 (충돌 해결 전)
git merge --abort

# 병합 완료 후 (아직 푸시 안 함)
git reset --hard HEAD~1

# 이미 푸시한 경우
git revert -m 1 <merge-commit-hash>
git push
```

## 🔙 되돌리기

### Q13: reset과 revert의 차이는?

**A:**

**reset**: 커밋을 제거 (이력 변경)
```bash
git reset --hard HEAD~1  # 마지막 커밋 삭제
# ⚠️ 푸시한 커밋에는 사용 금지!
```

**revert**: 새 커밋으로 되돌리기 (이력 보존)
```bash
git revert HEAD          # 새 커밋 생성
# ✅ 푸시한 커밋에도 안전
```

```
Reset:
A → B → C → D
        ↑ (reset 후 D 사라짐)

Revert:
A → B → C → D → E (D를 되돌리는 커밋)
```

### Q14: 파일을 실수로 삭제했어요

**A:**

```bash
# 아직 커밋 안 한 경우
git restore deleted_file.txt

# 이미 커밋한 경우
git checkout HEAD deleted_file.txt

# 특정 커밋에서 복구
git checkout <commit-hash> deleted_file.txt

# 모든 삭제된 파일 복구
git restore .
```

### Q15: 잘못 수정한 파일을 되돌리고 싶어요

**A:**

```bash
# 작업 디렉토리 변경 취소 (아직 add 안 함)
git restore file.txt

# 스테이징 취소 (add 했지만 commit 안 함)
git restore --staged file.txt

# 이전 커밋 상태로 복구
git checkout HEAD file.txt
```

## 📤 원격 저장소

### Q16: Push가 거부됩니다 (rejected)

**A:**

```bash
# 오류 메시지
! [rejected] main -> main (non-fast-forward)

# 원인: 원격에 새 커밋이 있음

# 해결책 1: Pull 후 Push
git pull --rebase origin main
git push

# 해결책 2: Merge 후 Push
git pull origin main
git push

# ⚠️ 강제 푸시 (주의!)
git push --force  # 혼자 사용하는 브랜치만!
```

### Q17: 대용량 파일을 푸시할 수 없어요

**A:**

```bash
# GitHub는 100MB 이상 파일 제한

# 해결책 1: .gitignore에 추가
echo "large_file.zip" >> .gitignore
git rm --cached large_file.zip

# 해결책 2: Git LFS 사용
git lfs install
git lfs track "*.zip"
git add .gitattributes
git add large_file.zip
git commit -m "Add large file with LFS"
git push

# 해결책 3: 이미 푸시한 경우 (이력에서 제거)
git filter-branch --tree-filter 'rm -f large_file.zip' HEAD
```

### Q18: 원격 브랜치를 로컬로 가져오고 싶어요

**A:**

```bash
# 원격 브랜치 확인
git branch -r

# 원격 브랜치 체크아웃
git switch feature-branch
# 또는
git checkout -b feature-branch origin/feature-branch

# 모든 원격 브랜치 가져오기
git fetch --all
```

## 🔒 인증 및 보안

### Q19: 매번 비밀번호를 입력해야 하나요?

**A:**

```bash
# SSH 키 사용 (권장)
# 1. SSH 키 생성
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. 공개키 복사
cat ~/.ssh/id_ed25519.pub

# 3. GitHub Settings → SSH keys에 추가

# 4. 원격 URL 변경
git remote set-url origin git@github.com:username/repo.git

# Personal Access Token 사용
# GitHub Settings → Developer settings → Personal access tokens
# 비밀번호 대신 토큰 사용
```

### Q20: .env 파일을 실수로 커밋했어요!

**A:**

```bash
# 1. 파일 제거 (추적만 제거, 파일은 유지)
git rm --cached .env

# 2. .gitignore에 추가
echo ".env" >> .gitignore

# 3. 커밋
git add .gitignore
git commit -m "Remove .env from tracking"

# 4. 푸시
git push

# ⚠️ 이미 푸시된 민감 정보는 이력에 남음!
# GitHub → Settings → Secrets 재생성 필요!

# 이력에서 완전히 제거 (고급)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env' \
  --prune-empty --tag-name-filter cat -- --all
```

## 🛠️ 작업 환경

### Q21: 여러 컴퓨터에서 작업하고 싶어요

**A:**

```bash
# 컴퓨터 A
git push origin main

# 컴퓨터 B
git pull origin main
# ... 작업 ...
git push origin main

# 컴퓨터 A
git pull origin main

# 💡 Tip: 항상 작업 시작 전 pull!
```

### Q22: 팀원과 같은 브랜치에서 작업하고 있어요

**A:**

```bash
# 작업 시작 전
git pull origin feature-branch

# 작업 후
git push origin feature-branch

# 충돌 발생 시
git pull --rebase origin feature-branch
# ... 충돌 해결 ...
git push origin feature-branch

# 💡 Tip: 자주 push/pull하고 소통하기!
```

### Q23: 임시로 다른 브랜치로 전환하고 싶어요

**A:**

```bash
# 현재 작업을 임시 저장
git stash save "WIP: working on feature"

# 다른 브랜치로 전환
git switch other-branch
# ... 작업 ...

# 원래 브랜치로 돌아오기
git switch original-branch
git stash pop

# 스태시 목록 보기
git stash list
```

## 🐛 디버깅

### Q24: 버그가 언제 생겼는지 찾고 싶어요

**A:**

```bash
# Git Bisect 사용
git bisect start
git bisect bad              # 현재는 버그 있음
git bisect good <commit>    # 과거 정상 지점

# Git이 중간 커밋으로 이동
# 테스트 후:
git bisect good  # 또는 bad

# 반복하면 버그 발생 커밋을 찾아줌
git bisect reset  # 종료
```

### Q25: 누가 이 코드를 작성했는지 알고 싶어요

**A:**

```bash
# 파일의 각 줄 작성자 확인
git blame file.py

# 특정 줄 범위만
git blame -L 10,20 file.py

# 더 자세한 정보
git log -p file.py

# 특정 함수 변경 이력
git log -L :function_name:file.py
```

## 📚 고급 질문

### Q26: Rebase와 Merge 중 무엇을 써야 하나요?

**A:**

**Merge** (일반적으로 추천):
```bash
git merge feature-branch
# 장점: 안전, 이력 보존
# 단점: 복잡한 이력
```

**Rebase** (선형 이력 선호 시):
```bash
git rebase main
# 장점: 깔끔한 선형 이력
# 단점: 이력 변경 (위험할 수 있음)
```

**규칙**:
- ✅ 로컬 브랜치: Rebase 사용 가능
- ❌ 공개 브랜치: Rebase 금지!
- ✅ 협업: Merge 권장

### Q27: Submodule이 뭔가요?

**A:**

```bash
# 다른 Git 저장소를 서브디렉토리로 포함
git submodule add https://github.com/user/repo.git libs/repo

# 클론 시 서브모듈 포함
git clone --recursive <url>

# 서브모듈 업데이트
git submodule update --remote
```

### Q28: Git 이력을 깔끔하게 유지하는 방법은?

**A:**

```bash
# 1. 작은 단위로 자주 커밋
git add specific_file.py
git commit -m "Add specific feature"

# 2. Squash merge 사용 (PR)
# GitHub에서 "Squash and merge"

# 3. 의미 없는 커밋 합치기
git rebase -i HEAD~5

# 4. 좋은 커밋 메시지 작성
# 5. Feature branch 정리
git branch -d merged-branch
```

## 🆘 긴급 상황

### Q29: 모든 것을 망쳤어요! 되돌릴 수 있나요?

**A:**

```bash
# Git은 거의 모든 것을 복구 가능!

# 1. Reflog 확인 (모든 HEAD 이동 기록)
git reflog

# 2. 원하는 시점 찾기
git reflog
# abc1234 HEAD@{5}: commit: Good state

# 3. 그 시점으로 복구
git reset --hard abc1234

# 또는 브랜치 생성
git branch recovery abc1234
```

### Q30: 강제 푸시로 코드가 사라졌어요!

**A:**

```bash
# 1. Reflog 확인
git reflog

# 2. 사라진 커밋 찾기
git reflog
# def5678 HEAD@{10}: commit: Lost commit

# 3. 복구
git cherry-pick def5678

# 또는 리셋
git reset --hard def5678

# 💡 서버에 백업이 있다면 팀원에게 요청!
```

## 💡 베스트 프랙티스

### 커밋 전 체크리스트
- [ ] 관련된 변경사항만 포함
- [ ] 테스트 실행 및 통과
- [ ] 의미 있는 커밋 메시지
- [ ] 큰 파일/민감 정보 제외

### Pull Request 전 체크리스트
- [ ] 최신 main 브랜치와 동기화
- [ ] 충돌 해결 완료
- [ ] 코드 리뷰 준비
- [ ] 테스트 및 문서 업데이트

### 협업 시 주의사항
- 항상 작업 시작 전 `git pull`
- 공개 브랜치에 `--force` 금지
- 민감 정보는 `.env`에 분리
- 자주 커밋하고 푸시하기

---

**더 궁금한 점이 있나요?**

- 📖 [공식 문서](https://git-scm.com/doc)
- 💬 [Stack Overflow](https://stackoverflow.com/questions/tagged/git)
- 📚 [Pro Git 책](https://git-scm.com/book)
