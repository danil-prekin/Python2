import sys


def get_mean_size(data: str) -> float:
    lines = data.strip().split('\n')
    if len(lines) < 2:
        return 0.0

    sizes = []
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 5:
            try:
                size = int(parts[4])
                sizes.append(size)
            except ValueError:
                pass
    if not sizes:
        return 0.0
    return sum(sizes) / len(sizes)


if __name__ == '__main__':
    data = sys.stdin.read()
    mean_size = get_mean_size(data)
    print(f"{mean_size:.2f}")
