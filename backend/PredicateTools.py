from pathlib import Path

import tyro

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


def math_evolution(lang: Lang, size: int | None = None):
    return Evolution.trans_generate(
        Translator(lang), size, True, True, True, True, True
    )


def main(
    lang_path: Path = Path("Languages/MathLexs.txt"),
    size: int = 25,
    out_path: Path = Path("TeX/Math.tex"),
):
    generated_formulas = []
    lang = Lang.open(str(lang_path))
    for pred in math_evolution(lang, size):
        print(pred)
        generated_formulas.append(pred)
    with open(str(out_path), "w") as f:
        f.write(str(TeX(generated_formulas)))


if __name__ == "__main__":
    tyro.cli(main)
