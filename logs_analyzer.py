#Розробіть Python-скрипт для аналізу файлів логів. Скрипт повинен вміти читати лог-файл, переданий як аргумент командного рядка, і виводити статистику за рівнями логування наприклад, 
#INFO, ERROR, DEBUG. Також користувач може вказати рівень логування як другий аргумент командного рядка, щоб отримати всі записи цього рівня.

import sys
from pathlib import Path
from collections import Counter

def load_logs(file_path: str) -> list:
    logs = []
    with open(file_path, "r", encoding="utf-8") as fh:
        for line in fh.readlines():
            logs.append(parse_log_line(line))
    return logs

def parse_log_line(line: str) -> dict:
    parsed_line = {"log_date": line.split(" ", 3)[0], "log_time": line.split(" ", 3)[1], "log_level": line.split(" ", 3)[2], "log_msg": line.split(" ", 3)[3].replace("\n","")}
    return parsed_line

def filter_logs_by_level(logs: list, level: str) -> list:
    filtered_logs = list(filter(lambda x: x["log_level"] == level, logs))
    return filtered_logs

def count_logs_by_level(logs: list) -> dict:
    logs_levels = []
    for log in logs:
        logs_levels.append(log["log_level"])
    logs_levels_stat = Counter(logs_levels)
    return logs_levels_stat

def display_log_counts(counts: dict):
    separator = len(f"| {"Log level":<15} | {"Logs number":<15} |")
    print("-"*separator, end="\n")
    print(f"| {"Log level":<15} | {"Logs number":<15} |", end="\n")
    print("-"*separator, end="\n")
    for key in counts:
        print(f"| {key:<15} | {counts.get(key):<15} |", end="\n")
    print("-"*separator, end="\n")

def main():
    try: 
        path = Path(sys.argv[1])
        level = sys.argv[2].upper() if (len(sys.argv) >= 3) else ""
        display_log_counts(count_logs_by_level(load_logs(path)))
        if level != "":
            print(f"Detailed info about logs level {level} :", end="\n")
            for el in filter_logs_by_level(load_logs(path), level):
                print(f"{el["log_date"]} {el["log_time"]} - {el["log_msg"]}")
    except Exception as e:
        return print(f"{e}")

if __name__ == "__main__":
    main()