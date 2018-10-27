from FormulaClasses import *
from ToTexTransformer import *

def TeX(formulas):
    if type(formulas) == list:
        return TeX_Transformer.transform_list(formulas)
    elif type(formulas) == str:
        return TeX_Transformer.transform_sent(formulas)

def basic_evolution(size):
    return Evolution.generate(size)
def natural_evolution(language, size): # Automatically removes
    return Evolution.trans_generate(Translator(language), size, True, True, True, True)
def math_evolution(interpretations, size):
    return Evolution.trans_generate(Translator(interpretations), size, True, True, True, True, True)

if __name__ == '__main__':
    print(TeX(math_evolution(Lang.open('MathLexs.txt'), 25)), file = open('TeX/Math.tex', 'w'))
