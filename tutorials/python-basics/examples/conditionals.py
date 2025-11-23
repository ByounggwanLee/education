"""
conditionals.py
조건문 예제
Conditional Statements Example
"""

# 기본 if 문 (Basic if statement)
temperature = 25

if temperature > 30:
    print("더워요!")
elif temperature > 20:
    print("적당해요.")
elif temperature > 10:
    print("선선해요.")
else:
    print("추워요!")

# 성적 등급 (Grade System)
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"점수: {score}, 등급: {grade}")

# 여러 조건 (Multiple Conditions)
age = 20
has_license = True

if age >= 18 and has_license:
    print("운전할 수 있습니다.")
elif age >= 18 and not has_license:
    print("면허증이 필요합니다.")
else:
    print("나이가 부족합니다.")

# 짝수/홀수 판별 (Even/Odd Check)
number = 7

if number % 2 == 0:
    print(f"{number}는 짝수입니다.")
else:
    print(f"{number}는 홀수입니다.")

# 범위 체크 (Range Check)
hour = 14

if 6 <= hour < 12:
    print("오전입니다.")
elif 12 <= hour < 18:
    print("오후입니다.")
elif 18 <= hour < 22:
    print("저녁입니다.")
else:
    print("밤입니다.")
