# 계산기 프로그램 - 보너스 버전 (Calculator Program - Bonus Version)

def calculate(num1, num2, operator):
    """계산 수행"""
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        if num2 == 0:
            return None
        return num1 / num2
    else:
        return None

def main():
    """메인 함수 - 반복 계산 및 히스토리 기능 포함"""
    print("=== 고급 계산기 ===")
    print("(종료하려면 'q'를 입력하세요)")
    
    history = []  # 계산 이력
    
    while True:
        print("\n" + "="*40)
        
        # 첫 번째 숫자 입력
        first_input = input("첫 번째 숫자를 입력하세요 (q=종료, h=히스토리): ")
        
        # 종료 확인
        if first_input.lower() == 'q':
            print("계산기를 종료합니다.")
            break
        
        # 히스토리 보기
        if first_input.lower() == 'h':
            if history:
                print("\n=== 계산 히스토리 ===")
                for i, record in enumerate(history, 1):
                    print(f"{i}. {record}")
            else:
                print("히스토리가 없습니다.")
            continue
        
        try:
            num1 = float(first_input)
            num2 = float(input("두 번째 숫자를 입력하세요: "))
            operator = input("연산자를 입력하세요 (+, -, *, /): ")
            
            # 계산
            result = calculate(num1, num2, operator)
            
            # 결과 처리
            if result is None:
                if operator == '/' and num2 == 0:
                    print("오류: 0으로 나눌 수 없습니다!")
                else:
                    print("오류: 잘못된 연산자입니다! (+, -, *, / 중 하나를 입력하세요)")
            else:
                calculation = f"{num1} {operator} {num2} = {result}"
                print(f"결과: {calculation}")
                history.append(calculation)
        
        except ValueError:
            print("오류: 올바른 숫자를 입력하세요!")
    
    # 종료 시 히스토리 표시
    if history:
        print("\n=== 전체 계산 히스토리 ===")
        for i, record in enumerate(history, 1):
            print(f"{i}. {record}")

if __name__ == "__main__":
    main()
