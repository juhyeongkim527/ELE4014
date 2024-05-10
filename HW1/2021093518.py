import os # file이 존재하는지 확인하기 위한 라이브러리
import argparse # input file과 problem number를 받기 위한 라이브러리

# Character classes
# 산술 표현식만 사용하기 때문에 LETTER는 사용하지 않음
DIGIT = 1
UNKNOWN = 99

class SyntaxAnalyzer:
    def __init__(self):
        self.charClass = 0 # char의 class를 나타내는 변수
        self.lexeme = ['' for i in range(100)] # lexeme을 저장하는 변수
        self.nextChar = '' # 다음 char를 저장하는 변수
        self.lexLen = 0 # lexeme의 길이를 저장하는 변수
        self.token = 0 # token을 저장하는 변수
        self.nextToken = 0 # 다음 token을 저장하는 변수
        self.file = '' # file을 저장하는 변수
        self.tokens = [] # token을 저장하는 리스트
        self.lexemes = [] # lexeme을 저장하는 리스트

    # addChar - a function to add nextChar to lexeme 
    def addChar(self): 
        if(self.lexLen <= 99): # lexeme의 최대 길이를 100으로 설정
                self.lexeme[self.lexLen] = self.nextChar # lexeme에 nextChar를 추가
                self.lexLen += 1 # lexLen을 1 증가
        else: # lexeme의 최대 길이(100)을 넘어가면 에러 출력
            print("Error - lexeme is too long \n")
    
    # getChar - a function to get the next character of input and determine its character class
    def getChar(self):
        self.nextChar = self.file.read(1) # argument로 받은 file에서 한 char씩 읽어 nextChar에 저장
        if(self.nextChar != ''): # nextChar가 EOF가 아닌 경우
            if(self.nextChar.isdigit()): # nextChar가 숫자인 경우
                self.charClass = DIGIT # charClass를 DIGIT으로 설정
            else: # nextChar가 숫자가 아닌 경우 (UNKNOWN)
                self.charClass = UNKNOWN # charClass를 UNKNOWN으로 설정
        else: # nextChar가 EOF인 경우
            self.charClass = '$' # charClass를 '$'로 설정

    # getNonBlank - a function to call getChar until it returns a non-whitespace character
    def getNonBlank(self): 
        while self.nextChar.isspace(): # nextChar가 공백인 경우
            self.getChar() # getChar를 호출해서 공백을 제거

    # lookup - a function to lookup operators and parentheses and return the token
    def lookup(self, ch):
        if ch == '+':
            self.addChar() 
            self.nextToken = '+'  
        
        elif ch == '-':
            self.addChar()
            self.nextToken = '-'
        
        elif ch == '*':
            self.addChar()
            self.nextToken = '*'
        
        elif ch == '/':
            self.addChar()
            self.nextToken = '/'
        
        else: # EOF인 경우(여기서 처리안해줘도 lex에서 처리 가능하지만 명시적으로 처리)
            self.addChar()
            self.nextToken = '$'
        
        return self.nextToken
    
    # lexer - a simple lexical anaylzer for arithmetic expressions
    def lex(self): 
        self.lexLen = 0 # lexLen을 0으로 초기화(호출할 때 마다 lexeme을 새로 저장하기 위해)
        self.lexeme = ['' for i in range(100)] # lexeme을 공백으로 초기화
        self.getNonBlank() # addChar를 하기 전에 공백을 제거
        
        # Parse integer literals
        if(self.charClass == DIGIT):
            self.addChar() # lexeme에 nextChar를 추가
            self.getChar() # 다음 char를 읽어 charClass 값을 업데이트
            while(self.charClass == DIGIT): # nextChar가 숫자인 경우
                self.addChar() # lexeme에 nextChar를 추가
                self.getChar() # 다음 char를 읽어 charClass 값을 업데이트
            self.nextToken = 'N' # 정수를 나타내는 'N'으로 token을 설정

        # Parentheses and operators
        elif(self.charClass == UNKNOWN): 
            self.lookup(self.nextChar) # nextChar가 정수가 아닌 경우 (HW1 BNF에서는 연산자 = +, - , *, /, $), lookup 함수를 호출해서 token을 설정
            self.getChar() # 다음 char를 읽어 charClass 값을 업데이트
        
        # EOF
        else: 
            self.nextToken = '$' # nextChar가 EOF인 경우 token을 '$'로 설정
            self.lexeme[0] = '$' # lexeme을 '$'로 설정 (addChar를 호출하지 않고 바로 lexeme에 저장)
            self.lexLen += 1 # lexLen을 1 증가 (addChar를 호출하지 않고 바로 lexeme에 저장했기 때문에)
        
        if(self.nextToken == 'N'): # token이 정수인 경우
            self.lexemes.append(int(''.join(self.lexeme))) # lexeme을 join해서('1','0','0' -> '100') int로 변환 후('100' -> 100) lexemes에 추가 
        else:
            self.lexemes.append(self.lexeme[0]) # token이 정수가 아닌 경우 한 문자이므로 join할 필요 없이 바로 lexeme을 lexemes에 추가
        
        self.tokens.append(self.nextToken) # token을 tokens에 추가
        
    def lexer(self, file): # 위에서 정의한 lex method를 이용해서 arithmetic expression을 parsing
        if os.path.exists(file):
            self.file = open(file, 'r')
            self.getChar() # 맨 앞의 char를 읽어서 nextChar를 업데이트
            while True: # EOF가 나올 때까지 반복
                self.lex() # arithmetic expression을 parsing
                if self.nextToken == '$': # EOF인 경우 loop 탈출
                    break 
            self.file.close()
        else: #  file이 존재하지 않는 경우 에러 출력
            print("ERROR - cannot open " + file + " \n")
        
        return self.lexemes, self.tokens # lexemes와 tokens를 반환 (main 함수에서 print하기 위해)
    
    # 2. Shift-Reduce Parser : parsing table을 이용해서 shift-reduce parser를 구현하고 result를 출력
    def shift_reduce_parser(self, lexemes, tokens):
        print('Tracing Start!!') 
        print()
        print('+-------+---------------------------+---------------------------------------+--------------------------+')
        print('| STATE |           STACK           |                 INPUT                 |          ACTION          |')
        print('+-------+---------------------------+---------------------------------------+--------------------------+')

        # parsing table 정의
        terminal = ['N', '+', '-', '*', '/', '$']
        non_terminal = ['E', 'T']
        action = [['S3', '', '', '', '', ''],
                  ['', 'S4', 'S5', '', '', 'accept'],
                  ['', 'R3', 'R3', 'S6', 'S7', 'R3'],
                  ['', 'R6', 'R6', 'R6', 'R6', 'R6'],
                  ['S3', '', '', '', '', ''],
                  ['S3', '', '', '', '', ''],
                  ['S10', '', '', '', '', ''],
                  ['S11', '', '', '', '', ''],
                  ['', 'R1', 'R1', 'S6', 'S7', 'R1'],
                  ['', 'R2', 'R2', 'S6', 'S7', 'R2'],
                  ['', 'R4', 'R4', 'R4', 'R4', 'R4'],
                  ['', 'R5', 'R5', 'R5', 'R5', 'R5']]
        goto = [[1, 2],
                ['', ''],
                ['', ''],
                ['', ''],
                ['', 8],
                ['', 9],
                ['', ''],
                ['', ''],
                ['', ''],
                ['', ''],
                ['', ''],
                ['', '']]

        stack = [] # stack을 저장하는 리스트
        stack.append(0) # stack에는 state 0 을 나타내기 위해 0을 추가
        
        input = tokens.copy() # tokens을 input에 복사 (다른 곳에서 쓰일 수 있는 tokens을 pop하는 것을 방지하기 위해)
        actions = [] # action을 저장하는 리스트
        tmp = 1 # accept를 만나면 아래의 while문을 탈출하기 위한 변수
        state = 0 # state를 나타내는 변수

        number = [] # result 계산을 위해 정수(N)을 저장하는 리스트
        lex_copy =  lexemes.copy() # lexemes를 lex_copy에 복사 (다른 곳에서 쓰일 수 있는 lexemes를 pop하는 것을 방지하기 위해)
        result = 0 # result를 저장하는 변수 (초기 값은 0으로 설정)

        while tmp: # accept를 만나기 전까지 반복
            print("| {:^5} | {:<25} | {:>37} |".format(state, ' '.join(map(str, stack)), ' '.join(map(str, input))), end=' ')
            
            if(len(actions) != 0): # action을 현재 state에 대한 것만 출력하기 위해 이전 state에서 append한 action은 clear
                actions.clear()
            
            if(action[stack[-1]][terminal.index(input[0])][0] == 'S'): # parsing table의 entry에서 Shift가 나온 경우
                actions.append('Shift') # action을 출력하기 위해 Shift 추가
                actions.append(int(action[stack[-1]][terminal.index(input[0])][1:])) # action을 출력하기 위해 Shift 뒤에 이동한 state 추가
                stack.append(input.pop(0)) # stack에 input의 front token 추가
                stack.append(int(action[stack[-2]][terminal.index(stack[-1])][1:])) # shift한 state 추가

                if(stack[-2] == 'N'): # shift를 통해 stack에 추가된 token이 정수인 경우
                    number.append(lex_copy.pop(0)) # number에 lexemes의 front lexeme 추가
                else: # shift를 통해 stack에 추가된 token이 정수가 아닌 경우
                    lex_copy.pop(0) # lexemes의 front lexeme 제거 (number가 아닌 operator나 $이기 때문에 다음 정수 lexeme를 받기 위해 제거)
            
            elif(action[stack[-1]][terminal.index(input[0])][0] == 'R'): # parsing table의 entry에서 Reduce가 나온 경우
                
                actions.append('Reduce') # action을 출력하기 위해 Reduce 추가
                actions.append(action[stack[-1]][terminal.index(input[0])][1]) # action을 출력하기 위해 Reduce 뒤에 BNF의 몇 번째 rule인지 추가
                if(action[stack[-1]][terminal.index(input[0])] == 'R1'): # E -> E + T 
                    # E, +, T와 각 token에 대한 state를 pop하고 E로 대체 (3*2 = 6개 pop)
                    stack.pop() 
                    stack.pop() 
                    stack.pop() 
                    stack.pop() 
                    stack.pop() 
                    stack.pop() 
                    
                    stack.append('E') # E로 대체
                    stack.append(goto[stack[-2]][non_terminal.index(stack[-1])]) # goto table을 이용해서 이동한 state 추가
                    
                    actions.append('(Goto[' + str(stack[-3]) + ', ' +  str(stack[-2]) + '])') # action을 출력하기 위해 어떤 goto table을 이용해서 이동했는지 추가

                    n1 = number.pop() 
                    n2 = number.pop() 
                    number.append(n2 + n1) # result를 누적하여 계산하기 위해 number에서 pop한 두 정수를 더한 값을 다시 number에 추가
                
                elif(action[stack[-1]][terminal.index(input[0])] == 'R2'): # E -> E - T
                    # E, -, T와 각 token에 대한 state를 pop하고 E로 대체 (3*2 = 6개 pop)
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.pop()

                    stack.append('E') # E로 대체
                    stack.append(goto[stack[-2]][non_terminal.index(stack[-1])]) # goto table을 이용해서 이동한 state 추가
                    
                    actions.append('(Goto[' + str(stack[-3]) + ', ' +  str(stack[-2]) + '])') # action을 출력하기 위해 어떤 goto table을 이용해서 이동했는지 추가

                    n1 = number.pop()
                    n2 = number.pop()
                    number.append(n2 - n1) # result를 누적하여 계산하기 위해 number에서 pop한 두 정수를 뺀 값을 다시 number에 추가

                elif(action[stack[-1]][terminal.index(input[0])] == 'R3'): # E -> T
                    # T와 해당 token에 대한 state를 pop하고 E로 대체 (1*2 = 2개 pop)
                    stack.pop()
                    stack.pop()
                    
                    stack.append('E') # E로 대체
                    stack.append(goto[stack[-2]][non_terminal.index(stack[-1])]) # goto table을 이용해서 이동한 state 추가
                    
                    actions.append('(Goto[' + str(stack[-3]) + ', ' +  str(stack[-2]) + '])') # action을 출력하기 위해 어떤 goto table을 이용해서 이동했는지 추가

                elif(action[stack[-1]][terminal.index(input[0])] == 'R4'): # T -> T * N
                    # T, *, N와 각 token에 대한 state를 pop하고 T로 대체 (3*2 = 6개 pop)
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.pop()

                    stack.append('T') # T로 대체
                    stack.append(goto[stack[-2]][non_terminal.index(stack[-1])]) # goto table을 이용해서 이동한 state 추가
                    actions.append('(Goto[' + str(stack[-3]) + ', ' +  str(stack[-2]) + '])') # action을 출력하기 위해 어떤 goto table을 이용해서 이동했는지 추가

                    n1 = number.pop()
                    n2 = number.pop()
                    number.append(n2 * n1) # result를 누적하여 계산하기 위해 number에서 pop한 두 정수를 곱한 값을 다시 number에 추가
                    
                elif(action[stack[-1]][terminal.index(input[0])] == 'R5'): # T -> T / N
                    # T, /, N와 각 token에 대한 state를 pop하고 T로 대체 (3*2 = 6개 pop)
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.pop()

                    stack.append('T') # T로 대체
                    stack.append(goto[stack[-2]][non_terminal.index(stack[-1])]) # goto table을 이용해서 이동한 state 추가
                    
                    actions.append('(Goto[' + str(stack[-3]) + ', ' +  str(stack[-2]) + '])') # action을 출력하기 위해 어떤 goto table을 이용해서 이동했는지 추가

                    n1 = number.pop()
                    n2 = number.pop()
                    number.append(n2 / n1) # result를 누적하여 계산하기 위해 number에서 pop한 두 정수를 나눈 값을 다시 number에 추가
                
                elif(action[stack[-1]][terminal.index(input[0])] == 'R6'): # T -> N
                    # N와 해당 token에 대한 state를 pop하고 T로 대체 (1*2 = 2개 pop)
                    stack.pop()
                    stack.pop()

                    stack.append('T') # T로 대체
                    stack.append(goto[stack[-2]][non_terminal.index(stack[-1])]) # goto table을 이용해서 이동한 state 추가
                    actions.append('(Goto[' + str(stack[-3]) + ', ' +  str(stack[-2]) + '])') # action을 출력하기 위해 어떤 goto table을 이용해서 이동했는지 추가
            
            elif(action[stack[-1]][terminal.index(input[0])] == 'accept'): # parsing table의 entry에서 accept가 나온 경우
                actions.append('Accept') # action을 출력하기 위해 Accept 추가
                result = number.pop() # 누적되어 마지막까지 계산된 number를 popout하여 result에 저장
                tmp = 0 # accept를 만났으니 tmp를 0으로 설정하여 while문 탈출

            state += 1 # accept를 만나지 않았다면 state를 1 증가하여 다음 state로 넘어감
            print("{:>24} |".format(' '.join(map(str, actions))), end=' ') # action은 계산 후에 출력해야 하므로 아래에서 출력
            print()
        
        print('+-------+---------------------------+---------------------------------------+--------------------------+')
        print()
        return result # result 반환
    
    # 3. Recursive Descent Parser : recursive descent parser를 구현하고 result를 출력
    # left recursion을 right recursion으로 변환하여 구현
    # E-> TE' 
    # E'-> +TE' | ε 
    # E'-> -TE' | ε
    # T-> NT'
    # T'-> *NT' | ε
    # T'-> /NT' | ε
    def recursive_descent_parser(self, lexemes, tokens):
        print('=' * 50)
        print("Start !!")
        print()
        result = self.E1(lexemes, tokens) # recursive하게 먼저 start symbol인 E를 호출
        return result

    # E -> TE'
    def E1(self, lexemes, tokens):
        print('enter E') # E에 처음 들어오면 출력
        term = self.T1(lexemes, tokens) # recursive하게 E(E1) 다음에는 바로 T(T1)가 오므로 T(T1)를 호출
        result = term + self.E2(lexemes, tokens) # recursive하게 T(T1)의 결과와 E'(E2)의 결과를 서로 더해서 result에 저장
        print('exit E') # E에서 빠져나오면 출력
        return result
    
    # E' -> +TE' | -TE' | ε
    def E2(self, lexemes, tokens): 
        print('enter E\'') # E'에 처음 들어오면 출력
        if(tokens[0] == '+'): # E' -> +TE' 인 경우
            tokens.pop(0) # + 를 pop
            lexemes.pop(0) # + 연산을 위해 lexemes에서 pop
            term = self.T1(lexemes, tokens) # recursive하게 E'(E2) 다음에는 바로 T(T1)가 오므로 T(T1)를 호출
            result = self.E2(lexemes, tokens) + term # recursive하게 T(T1)의 결과와 E'(E2)의 결과를 더하여 result에 저장
        
        elif(tokens[0] == '-'): # E' -> -TE' 인 경우
            tokens.pop(0) # - 를 pop
            lexemes.pop(0) # - 연산을 위해 lexemes에서 pop
            term = self.T1(lexemes, tokens) # recursive하게 E'(E2) 다음에는 바로 T(T1)가 오므로 T(T1)를 호출
            result = self.E2(lexemes, tokens) - term # recursive하게 T(T1)의 결과와 E'(E2)의 결과를 서로 뺄셈해서 result에 저장
        
        else: # E' -> ε 인 경우
            result = 0 # E'가 epsilon인 경우 0을 반환
            print('epsilon') # epsilon인 경우 출력
        
        print('exit E\'') # E'에서 빠져나오면 출력
        return result
    
    # T -> NT'
    def T1(self, lexemes, tokens): 
        print('enter T') # T에 처음 들어오면 출력
        number = self.N1(lexemes, tokens) # recursive하게 T(T1) 다음에는 바로 N(N1)이 오므로 N(N1)를 호출
        result = number * self.T2(lexemes, tokens) # recursive하게 N(N1)의 결과와 T'(T2)의 결과를 서로 곱하여 result에 저장
        print('exit T') # T에서 빠져나오면 출력
        return result
    
    # T' -> *NT' | /NT' | ε
    def T2(self, lexemes, tokens): 
        print('enter T\'') # T'에 처음 들어오면 출력
        if(tokens[0] == '*'): # T' -> *NT' 인 경우
            tokens.pop(0) # * 를 pop
            lexemes.pop(0) # * 연산을 위해 lexemes에서 pop
            number = self.N1(lexemes, tokens) # recursive하게 T'(T2) 다음에는 바로 N(N1)이 오므로 N(N1)를 호출
            result = self.T2(lexemes, tokens) * number # recursive하게 N(N1)의 결과와 T'(T2)의 결과를 서로 곱하여 result에 저장
    
        elif(tokens[0] == '/'): # T' -> /NT' 인 경우
            tokens.pop(0) # / 를 pop
            lexemes.pop(0) # / 연산을 위해 lexemes에서 pop
            number = self.N1(lexemes, tokens) # recursive하게 T'(T2) 다음에는 바로 N(N1)이 오므로 N(N1)를 호출
            result = self.T2(lexemes, tokens) / number # recursive하게 N(N1)의 결과와 T'(T2)의 결과를 서로 나누어 result에 저장
            
        else: # T' -> ε 인 경우
            result = 1 # T'가 epsilon인 경우 1을 반환 (곱셈이나 나눗셈에서는 덧셈과 뺄셈과 달리 1을 곱하거나 나누어야 값이 변하지 않기 때문에)
            print('epsilon') # epsilon인 경우 출력
        
        print('exit T\'') # T'에서 빠져나오면 출력
        return result
        
    def N1(self, lexemes, tokens):
        number = lexemes[0] # N(N1)은 정수이므로 lexems의 front lexeme을 number에 저장
        tokens.pop(0) # 정수를 사용했으므로 token을 pop
        lexemes.pop(0) # 정수를 사용했으므로 lexemes에서 pop
        return number 

# main driver
def main(input_file_name, problem_number):
    S = SyntaxAnalyzer() # SyntaxAnalyzer instance 생성
    lexemes, tokens = S.lexer(input_file_name) # 1. lexer를 호출하여 lexemes와 tokens를 반환받아서 저장
    
    if(problem_number == 1): #  problem_number 1. Lexical Analyzer에 대한 결과 출력
        print()
        print('Lexemes : ' + str(lexemes)) 
        print()
        print('Tokens : ' + str(tokens)) 
        print()

    elif(problem_number == 2): # problem_number 2. Shift-Reduce Parser에 대한 결과 출력
        print()
        result = S.shift_reduce_parser(lexemes, tokens) # shift-reduce parser 메소드를 통해 parsing결과를 출력하고 result를 반환받아서 저장
        if(result == int(result)): # result가 정수인 경우 깔끔한 출력을 위해 int로 변환하여 출력
            print('Result :', int(result))
            print()
        else: 
            print('Result :', result)
            print()
    
    elif(problem_number == 3): # problem_number 3. Recursive Descent Parser에 대한 결과 출력
        print() 
        result = S.recursive_descent_parser(lexemes, tokens) # recursive descent parser 메소드를 통해 parsing결과를 출력하고 result를 반환받아서 저장
        if(result == int(result)): # 마찬가지로 result가 정수인 경우 깔끔한 출력을 위해 int로 변환하여 출력
            print('Result :', int(result)) 
            print()
        else:
            print('Result :', result)
            print()
    
    else: # problem_number가 1, 2, 3이 아닌 경우 에러 출력
        print('Invalid Problem Number (Problem Number : 1~3)')
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser() # input file과 problem number를 command line을 통해 받기 위한 parser
    parser.add_argument("input_file_name", type = str) # argument1 : input file name
    parser.add_argument("problem_number", type = int) # argument2 : problem number
    args = parser.parse_args()
    input_file_name = args.input_file_name 
    problem_number = args.problem_number
    main(input_file_name, problem_number)