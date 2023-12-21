## Defense.py Module 

import socket
import threading
import subprocess
import time
import logging

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
    def __init__(self, target_ip, target_port, attacker_ip, attacker_port, num_threads=DEFAULT_NUM_THREADS, num_requests=DEFAULT_NUM_REQUESTS):
        threading.Thread.__init__(self)
        self.target_ip = target_ip
        self.target_port = target_port
        self.attacker_ip = attacker_ip
        self.attacker_port = attacker_port
        self.num_threads = num_threads
        self.num_requests = num_requests

    def run(self):
        logging.info(f"Performing DDoS attack on {self.target_ip}:{self.target_port}...")
        for _ in range(self.num_threads):
            subprocess.run(["python", "DDoS_Attack.py", str(self.target_ip), str(self.target_port), str(self.attacker_ip), str(self.attacker_port), str(self.num_requests)])
        logging.info("DDoS attack completed.")

class DeadmanSwitch(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        logging.info("Running the Deadman Switch...")
        time.sleep(5)  
        subprocess.run(["python", "Deadman_Switch.py"])
        logging.info("Deadman Switch completed.")

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
