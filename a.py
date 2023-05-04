import sys

class Neolang:
    def __init__(self):
        self.memory = [0]*32768
        self.pointLocation = 0

    def interger(self, code):
        now_char = code[0]
        now_num = 0
        index = 0

        while now_char == '에' or now_char == '오':
            if index >= len(code):
                break

            now_char = code[index]
            if now_char == '에':
                now_num += 1
            elif now_char == '오':
                now_num -= 1
            else:
                break

            index += 1
        
        return now_num, index


    def variable(self, code):
        now_char = code[1]
        now_var = ''
        index = 1
        ne = 1
        ol = 0

        try:
            while ne > ol:
                if index >= len(code):
                    raise

                now_char = code[index]
                if now_char == '네':
                    ne += 1
                elif now_char == '올':
                    ol += 1
                    if ne == ol:
                        break
                
                index += 1
                
        except:
            print('변수 끝에 올이 없네올...')
        
        now_var = code[1:index]
        var_num = self.number(now_var)
        return self.memory[self.pointLocation + var_num], index + 1

    def number(self, code):
        output = 0
        now_add = True
        now_num = 0
        cut = 0
        try:
            while len(code) != 0:
                if code.startswith(' '):
                    now_add = False
                    cut = 1
                else:
                    if code.startswith('김혜성'):
                        now_num = int(input())
                        cut = 3
                    elif code.startswith('솔로몬'):
                        now_num = int(ord(input()))
                        cut = 3
                    elif code.startswith('네'):
                        varResult = self.variable(code)
                        now_num = varResult[0]
                        cut = varResult[1]
                    elif code.startswith('에') or code.startswith('오'):
                        intResult = self.interger(code)
                        now_num = intResult[0]
                        cut = intResult[1]
                    else:
                        raise ValueError
                    
                    if now_add:
                        output += now_num
                    else:
                        output *= now_num
                        now_add = True
                
                code = code[cut:]
            
            return output
        
        except:
            print(code + '은(는) 잘못된 수 표현이네올...')
                        

    def type(self, code):
        try:
            if '?' in code and '이' in code:
                return 'IF'
            elif '!' in code and '이' in code:
                return 'UNLESS'
            elif '이' in code:
                return 'DEF'
            elif '하네올' in code:
                return 'GOTO'
            elif '바보' in code:
                return 'PRINTINTERGER'
            elif '귀엽' in code:
                return 'PRINTASCII'
            else:
                raise
        except:
            print(code + '을(를) 이해할 수 없네올...')
        
    def compileLine(self, code):
        if code == '' or code == 'ㅎㅇ네올' or code == 'ㅂㅂ네올':
            return None
        TYPE = self.type(code)
        '''print(TYPE)'''

        if TYPE == 'DEF':
            cmd, var = code.split('이', maxsplit = 1)
            var = var.replace('네', '').replace('올', '')
            var_value = self.number(var)
            self.memory[self.pointLocation + var_value] = self.number(cmd)
            self.pointLocation += var_value

        elif TYPE == 'IF':
            cond, cmd = code.split('?', maxsplit = 1)
            tar1, tar2 = cond.split('이', maxsplit = 1)
            if self.number(tar1) == self.number(tar2):
                return cmd
            
        elif TYPE == 'UNLESS':
            cond, cmd = code.split('!', maxsplit = 1)
            tar1, tar2 = cond.split('이', maxsplit = 1)
            if self.number(tar1) != self.number(tar2):
                return cmd
            
        elif TYPE == 'GOTO':
            loc = code.replace('하네올', '')
            return self.number(loc)
        
        elif TYPE == 'PRINTINTERGER':
            value = code.replace('바보', '')
            print(self.number(value), end=" ")
        
        elif TYPE == 'PRINTASCII':
            value = code.replace('귀엽', '')
            print(chr(self.number(value)), end="")

    def compile(self, code, errors = 100000):
        index = 0
        error = 0
        errorline = 0
        needRecode = False
        recode = ''
        try:
            while index < len(code):
                errorline = index
                c = code[index].strip()
                res = self.compileLine(c)
                if needRecode:
                    needRecode = False
                    code[index] = recode
                if isinstance(res, int):
                    index = res - 2
                if isinstance(res, str):
                    recode = code[index]
                    code[index] = res
                    index -= 1
                    needRecode = True

                index += 1
                error += 1
                if error == errors:
                    raise
        except:
            print(errorline + '번째 줄이 무한 반복이네올...')

    def defineCode(self, code):
        startLine = 0
        endLine = 0
        index = 0

        try:
            while index < len(code):
                if code[index] == 'ㅎㅇ네올':
                    startLine = index
                    break

                index += 1

                if index == len(code):
                    raise
        except:
            print('왔는데 인사를 안해주네올...')

        try:
            while index < len(code):
                if code[index] == 'ㅂㅂ네올':
                    endLine = index
                    break

                index += 1

                if index == len(code):
                    raise
        except:
            print('말도 안하고 가버리면 어떡하네올...')

        self.compile(code[startLine:endLine - 1])

    def compileFile(self, path):
        try:
            with open(path, encoding='utf-8-sig') as mte_file:
                code = mte_file.read().split('\n')
                self.defineCode(code)
        except:
            print('파일을 찾을 수 없네올...')

compiler = None
filename = ''

if __name__ == '__main__':
    filename = input('.nl 파일 이름을 입력하세올')
    compiler = Neolang()
    compiler.compileFile(filename)
