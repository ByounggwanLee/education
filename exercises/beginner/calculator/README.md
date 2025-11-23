# 연습 문제: 간단한 계산기 (Exercise: Simple Calculator)

## 난이도 (Difficulty)
초급 (Beginner) ⭐

## 문제 설명 (Problem Description)

사용자로부터 두 개의 숫자와 연산자(+, -, *, /)를 입력받아 계산 결과를 출력하는 프로그램을 작성하세요.

Write a program that takes two numbers and an operator (+, -, *, /) from the user and prints the calculation result.

## 요구사항 (Requirements)

1. 두 개의 숫자를 입력받기
2. 연산자를 입력받기 (+, -, *, /)
3. 입력된 연산자에 따라 계산 수행
4. 결과 출력
5. 0으로 나누는 경우 에러 메시지 출력

Requirements:
1. Get two numbers from user
2. Get an operator (+, -, *, /)
3. Perform calculation based on operator
4. Print the result
5. Show error message for division by zero

## 예제 입출력 (Example Input/Output)

### 예제 1
```
첫 번째 숫자를 입력하세요: 10
두 번째 숫자를 입력하세요: 5
연산자를 입력하세요 (+, -, *, /): +
결과: 10 + 5 = 15
```

### 예제 2
```
첫 번째 숫자를 입력하세요: 20
두 번째 숫자를 입력하세요: 4
연산자를 입력하세요 (+, -, *, /): /
결과: 20 / 4 = 5.0
```

### 예제 3
```
첫 번째 숫자를 입력하세요: 10
두 번째 숫자를 입력하세요: 0
연산자를 입력하세요 (+, -, *, /): /
오류: 0으로 나눌 수 없습니다!
```

## 힌트 (Hints)

1. `input()` 함수를 사용하여 사용자 입력 받기
2. 입력받은 문자열을 `float()` 또는 `int()`로 변환
3. `if-elif-else`를 사용하여 연산자 구분
4. 나눗셈의 경우 분모가 0인지 확인

Hints:
1. Use `input()` function to get user input
2. Convert input string to `float()` or `int()`
3. Use `if-elif-else` to distinguish operators
4. For division, check if denominator is zero

## 보너스 도전 (Bonus Challenge)

1. 여러 번 계속 계산할 수 있도록 반복 기능 추가
2. 잘못된 연산자 입력 시 에러 메시지 표시
3. 계산 이력을 저장하고 보여주는 기능 추가

Bonus challenges:
1. Add loop to continue calculating
2. Show error message for invalid operators
3. Add feature to store and display calculation history

## 시작 코드 (Starter Code)

`calculator.py` 파일을 만들고 아래 코드로 시작하세요:

Create `calculator.py` file and start with:

```python
# 계산기 프로그램
# Calculator Program

# TODO: 첫 번째 숫자 입력받기

# TODO: 두 번째 숫자 입력받기

# TODO: 연산자 입력받기

# TODO: 계산 수행 및 결과 출력
```

## 테스트 방법 (How to Test)

1. 프로그램 실행: `python calculator.py`
2. 여러 가지 숫자와 연산자 조합으로 테스트
3. 0으로 나누기 시도
4. 예상된 결과와 비교

Testing steps:
1. Run: `python calculator.py`
2. Test with various numbers and operators
3. Try division by zero
4. Compare with expected results

## 학습 목표 (Learning Goals)

이 연습 문제를 통해 다음을 배웁니다:
- 사용자 입력 처리
- 데이터 타입 변환
- 조건문 사용
- 에러 처리

Learning goals:
- Handle user input
- Convert data types
- Use conditional statements
- Error handling
