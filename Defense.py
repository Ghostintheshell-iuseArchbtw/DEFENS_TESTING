## Defense.py Module 
## This module contains the classes and functions required to implement the DEFENS Framework.

import socket
import threading
import subprocess
import time

DEFAULT_NUM_THREADS = 5
DEFAULT_NUM_REQUESTS = 10

class SocketWrapper:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send(self, data):
        self.socket.sendall(data.encode())

    def receive(self, buffer_size):
        return self.socket.recv(buffer_size).decode()

    def close(self):
        self.socket.close()

class DdosAttack(threading.Thread):
    def __init__(self, target_host, target_port, attacker_ip, attacker_port, num_threads=DEFAULT_NUM_THREADS, num_requests=DEFAULT_NUM_REQUESTS):
        threading.Thread.__init__(self)
        self.target_host = target_host
        self.target_port = target_port
        self.attacker_ip = attacker_ip
        self.attacker_port = attacker_port
        self.num_threads = num_threads
        self.num_requests = num_requests

    def run(self):
        for _ in range(self.num_threads):
            subprocess.run(["python", "DDoS_Attack.py", str(self.target_host), str(self.target_port), str(self.attacker_ip), str(self.attacker_port), str(self.num_requests)])

class DeadmanSwitch(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(5)
        subprocess.run(["python", "Deadman_Switch.py"])

class Honeypot:
    def __init__(self, ip_address, port):
        self._ip_address = ip_address
        self._port = port
        self._logged_connections = []

    def log_connection(self, ip_address):
        self._logged_connections.append(ip_address)

    def has_connection_from(self, ip_address):
        return ip_address in self._logged_connections

class IDSRule:
    def __init__(self, ip_address, action):
        self.ip_address = ip_address
        self.action = action
    
    def self_defense(self):
        if self.action in ["BLOCK", "ALERT", "LOG"]:
            subprocess.run(["python", "ids_rules.py", str(self.ip_address), str(self.action)])

class DefenseFramework:
    def __init__(self):
        self._honeypots = []
        self._ids_rules = []
        self._ddos_attack = None
        self._deadman_switch = None
        self._initialize_honeypots()
        self._initialize_ids()

    def _initialize_honeypots(self):
        localhost = "127.0.0.1"
        honeypot1 = Honeypot(localhost, 4040)
        honeypot2 = Honeypot(localhost, 8080)
        self._honeypots = [honeypot1, honeypot2]

    def _is_attacker_detected(self, attacker_ip):
        return any(honeypot.has_connection_from(attacker_ip) for honeypot in self._honeypots)

    def _initialize_ids(self):
        localhost = "127.0.0.1"
        ids_rule = IDSRule(localhost, "BLOCK")
        self._ids_rules.append(ids_rule)

    def _initialize_ddos_attack(self, attacker_ip, attacker_port):
        self._ddos_attack = DdosAttack(self._honeypots[0]._ip_address, self._honeypots[0]._port, attacker_ip, attacker_port, DEFAULT_NUM_THREADS, DEFAULT_NUM_REQUESTS)
    
