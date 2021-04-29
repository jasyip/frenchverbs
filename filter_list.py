import json
import sys
import datetime
from queue import PriorityQueue
import re
import string

class State:
    def __init__(self, words, length, word_length):
        self.words = words
        self.length = length
        self.word_length = word_length

    def copy(self):
        return State(self.words.copy(), self.length, self.word_length)

    def insert(self, word):
        for cur_word in self.words:
            if word in cur_word or cur_word in word:
                break
        else:
            self.words.append(word)
            self.word_length += len(list(c for c in word if c not in string.whitespace))
        self.length += 1

    def __repr__(self):
        return repr((self.words, self.length, self.word_length))

    def __len__(self):
        return self.word_length

    def __lt__(self, other):
        if len(self) == len(other):
            return self.words < other.words
        return len(self) < len(other) 

def filter_def(def_list):
    pq = PriorityQueue()
    pq.put(State([], 0, 0))

    while pq:
        cur = pq.get() 
        idx = cur.length

        if idx == len(def_list):
            return cur.words
        else:
            for word in def_list[idx]:
                nxt_state = cur.copy()
                nxt_state.insert(word)
                pq.put(nxt_state)

    return []

def main():
    with open(sys.argv[1], 'r', encoding="utf-8") as in_file:
        data = json.load(in_file)

        output_data = {}
        for word in data:
            #for word in dict(list(data.items())[: 2]):
            print(word)
            output_data[word] = filter_def(data[word])

    with open(datetime.datetime.now().strftime("%y%m%d_%H%M%S") + "_filtered.json",
            'w', encoding = "utf-8") as out_file:
        json.dump(output_data, out_file, ensure_ascii=False)

if __name__ == '__main__':
    main()
