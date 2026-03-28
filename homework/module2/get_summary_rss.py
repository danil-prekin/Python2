import sys


def get_summary_rss(file_path: str) -> str:
    total_rss = 0
    with open(file_path, 'r') as f:
        lines = f.readlines()[1:]
        for line in lines:
            columns = line.split() try:
                rss = int(columns[5])
                total_rss += rss
            except (ValueError, IndexError):
                continue

    for unit in ['Б', 'KiB', 'MiB', 'GiB', 'TiB']:
        if total_rss < 1024:
            return f"{total_rss:.2f} {unit}"
        total_rss /= 1024
    return f"{total_rss:.2f} PiB"


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Использование: python3 get_summary_rss.py <файл_с_ps_aux>")
        sys.exit(1)
    print(get_summary_rss(sys.argv[1]))
