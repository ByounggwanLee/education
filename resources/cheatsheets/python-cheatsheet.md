# Python 치트시트 (Python Cheat Sheet)

빠른 참조를 위한 Python 핵심 문법 정리
Quick reference for essential Python syntax

## 📝 변수와 데이터 타입 (Variables and Data Types)

```python
# 변수 할당 (Variable Assignment)
x = 5
name = "Python"
is_valid = True

# 데이터 타입 (Data Types)
integer = 42           # int
floating = 3.14        # float
text = "Hello"         # str
boolean = True         # bool
nothing = None         # NoneType
```

## 📊 자료구조 (Data Structures)

```python
# 리스트 (List) - 수정 가능
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")
fruits[0]  # "apple"

# 튜플 (Tuple) - 수정 불가
coordinates = (10, 20)

# 딕셔너리 (Dictionary)
person = {
    "name": "홍길동",
    "age": 25,
    "city": "서울"
}
person["name"]  # "홍길동"

# 집합 (Set)
unique_numbers = {1, 2, 3, 4, 5}
```

## 🔄 조건문 (Conditionals)

```python
# if-elif-else
if x > 10:
    print("크다")
elif x > 5:
    print("중간")
else:
    print("작다")

# 삼항 연산자 (Ternary)
result = "짝수" if x % 2 == 0 else "홀수"
```

## 🔁 반복문 (Loops)

```python
# for 반복문
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

for item in [1, 2, 3]:
    print(item)

# while 반복문
count = 0
while count < 5:
    print(count)
    count += 1

# break, continue
for i in range(10):
    if i == 5:
        break  # 종료
    if i % 2 == 0:
        continue  # 건너뛰기
    print(i)
```

## 🎯 함수 (Functions)

```python
# 기본 함수
def greet(name):
    return f"Hello, {name}!"

# 기본값 매개변수
def power(base, exp=2):
    return base ** exp

# 가변 인자
def sum_all(*args):
    return sum(args)

# 키워드 인자
def info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# 람다 함수
square = lambda x: x ** 2
```

## 📦 리스트 컴프리헨션 (List Comprehension)

```python
# 기본
squares = [x**2 for x in range(5)]
# [0, 1, 4, 9, 16]

# 조건부
evens = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]

# 딕셔너리 컴프리헨션
squared_dict = {x: x**2 for x in range(5)}
```

## 📄 문자열 (Strings)

```python
# 포맷팅
name = "Python"
f"Hello, {name}!"  # f-string
"Hello, {}!".format(name)
"Hello, %s!" % name

# 메서드
text = "hello world"
text.upper()        # "HELLO WORLD"
text.capitalize()   # "Hello world"
text.split()        # ["hello", "world"]
"-".join(["a", "b"])  # "a-b"

# 슬라이싱
text = "Python"
text[0]      # "P"
text[-1]     # "n"
text[0:3]    # "Pyt"
text[::-1]   # "nohtyP" (역순)
```

## 🔧 자주 사용하는 내장 함수 (Common Built-in Functions)

```python
# 타입 변환
int("42")       # 42
float("3.14")   # 3.14
str(42)         # "42"
list("abc")     # ["a", "b", "c"]

# 수학
abs(-5)         # 5
min(1, 2, 3)    # 1
max(1, 2, 3)    # 3
sum([1, 2, 3])  # 6
pow(2, 3)       # 8
round(3.7)      # 4

# 기타
len([1, 2, 3])  # 3
type(42)        # <class 'int'>
range(5)        # 0, 1, 2, 3, 4
enumerate(["a", "b"])  # (0, "a"), (1, "b")
zip([1, 2], ["a", "b"])  # (1, "a"), (2, "b")
```

## 📚 파일 입출력 (File I/O)

```python
# 읽기
with open("file.txt", "r") as f:
    content = f.read()
    lines = f.readlines()

# 쓰기
with open("file.txt", "w") as f:
    f.write("Hello, World!")
    f.writelines(["line1\n", "line2\n"])

# 추가
with open("file.txt", "a") as f:
    f.write("Additional text")
```

## 🎨 클래스 (Classes)

```python
# 기본 클래스
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"안녕, {self.name}!"

# 사용
person = Person("홍길동", 25)
person.greet()

# 상속
class Student(Person):
    def __init__(self, name, age, grade):
        super().__init__(name, age)
        self.grade = grade
```

## ⚠️ 예외 처리 (Exception Handling)

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다!")
except Exception as e:
    print(f"오류: {e}")
else:
    print("성공!")
finally:
    print("항상 실행")

# 예외 발생
raise ValueError("잘못된 값입니다!")
```

## 📦 모듈 임포트 (Module Import)

```python
# 전체 임포트
import math
math.sqrt(16)

# 특정 함수 임포트
from math import sqrt, pi
sqrt(16)

# 별칭 사용
import numpy as np
import pandas as pd

# 전체 임포트 (권장하지 않음)
from math import *
```

## 💡 유용한 팁 (Useful Tips)

```python
# 변수 교환
a, b = b, a

# 다중 할당
x, y, z = 1, 2, 3

# 언패킹
first, *rest, last = [1, 2, 3, 4, 5]
# first=1, rest=[2,3,4], last=5

# any, all
any([True, False, False])  # True
all([True, True, False])   # False

# 리스트 복사
original = [1, 2, 3]
copy = original.copy()
# 또는
copy = original[:]

# 정렬
sorted([3, 1, 2])           # [1, 2, 3]
sorted([3, 1, 2], reverse=True)  # [3, 2, 1]
```

## 🚀 성능 팁 (Performance Tips)

```python
# 리스트보다 제너레이터 사용 (메모리 효율)
gen = (x**2 for x in range(1000000))

# in 연산자는 set이 list보다 빠름
my_set = {1, 2, 3, 4, 5}
if 3 in my_set:  # O(1)
    pass

# 문자열 결합은 join 사용
result = "".join(["a", "b", "c"])  # 더 빠름
# result = "a" + "b" + "c"  # 느림
```

## 📌 기억해야 할 것들 (Things to Remember)

1. **들여쓰기**: Python은 들여쓰기로 코드 블록 구분
2. **0-based 인덱싱**: 첫 번째 요소는 인덱스 0
3. **불변 타입**: str, tuple, int, float는 변경 불가
4. **가변 타입**: list, dict, set은 변경 가능
5. **PEP 8**: Python 코드 스타일 가이드 준수

Key points:
1. **Indentation**: Python uses indentation for code blocks
2. **0-based indexing**: First element has index 0
3. **Immutable types**: str, tuple, int, float cannot be changed
4. **Mutable types**: list, dict, set can be modified
5. **PEP 8**: Follow Python style guide
