# Git 치트시트 (Cheat Sheet)

Git 명령어를 빠르게 참조할 수 있는 요약본입니다.

## 🎯 설정 (Configuration)

```bash
# 사용자 정보 설정
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 설정 확인
git config --list
git config user.name
git config user.email

# 에디터 설정
git config --global core.editor "code --wait"

# 별칭 설정
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.lg "log --oneline --graph --all"
```

## 📁 저장소 초기화 (Repository)

```bash
# 새 저장소 생성
git init

# 원격 저장소 복제
git clone <url>
git clone <url> <directory>
git clone -b <branch> <url>  # 특정 브랜치만

# 원격 저장소 관리
git remote add origin <url>
git remote -v
git remote remove <name>
git remote rename <old> <new>
```

## 📊 상태 확인 (Status)

```bash
# 현재 상태
git status
git status -s        # 짧게

# 변경사항 확인
git diff             # 작업 디렉토리 vs 스테이징
git diff --staged    # 스테이징 vs 저장소
git diff HEAD        # 작업 디렉토리 vs 저장소
git diff <branch1> <branch2>  # 브랜치 비교
git diff <commit1> <commit2>  # 커밋 비교

# 로그 확인
git log
git log --oneline
git log --graph --all
git log --stat
git log -p           # 패치 포함
git log -n 5         # 최근 5개
git log --since="2 weeks ago"
git log --author="Name"
git log --grep="keyword"
git log <file>       # 특정 파일 이력
```

## ➕ 파일 추가 및 커밋 (Add & Commit)

```bash
# 스테이징
git add <file>
git add .            # 모든 변경사항
git add *.py         # 패턴 매칭
git add -p           # 대화형 스테이징

# 스테이징 취소
git restore --staged <file>
git reset HEAD <file>    # 구버전

# 커밋
git commit -m "message"
git commit -am "message"  # add + commit (추적 중인 파일만)
git commit --amend        # 마지막 커밋 수정
git commit --amend -m "new message"

# 작업 디렉토리 변경 취소
git restore <file>
git checkout -- <file>    # 구버전
```

## 🌿 브랜치 (Branching)

```bash
# 브랜치 목록
git branch
git branch -a        # 원격 포함
git branch -v        # 마지막 커밋 포함

# 브랜치 생성
git branch <name>
git branch <name> <commit>  # 특정 커밋에서

# 브랜치 전환
git switch <branch>
git switch -c <branch>       # 생성 + 전환
git checkout <branch>        # 구버전
git checkout -b <branch>     # 구버전 생성 + 전환

# 브랜치 삭제
git branch -d <branch>       # 병합된 브랜치만
git branch -D <branch>       # 강제 삭제

# 브랜치 이름 변경
git branch -m <old> <new>
git branch -m <new>          # 현재 브랜치
```

## 🔀 병합 (Merging)

```bash
# 병합
git merge <branch>
git merge --no-ff <branch>   # Fast-forward 방지
git merge --squash <branch>  # 커밋 하나로 압축

# 병합 취소
git merge --abort

# 충돌 해결
git status                   # 충돌 파일 확인
# ... 파일 수정 ...
git add <file>
git commit

# 충돌 시 선택
git checkout --ours <file>   # 현재 브랜치 선택
git checkout --theirs <file> # 병합 브랜치 선택
```

## 🔄 원격 저장소 (Remote)

```bash
# 가져오기
git fetch origin
git fetch --all

# 풀 (fetch + merge)
git pull
git pull origin main
git pull --rebase            # 리베이스로 풀

# 푸시
git push
git push origin main
git push -u origin main      # upstream 설정
git push --all               # 모든 브랜치
git push --tags              # 모든 태그

# 원격 브랜치 삭제
git push origin --delete <branch>

# 원격 브랜치 추적
git branch --set-upstream-to=origin/<branch>
git branch -u origin/<branch>
```

## ⏮️ 되돌리기 (Undo)

```bash
# 작업 디렉토리 변경 취소
git restore <file>
git checkout -- <file>       # 구버전

# 스테이징 취소
git restore --staged <file>
git reset HEAD <file>        # 구버전

# 커밋 되돌리기
git reset --soft HEAD~1      # 커밋만 취소 (변경사항 유지)
git reset --mixed HEAD~1     # 커밋 + 스테이징 취소 (기본)
git reset --hard HEAD~1      # 모두 취소 (주의!)
git reset --hard <commit>    # 특정 커밋으로

# 커밋 되돌리기 (새 커밋 생성)
git revert <commit>
git revert HEAD
git revert HEAD~3..HEAD      # 범위 지정

# 특정 파일만 복구
git checkout <commit> -- <file>
git restore --source=<commit> <file>
```

## 🏷️ 태그 (Tagging)

```bash
# 태그 목록
git tag
git tag -l "v1.*"

# 태그 생성
git tag <tagname>
git tag <tagname> <commit>
git tag -a v1.0 -m "Version 1.0"  # Annotated tag

# 태그 보기
git show <tagname>

# 태그 삭제
git tag -d <tagname>
git push origin --delete <tagname>  # 원격

# 태그 푸시
git push origin <tagname>
git push origin --tags           # 모든 태그
```

## 📦 Stash (임시 저장)

```bash
# 스태시 저장
git stash
git stash save "message"
git stash -u              # untracked 파일 포함

# 스태시 목록
git stash list

# 스태시 적용
git stash apply           # 최근 stash
git stash apply stash@{n}
git stash pop             # apply + drop

# 스태시 삭제
git stash drop stash@{n}
git stash clear           # 모두 삭제

# 스태시 브랜치로
git stash branch <branch>
```

## 🔍 검색 및 조회

```bash
# 커밋 검색
git log --grep="keyword"
git log --author="name"
git log -S"function_name"    # 코드 검색

# 파일 검색
git grep "keyword"
git grep -n "keyword"        # 줄 번호 포함

# 누가 수정했나
git blame <file>
git blame -L 10,20 <file>    # 특정 줄

# 특정 커밋 보기
git show <commit>
git show <commit>:<file>     # 특정 파일
```

## 🧹 정리 (Cleanup)

```bash
# 추적되지 않는 파일 확인
git clean -n

# 추적되지 않는 파일 삭제
git clean -f
git clean -fd             # 디렉토리 포함
git clean -fx             # ignored 파일 포함

# 원격에서 삭제된 브랜치 정리
git remote prune origin
git fetch -p              # fetch + prune

# 가비지 컬렉션
git gc
git gc --aggressive
```

## 🔧 고급 명령어

```bash
# Rebase
git rebase <branch>
git rebase -i HEAD~3         # Interactive rebase
git rebase --continue
git rebase --abort

# Cherry-pick
git cherry-pick <commit>
git cherry-pick <commit1> <commit2>

# Bisect (이진 탐색)
git bisect start
git bisect bad               # 현재는 bad
git bisect good <commit>     # 과거 good 지점
# ... 테스트 후 good/bad 표시 반복 ...
git bisect reset

# Reflog (참조 로그)
git reflog
git reflog show <branch>

# Submodules
git submodule add <url>
git submodule init
git submodule update
```

## 🛠️ 유용한 조합

```bash
# 마지막 커밋 메시지 수정
git commit --amend -m "New message"

# 마지막 커밋에 파일 추가
git add forgotten_file
git commit --amend --no-edit

# 특정 파일만 다른 브랜치에서 가져오기
git checkout <branch> -- <file>

# 특정 커밋의 파일 보기
git show <commit>:<file>

# 모든 브랜치의 이력 보기
git log --oneline --graph --all --decorate

# 파일 이름 변경 (Git 추적 유지)
git mv <old> <new>

# 파일 삭제 (Git 추적 제거)
git rm <file>
git rm --cached <file>       # 파일은 유지, 추적만 제거

# 대화형 스테이징
git add -i
git add -p

# 임시 커밋 (작업 중 저장)
git commit -m "WIP: work in progress"
```

## 📋 .gitignore 패턴

```bash
# 기본 패턴
*.log                # 모든 .log 파일
!important.log       # 제외 (important.log는 추적)
/TODO                # 루트의 TODO만
build/               # build 디렉토리
doc/*.txt            # doc의 txt (하위 제외)
doc/**/*.pdf         # doc의 모든 pdf (하위 포함)

# 일반적인 패턴
__pycache__/
*.pyc
.env
node_modules/
.DS_Store
.vscode/
*.swp
```

## 🎨 Git 별칭 (Aliases)

```bash
# 유용한 별칭들
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.last 'log -1 HEAD'
git config --global alias.unstage 'restore --staged'
git config --global alias.visual 'log --oneline --graph --all --decorate'
git config --global alias.amend 'commit --amend --no-edit'
```

## 🚀 Git 플로우

### Feature Branch 플로우
```bash
# 1. 최신 main 가져오기
git checkout main
git pull origin main

# 2. Feature 브랜치 생성
git checkout -b feature/new-feature

# 3. 작업 및 커밋
git add .
git commit -m "Add new feature"

# 4. 푸시
git push -u origin feature/new-feature

# 5. PR 생성 (GitHub에서)

# 6. 병합 후 정리
git checkout main
git pull origin main
git branch -d feature/new-feature
```

### Hotfix 플로우
```bash
# 1. Hotfix 브랜치 생성
git checkout -b hotfix/critical-bug main

# 2. 수정 및 커밋
git add .
git commit -m "Fix critical bug"

# 3. main에 병합
git checkout main
git merge hotfix/critical-bug
git push origin main

# 4. develop에도 병합 (있다면)
git checkout develop
git merge hotfix/critical-bug
git push origin develop

# 5. 정리
git branch -d hotfix/critical-bug
```

## 🆘 긴급 상황

```bash
# 실수로 변경사항을 잃어버렸을 때
git reflog
git checkout <commit>

# 잘못된 병합을 되돌리고 싶을 때
git reset --hard ORIG_HEAD

# 푸시한 커밋을 되돌리고 싶을 때
git revert <commit>
git push

# 강제 푸시 (주의!)
git push --force
git push --force-with-lease  # 더 안전

# 커밋을 잃어버렸을 때
git fsck --lost-found
```

## 📱 Git 단축키

### Bash/Zsh
```bash
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git pull'
alias gco='git checkout'
alias gb='git branch'
alias glog='git log --oneline --graph --all'
```

## 🔗 유용한 링크

- 공식 문서: https://git-scm.com/doc
- Pro Git 책: https://git-scm.com/book
- GitHub Docs: https://docs.github.com
- Git 시각화: https://git-school.github.io/visualizing-git/
- Learn Git Branching: https://learngitbranching.js.org/

---

**💡 Tip**: 이 치트시트를 인쇄하거나 즐겨찾기에 추가하세요!
