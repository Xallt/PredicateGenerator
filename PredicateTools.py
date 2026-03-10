from FormulaClasses import Evolution, Lang, Translator
from ToTexTransformer import TeX_Transformer


def TeX(formulas):
    if isinstance(formulas, list):
        return TeX_Transformer.transform_list(formulas)
    elif isinstance(formulas, str):
        return TeX_Transformer.transform_sent(formulas)


def basic_evolution(size):
    return Evolution.generate(size)


def natural_evolution(language, size):  # Automatically removes
    return Evolution.trans_generate(Translator(language), size, True, True, True, True)


def math_evolution(interpretations, size):
    return Evolution.trans_generate(
        Translator(interpretations), size, True, True, True, True, True
    )


if __name__ == "__main__":
    generated_formulas = []
    for pred in math_evolution(Lang.open("Languages/MathLexs.txt"), 25):
        print(pred)
        generated_formulas.append(pred)
    print(
        TeX(generated_formulas),
        file=open("TeX/Math.tex", "w"),
    )
