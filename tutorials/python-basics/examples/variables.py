"""
variables.py
변수와 데이터 타입 예제
Variables and Data Types Example
"""

# 문자열 변수 (String Variables)
name = "김철수"
city = "서울"
print(f"이름: {name}, 도시: {city}")

# 숫자 변수 (Numeric Variables)
age = 25
height = 175.5
weight = 70.2

print(f"나이: {age}세")
print(f"키: {height}cm")
print(f"몸무게: {weight}kg")

# 불리언 변수 (Boolean Variables)
is_student = True
has_job = False

print(f"학생 여부: {is_student}")
print(f"직업 유무: {has_job}")

# 데이터 타입 확인 (Check Data Types)
print(f"name의 타입: {type(name)}")
print(f"age의 타입: {type(age)}")
print(f"height의 타입: {type(height)}")
print(f"is_student의 타입: {type(is_student)}")

# 타입 변환 (Type Conversion)
num_string = "100"
num_int = int(num_string)
print(f"문자열 '{num_string}'을 정수로: {num_int}")

# 계산 (Calculations)
price = 10000
quantity = 3
total = price * quantity
print(f"총 금액: {total}원")
