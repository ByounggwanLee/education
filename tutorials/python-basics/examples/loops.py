"""
loops.py
반복문 예제
Loops Example
"""

# for 반복문 - 리스트 (for loop - list)
print("=== 과일 목록 ===")
fruits = ["사과", "바나나", "오렌지", "포도", "딸기"]

for fruit in fruits:
    print(f"과일: {fruit}")

# for 반복문 - range (for loop - range)
print("\n=== 1부터 5까지 ===")
for i in range(1, 6):
    print(f"숫자: {i}")

# 구구단 (Multiplication Table)
print("\n=== 3단 구구단 ===")
for i in range(1, 10):
    result = 3 * i
    print(f"3 x {i} = {result}")

# while 반복문 (while loop)
print("\n=== 카운트다운 ===")
count = 5
while count > 0:
    print(f"카운트: {count}")
    count -= 1
print("발사!")

# 합계 계산 (Sum Calculation)
print("\n=== 1부터 10까지의 합 ===")
total = 0
number = 1

while number <= 10:
    total += number
    number += 1

print(f"합계: {total}")

# 중첩 반복문 (Nested Loops)
print("\n=== 구구단 2단~5단 ===")
for dan in range(2, 6):
    print(f"\n{dan}단:")
    for i in range(1, 10):
        print(f"{dan} x {i} = {dan * i}")

# break와 continue (break and continue)
print("\n=== 숫자 찾기 (5 발견 시 중단) ===")
for num in range(1, 11):
    if num == 5:
        print(f"{num} 발견! 중단합니다.")
        break
    print(num)

print("\n=== 홀수만 출력 ===")
for num in range(1, 11):
    if num % 2 == 0:  # 짝수는 건너뛰기
        continue
    print(num)

# 리스트 컴프리헨션 (List Comprehension)
print("\n=== 제곱수 리스트 ===")
squares = [x**2 for x in range(1, 6)]
print(squares)

# 조건부 리스트 컴프리헨션 (Conditional List Comprehension)
print("\n=== 짝수만 필터링 ===")
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = [x for x in numbers if x % 2 == 0]
print(even_numbers)
