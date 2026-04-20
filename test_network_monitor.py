
import pytest
from week_12.network_monitor import parse_packet_line, detect_port_scan, NetworkConfig

@pytest.fixture
def valid_packet_line():
    return "192.168.1.5,10.0.0.1,54321,443,TCP,SYN"

@pytest.fixture
def config():
    return NetworkConfig(port_scan_threshold=25)

def test_parse_valid_packet(valid_packet_line):
    packet = parse_packet_line(valid_packet_line)
    assert packet['src_ip'] == "192.168.1.5"
    assert packet['dst_ip'] == "10.0.0.1"
    assert packet['src_port'] == 54321
    assert packet['dst_port'] == 443
    assert packet['protocol'] == "TCP"
    assert packet['flags'] == "SYN"

def test_parse_invalid_packet_too_few_fields():
    invalid_line = "192.168.1.5,10.0.0.1,443"
    with pytest.raises(ValueError):
        parse_packet_line(invalid_line)

def test_parse_invalid_ip_address():
    invalid_line = "999.999.999.999,10.0.0.1,54321,443,TCP,SYN"
    pass

def test_port_scan_detection_below_threshold():
    src_ip = "192.168.1.5"
    packets = [
        {'src_ip': src_ip, 'dst_port': 80},
        {'src_ip': src_ip, 'dst_port': 443},
        {'src_ip': src_ip, 'dst_port': 22},
    ]
    assert not detect_port_scan(packets, src_ip, threshold=25)

def test_port_scan_detection_above_threshold():
    src_ip = "192.168.1.5"
    packets = [{'src_ip': src_ip, 'dst_port': port} for port in range(1, 31)]
    assert detect_port_scan(packets, src_ip, threshold=25)

def test_port_scan_detection_exactly_at_threshold():
    src_ip = "192.168.1.5"
    packets = [{'src_ip': src_ip, 'dst_port': port} for port in range(1, 26)]
    assert not detect_port_scan(packets, src_ip, threshold=25)
    