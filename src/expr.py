import re
import operator

class Parser:
    maxLevel = 3
    ops = {'+' : (0,  True,     operator.add),
           '-' : (0,  True,     operator.sub),
           '*' : (1,  True,     operator.mul),
           '/' : (1,  True, operator.truediv),
           '%' : (1,  True,     operator.mod),
           '^' : (2, False,     operator.pow)}
    un = {'+' : operator.pos,
          '-' : operator.neg}

    def __init__(self, s):
        self.s = s
        self.l = re.compile('\w+|\d+|[-+*/%^]').findall(s) + ['\0']
        self.i = 0
        self.x = self.l[0]

    def isLevel(self, lv):
        op = self.x
        return (op in self.ops) and (self.ops[op][0] == lv)

    def next(self):
        self.i += 1
        self.x = self.l[self.i]
        return self.l[self.i - 1]

    def parseOperator(self, lv):
        if lv > self.maxLevel:
            return self.parseTerm()
        op = self.next() if self.x in self.un and lv == self.maxLevel else None
        e = self.parseOperator(lv + 1)
        if not op is None:
            return (self.un[op], [e])
        while self.isLevel(lv):
            op = self.next()
            e = (self.ops[op][2], [e, self.parseOperator(lv + self.ops[op][1])])
            if self.ops[op][1]:
                break
        return e

    def parseTerm(self):
        if self.x == '(':
            self.next()
            r = self.parseOperator(0)
            self.next()
            return r
        elif self.x.isdigit():
            return int(self.next())
        else:
            return self.next()

def evm(e, m):
    def ev(e):
        if type(e) is int:
            return e
        if type(e) is str:
            return m[e]
        return e[0](*map(ev, e[1]))
    return ev(e)

def evsm(s, m):
    return evm(Parser(s).parseOperator(0), m)

def evs(s):
    return evsm(s, {})

print(evs("2+2"))
