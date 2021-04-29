import sys
import datetime
import json

def main():
    with open(sys.argv[1], 'r', encoding = "utf-8") as f:
        definitions = json.load(f)

    with open(datetime.datetime.now().strftime("%y%m%d_%H%M%S") + "_flashcards.txt",
            'w', encoding = "utf-8") as f:
        for k, v in definitions.items():
            f.write(k + "\tto " + '/'.join(v) + '\n')

if __name__ == "__main__":
    main()
