
#!/usr/bin/env python3

import sys, argparse, json, logging
from pathlib import Path
from typing import List


class NetworkConfig:
    DEFAULT_PORT_SCAN_THRESHOLD = 25
    DEFAULT_SYN_FLOOD_THRESHOLD = 100

    def __init__(self, port_scan_threshold=None, syn_flood_threshold=None):
        self.port_scan_threshold = port_scan_threshold or self.DEFAULT_PORT_SCAN_THRESHOLD
        self.syn_flood_threshold = syn_flood_threshold or self.DEFAULT_SYN_FLOOD_THRESHOLD

__all__ = ["parse_packet_line", "detect_port_scan", "NetworkConfig"]
def detect_port_scan(packets, src_ip, threshold):
    """Return True if unique dst ports from src_ip > threshold."""
    dst_ports = set()
    for pkt in packets:
        if pkt.get("src_ip") == src_ip:
            dst_ports.add(pkt.get("dst_port"))
    return len(dst_ports) > threshold

def setup_logging(log_file="network_monitor.log", log_level="INFO"):
    logger = logging.getLogger("network_monitor")
    logger.setLevel(getattr(logging, log_level.upper()))
    if logger.hasHandlers():
        logger.handlers.clear()

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, log_level.upper()))
    ch.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def create_parser():
    p = argparse.ArgumentParser(description="Network Traffic Monitor")
    p.add_argument("input_file", type=Path)
    p.add_argument("-o", "--output", type=Path, default=Path("results.json"))
    p.add_argument("-p", "--port-scan-threshold", type=int, default=25)
    p.add_argument("-s", "--syn-flood-threshold", type=int, default=100)
    p.add_argument("--log-level", default="INFO", choices=["DEBUG","INFO","WARNING","ERROR"])
    p.add_argument("-v", "--verbose", action="store_true")
    return p


def validate_args(a):
    if not a.input_file.exists(): raise FileNotFoundError(a.input_file)
    if not a.input_file.is_file(): raise ValueError(a.input_file)
    if a.port_scan_threshold < 1: raise ValueError()
    if a.syn_flood_threshold < 1: raise ValueError()
    if a.verbose: a.log_level = "DEBUG"


def parse_packet_line(line):
    p = [x.strip() for x in line.split(",")]
    if len(p) != 6: raise ValueError(line)
    try:
        return {
            "src_ip": p[0],
            "dst_ip": p[1],
            "src_port": int(p[2]),
            "dst_port": int(p[3]),
            "protocol": p[4],
            "flags": p[5]
        }
    except ValueError:
        raise ValueError(line)


def is_syn(p): 
    return p.get("protocol") == "TCP" and p.get("flags") == "SYN"


def load_traffic_log(f, log=None):
    out = []
    with open(f) as fp:
        for i, line in enumerate(fp,1):
            if not line.strip(): continue
            try:
                out.append(parse_packet_line(line))
                if log: log.debug("packet ok")
            except ValueError as e:
                if log: log.error("line %d bad", i)
    return out


def analyze(packets, cfg, log=None):
    res = {"total_packets": len(packets), "port_scans": [], "syn_floods": []}
    pairs, syn = {}, {}

    for p in packets:
        k = (p.get("src_ip"), p.get("dst_ip"))
        pairs.setdefault(k, set()).add(p.get("dst_port"))
        if is_syn(p):
            syn[p.get("src_ip")] = syn.get(p.get("src_ip"), 0) + 1

    for (s,d), ports in pairs.items():
        if len(ports) > cfg.port_scan_threshold:
            res["port_scans"].append({"src_ip": s, "dst_ip": d, "unique_ports": len(ports)})
            if log: log.warning("port scan %s->%s", s, d)

    for s,c in syn.items():
        if c > cfg.syn_flood_threshold:
            res["syn_floods"].append({"src_ip": s, "syn_count": c})
            if log: log.warning("syn flood %s", s)

    return res


def main():
    p = create_parser()
    a = p.parse_args()

    try:
        validate_args(a)
        log = setup_logging(log_level=a.log_level)
        cfg = NetworkConfig(a.port_scan_threshold, a.syn_flood_threshold)

        packets = load_traffic_log(a.input_file, log)
        results = analyze(packets, cfg, log)

        with open(a.output, "w") as f:
            json.dump(results, f, indent=2)

        log.info("done")
        return 0

    except Exception as e:
        log = setup_logging()
        log.error(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())