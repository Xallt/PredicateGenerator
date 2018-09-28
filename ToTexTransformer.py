def clear_scobes(line):
    if line [0] == '[':
        return line[1:-1]
    return line
class TeX_Transformer:
    @staticmethod
    def transform_sent(sent):
        trsent = '$'
        i = 0
        while i < len(sent):
            if sent[i:i+3] == '%A%':
                trsent += '\\forall '
                i += 3
            elif sent[i:i+3] == '%E%':
                trsent += '\\exists '
                i += 3
            elif sent[i:i + 3] == '%-%':
                trsent += '\\neg '
                i += 3
            elif sent[i:i + 3] == '%v%':
                trsent += '\\lor '
                i += 3
            elif sent[i:i + 3] == '%&%':
                trsent += '\\wedge '
                i += 3
            elif sent[i:i + 3] == ':':
                trsent += '\\vdots '
                i += 3
            elif sent[i] == '*':
                trsent += '\\cdot'
                i += 1
            elif (sent[i] == '|') or (sent[i] == ';'):
                trsent += '_{'
                while sent[i] in ['|', ';']:
                    trsent += sent[i]
                    i += 1
                    if i == len(sent):
                        break
                trsent += '}'
            else:
                trsent += sent[i]
                i += 1
        return trsent.replace(' ',' \\ ') + '$'
    @staticmethod
    def transform_list(sent_list, pairs=False):
        tex_begin = '\\documentclass{article}\n\\usepackage{amssymb}\n\\begin{document}\n\\begin{enumerate}\n\n'
        tex_end = '\n\n\\end{enumerate}\n\\end{document}'
        #if pairs:
        #    tr_sent_list = ['{} {}'.format('\\item' * int(i % 2 == 0), transform_sent(sent_list[i])) for i in range(len(sent_list))]
        #else:
        tr_sent_list = ['{} {}'.format('\\item', TeX_Transformer.transform_sent(clear_scobes(sent_list[i]))) for i in range(len(sent_list))]
        return  tex_begin + '\n\n'.join(tr_sent_list) + tex_end
