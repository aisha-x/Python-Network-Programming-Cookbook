

'''
this code will do one of the following:
1. start Monitoring
2. Add Block Rule
3. Remove Block Rule
4. View Current Rules

'''



from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP
import logging

# Initialize logging
logging.basicConfig(
    filename="firewall_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Default blocking rules
BLOCKED_IPS = ["192.168.1.5"]  # Example blocked IP addresses
BLOCKED_PORTS = [80, 443]      # Example blocked ports (HTTP/HTTPS)

def log_blocked_packet(packet, reason):
    """
    Logs the details of blocked packets.
    """
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        log_message = f"Blocked packet: {src_ip} -> {dst_ip} | Reason: {reason}"
        print(log_message)
        logging.info(log_message)

def packet_filter(packet):
    """
    Function to analyze and filter packets based on rules.
    """
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        # Check if source or destination IP is in blocked list
        if src_ip in BLOCKED_IPS or dst_ip in BLOCKED_IPS:
            log_blocked_packet(packet, "Blocked IP")
            return False

        if TCP in packet or UDP in packet:
            src_port = packet.sport
            dst_port = packet.dport

            # Check if port is in blocked list
            if src_port in BLOCKED_PORTS or dst_port in BLOCKED_PORTS:
                log_blocked_packet(packet, f"Blocked Port {src_port}/{dst_port}")
                return False

    # Allow packet if it doesn't match blocking rules
    return True

def add_rule(rule_type, value):
    """
    Add a new rule to block IP or port.
    """
    if rule_type == "ip":
        if value not in BLOCKED_IPS:
            BLOCKED_IPS.append(value)
            print(f"Added IP block rule: {value}")
            logging.info(f"Added IP block rule: {value}")
        else:
            print("IP rule already exists.")
    elif rule_type == "port":
        value = int(value)
        if value not in BLOCKED_PORTS:
            BLOCKED_PORTS.append(value)
            print(f"Added Port block rule: {value}")
            logging.info(f"Added Port block rule: {value}")
        else:
            print("Port rule already exists.")
    else:
        print("Invalid rule type. Use 'ip' or 'port'.")

def remove_rule(rule_type, value):
    """
    Remove an existing rule for IP or port.
    """
    if rule_type == "ip":
        if value in BLOCKED_IPS:
            BLOCKED_IPS.remove(value)
            print(f"Removed IP block rule: {value}")
            logging.info(f"Removed IP block rule: {value}")
        else:
            print("IP rule not found.")
    elif rule_type == "port":
        value = int(value)
        if value in BLOCKED_PORTS:
            BLOCKED_PORTS.remove(value)
            print(f"Removed Port block rule: {value}")
            logging.info(f"Removed Port block rule: {value}")
        else:
            print("Port rule not found.")
    else:
        print("Invalid rule type. Use 'ip' or 'port'.")

def monitor_traffic(interface="eth0"):
    """
    Start sniffing packets on the specified interface.
    """
    print(f"Starting packet monitoring on interface: {interface}")
    sniff(iface=interface, prn=lambda pkt: pkt.summary() if packet_filter(pkt) else None, store=False)

if __name__ == "__main__":
    interface_name = input("Enter your network interface (e.g., eth0, wlan0): ")
    try:
        while True:
            print("\nFirewall Menu:")
            print("1. Start Monitoring")
            print("2. Add Block Rule (IP/Port)")
            print("3. Remove Block Rule (IP/Port)")
            print("4. View Current Rules")
            print("5. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                monitor_traffic(interface=interface_name)
            elif choice == "2":
                rule_type = input("Enter rule type (ip/port): ").strip().lower()
                value = input("Enter value to block (e.g., 192.168.1.10 or 80): ").strip()
                add_rule(rule_type, value)
            elif choice == "3":
                rule_type = input("Enter rule type (ip/port): ").strip().lower()
                value = input("Enter value to unblock (e.g., 192.168.1.10 or 80): ").strip()
                remove_rule(rule_type, value)
            elif choice == "4":
                print("\nCurrent Blocked IPs:", BLOCKED_IPS)
                print("Current Blocked Ports:", BLOCKED_PORTS)
            elif choice == "5":
                print("Exiting Firewall...")
                break
            else:
                print("Invalid choice. Try again.")
    except KeyboardInterrupt:
        print("\nStopping packet monitoring.")
    except Exception as e:
        print(f"Error: {e}")
