# Python 기초 튜토리얼 (Python Basics Tutorial)

## 개요 (Overview)

이 튜토리얼은 Python 프로그래밍의 기초를 배우는 초보자를 위한 가이드입니다.

This tutorial is a beginner's guide to learning the fundamentals of Python programming.

## 사전 요구사항 (Prerequisites)

- 컴퓨터 기본 사용 능력
- 프로그래밍에 대한 열정
- Python 설치 (버전 3.8 이상)

Prerequisites:
- Basic computer literacy
- Enthusiasm for programming
- Python installed (version 3.8+)

## 학습 목표 (Learning Objectives)

이 튜토리얼을 완료하면 다음을 할 수 있습니다:

Upon completion, you will be able to:

1. Python의 기본 문법 이해하기
2. 변수와 데이터 타입 사용하기
3. 조건문과 반복문 작성하기
4. 함수를 정의하고 호출하기
5. 간단한 프로그램 작성하기

## 내용 (Content)

### 1. Hello, World!

모든 프로그래밍 학습의 시작, "Hello, World!" 프로그램입니다.

The beginning of every programming journey: "Hello, World!"

```python
# 첫 번째 Python 프로그램
print("Hello, World!")
```

**설명 (Explanation):**
- `print()`: 화면에 텍스트를 출력하는 함수
- `"Hello, World!"`: 문자열 (string) 데이터

### 2. 변수와 데이터 타입 (Variables and Data Types)

변수는 데이터를 저장하는 컨테이너입니다.

Variables are containers for storing data.

```python
# 변수 선언
name = "홍길동"        # 문자열 (string)
age = 25              # 정수 (integer)
height = 175.5        # 실수 (float)
is_student = True     # 불리언 (boolean)

# 변수 출력
print(f"이름: {name}")
print(f"나이: {age}")
print(f"키: {height}cm")
print(f"학생 여부: {is_student}")
```

**주요 데이터 타입 (Main Data Types):**
- `str`: 문자열
- `int`: 정수
- `float`: 실수
- `bool`: 참/거짓

### 3. 조건문 (Conditional Statements)

조건에 따라 다른 코드를 실행합니다.

Execute different code based on conditions.

```python
# if-elif-else 문
score = 85

if score >= 90:
    print("등급: A")
elif score >= 80:
    print("등급: B")
elif score >= 70:
    print("등급: C")
else:
    print("등급: F")
```

### 4. 반복문 (Loops)

반복 작업을 자동화합니다.

Automate repetitive tasks.

```python
# for 반복문
fruits = ["사과", "바나나", "오렌지"]
for fruit in fruits:
    print(f"과일: {fruit}")

# while 반복문
count = 1
while count <= 5:
    print(f"카운트: {count}")
    count += 1
```

### 5. 함수 (Functions)

재사용 가능한 코드 블록을 만듭니다.

Create reusable code blocks.

```python
# 함수 정의
def greet(name):
    """인사 메시지를 출력하는 함수"""
    return f"안녕하세요, {name}님!"

# 함수 호출
message = greet("홍길동")
print(message)

# 계산 함수
def add(a, b):
    """두 수를 더하는 함수"""
    return a + b

result = add(5, 3)
print(f"5 + 3 = {result}")
```

## 연습 문제 (Exercises)

### 연습 1: 계산기
두 수를 입력받아 더하기, 빼기, 곱하기, 나누기를 수행하는 프로그램을 작성하세요.

Exercise 1: Calculator
Write a program that takes two numbers and performs addition, subtraction, multiplication, and division.

### 연습 2: 숫자 맞추기 게임
1부터 100 사이의 랜덤 숫자를 맞추는 게임을 만드세요.

Exercise 2: Number Guessing Game
Create a game to guess a random number between 1 and 100.

### 연습 3: 온도 변환기
섭씨를 화씨로, 화씨를 섭씨로 변환하는 프로그램을 작성하세요.

Exercise 3: Temperature Converter
Write a program to convert Celsius to Fahrenheit and vice versa.

## 다음 단계 (Next Steps)

Python 기초를 마스터했다면:

After mastering Python basics:

1. 리스트, 딕셔너리 등 자료구조 학습
2. 파일 입출력 배우기
3. 객체 지향 프로그래밍 시작하기
4. 실전 프로젝트 도전하기

1. Learn data structures (lists, dictionaries)
2. Study file I/O
3. Start object-oriented programming
4. Take on practical projects

## 추가 자료 (Additional Resources)

- [Python 공식 문서](https://docs.python.org/ko/3/)
- [Python 튜토리얼](https://docs.python.org/ko/3/tutorial/)
- [Real Python](https://realpython.com/)
- [Python for Beginners](https://www.python.org/about/gettingstarted/)

## 도움이 필요하신가요? (Need Help?)

궁금한 점이 있다면 이슈를 생성하거나 커뮤니티에 질문하세요!

If you have questions, create an issue or ask in the community!
