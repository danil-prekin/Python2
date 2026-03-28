import sys


def decrypt(encrypted: str) -> str:
    result = []
    i = 0
    n = len(encrypted)
    while i < n:
        ch = encrypted[i]
        if ch == '.':
            if i + 1 < n and encrypted[i + 1] == '.':
                if result:
                    result.pop()
                i += 2
            else:
                i += 1
        else:
            result.append(ch)
            i += 1
    return ''.join(result)


if __name__ == '__main__':
    data = sys.stdin.read().strip()
    print(decrypt(data))
