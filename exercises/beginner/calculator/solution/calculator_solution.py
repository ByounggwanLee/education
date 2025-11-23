# 계산기 프로그램 - 해답 (Calculator Program - Solution)

def calculate(num1, num2, operator):
    """
    두 숫자와 연산자로 계산을 수행하는 함수
    Performs calculation with two numbers and an operator
    """
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        if num2 == 0:
            return None  # 0으로 나누기 에러
        return num1 / num2
    else:
        return None  # 잘못된 연산자

def main():
    """메인 함수"""
    print("=== 간단한 계산기 ===")
    
    # 사용자 입력 받기
    try:
        num1 = float(input("첫 번째 숫자를 입력하세요: "))
        num2 = float(input("두 번째 숫자를 입력하세요: "))
        operator = input("연산자를 입력하세요 (+, -, *, /): ")
        
        # 계산 수행
        result = calculate(num1, num2, operator)
        
        # 결과 출력
        if result is None:
            if operator == '/' and num2 == 0:
                print("오류: 0으로 나눌 수 없습니다!")
            else:
                print("오류: 잘못된 연산자입니다!")
        else:
            print(f"결과: {num1} {operator} {num2} = {result}")
    
    except ValueError:
        print("오류: 올바른 숫자를 입력하세요!")

if __name__ == "__main__":
    main()
