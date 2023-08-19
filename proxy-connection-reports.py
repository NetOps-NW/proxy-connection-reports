#!/usr/bin/python3

import json, sys, re;

def collect_local_socket_details(local_socket_port = list()):
    with open(sys.argv[1], "r") as file:
        for line in file.read().split("\n"):
            if re.search(r"[\w\s]+?([\d\.]{7,15}):([\d]{1,5})\s+([\d\.]{7,15}):([\d\*]{1,5})\s+LISTEN", line):
                re_listener_pattern = re.search(r"[\w\s]+?([\d\.]{7,15}):([\d]{1,5})\s+([\d\.]{7,15}):([\d\*]{1,5})\s+LISTEN", line);
                if re_listener_pattern[2] not in local_socket_port:
                    local_socket_port.append(re_listener_pattern[2]);
    return sorted(local_socket_port);
    
def collect_top_ip_details(local_socket_port, top_inbound_ip = dict(), top_outbound_ip = dict()):
    with open(sys.argv[1], "r") as file:
        for line in file.read().split("\n"):
            if re.search(r"[\w\s]+?([\d\.]{7,15}):([\d]{1,5})\s+([\d\.]{7,15}):([\d\*]{1,5})\s+ESTABLISHED", line):
                re_connection_pattern = re.search(r"[\w\s]+?([\d\.]{7,15}):([\d]{1,5})\s+([\d\.]{7,15}):([\d\*]{1,5})\s+ESTABLISHED", line);
                if re_connection_pattern[2] in local_socket_port:
                    if re_connection_pattern[3] not in top_inbound_ip:
                        top_inbound_ip[re_connection_pattern[3]] = 1;
                    else:
                        top_inbound_ip[re_connection_pattern[3]] += 1;
                if re_connection_pattern[2] not in local_socket_port:
                    if re_connection_pattern[3] not in top_outbound_ip:
                        top_outbound_ip[re_connection_pattern[3]] = 1;
                    else:
                        top_outbound_ip[re_connection_pattern[3]] += 1;
    return dict(sorted(top_inbound_ip.items(), key=lambda item: item[1], reverse=True)[:10]), dict(sorted(top_outbound_ip.items(), key=lambda item: item[1], reverse=True)[:10]);
    
def collect_top_port_details(local_socket_port, top_inbound_port = dict(), top_outbound_port = dict()):
    with open(sys.argv[1], "r") as file:
        for line in file.read().split("\n"):
            if re.search(r"[\w\s]+?([\d\.]{7,15}):([\d]{1,5})\s+([\d\.]{7,15}):([\d\*]{1,5})\s+ESTABLISHED", line):
                re_connection_pattern = re.search(r"[\w\s]+?([\d\.]{7,15}):([\d]{1,5})\s+([\d\.]{7,15}):([\d\*]{1,5})\s+ESTABLISHED", line);
                if re_connection_pattern[2] in local_socket_port:
                    if re_connection_pattern[2] not in top_inbound_port:
                        top_inbound_port[re_connection_pattern[2]] = 1;
                    else:
                        top_inbound_port[re_connection_pattern[2]] += 1;
                if re_connection_pattern[2] not in local_socket_port:
                    if re_connection_pattern[4] not in top_outbound_port:
                        top_outbound_port[re_connection_pattern[4]] = 1;
                    else:
                        top_outbound_port[re_connection_pattern[4]] += 1;
    return dict(sorted(top_inbound_port.items(), key=lambda item: item[1], reverse=True)[:10]), dict(sorted(top_outbound_port.items(), key=lambda item: item[1], reverse=True)[:10]);
    
def collect_top_connection_details(local_socket_port, top_inbound_connection = dict(), top_outbound_connection = dict()):
    with open(sys.argv[1], "r") as file:
        for line in file.read().split("\n"):
            if re.search(r"[\w\s]+?([\d\.]{7,15}):([\d]{1,5})\s+([\d\.]{7,15}):([\d\*]{1,5})\s+ESTABLISHED", line):
                re_connection_pattern = re.search(r"[\w\s]+?([\d\.]{7,15}):([\d]{1,5})\s+([\d\.]{7,15}):([\d\*]{1,5})\s+ESTABLISHED", line);
                if re_connection_pattern[2] in local_socket_port:
                    network_connecting_string = f"Src_{re_connection_pattern[3]} Dst_{re_connection_pattern[1]}:{re_connection_pattern[2]}";
                    if network_connecting_string not in top_inbound_connection:
                        top_inbound_connection[network_connecting_string] = 1;
                    else:
                        top_inbound_connection[network_connecting_string] += 1;
                if re_connection_pattern[2] not in local_socket_port:
                    network_connecting_string = f"Src_{re_connection_pattern[1]} Dst_{re_connection_pattern[3]}:{re_connection_pattern[4]}";
                    if network_connecting_string not in top_outbound_connection:
                        top_outbound_connection[network_connecting_string] = 1;
                    else:
                        top_outbound_connection[network_connecting_string] += 1;
        return dict(sorted(top_inbound_connection.items(), key=lambda item: item[1], reverse=True)[:10]), dict(sorted(top_outbound_connection.items(), key=lambda item: item[1], reverse=True)[:10]);
    
def main():
    local_socket_port = collect_local_socket_details();
    top_inbound_ip, top_outbound_ip = collect_top_ip_details(local_socket_port);
    top_inbound_port, top_outbound_port = collect_top_port_details(local_socket_port);
    top_inbound_connection, top_outbound_connection = collect_top_connection_details(local_socket_port);
    
    print("\n" + " Top Inbound IP ".center(156, "-") + "\n" , json.dumps(top_inbound_ip, indent=4));
    print("\n" + " Top Inbound Port ".center(156, "-") + "\n" , json.dumps(top_inbound_port, indent=4));
    print("\n" + " Top Inbound Connection ".center(156, "-") + "\n" , json.dumps(top_inbound_connection, indent=4));

    print("\n" + " Top Outbound IP ".center(156, "-") + "\n" , json.dumps(top_outbound_ip, indent=4));
    print("\n" + " Top Outbound Port ".center(156, "-") + "\n" , json.dumps(top_outbound_port, indent=4));
    print("\n" + " Top Outbound Connection ".center(156, "-") + "\n" , json.dumps(top_outbound_connection, indent=4));

if "__main__" in __name__:
    if len(sys.argv[1:]) != 1:
        print(f"\n[+] Usage: {sys.argv[0]} proxy-connection-dump.log\n");
    else:
        main();
