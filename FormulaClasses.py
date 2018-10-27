import numpy as np
def prime(x):
    if x <= 1:
        return False
    i = 2
    while i * i <= x:
        if x % i == 0:
            return False
        i += 1
    return True

F_compute = {
    (2, 0): lambda x,y: x + y,
    (2, 1): lambda x,y: x * y,
    (0, 0): lambda : 0,
    (0, 1): lambda : 1,
    (0, 2): lambda: 2,
    (0, 3): lambda: 4,
}

P_compute = {
    (1, 0): prime,
    (2, 0): lambda x,y: x == y,
    (2, 1): lambda x,y: x >= y,
    (2, 2): lambda x,y: x > y,
    (2, 3): lambda x,y: (y != 0) and (x % y == 0),
    (0, 0): lambda : True,
    (0, 1): lambda : False,
}

def scrap_x(sent, t):
    s = 0
    t += 1
    while t < len(sent) and sent[t] == '|':
        t += 1
        s += 1
    return s
def find_arg(sent):
    arg_list = []
    for i in range(len(sent)):
        if sent[i] == 'x':
            arg_list += ['x' + '|' * scrap_x(sent, i)]
    return arg_list
def find_quanted(sent):
    arg_list = []
    for i in range(len(sent)):
        if sent[i - 1] in 'AE':
            arg_list += ['x' + '|' * scrap_x(sent, i)]
    return arg_list
def arg_out(size, sent):
    arg_list = list(np.unique(find_arg(sent)))
    if '' in arg_list:
        arg_list.remove('')
    gen_arg_out = []
    for i in arg_list:
        if len(i) + len(sent) + 2 == size and (i + '[') not in sent:
            gen_arg_out += [i + '[' + sent + ']']
    return gen_arg_out
def combs(*args):
    if len(args) == 1:
        return args[0]
    gen = []
    for first in args[0]:
        for second in combs(*args[1:]):
            gen.append(first + second)
    return gen
def gen_args(arg, size, pre=None):
    if arg == 0:
        return ['']
    if arg == 1:
        return combs([','], Term.generate(size - 1, pre))
    gen_arg = []
    for pre_size in range(1, size - 2 * (arg - 1)):
        gen_arg += combs([','],Term.generate(pre_size, pre), gen_args(arg - 1, size - pre_size - 1, pre))
    return gen_arg
def find_right_scope(line, ind):
    assert line[ind] in '[({'
    i = ind
    balance = 1
    while balance > 0:
        i += 1
        if line[i] in '([{':
            balance += 1
        if line[i] in ')]}':
            balance -= 1
    return i
def split_args(arg_line):
    if len(arg_line) == 0:
        return []
    assert arg_line[0] == ','
    balance = 0
    t = 1
    i = 1
    args = []
    while i < len(arg_line) - 1:
        i += 1
        if arg_line[i] in '([':
            balance += 1
        if arg_line[i] in ')]':
            balance -= 1
        if balance == 0 and arg_line[i] == ',':
            args.append(arg_line[t:i])
            i += 1
            t = i
    args.append(arg_line[t:len(arg_line)])
    return args
class UnitFormula:
    @classmethod
    def generate(cls, size, pre=None):
        if pre is not None and size < len(pre.terms):
            return pre.terms[size]
        gen = []
        for subcls in cls.__subclasses__():
            gen += subcls.generate(size, pre)
        return gen
    @classmethod
    def check(cls, line):
        checked = False
        for subcls in cls.__subclasses__():
            checked = checked or subcls.check(line)
        return checked
    @classmethod
    def parse(cls, line):
        if type(line) != str:
            return line
        if line[0] == '{':
            return Placeholder.parse(line)
        for subcls in cls.__subclasses__():
            if subcls.check(line):
                return subcls.parse(line)
        raise SyntaxError("Cannot parse {}".format(line))
    @staticmethod
    def check_x_range(line):
        xs = set([len(i) - 1 for i in find_arg(line)])
        if len(xs) == 0:
            return True
        minx, maxx = min(xs), max(xs)
        return minx == 0 and maxx == len(xs) - 1
    @staticmethod
    def check_has_free(line):
        xs = find_arg(line)
        con_xs = find_quanted(line)
        return len(set(xs) - set(con_xs)) > 0
    @staticmethod
    def check_double_inv(line):
        return '[%-%[%-%' in line
    @staticmethod
    def is_const_expression(line):
        return len(find_arg(line)) == 0
    @staticmethod
    def check_ok(line, check_x_range=False, check_free=False, check_double_inv=False, check_correct=False):
        return (UnitFormula.check_x_range(line) or not check_x_range) and \
               (not UnitFormula.check_has_free(line) or not check_free) and \
               (not UnitFormula.check_double_inv(line) or not check_double_inv) and \
               (not check_correct or Predicate.is_correct(line))

class Term(UnitFormula):
    @classmethod
    def generate(cls, size, pre=None):
        if pre is not None and size < len(pre.terms):
            return pre.terms[size]
        gen = []
        for subcls in cls.__subclasses__():
            gen += subcls.generate(size, pre)
        return gen
    @classmethod
    def check(cls, line):
        checked = False
        for subcls in cls.__subclasses__():
            checked = checked or subcls.check(line)
        return checked
    @classmethod
    def parse(cls, line):
        if line[0] == '{':
            return Placeholder.parse(line)
        for subcls in cls.__subclasses__():
            if subcls.check(line):
                return subcls.parse(line)
        raise SyntaxError("Cannot parse {}".format(line))
class X(Term):
    @classmethod
    def generate(cls, size, pre=None):
        return ['x' + '|' * (size - 1)]
    @classmethod
    def check(cls, line):
        return line[0] == 'x'
    @classmethod
    def parse(cls, line):
        assert cls.check(line)
        i = 1
        while i < len(line) and line[i] == '|':
            i += 1
        return X(i - 1)
    def __init__(self, num):
        self.num = num
    def __str__(self):
        return 'x' + '|' * self.num
class F(Term):
    @classmethod
    def generate(cls, size, pre=None):
        gen = []
        for num in range(size):
            for arg in range(size):
                if arg == 0:
                    if num == size - 4:
                        gen += ['F;' + '|' * num + '()']
                    continue
                if 4 + num + 3 * arg > size:
                    break
                pre_str = ['F' + '|' * arg + ';' + '|' * num + '(']
                gen += combs(pre_str, gen_args(arg, size - len(pre_str[0]) - 1, pre), [')'])
        return gen
    @classmethod
    def parse(cls, line):
        assert cls.check(line)
        i = line.find(';') + 1
        count = 0
        while i < len(line) and line[i] == '|':
            count += 1
            i += 1
        num = count
        arg_line = line[i + 1 : find_right_scope(line, i)]
        args = split_args(arg_line)
        return F(num, [Term.parse(arg) for arg in args])
    @classmethod
    def check(cls, line):
        return line[0] == 'F'
    def __init__(self, num, params):
        self.num = num
        self.arg_size = len(params)
        self.args = params
    def __str__(self):
        return 'F' + '|' * self.arg_size + ';' + '|' * self.num + '({})'.format(''.join([',' + str(i) for i in self.args]))
    def get_computer(self):
        tup = (self.arg_size, self.num)
        if tup not in F_compute:
            raise KeyError("{} not computable".format(str(self)))
        return F_compute[tup]
    def compute(self):
        func = self.get_computer()
        return func(*[i.compute() for i in self.args])
class Predicate(UnitFormula):
    @classmethod
    def generate(cls, size, pre=None):
        if (size < 4):
            return []
        if pre is not None and size < len(pre.predicates):
            return pre.predicates[size]
        gen = []
        for subcls in cls.__subclasses__():
            gen += subcls.generate(size, pre)
        return gen
    @classmethod
    def check(cls, line):
        checked = False
        for subcls in cls.__subclasses__():
            checked = checked or subcls.check(line)
        return checked
    @classmethod
    def parse(cls, line):
        if line[0] == '{':
            return Placeholder.parse(line)
        for subcls in cls.__subclasses__():
            if subcls.check(line):
                return subcls.parse(line)
        raise SyntaxError("Cannot parse given line")
    @classmethod
    def is_correct(cls, line):
        if not Predicate.check(str(line)):
            raise TypeError('{} not a predicate'.format(line))
        if not UnitFormula.is_const_expression(str(line)):
            return True
        line = UnitFormula.parse(line)
        return line.compute()

class P(Predicate):
    @classmethod
    def generate(cls, size, pre=None):
        gen = []
        for num in range(size):
            for arg in range(size):
                if arg == 0:
                    if num == size - 4:
                        gen += ['P;' + '|' * num + '()']
                    continue
                if 4 + num + 3 * arg > size:
                    break
                pre_str = ['P' + '|' * arg + ';' + '|' * num + '(']
                gen += combs(pre_str, gen_args(arg, size - len(pre_str[0]) - 1, pre), [')'])
        return gen
    @classmethod
    def parse(cls, line):
        assert cls.check(line)
        i = line.find(';') + 1
        count = 0
        while i < len(line) and line[i] == '|':
            count += 1
            i += 1
        num = count
        arg_line = line[i + 1 : find_right_scope(line, i)]
        args = split_args(arg_line)
        return P(num, [Term.parse(arg) for arg in args])
    @classmethod
    def check(cls, line):
        return line[0] == 'P'
    def __init__(self, num, params):
        self.num = num
        self.arg_size = len(params)
        self.args = params
        self.type = 'P'
    def __str__(self):
        return 'P' + '|' * self.arg_size + ';' + '|' * self.num + '({})'.format(''.join([',' + str(i) for i in self.args]))
    def get_computer(self):
        tup = (self.arg_size, self.num)
        if tup not in P_compute:
            raise KeyError('{} not computable')
        return P_compute[tup]
    def compute(self):
        func = self.get_computer()
        return func(*[i.compute() for i in self.args])
class WrapPredicate(Predicate):
    @classmethod
    def generate(cls, size, pre=None):
        if pre is not None and size < len(pre.predicates):
            return pre.predicates[size]
        gen = []
        for subcls in cls.__subclasses__():
            gen += subcls.generate(size, pre)
        return gen
    @classmethod
    def check(cls, line):
        checked = False
        for subcls in cls.__subclasses__():
            checked = checked or subcls.check(line)
        return checked
    @classmethod
    def parse(cls, line):
        for subcls in cls.__subclasses__():
            if subcls.check(line):
                return subcls.parse(line)
        raise SyntaxError("Cannot parse given line")
class AWrap(WrapPredicate):
    @classmethod
    def generate(cls, size, pre=None):
        gen_quantA = []
        for i in range(4, size - 5):
            pA = Predicate.generate(i, pre)
            for t in pA:
                gen_quantA += combs(['[%A%'], arg_out(size - 3, t), [']'])
        return gen_quantA
    @classmethod
    def check(cls, line):
        return line[1:4] == '%A%'
    @classmethod
    def parse(cls, line):
        assert cls.check(line)
        left_scope_ind = line[1:].find('[') + 1
        right_scope_ind = find_right_scope(line, left_scope_ind)
        x_param = line[4:left_scope_ind]
        predicate = line[left_scope_ind + 1:right_scope_ind]
        return AWrap(X.parse(x_param), Predicate.parse(predicate))
    def __init__(self, x_param, predicate):
        self.x = x_param
        self.predicate = predicate
    def __str__(self):
        return '[%A%{}[{}]]'.format(str(self.x), str(self.predicate))
class EWrap(WrapPredicate):
    @classmethod
    def generate(cls, size, pre=None):
        gen_quantA = []
        for i in range(4, size - 5):
            pA = Predicate.generate(i, pre)
            for t in pA:
                gen_quantA += combs(['[%E%'], arg_out(size - 3, t), [']'])
        return gen_quantA
    @classmethod
    def check(cls, line):
        return line[1:4] == '%E%'
    @classmethod
    def parse(cls, line):
        assert cls.check(line)
        left_scope_ind = line[1:].find('[') + 1
        right_scope_ind = find_right_scope(line, left_scope_ind)
        x_param = line[4:left_scope_ind]
        predicate = line[left_scope_ind + 1:right_scope_ind]
        return EWrap(Term.parse(x_param), Predicate.parse(predicate))
    def __init__(self, x_param, predicate):
        self.x = x_param
        self.predicate = predicate
    def __str__(self):
        return '[%E%{}[{}]]'.format(str(self.x), str(self.predicate))
class InvWrap(WrapPredicate):
    @classmethod
    def generate(cls, size, pre=None):
        return combs(['[%-%'], Predicate.generate(size - 3, pre), [']'])
    @classmethod
    def check(cls, line):
        return line[1:4] == '%-%'
    @classmethod
    def parse(cls, line):
        assert cls.check(line)
        predicate = line[4:-1]
        return InvWrap(UnitFormula.parse(predicate))
    def __init__(self, predicate):
        self.predicate = predicate
    def __str__(self):
        return '[%-%{}]'.format(str(self.predicate))
    def compute(self):
        return not self.predicate.compute()
class BinAndWrap(WrapPredicate):
    @classmethod
    def generate(cls, size, pre=None):
        gen_and = []
        for i in range(4, size - 6):
            p1 = Predicate.generate(i, pre)
            p2 = Predicate.generate(size - 3 - i, pre)
            gen_and += combs('[', p1, ['%&%'], p2, ']')
        return gen_and
    @classmethod
    def check(cls, line):
        balance = 0
        i = 1
        while i < len(line):
            if line[i] in '[(':
                balance += 1
            if line[i] in ')]':
                balance -= 1
            if balance == 0 and line[i:i+3] == '%&%':
                return True
            i += 1
        return False
    @classmethod
    def parse(cls, line):
        balance = 0
        i = 1
        while i < len(line):
            if line[i] in '[(':
                balance += 1
            if line[i] in ')]':
                balance -= 1
            if balance == 0 and line[i:i+3] == '%&%':
                return BinAndWrap(Predicate.parse(line[1:i]), Predicate.parse(line[i+3:-1]))
            i += 1
        assert False
    def __init__(self, first, second):
        self.p1 = first
        self.p2 = second
    def __str__(self):
        return '[{}%&%{}]'.format(str(self.p1), str(self.p2))
    def compute(self):
        return self.p1.compute() and self.p2.compute()
class BinOrWrap(WrapPredicate):
    @classmethod
    def generate(cls, size, pre=None):
        gen_and = []
        for i in range(4, size - 6):
            p1 = Predicate.generate(i, pre)
            p2 = Predicate.generate(size - 3 - i, pre)
            gen_and += combs('[', p1, ['%v%'], p2, ']')
        return gen_and
    @classmethod
    def check(cls, line):
        balance = 0
        i = 1
        while i < len(line):
            if line[i] in '[(':
                balance += 1
            if line[i] in ')]':
                balance -= 1
            if balance == 0 and line[i:i+3] == '%v%':
                return True
            i += 1
        return False
    @classmethod
    def parse(cls, line):
        balance = 0
        i = 1
        while i < len(line):
            if line[i] in '[(':
                balance += 1
            if line[i] in ')]':
                balance -= 1
            if balance == 0 and line[i:i+3] == '%v%':
                return BinOrWrap(Predicate.parse(line[1:i]), Predicate.parse(line[i+3:-1]))
            i += 1
        assert False
    def __init__(self, first, second):
        self.p1 = first
        self.p2 = second
    def __str__(self):
        return '[{}%v%{}]'.format(str(self.p1), str(self.p2))
    def compute(self):
        return self.p1.compute() and self.p2.compute()

class Evolution:
    def __init__(self, terms, predicates):
        self.terms = terms
        self.predicates = predicates
    @staticmethod
    def generate(size):
        ev = Evolution([], [])
        res_predicates = []
        for i in range(size + 1):
            tts = Term.generate(i, ev)
            preds = Predicate.generate(i, ev)
            ev.terms.append(tts)
            ev.predicates.append(preds)
            res_predicates += ev.predicates[i]
        return [str(i) for i in res_predicates]
    @staticmethod
    def trans_generate(translator, size, check_untranslatable=False, check_x_range=False, check_free=False, check_double_inv=False, check_correct=False, do_translation=True, verbose=False):
        ev = Evolution([], [])
        res_predicates = []
        for i in range(size + 1):
            tts = Term.generate(i, ev)
            preds = Predicate.generate(i, ev)
            ev.terms.append(translator.clear_gen(tts, check_untranslatable, check_x_range))
            ev.predicates.append([i for i in translator.clear_gen(preds, check_untranslatable, check_x_range) if UnitFormula.check_ok(i,check_double_inv = check_double_inv,check_x_range=check_x_range, check_correct=check_correct)])
            add_predicates = [i for i in ev.predicates[i] if UnitFormula.check_ok(i, check_free=check_free)]
            res_predicates += add_predicates
            if verbose:
                print('Size {} done'.format(i))
        if do_translation:
            return translator.translate_gen(res_predicates)
        else:
            return res_predicates
class Placeholder:
    def __init__(self, name):
        self.name = name.strip('{').strip('}')
    @classmethod
    def parse(cls, line):
        right = find_right_scope(line, 0)
        return Placeholder(line[1:right])
    def __str__(self):
        return '{' + self.name + '}'
class Interpretation:
    def __init__(self, origin, result):
        self.origin = UnitFormula.parse(origin)
        self.result = result
class Translation:
    def __init__(self):
        self.dict = {}
        self.valid = True
    @staticmethod
    def build(interp, arg):
        trans = Translation()
        trans.scan(interp, arg)
        return trans
    def scan(self, interp, arg):
        if not self.valid:
            return
        if type(interp) == Placeholder:
            if interp.name in self.dict and self.dict[interp.name] != str(arg):
                self.valid = False
                return
            self.dict[interp.name] = str(arg)
            return
        if not Translator.match(interp, arg):
            self.valid = False
            return
        if type(arg) in (F, P):
            for i in range(arg.arg_size):
                self.scan(interp.args[i], arg.args[i])
            return

        elif type(arg) in (AWrap, EWrap):
            self.scan(interp.x, arg.x)
            self.scan(interp.predicate, arg.predicate)
            return
        elif type(arg) == InvWrap:
            self.scan(interp.predicate, arg.predicate)
            return
        elif type(arg) in (BinAndWrap, BinOrWrap):
            self.scan(interp.p1, arg.p1)
            self.scan(interp.p2, arg.p2)
            return
        raise Exception("Something definitely went wrong with {} and {}".format(interp, arg))
class Translator:
    def __init__(self, lang):
        self.lang = lang
    @staticmethod
    def match(a, b):
        if type(a) == type(b):
            if type(a) in {F, P}:
                if a.arg_size == b.arg_size and a.num == b.num:
                    return True
                return False
            if type(a) == X:
                if a.num == b.num:
                    return True
                return False
            return True
        return False
    def use_interpretation(self, interp, arg, check_untranslatable=False):
        trans = Translation.build(interp.origin, arg)
        if trans.valid:
            for key in trans.dict:
                trans.dict[key] = self.translate(trans.dict[key], check_untranslatable)
            return interp.result.format(**trans.dict)
        else:
            if check_untranslatable:
                return '#'
            else:
                return arg
    def translate(self, arg, check_untranslatable=False):
        #print(arg)
        if type(arg) == str:
            arg = UnitFormula.parse(arg)
        for interp in self.lang.interpretations:
            if Translator.match(interp.origin, arg):
                t = str(self.use_interpretation(interp, arg, check_untranslatable))
                if t == '#':
                    continue
                return t
        if type(arg) in (F, P):
            if check_untranslatable:
                return '#'
            return str(type(arg)(arg.num, [self.translate(i, check_untranslatable) for i in arg.args]))
        elif type(arg) in (AWrap, EWrap):
            return str(type(arg)(self.translate(arg.x, check_untranslatable), self.translate(arg.predicate, check_untranslatable)))
        elif type(arg) == InvWrap:
            return str(type(arg)(self.translate(arg.predicate, check_untranslatable)))
        elif type(arg) in (BinAndWrap, BinOrWrap):
            return str(type(arg)(self.translate(arg.p1, check_untranslatable), self.translate(arg.p2, check_untranslatable)))
        return str(arg)
    def translate_gen(self, gen, check_untranslatable=False, check_x_range=False):
        ans = []
        for i in gen:
            t = self.translate(i, check_untranslatable)
            if (check_untranslatable and '#' in t) or (check_x_range and not UnitFormula.check_x_range(str(i)) and not X.check(i)):
                continue
            ans.append(str(t))
        return ans
    def clear_gen(self, gen, check_untranslatable=False, check_x_range=False):
        ans = []
        for i in gen:
            t = self.translate(i, check_untranslatable)
            if (check_untranslatable and '#' in t) or (check_x_range and not UnitFormula.check_x_range(str(i)) and not X.check(i)):
                continue
            ans.append(str(i))
        return ans
class Lang:
    def __init__(self, interps):
        self.interpretations = interps
    @staticmethod
    def open(filename):
        text = open(filename, 'r').read().split('\n')
        interps = []
        for line in text:
            if line == '' or line[0] == '#':
                continue
            func, translate = line[:line.find('=')].strip(' '), line[line.find('=') + 1:].strip(' ')
            interps.append(Interpretation(func, translate))
        return Lang(interps)
