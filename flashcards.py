import sys
import datetime
import json
import re
import time

def parenthesize(a, b):
    if type(b) is not list:
        b = re.sub(rf"(.+?)(?=\s*{a})", r"(\1)", b, 1, re.U) #deal with left side
        a_end = b.index(a) + len(a)
        right_results = re.subn(r"(\S)", r'(\1', b[ a_end : ], 1, re.U)
        return b[ : a_end ] + right_results[0] + ')' if right_results[1] else b
    else:
        listed_synonyms = '/'.join(s[ len(a) : ].lstrip() for s in b)
        return a + (f" ({listed_synonyms})" if listed_synonyms else "")

def main():
    with open(sys.argv[1], 'r', encoding = "utf-8") as f:
        verbs = [ re.sub(r"\(.*?\)", "", verb, re.U).strip() for verb in f.readlines()]
    with open(sys.argv[2], 'r', encoding = "utf-8") as f:
        definitions = json.load(f)

    as_list = list([k, v] for k, v in definitions.items())
    inds_to_del = []

    for verb in verbs:
        inds_to_use = []
        for i in range(len(as_list)):
            if verb in as_list[i][0]:
                inds_to_use.append(i)

        inds_to_skip = set()

        for j in inds_to_use:
            for k in inds_to_use:
                if (j != k and not {j, k} & inds_to_skip and
                        as_list[j][0].replace("qqn", "qch") == as_list[k][0]):
                    as_list[k][1].extend(as_list[j][1])
                    inds_to_skip |= {j, k}
                    inds_to_del.append(j)

    inds_to_del.sort(reverse=True)
    for i in inds_to_del:
        del as_list[i]

    inds_to_del.clear()
    inds_to_repl = {}

    i = 0
    while i < len(as_list):
        found = False
        for j in range(i + 1, len(as_list)):
            if as_list[i][0] not in as_list[j][0]:
                break
            if not found:
                if (len(as_list[i][1]) == 1 and
                        as_list[i][1][0] in as_list[j][1][0] and
                        all(bool(x.startswith(as_list[i][1][0])) for x in as_list[j][1])):
                    inds_to_del.extend([i, j])
                    inds_to_repl[i] = (parenthesize(as_list[i][0], as_list[j][0]), 
                            [parenthesize(as_list[i][1][0], as_list[j][1])])
                    found = True
        i = j + 1
    inds_to_del.reverse()
    for i in inds_to_del:
        del as_list[i]
        if i in inds_to_repl:
            as_list.insert(i, inds_to_repl[i])


    inds_to_del.clear()
    for verb in verbs:
        verb = re.sub(r"\(.*?\)", "", verb, re.U).strip()
        inds_to_use = []
        for i in range(len(as_list)):
            if verb in as_list[i][0]:
                inds_to_use.append(i)

        inds_to_skip = set()

        for j in inds_to_use:
            for k in inds_to_use:
                if (j != k and not {j, k} & inds_to_skip and
                        '(' not in as_list[j][0] and '(' not in as_list[k][0] and
                        re.fullmatch(as_list[j][0] + r" \[\w*?\]", as_list[k][0])):
                    as_list[j][1].extend(as_list[k][1])
                    inds_to_skip.add(k)
                    inds_to_del.append(k)

    inds_to_del.sort(reverse=True)
    for i in inds_to_del:
        del as_list[i]
    




    with open(datetime.datetime.now().strftime("%y%m%d_%H%M%S") + "_flashcards.txt",
            'w', encoding = "utf-8") as f:
        for k, v in as_list:
            f.write(k + "\tto " + '/'.join(v) + '\n')

if __name__ == "__main__":
    main()
