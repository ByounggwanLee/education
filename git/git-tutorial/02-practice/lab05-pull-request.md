# 실습 5: Pull Request 만들기

**목표**: GitHub Pull Request를 통해 코드 리뷰와 협업 프로세스를 경험합니다.

**소요 시간**: 30-35분

**난이도**: ⭐⭐⭐ 고급

## 🎯 학습 목표

이 실습을 완료하면 다음을 할 수 있습니다:
- Feature 브랜치에서 작업
- Pull Request (PR) 생성
- 코드 리뷰 진행
- PR 병합
- 브랜치 정리

## 📝 사전 준비

- GitHub 계정
- 실습 4에서 만든 `remote-practice` 저장소
- 또는 새로운 저장소 생성

## 🚀 실습 단계

### 1단계: 새 기능을 위한 브랜치 생성

```bash
# 저장소로 이동 (또는 클론)
cd remote-practice
git pull  # 최신 상태로 업데이트

# 새 기능 브랜치 생성
git switch -c feature/add-calculator

# 브랜치 확인
git branch
```

**브랜치 이름 규칙**:
- `feature/` : 새 기능
- `bugfix/` : 버그 수정
- `hotfix/` : 긴급 수정
- `docs/` : 문서 작업

### 2단계: 기능 구현

```bash
# calculator.py 파일 생성
cat > calculator.py << 'EOF'
"""
Simple calculator module
"""

def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract b from a"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
EOF

# 파일 확인
cat calculator.py
```

### 3단계: 테스트 파일 추가

```bash
# test_calculator.py 생성
cat > test_calculator.py << 'EOF'
"""
Tests for calculator module
"""
from calculator import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    print("✓ test_add passed")

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5
    print("✓ test_subtract passed")

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    print("✓ test_multiply passed")

def test_divide():
    assert divide(6, 2) == 3
    assert divide(5, 2) == 2.5
    print("✓ test_divide passed")

if __name__ == "__main__":
    test_add()
    test_subtract()
    test_multiply()
    test_divide()
    print("\nAll tests passed! ✓")
EOF
```

### 4단계: 커밋 생성

```bash
# 파일 스테이징
git add calculator.py test_calculator.py

# 커밋
git commit -m "Add calculator module with basic operations

- Implement add, subtract, multiply, divide functions
- Add comprehensive test suite
- Include error handling for division by zero"

# 로그 확인
git log --oneline
```

**좋은 커밋 메시지**:
- 첫 줄: 간단한 요약 (50자 이내)
- 빈 줄
- 상세 설명 (필요시)

### 5단계: README 업데이트

```bash
# README에 기능 설명 추가
cat >> README.md << 'EOF'

## Calculator Module

A simple calculator with basic arithmetic operations.

### Features
- Addition
- Subtraction
- Multiplication
- Division (with zero check)

### Usage
```python
from calculator import add, subtract, multiply, divide

result = add(5, 3)        # 8
result = subtract(10, 4)  # 6
result = multiply(3, 4)   # 12
result = divide(10, 2)    # 5.0
```

### Testing
```bash
python test_calculator.py
```
EOF

# 커밋
git add README.md
git commit -m "Update README with calculator documentation"
```

### 6단계: 원격에 푸시

```bash
# feature 브랜치를 원격에 푸시
git push -u origin feature/add-calculator
```

**예상 결과**:
```
remote: Create a pull request for 'feature/add-calculator' on GitHub by visiting:
remote:      https://github.com/YOUR_USERNAME/remote-practice/pull/new/feature/add-calculator
```

### 7단계: GitHub에서 Pull Request 생성

#### 웹 브라우저에서:

1. **저장소 페이지로 이동**
   - `https://github.com/YOUR_USERNAME/remote-practice`

2. **PR 생성 시작**
   - 노란색 배너의 "Compare & pull request" 클릭
   - 또는 "Pull requests" 탭 → "New pull request"

3. **PR 정보 입력**
   ```
   Title: Add calculator module with basic operations
   
   Description:
   ## Changes
   - ✨ Add calculator module with 4 basic operations
   - ✅ Add comprehensive test suite
   - 📝 Update README with usage documentation
   - 🛡️ Add error handling for division by zero
   
   ## Testing
   - [x] All tests pass
   - [x] Documentation updated
   
   ## Screenshots (if applicable)
   N/A
   
   Closes #1 (if there's an issue)
   ```

4. **설정 확인**
   - Base branch: `main`
   - Compare branch: `feature/add-calculator`
   - Reviewers: (팀원이 있다면 지정)
   - Labels: `enhancement`, `feature`

5. **"Create pull request" 클릭**

### 8단계: 코드 리뷰 진행

#### PR 페이지에서:

1. **Files changed 탭 클릭**
   - 변경된 파일들 확인
   - 초록색: 추가된 줄
   - 빨간색: 삭제된 줄

2. **코드에 댓글 추가**
   - 코드 줄 번호 옆 `+` 아이콘 클릭
   - 예: "Good error handling!" 또는 "Consider adding more test cases"

3. **전체 리뷰 작성**
   - "Review changes" 버튼 클릭
   - 옵션 선택:
     - ✅ **Approve**: 승인
     - 💬 **Comment**: 일반 코멘트
     - ❌ **Request changes**: 수정 요청

4. **리뷰 제출**
   - "Submit review" 클릭

### 9단계: 피드백 반영 (선택사항)

만약 수정 요청이 있다면:

```bash
# 같은 브랜치에서 수정
echo "" >> calculator.py
echo "def power(a, b):" >> calculator.py
echo '    """Calculate a to the power of b"""' >> calculator.py
echo "    return a ** b" >> calculator.py

# 테스트 추가
echo "" >> test_calculator.py
echo "def test_power():" >> test_calculator.py
echo "    assert power(2, 3) == 8" >> test_calculator.py
echo "    assert power(5, 0) == 1" >> test_calculator.py
echo '    print("✓ test_power passed")' >> test_calculator.py

# 커밋
git add calculator.py test_calculator.py
git commit -m "Add power function based on review feedback"

# 푸시 (PR에 자동으로 추가됨)
git push
```

#### 브라우저에서 확인
- PR 페이지에 새 커밋이 자동으로 추가됨
- Conversation 탭에서 이력 확인 가능

### 10단계: PR 병합

#### 병합 전 확인사항:
- ✅ 모든 테스트 통과 (CI가 있다면)
- ✅ 코드 리뷰 승인
- ✅ 충돌 없음
- ✅ 문서 업데이트됨

#### GitHub에서 병합:

1. **Conversation 탭에서**
   - 하단 "Merge pull request" 버튼 확인
   - 병합 방식 선택:
     - **Merge commit**: 모든 커밋 유지 (기본)
     - **Squash and merge**: 하나의 커밋으로 합침
     - **Rebase and merge**: 선형 히스토리 유지

2. **"Merge pull request" 클릭**

3. **커밋 메시지 확인/수정**

4. **"Confirm merge" 클릭**

5. **브랜치 삭제**
   - "Delete branch" 버튼 클릭 (권장)

**예상 결과**:
```
✓ Pull request successfully merged and closed
✓ feature/add-calculator branch has been deleted
```

### 11단계: 로컬 저장소 업데이트

```bash
# main 브랜치로 전환
git switch main

# 원격의 최신 내용 가져오기
git pull origin main

# 로컬 feature 브랜치 삭제
git branch -d feature/add-calculator

# 원격 브랜치 참조 정리
git remote prune origin

# 확인
git log --oneline --graph
git branch -a
```

## 🎓 PR 프로세스 요약

```
1. 브랜치 생성
   ↓
2. 코드 작성 및 커밋
   ↓
3. 푸시
   ↓
4. PR 생성
   ↓
5. 코드 리뷰
   ↓
6. 피드백 반영 (필요시)
   ↓
7. 승인
   ↓
8. 병합
   ↓
9. 브랜치 삭제
   ↓
10. 로컬 업데이트
```

## ✅ 실습 확인

### GitHub에서:
- ✅ PR이 병합됨 (Merged 표시)
- ✅ feature 브랜치가 삭제됨
- ✅ main 브랜치에 새 커밋들이 추가됨

### 로컬에서:
```bash
# main 브랜치에 코드가 있는지 확인
ls
cat calculator.py

# 브랜치 정리 확인
git branch  # feature 브랜치가 없어야 함
```

## 💡 PR 베스트 프랙티스

### 1. 좋은 PR 크기
- ✅ 작고 집중된 변경사항
- ✅ 하나의 기능 또는 버그 수정
- ❌ 너무 큰 PR (리뷰하기 어려움)

### 2. 좋은 PR 제목
```
✅ Add user authentication with JWT
✅ Fix memory leak in data processor
✅ Update README with installation steps

❌ Updated files
❌ Fixed stuff
❌ Changes
```

### 3. 좋은 PR 설명
```markdown
## 변경 내용
- 주요 변경사항 나열

## 왜 필요한가?
- 문제 또는 요구사항 설명

## 어떻게 테스트했나?
- 테스트 방법 설명

## 스크린샷 (있다면)
- UI 변경사항이 있다면 첨부

## 체크리스트
- [ ] 테스트 추가/업데이트
- [ ] 문서 업데이트
- [ ] 코드 리뷰 준비됨
```

### 4. 코드 리뷰 팁

**리뷰어로서**:
- 💬 건설적인 피드백
- 💡 구체적인 제안
- 👍 좋은 코드는 칭찬하기
- ❓ 이해 안 되는 부분 질문

**작성자로서**:
- 📝 명확한 설명
- 🧪 충분한 테스트
- 📚 문서 업데이트
- 🙏 피드백에 감사하기

## 🔄 추가 연습

### 연습 1: Draft PR 만들기

```bash
git switch -c feature/work-in-progress
echo "# WIP" > wip.md
git add wip.md
git commit -m "WIP: Start new feature"
git push -u origin feature/work-in-progress
```

GitHub에서:
- PR 생성 시 "Create draft pull request" 선택
- 준비되면 "Ready for review" 클릭

### 연습 2: PR 템플릿 추가

```bash
mkdir .github
cat > .github/pull_request_template.md << 'EOF'
## 변경 내용
<!-- 변경사항을 간단히 설명하세요 -->

## 관련 이슈
<!-- Closes #이슈번호 -->

## 테스트
- [ ] 로컬에서 테스트 완료
- [ ] 새 테스트 추가

## 체크리스트
- [ ] 코드가 프로젝트 스타일을 따름
- [ ] 문서 업데이트
- [ ] 커밋 메시지가 명확함
EOF

git add .github/
git commit -m "Add PR template"
git push
```

### 연습 3: 충돌 해결 연습

다음 실습에서 다룹니다!

## ❓ 문제 해결

### Q: PR을 만들 수 없어요
- main 브랜치와 차이가 있는지 확인
- 푸시가 완료되었는지 확인

### Q: PR이 자동으로 병합되지 않아요
- 충돌이 있는지 확인
- "Resolve conflicts" 버튼 클릭

### Q: 잘못된 브랜치에서 PR을 만들었어요
- PR을 닫고 올바른 브랜치에서 새로 생성

## 🎯 다음 단계

Pull Request 워크플로우를 익혔습니다! 🎉

다음 실습에서는 실제 협업에서 자주 발생하는 충돌을 해결하는 방법을 배웁니다.

➡️ **[실습 6: 충돌 해결하기](./lab06-conflict-resolution.md)**

## 📚 관련 이론

- [Git으로 협업하기](../01-theory/08-collaboration.md)
- [원격 저장소](../01-theory/07-remote-repository.md)
- [Git 브랜치 관리](../01-theory/06-branching.md)
