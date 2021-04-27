from bs4 import BeautifulSoup
import requests
import re
import sys
import pprint


class WordReference:

    def __init__(self, direction = "fren"):
        self.direction = direction
        self.url = "https://www.wordreference.com/" + direction

    def max_flow(self, defintions):
        pass

    def scrape(self, word):
        r = requests.get(self.url + '/' + word)
        sp = BeautifulSoup(r.content, "html.parser")
        translations = {}
        for table in sp.find_all("table", attrs = {"class" : "WRD"}):
            translation_html = table.find_all(attrs = {"class" : ["even", "odd"]})
            main_translation = None
            for translation in translation_html:
                to_word_tag = translation.find("td", attrs = {"class" : "ToWrd"})
                if to_word_tag is not None:
                    if re.fullmatch(self.direction + r":\d+", translation.get("id", "")):
                        from_word_tag = translation.find("td", attrs = {"class" : "FrWrd"})
                        if from_word_tag is not None:
                            word_type = list(from_word_tag.find("em").strings)
                            if len(word_type) > 0 and word_type[0][0] != "v":
                                main_translation = None
                                continue
                            main_translation = list(from_word_tag.strong.strings)[0].strip()
                            if main_translation not in translations:
                                translations[main_translation] = []
                            translations[main_translation].append(set())
                    if main_translation is not None:
                        for unnecessary_tag in to_word_tag.find_all(["a", "em"]):
                            unnecessary_tag.decompose()
                        translations[main_translation][-1].update(
                                [synonym.strip() for synonym in
                                ' '.join(s.strip() for s in to_word_tag.strings).split(",")])
        """
        for k, definitions in translations.items():
            i = 0
            while i < len(definitions):
                for j in range(len(definitions) - 1, i, -1):
                    intersection = definitions[i] & definitions[j]
                    if len(intersection) > 0:
                        definitions[i] |= definitions[j]
                        del definitions[j]
                i += 1
            for i, definition in enumerate(definitions):
                definitions[i] = min(definition, key = lambda s: len(s) + 0.125 * s.count(' '))
            translations[k] = definitions
            translations[k].sort(key = len)
        """

        return translations

if __name__ == "__main__":
    wr = WordReference()
    with open(sys.argv[1], 'r', encoding='utf8') as f:
        manual_translations = dict([ translation.split("\t") for translation in f.readlines() ])
    with open(sys.argv[2], 'r', encoding='utf8') as f:
        verbs = [ translation.split("\t")[0] for translation in f.readlines() ]
    automatic_translations = {}
    for verb in verbs[:5]:
        print(verb)
        if " " not in verb:
            verb = re.sub(r"\(.*\)", "", verb)
            verb = re.sub(r"^s'", "", verb)
            automatic_translations.update(wr.scrape(verb))

    print(automatic_translations["abaisser"])
    print(automatic_translations["abolir"])

    print(manual_translations["abaisser"])
    print(manual_translations["abolir"])
