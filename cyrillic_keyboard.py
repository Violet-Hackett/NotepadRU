from cyrillic_map import cyrillic_map

def RU(s):
    result = ""
    i = 0
    j = 3
    while i < len(s):
        if s[i:j] in cyrillic_map:
            result += cyrillic_map[s[i:j]]
            i = j
            if j + 3 > len(s):
                j = len(s)
            else:
                j += 3
        elif j - i == 1:
            if s[i] != '|':
                result += s[i]
            i += 1
            if j + 3 > len(s):
                j = len(s)
            else:
                j += 3
        else:
            j -= 1

    return result

def print_RU(s):
    print(RU(s))