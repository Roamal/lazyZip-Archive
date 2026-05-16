def find_matches(text):
    dict_forF = {}
    itog = []
    info = ()
    i = 0
    while i < len(text):
        pattern = text[i:i+3]  
        if pattern not in dict_forF.keys():
            dict_forF[pattern] = i 
            itog.append(text[i])
        else:
            n = 4
            fin = dict_forF[pattern]
            while text[i:i+n] == text[fin: fin + n]:
                info = (i - fin, n)
                n += 1
            if info:
                itog.append(info)
                i += n - 2  # перепрыгиваем
                info = ()
                continue
        i+=1
    return itog

def count_freq(encoded):
    total = {i:0 for i in encoded if isinstance(i, str)}
    
    for i in encoded:
        if isinstance(i, str):
            total[i] += 1
        elif isinstance(i, tuple):
            length = i[1]
            key = f"LEN:{length}"
            if key not in total:
                total[key] = 0
            total[key] += 1
    return total



class Node:
    def __init__(self, name, freq):
        self.name = name
        self.freq = freq
        self.left = None
        self.right = None
    def __repr__(self):
        return f"Node({self.name}, {self.freq})"
    
def build_tree(freq_dict):
    nodel = []
    for k in freq_dict.keys():
        node = Node(k, freq_dict[k])
        nodel.append(node)
    while len(nodel) > 1:
        nodel.sort(key = lambda x: x.freq)
        twof = nodel[:2]
        new_node = Node(str(twof[0].name) + str(twof[1].name),
        twof[0].freq + twof[1].freq)
        new_node.left = twof[0]
        new_node.right = twof[1]
        nodel = nodel[2:]
        nodel.append(new_node)
    return nodel

def get_codes(node, code=""):
    if node.left is None and node.right is None:
        return {node.name: code}
    
    codes = {}
    if node.left:
        codes.update(get_codes(node.left, code + "0"))
    if node.right:
        codes.update(get_codes(node.right, code + "1"))
    return codes


def compress(text):

    matches = find_matches(text)
    freq = count_freq(matches)
    tree = build_tree(freq)

    codes = get_codes(tree[0])
    total_code = ''
    for w in matches:
        if isinstance(w, str):
            total_code += codes[w]
        elif isinstance(w, tuple):
            back, length = w
            total_code += codes[f"LEN:{length}"]
            total_code += bin(back)[2:].zfill(15)
    return total_code, codes


def decode(bits, codes):
    reverse_codes = {v:k for k, v in codes.items()}
    text = ""
    before = ""
    c = 0
    while c < len(bits):
        code = before + bits[c]
        if code in reverse_codes:
            symbol = reverse_codes[code]
            if isinstance(symbol, str) and symbol.startswith("LEN:"):
                length = int(symbol[4:])
                distance = int(bits[c+1:c+16], 2)
                text += f"({distance},{length})"
                c += 15
                before = ""
            else:
                text += str(symbol)
                before = ""
        else:
            before = code
        c += 1
    return text





def show_matches(text):
    matches = find_matches(text)
    i = 0
    for item in matches:
        if isinstance(item, tuple):
            back, length = item
            start = i - back
            original = text[start:start+length]
            print(f"ссылка {item} = '{original}'")
            i += length
        else:
            i += 1



compres, codes = compress('abracadabra')

print(find_matches("abracabraabracabra"))
print(compress("abracabraabracabra"))