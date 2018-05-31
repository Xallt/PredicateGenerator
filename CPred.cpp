#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

vector<int> get_pi(string s) {
	vector<int> pi(s.size(), 0);
	for (int i = 1; i < pi.size(); ++i) {
		int q = pi[i - 1];
		while (q > 0 && s[q] != s[i])
			q = pi[q - 1];
		if (q > 0)
			pi[i] = q;
		if (s[q] == s[i])
			++pi[i];
	}
	return pi;
}

bool has_substr(string s, string sub) {
	vector<int> pi = get_pi(sub + '#' + s);
	for (int i = 0; i < pi.size(); ++i)
		if (pi[i] == a.size())
			return 1;
	return 0;
}

template <class T>
bool has_char(string ar, char elem) {
	for (int i = 0; i < ar.size(); ++i)
		if (ar[i] == elem)
			return 1;
	return 0;
}

vector<string> scrap_x(string sent, int t) {
	s = 0;
	t += 1;
	while t < len(sent) and sent[t] == '|' {
		t += 1;
		s += 1;
	}
	return s;
}
vector<string> find_arg(string sent) {
	vector<string> arg_list;
	for (int i = 0; i < sent.size(); ++i) {
		if (sent[i] == 'x')
			arg_list.push_back("x" + string(scrap_x(sent, i), '|'));
	}
	return arg_list;
}
vector<string> find_quanted(string sent) {
	vector<string> arg_list;
	for (int i = 0; i < sent.size(); ++i) {
		if (sent[i - 1] == 'A' || sent[i - 1] == 'E') :
			arg_list.push_back("x" + string(scrap_x(sent, i), '|'));
	}
	return arg_list
}
vector<string> arg_out(int size, string sent) {
	arg_list = find_arg(sent);
	arg_list.resize(unique(arg_list.begin(), arg_list.end()));
	if (count(arg_list.begin(), arg_list.end(), ""))
		arg_list.erase("");
	vector<string> gen_arg_out;
	for (string i : arg_list) {
		if (i.size() + sent.size() + 2 == size && has_substr(sent, i + "["))
			gen_arg_out.push_back(i + "[" + sent + "]");
	}
	return gen_arg_out;
}

template <class T>
vector<T> concatenate(vector<T> &a, vector<T> &b) {
	vector<T> c;
	for (int i = 0; i < a.size(); ++i)
		c.push_back(a[i]);
	for (int i = 0; i < b.size(); ++i)
		c.push_back(b[i]);
	return c;
}
template <class T>
void add(vector<T> &a, vector<t> &b) {
	for (int i = 0; i < b.size(); ++i)
		a.push_back(b[i]);
}

template <class T>
vector<T> slice(vector<T> &a, int l, int r = 1 << 30) {
	vector<T> c;
	if (l < 0)
		l += a.size();
	if (r < 0)
		r += a.size();
	for (int i = max(l, 0), i < min(a.size(), r); ++i)
		c.push_back(a[i]);
	return c;
}

template <class T>
vector<T> combs(vector<vector<T>> &args) {
	if (args.size() == 1)
		return args[0];
	vector<T> gen;
	for (auto first : args[0]) {
		for (auto second : combs(slice(args, 1)))
			gen.push_back(concatenate(first, second));
		return gen;
	}
}
vector<string> gen_args(int arg, int size, Evolution *pre = nullptr) {
	if (arg == 0)
		return vector<string>(1, "");
	if (arg == 1)
		return combs([','], Term.generate(size - 1, pre));
	vector<string> gen_arg;
	for (pre_size = 1; pre_size < size - 2 * (arg - 1); ++pre_size)
		add(gen_arg, combs(vector<string>(1, ","), Term.generate(pre_size, pre), gen_args(arg - 1, size - pre_size - 1, pre)));
	return gen_arg;
}
int find_right_scope(string line, int ind) {
	int i = ind;
	int balance = 1;
	while (balance > 0) {
		i += 1;
		if (has_char("([{", line[i]))
			++balance;
		if (line[i] in ')]}')
			--balance;
	}
	return i;
}
vector<string> split_args(string arg_line) {
	if (len(arg_line) == 0)
		return vector<string>();
	int balance = 0,
		t = 1,
		i = 1;
	vector<string> args;
	while (i < len(arg_line) - 1) {
		++i;
		if (has_char("([{", arg_line[i]))
			++balance;
		if (has_char(")]}", arg_line[i]))
			--balance;
		if (balance == 0 && arg_line[i] == ',') :
			args.append(slice(arg_line, t, i));
		++i;
		t = i;
	}
	args.append(slice(arg_line, t, arg_line.size()));
	return args;
}
class UnitFormula {
public:
	static vector<string> generate(int size, Evolution *pre = nullptr) {
		if (pre != nullptr && size < pre->size())
			return concatenate(pre->terms[size], pre->predicates[size]);
		return concatenate(Term.generate(size, pre), Predicate.generate(size, pre));
	}
	static bool check(string line) {
		return Term.check(line) || Predicate.check(line);
	}
	static UnitFormula parse(string line) {
		if (line[0] == '{')
			return Placeholder.parse(line);
		if (Predicate.check(line))
			return Predicate.parse(line);
		if (Term.check(line))
			return Term.parse(line);
		throw exception("Cannot parse " + line);
	}
	static bool check_x_range(string line) {
		vector<string> xs = find_arg(line);
		if (xs.size() == 0)
			return 1;
		minx, maxx = line.size(), -1;
		for (int i = 0; i < xs.size(); ++i)
			minx = min(minx, xs[i].size() - 1), maxx = max(maxx, xs[i].size() - 1);
		return minx == 0 and maxx == len(xs) - 1;
	}
	static bool check_has_free(string line) {
		xs = find_arg(line);
		con_xs = find_quanted(line);
		set<int> c;
		for (int i = 0; i < xs.size(); ++i)
			c.insert(xs[i].size());
		for (int i = 0; i < con_xs.size(); ++i)
			if (c.count(con_xs[i].size()))
				c.erase(con_xs[i].size());
		return c.size() > 0;
	}
}
class Term : public UnitFormula {
	static vector<string> generate(int size, Evolution *pre = nullptr) {
		if (pre != nullptr && size < pre->size()) :
			return pre->terms[size];
		return concatenate(X.generate(size, pre), F.generate(size, pre));
	}
	static bool check(string line) {
		return X.check(line) || F.check(line);
	}
	static UnitFormula parse(string line) {
		if (line[0] == '{')
			return Placeholder.parse(line);
		if (F.check(line))
			return F.parse(line);
		if (X.check(line))
			return X.parse(line);
		throw exception("Cannot parse given line");
	}
}
class X(Term) {
	static vector<string> generate(int size, Evolution pre = nullptr) {
		return vector<string>(1, "x" + string(size - 1, '|'));
	}
	static bool check(string line) {
		return line[0] == 'x';
	}
	static UnitFormula parse(cls, line) {
		assert cls.check(line)
			i = 1
			while i < len(line) and line[i] == '|' :
		i += 1
			return X(i - 1)
			def __init__(self, num) :
			self.num = num
	}
	string to_string() {
		return "x" + string(this->num, '|');
	}
}
class F(Term) {
	static vector<string> generate(int size, Evolution pre = nullptr) {
		vector<string> gen;
		for num in range(size) {
			for arg in range(size) {
				if (arg == 0) {
					if (num == size - 4)
						gen.push_back("F;" + string(num, '|') + "()");
					continue;
				}
				if (4 + num + 3 * arg > size)
					break;
				vector<string> pre_str(1, "F" + string(arg, '|') + ";" + string(num, '|') + "(");

				vector<vector<string>> to_add;
				to_add.push_back(pre_str);
				to_add.push_back(gen_args(arg, size - pre_str[0].size() - 1, pre));
				to_add.push_back(vector<string>(1, ")"));

				add(gen, combs(to_add));
			}
		}
		return gen;
	}
	static UnitFormula parse(string line) {
			i = line.find(';') + 1
			count = 0
			while i < len(line) and line[i] == '|' :
		count += 1
			i += 1
			num = count
			arg_line = line[i + 1:find_right_scope(line, i)]
			args = split_args(arg_line)
			return F(num, [Term.parse(arg) for arg in args])
	}
			@classmethod
			def check(cls, line) :
			return line[0] == 'F'
			def __init__(self, num, params) :
			self.num = num
			self.arg_size = len(params)
			self.args = params
			def __str__(self) :
			return 'F' + '|' * self.arg_size + ';' + '|' * self.num + '({})'.format(''.join([',' + str(i) for i in self.args]))
}
		class Predicate(UnitFormula) :
		@classmethod
		def generate(cls, size, pre = None) :
		if (size < 4) :
			return[]
			if pre is not None and size < len(pre.predicates) :
				return pre.predicates[size]
				gen = []
				for subcls in cls.__subclasses__() :
					gen += subcls.generate(size, pre)
					return gen
					@classmethod
					def check(cls, line) :
					checked = False
					for subcls in cls.__subclasses__() :
						checked = checked or subcls.check(line)
						return checked
						@classmethod
						def parse(cls, line) :
						if line[0] == '{' :
							return Placeholder.parse(line)
							for subcls in cls.__subclasses__() :
								if subcls.check(line) :
									return subcls.parse(line)
									raise SyntaxError("Cannot parse given line")
									class P(Predicate) :
									@classmethod
									def generate(cls, size, pre) :
									gen = []
									for num in range(size) :
										for arg in range(size) :
											if arg == 0 :
												if num == size - 4 :
													gen += ['P;' + '|' * num + '()']
													continue
													if 4 + num + 3 * arg > size:
break
pre_str = ['P' + '|' * arg + ';' + '|' * num + '(']
gen += combs(pre_str, gen_args(arg, size - len(pre_str[0]) - 1, pre), [')'])
return gen
@classmethod
def parse(cls, line) :
	assert cls.check(line)
	i = line.find(';') + 1
	count = 0
	while i < len(line) and line[i] == '|' :
		count += 1
		i += 1
		num = count
		arg_line = line[i + 1:find_right_scope(line, i)]
		args = split_args(arg_line)
		return P(num, [Term.parse(arg) for arg in args])
		@classmethod
		def check(cls, line) :
		return line[0] == 'P'
		def __init__(self, num, params) :
		self.num = num
		self.arg_size = len(params)
		self.args = params
		self.type = 'P'
		def __str__(self) :
		return 'P' + '|' * self.arg_size + ';' + '|' * self.num + '({})'.format(''.join([',' + str(i) for i in self.args]))
		class WrapPredicate(Predicate) :
		@classmethod
		def generate(cls, size, pre = None) :
		if pre is not None and size < len(pre.predicates) :
			return pre.predicates[size]
			gen = []
			for subcls in cls.__subclasses__() :
				gen += subcls.generate(size, pre)
				return gen
				@classmethod
				def check(cls, line) :
				checked = False
				for subcls in cls.__subclasses__() :
					checked = checked or subcls.check(line)
					return checked
					@classmethod
					def parse(cls, line) :
					for subcls in cls.__subclasses__() :
						if subcls.check(line) :
							return subcls.parse(line)
							raise SyntaxError("Cannot parse given line")
							class AWrap(WrapPredicate) :
							@classmethod
							def generate(cls, size, pre = None) :
							gen_quantA = []
							for i in range(4, size - 5) :
								pA = Predicate.generate(i, pre)
								for t in pA :
gen_quantA += combs(['[A'], arg_out(size - 3, t), [']'])
return gen_quantA
@classmethod
def check(cls, line) :
	return line[1] == 'A'
	@classmethod
	def parse(cls, line) :
	assert cls.check(line)
	left_scope_ind = line[1:].find('[') + 1
	right_scope_ind = find_right_scope(line, left_scope_ind)
	x_param = line[2:left_scope_ind]
	predicate = line[left_scope_ind + 1:right_scope_ind]
	return AWrap(X.parse(x_param), Predicate.parse(predicate))
	def __init__(self, x_param, predicate) :
	self.x = x_param
	self.predicate = predicate
	def __str__(self) :
	return '[A{}[{}]]'.format(str(self.x), str(self.predicate))
	class EWrap(WrapPredicate) :
	@classmethod
	def generate(cls, size, pre = None) :
	gen_quantA = []
	for i in range(4, size - 5) :
		pA = Predicate.generate(i, pre)
		for t in pA :
gen_quantA += combs(['[E'], arg_out(size - 3, t), [']'])
return gen_quantA
@classmethod
def check(cls, line) :
	return line[1] == 'E'
	@classmethod
	def parse(cls, line) :
	assert cls.check(line)
	left_scope_ind = line[1:].find('[') + 1
	right_scope_ind = find_right_scope(line, left_scope_ind)
	x_param = line[2:left_scope_ind]
	predicate = line[left_scope_ind + 1:right_scope_ind]
	return EWrap(Term.parse(x_param), Predicate.parse(predicate))
	def __init__(self, x_param, predicate) :
	self.x = x_param
	self.predicate = predicate
	def __str__(self) :
	return '[E{}[{}]]'.format(str(self.x), str(self.predicate))
	class InvWrap(WrapPredicate) :
	@classmethod
	def generate(cls, size, pre = None) :
	return combs(['[-'], Predicate.generate(size - 3, pre), [']'])
	@classmethod
	def check(cls, line) :
	return line[1] == '-'
	@classmethod
	def parse(cls, line) :
	assert cls.check(line)
	predicate = line[2:-1]
	return InvWrap(predicate)
	def __init__(self, predicate) :
	self.predicate = predicate
	def __str__(self) :
	return '[-{}]'.format(str(self.predicate))
	class BinAndWrap(WrapPredicate) :
	@classmethod
	def generate(cls, size, pre = None) :
	gen_and = []
	for i in range(4, size - 6) :
		p1 = Predicate.generate(i, pre)
		p2 = Predicate.generate(size - 3 - i, pre)
		gen_and += combs('[', p1, '&', p2, ']')
		return gen_and
		@classmethod
		def check(cls, line) :
		balance = 0
		i = 1
		while i < len(line) :
			if line[i] in '[(' :
				balance += 1
				if line[i] in ')]' :
					balance -= 1
					if balance == 0 and line[i] == '&' :
						return True
						i += 1
						return False
						@classmethod
						def parse(cls, line) :
						balance = 0
						i = 1
						while i < len(line) :
							if line[i] in '[(' :
								balance += 1
								if line[i] in ')]' :
									balance -= 1
									if balance == 0 and line[i] == '&' :
										return BinAndWrap(Predicate.parse(line[1:i]), Predicate.parse(line[i + 1:-1]))
										i += 1
										assert False
										def __init__(self, first, second) :
										self.p1 = first
										self.p2 = second
										def __str__(self) :
										return '[{}&{}]'.format(str(self.p1), str(self.p2))
										class BinOrWrap(WrapPredicate) :
										@classmethod
										def generate(cls, size, pre = None) :
										gen_and = []
										for i in range(4, size - 6) :
											p1 = Predicate.generate(i, pre)
											p2 = Predicate.generate(size - 3 - i, pre)
											gen_and += combs('[', p1, 'v', p2, ']')
											return gen_and
											@classmethod
											def check(cls, line) :
											balance = 0
											i = 1
											while i < len(line) :
												if line[i] in '[(' :
													balance += 1
													if line[i] in ')]' :
														balance -= 1
														if balance == 0 and line[i] == 'v' :
															return True
															i += 1
															return False
															@classmethod
															def parse(cls, line) :
															balance = 0
															i = 1
															while i < len(line) :
																if line[i] in '[(' :
																	balance += 1
																	if line[i] in ')]' :
																		balance -= 1
																		if balance == 0 and line[i] == 'v' :
																			return BinOrWrap(Predicate.parse(line[1:i]), Predicate.parse(line[i + 1:-1]))
																			i += 1
																			assert False
																			def __init__(self, first, second) :
																			self.p1 = first
																			self.p2 = second
																			def __str__(self) :
																			return '[{}v{}]'.format(str(self.p1), str(self.p2))
																			class Evolution :
																			def __init__(self, terms, predicates) :
																			self.terms = terms
																			self.predicates = predicates
																			@staticmethod
																			def generate(size, translator = None, check_untranslatable = False, check_x_range = False, check_free = False) :
																			ev = Evolution([], [])
																			res_predicates = []
																			for i in range(size + 1) :
																				tts = Term.generate(i, ev)
																				preds = Predicate.generate(i, ev)
																				ev.terms.append(translator.clear_gen(tts, check_untranslatable, check_x_range))
																				ev.predicates.append(translator.clear_gen(preds, check_untranslatable, check_x_range))
																				add_predicates = ev.predicates[i]
																				if check_free:
add_predicates = [i for i in add_predicates if not UnitFormula.check_has_free(i)]
res_predicates += add_predicates
return res_predicates
@staticmethod
def trans_generate(translator, size, check_untranslatable = False, check_x_range = False, check_free = False) :
	ev = Evolution([], [])
	res_predicates = []
	for i in range(size + 1) :
		tts = Term.generate(i, ev)
		preds = Predicate.generate(i, ev)
		ev.terms.append(translator.clear_gen(tts, check_untranslatable, check_x_range))
		ev.predicates.append(translator.clear_gen(preds, check_untranslatable, check_x_range))
		add_predicates = ev.predicates[i]
		if check_free:
add_predicates = [i for i in add_predicates if not UnitFormula.check_has_free(i)]
res_predicates += add_predicates
return translator.translate_gen(res_predicates)

class Placeholder :
	def __init__(self, name) :
	self.name = name.strip('{').strip('}')
	@classmethod
	def parse(cls, line) :
	right = find_right_scope(line, 0)
	return Placeholder(line[1:right])
	def __str__(self) :
	return '{' + self.name + '}'
	class Interpretation :
	def __init__(self, origin, result) :
	self.origin = UnitFormula.parse(origin)
	self.result = result
	class Translation :
	def __init__(self) :
	self.dict = {}
	self.valid = True
	@staticmethod
	def build(interp, arg) :
	trans = Translation()
	trans.scan(interp, arg)
	return trans
	def scan(self, interp, arg) :
	if not self.valid :
		return
		if type(interp) == Placeholder :
			if interp.name in self.dict and self.dict[interp.name] != str(arg) :
				self.valid = False
				return
				self.dict[interp.name] = str(arg)
				return
				if not Translator.match(interp, arg) :
					self.valid = False
					return
					if type(arg) in(F, P) :
						for i in range(arg.arg_size) :
							self.scan(interp.args[i], arg.args[i])
							return

							elif type(arg) in(AWrap, EWrap) :
							self.scan(interp.x, arg.x)
							self.scan(interp.predicate, arg.predicate)
							return
							elif type(arg) == InvWrap :
							self.scan(interp.predicate, arg.predicate)
							return
							elif type(arg) in(BinAndWrap, BinOrWrap) :
							self.scan(interp.p1, arg.p1)
							self.scan(interp.p2, arg.p2)
							return
							raise Exception("Something definitely went wrong")
							class Translator :
							def __init__(self, lang) :
							self.lang = lang
							@staticmethod
							def match(a, b) :
							if type(a) == type(b) :
								if type(a) in { F, P } :
									if a.arg_size == b.arg_size and a.num == b.num :
										return True
										return False
										if type(a) == X :
											if a.num == b.num :
												return True
												return False
												return True
												return False
												def use_interpretation(self, interp, arg, check_untranslatable) :
												trans = Translation.build(interp.origin, arg)
												if trans.valid :
													for key in trans.dict :
														trans.dict[key] = self.translate(trans.dict[key], check_untranslatable)
														return interp.result.format(**trans.dict)
												else:
if check_untranslatable :
	return '#'
else :
	return arg
	def translate(self, arg, check_untranslatable = False) :
	if type(arg) == str :
		arg = UnitFormula.parse(arg)
		for interp in self.lang.interpretations :
			if Translator.match(interp.origin, arg) :
				return str(self.use_interpretation(interp, arg, check_untranslatable))
				if type(arg) in(F, P) :
					if check_untranslatable :
						return '#'
						return str(type(arg)(arg.num, [self.translate(i, check_untranslatable) for i in arg.args]))
						elif type(arg) in(AWrap, EWrap) :
						return str(type(arg)(self.translate(arg.x, check_untranslatable), self.translate(arg.predicate, check_untranslatable)))
						elif type(arg) == InvWrap :
						return str(type(arg)(self.translate(arg.predicate, check_untranslatable)))
						elif type(arg) in(BinAndWrap, BinOrWrap) :
						return str(type(arg)(self.translate(arg.p1, check_untranslatable), self.translate(arg.p2, check_untranslatable)))
						return str(arg)
						def translate_gen(self, gen, check_untranslatable = False, check_x_range = False) :
						ans = []
						for i in gen :
t = self.translate(i, check_untranslatable)
if (check_untranslatable and '#' in t) or (check_x_range and not UnitFormula.check_x_range(str(i)) and not X.check(i)) :
	continue
	ans.append(str(t))
	return ans
	def clear_gen(self, gen, check_untranslatable = False, check_x_range = False) :
	ans = []
	for i in gen :
t = self.translate(i, check_untranslatable)
if (check_untranslatable and '#' in t) or (check_x_range and not UnitFormula.check_x_range(str(i)) and not X.check(i)) :
	continue
	ans.append(str(i))
	return ans
	class Lang :
	def __init__(self, interps) :
	self.interpretations = interps
	@staticmethod
	def open(file) :
	text = file.read().split('\n')
	interps = []
	for line in text :
if line == '' or line[0] == '#' :
	continue
	func, translate = line[:line.find('=')].strip(' '), line[line.find('=') + 1:].strip(' ')
	interps.append(Interpretation(func, translate))
	return Lang(interps)
	if __name__ == '__main__' :
		from PredicateTask.ToTexTransformer import *
		import time
		start = time.clock()
		translator = Translator(Lang.open(open('Lexs1.txt')))
		sents = Evolution.generate(36, translator, True, True, True)
		print(TeX_Transformer.transform_list(translator.translate_gen(sents)), file = open('TeX/TeX_doc.tex', 'w'))
		print(len(sents))
		print(sents.index('P||;(,F||;|(,F;||(),F;||()),F;|||())'))
		print('This process took {} seconds'.format(time.clock() - start))
