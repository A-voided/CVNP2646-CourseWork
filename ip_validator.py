
def validate_ip(ip_address):
    """
    Checks if the input string is a valid IPv4 address (4 octets, each 0-255).
    """
    try:
        octets = ip_address.split('.')
        
        if len(octets) != 4:
            return False
        for octet in octets:
        
            try:
                int_octet = int(octet)
            except ValueError:
                return False
            if not (0 <= int_octet <= 255):
                return False
                
    except Exception as e:
        
        print(f"An error occurred during validation: {e}")
        return False
        
    return True
test_ips = [
    "127.0.0.3",
    "256.100.50.25",
    "192.tye.812.1",
    "19.12.3.45",
    '192.168.1.1',
    'thi.s.is.not.ip',
]
if __name__ == "__main__":
    print("+=+=+ip validation test results+=+=+")
    for ip in test_ips:
        if validate_ip(ip):
            print(f"'{ip}' is a valid ipv4 address.")
        else:
            print(f"'{ip}' is an invalid ipv4 address.")
