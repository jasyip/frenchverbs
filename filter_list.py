import json

class State:
    def __init__(self, words, length):
        self.words = words
        self.length = length

    def copy(self):
        return State(self.words.copy(), self.length)

    def insert(self, word):
        if word not in self.words:
            self.words.append(word)
        self.length += 1

def filter_def(def_list):
    stack = [State([], 0)]
    ans = []

    while stack:
        cur = stack.pop()
        idx = cur.length

        if idx == len(def_list):
            if not ans or len(cur.words) < len(ans):
                ans = cur.words
        else:
            for word in def_list[idx]:
                nxt_state = cur.copy()
                nxt_state.insert(word)
                stack.append(nxt_state)

    return ans

def main():
    input_file = input('name of input file: ')
    output_file = input('name of output file: ')

    try:
        output_data = {}

        with open(input_file, 'r') as in_file:
            data = json.load(in_file)

            output_data = {}
            for word in data:
                output_data[word] = filter_def(data[word])

        with open(output_file, 'w') as out_file:
            json.dump(output_data, out_file)
    except FileNotFoundError:
        print('input file not found / formatted incorrectly')
        return

if __name__ == '__main__':
    main()
