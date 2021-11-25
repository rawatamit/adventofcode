from io import StringIO


class BinExpr:
    def __init__(self, op, lhs, rhs) -> None:
        super().__init__()
        self.op = op
        self.lhs = lhs
        self.rhs = rhs
        self.fn = {'+': lambda x, y: x + y,
                   '*': lambda x, y: x * y}
    
    def evaluate(self) -> int:
        return self.fn[self.op](self.lhs.evaluate(), self.rhs.evaluate())
    
    def __str__(self) -> str:
        return f'BinExpr(op={self.op}, lhs={self.lhs}, rhs={self.rhs})'


class Number:
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
    
    def evaluate(self) -> int:
        return self.value

    def __str__(self) -> str:
        return f'Number(value={self.value})'


class Parser:
    def __init__(self, stream) -> None:
        self.stream = stream
        self.c = ' '
        self.nextchar()

    def nextchar(self):
        self.c = self.stream.read(1)
        self.skipws()
        return self.c
    
    def skipws(self):
        while self.c.isspace():
            self.c = self.stream.read(1)

    def match(self, expected):
        if self.c == expected:
            return self.nextchar()
        raise Exception(f'expected {expected}, got {self.c}')
    
    parse_expr = lambda self: self.parse_expr_part2()

    def parse(self):
        return self.parse_expr()
     
    def parse_expr_part2(self):
        t = self.parse_addition()

        while self.c in ('*',):
            op = self.c
            self.match(op)
            t1 = self.parse_addition()
            t = BinExpr(op, t, t1)

        return t
    
    def parse_addition(self):
        t = self.parse_term()

        while self.c in ('+',):
            op = self.c
            self.match(op)
            t1 = self.parse_term()
            t = BinExpr(op, t, t1)
        
        return t

    def parse_expr_part1(self):
        t = self.parse_term()
        
        while self.c in ('+', '*'):
            op = self.c
            self.match(op)
            t1 = self.parse_term()
            t = BinExpr(op, t, t1)
        
        return t
    
    def parse_term(self):
        if self.c.isdigit():
            x = 0
            while self.c.isdigit():
                x = x * 10 + (ord(self.c) - ord('0'))
                self.nextchar()
            return Number(x)
        elif self.c == '(':
            self.match('(')
            ret = self.parse_expr()
            self.match(')')
            return ret
        
        raise Exception(f'parse_term has {self.c}')


def main():
    expr_values = []
    with open('d18.txt') as fin:
        for line in fin:
            if line.strip():
                parser = Parser(StringIO(line))
                expr = parser.parse()
                expr_values.append(expr.evaluate())
    
    # Change the correct parsing function in Parser class

    # part 1
    #print(sum(expr_values))

    # part 2
    print(sum(expr_values))


main()
