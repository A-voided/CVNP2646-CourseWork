from utilis import validate_ip, get_timestamp
from port_checker import check_port_status
from report_gen import generate_report

def main():
	target_ip = input("Enter target IP address: ")
	if not validate_ip(target_ip):
		print("Invalid IP address format.")
		return

	print(f"Scanning {target_ip} on ports 20-100...")
	open_ports = []
	scan_results = []
	for port in range(20, 101):
		status = check_port_status(port)
		scan_results.append({"port": port, "status": status})
		if status == "OPEN":
			open_ports.append(port)
		print(f"Port {port}: {status}")

	report_data = {
		"target_ip": target_ip,
		"timestamp": get_timestamp(),
		"open_ports": open_ports,
		"scan_results": scan_results
	}
	generate_report(report_data)
	print("\nScan complete. Report saved as scan_data.json.")

if __name__ == "__main__":
	main()
