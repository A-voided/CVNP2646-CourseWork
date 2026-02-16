import sys
from collections import Counter
from datetime import datetime

def parse_log_line(line):
    parts = line.strip().split()
    if len(parts) != 6:
        return None
    timestamp_str = f"{parts[0]} {parts[1]}"
    action = parts[2]
    src_ip = parts[3]
    dst_ip = parts[4]
    port = parts[5]
    return timestamp_str, action, src_ip, dst_ip, port

def analyze_firewall_log(log_path):
    allow_count = 0
    deny_count = 0
    denied_src_ips = set()
    denied_ports = []
    timestamps = []

    with open(log_path, 'r') as f:
        for line in f:
            parsed = parse_log_line(line)
            if not parsed:
                continue
            timestamp_str, action, src_ip, dst_ip, port = parsed
            timestamps.append(timestamp_str)
            if action == 'ALLOW':
                allow_count += 1
            elif action == 'DENY':
                deny_count += 1
                denied_src_ips.add(src_ip)
                denied_ports.append(port)

    port_counter = Counter(denied_ports)
    most_targeted_port = port_counter.most_common(1)[0][0] if port_counter else None

    if timestamps:
        dt_objects = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]
        first_ts = min(dt_objects)
        last_ts = max(dt_objects)
    else:
        first_ts = last_ts = None

    print(f"Total ALLOW: {allow_count}")
    print(f"Total DENY: {deny_count}")
    print(f"Unique source IPs denied: {', '.join(denied_src_ips) if denied_src_ips else 'None'}")
    print(f"Most targeted port (DENY): {most_targeted_port if most_targeted_port else 'None'}")
    print(f"First timestamp: {first_ts if first_ts else 'None'}")
    print(f"Last timestamp: {last_ts if last_ts else 'None'}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <firewall_log_path>")
        sys.exit(1)
    analyze_firewall_log(sys.argv[1])
