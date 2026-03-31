import argparse
import csv
import re
from collections import Counter
from pathlib import Path


LOG_PATTERN = re.compile(
    r'(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) ([^"]*?) (\S+)" (\d{3}) (\S+) "([^"]*)" "([^"]*)"'
)


def parse_line(line: str):
    match = LOG_PATTERN.match(line)
    if not match:
        return None

    return {
        "ip": match.group(1),
        "datetime": match.group(2),
        "method": match.group(3),
        "path": match.group(4),
        "protocol": match.group(5),
        "status": match.group(6),
        "size": match.group(7),
        "referer": match.group(8),
        "user_agent": match.group(9),
    }


def is_bot(user_agent: str) -> bool:
    ua = user_agent.lower()
    bot_keywords = ["bot", "crawler", "spider", "curl", "wget"]
    return any(word in ua for word in bot_keywords)


def write_counter_csv(output_file: Path, header_name: str, counter: Counter):
    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([header_name, "count"])
        for key, count in counter.most_common():
            writer.writerow([key, count])


def write_404_csv(output_file: Path, errors_404: list[tuple[str, str]]):
    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ip", "path"])
        for ip, path in errors_404:
            writer.writerow([ip, path])


def parse_args():
    parser = argparse.ArgumentParser(
        description="Parse Apache/Nginx style access logs and summarize requests."
    )
    parser.add_argument(
        "logfile",
        help="Path to the access log file"
    )
    parser.add_argument(
        "--output-dir",
        help="Directory to write CSV summary files"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    log_file = Path(args.logfile)

    if not log_file.exists():
        print(f"File not found: {log_file}")
        raise SystemExit(1)

    total_requests = 0
    parse_errors = 0

    ip_counter = Counter()
    status_counter = Counter()
    path_counter = Counter()
    bot_counter = Counter()
    errors_404 = []

    with log_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            record = parse_line(line)
            if record is None:
                parse_errors += 1
                continue

            total_requests += 1
            ip_counter[record["ip"]] += 1
            status_counter[record["status"]] += 1
            path_counter[record["path"]] += 1

            if is_bot(record["user_agent"]):
                bot_counter[record["user_agent"]] += 1

            if record["status"] == "404":
                errors_404.append((record["ip"], record["path"]))

    print(f"\nTotal requests: {total_requests}")
    print(f"Parse errors: {parse_errors}")

    print("\nTop IPs:")
    for ip, count in ip_counter.most_common(10):
        print(f"{ip:<20} {count}")

    print("\nStatus codes:")
    for status, count in status_counter.most_common():
        print(f"{status:<10} {count}")

    print("\nTop Paths:")
    for path, count in path_counter.most_common(10):
        print(f"{path:<30} {count}")

    print("\nBot-like User-Agents:")
    for ua, count in bot_counter.most_common(10):
        print(f"{count:<5} {ua}")

    print("\n404 Records:")
    for ip, path in errors_404[:10]:
        print(f"{ip:<20} {path}")

    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        write_counter_csv(output_dir / "top_ips.csv", "ip", ip_counter)
        write_counter_csv(output_dir / "status_codes.csv", "status", status_counter)
        write_counter_csv(output_dir / "top_paths.csv", "path", path_counter)
        write_counter_csv(output_dir / "bot_user_agents.csv", "user_agent", bot_counter)
        write_404_csv(output_dir / "errors_404.csv", errors_404)

        print(f"\nCSV files written to: {output_dir}")


if __name__ == "__main__":
    main()