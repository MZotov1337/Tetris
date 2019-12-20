def read_highscore_data_from_file():
    input_file = open('highscore.dat', 'r')
    data = input_file.readline()
    data = descrypt_many_times(data, 6)
    if data != '':
        data = int(data)
    else:
        data = 0
    print('&', data)
    input_file.close()
    return int(data)

def write_highscore_data_to_file(output_data):
    output_file = open('highscore.dat', 'w')
    print('#', output_data)
    output_data = enscrypt_many_times(str(output_data), 6)
    print(output_data, file = output_file)
    output_file.close()

def enscrypt(s):
    s += '$'
    s1 = ''
    index = 0
    while index < len(s):
        for index2 in range(index, len(s)):
            if s[index] != s[index2]:
                break
        s1 += str(index2 - index) + s[index]
        index = index2
        if index == len(s) - 1:
            break
    return s1

def enscrypt_many_times(s, times):
    for i in range(times):
        s = enscrypt(s)
    return s

def descrypt(s):
    if s == '':
        return ''
    s1 = ''
    for index in range(len(s)//2):
        s1 += int(s[index * 2]) * s[index * 2 + 1]
    return s1

def descrypt_many_times(s, times):
    for i in range(times):
        s = descrypt(s)
    return s

if __name__ == "__main__":
    print("This module is not for direct call!")
