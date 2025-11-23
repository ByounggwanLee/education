"""
functions.py
함수 예제
Functions Example
"""

# 기본 함수 (Basic Function)
def greet():
    """간단한 인사 함수"""
    print("안녕하세요!")

greet()

# 매개변수가 있는 함수 (Function with Parameters)
def greet_person(name):
    """이름을 받아 인사하는 함수"""
    print(f"안녕하세요, {name}님!")

greet_person("홍길동")
greet_person("김철수")

# 반환값이 있는 함수 (Function with Return Value)
def add(a, b):
    """두 수를 더하는 함수"""
    return a + b

result = add(5, 3)
print(f"5 + 3 = {result}")

# 여러 매개변수 (Multiple Parameters)
def calculate_rectangle_area(width, height):
    """직사각형의 넓이를 계산하는 함수"""
    area = width * height
    return area

area = calculate_rectangle_area(10, 5)
print(f"직사각형 넓이: {area}")

# 기본값 매개변수 (Default Parameters)
def introduce(name, age=20, city="서울"):
    """자기소개 함수 (기본값 포함)"""
    print(f"이름: {name}, 나이: {age}, 도시: {city}")

introduce("김철수")
introduce("이영희", 25)
introduce("박민수", 30, "부산")

# 여러 반환값 (Multiple Return Values)
def get_min_max(numbers):
    """리스트의 최솟값과 최댓값을 반환"""
    return min(numbers), max(numbers)

nums = [3, 7, 1, 9, 4]
minimum, maximum = get_min_max(nums)
print(f"최솟값: {minimum}, 최댓값: {maximum}")

# 가변 인자 (Variable Arguments)
def sum_all(*numbers):
    """모든 인자의 합을 계산"""
    total = 0
    for num in numbers:
        total += num
    return total

print(f"합계 1: {sum_all(1, 2, 3)}")
print(f"합계 2: {sum_all(1, 2, 3, 4, 5)}")

# 키워드 인자 (Keyword Arguments)
def create_profile(**info):
    """프로필 정보를 출력하는 함수"""
    for key, value in info.items():
        print(f"{key}: {value}")

print("\n=== 프로필 ===")
create_profile(name="홍길동", age=25, job="개발자")

# 람다 함수 (Lambda Function)
square = lambda x: x ** 2
print(f"\n5의 제곱: {square(5)}")

# 리스트와 람다 함수
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(f"제곱 리스트: {squared}")

# 재귀 함수 (Recursive Function)
def factorial(n):
    """팩토리얼을 계산하는 재귀 함수"""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print(f"\n5! = {factorial(5)}")

# 함수 내부 함수 (Nested Function)
def outer_function(x):
    """외부 함수"""
    def inner_function(y):
        """내부 함수"""
        return y * 2
    
    return inner_function(x) + 1

result = outer_function(5)
print(f"\n결과: {result}")
