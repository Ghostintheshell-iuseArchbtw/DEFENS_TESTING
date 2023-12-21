## main framework and script for the DEFENS_FRAMEWORK

import logging
from Defense import DdosAttack, DeadmanSwitch, Honeypot , IDSRule, DEFAULT_NUM_THREADS, DEFAULT_NUM_REQUESTS

class DefenseFramework:
    def __init__(self):
        self._honeypots = []
        self._ids_rules = []
        self._ddos_attack = None
        self._deadman_switch = None

    def _initialize_honeypots(self):
        localhost = "127.0.0.1"
        honeypot1 = Honeypot(localhost, 4040)
        honeypot2 = Honeypot(localhost, 8080)
        self._honeypots = [honeypot1, honeypot2]
    
    def _initialize_ids(self):
        localhost = "127.0.0.1"
        ids_rule = IDSRule(localhost, "BLOCK")
        self._ids_rules.append(ids_rule)
    
    def _is_attacker_detected(self, attacker_ip):
        logging.info(f"Checking if the attacker's IP address {attacker_ip} is detected...")
        return any(honeypot.has_connection_from(attacker_ip) for honeypot in self._honeypots)
        
    def _initialize_ddos_attack(self, attacker_ip, attacker_port):
        self._ddos_attack = DdosAttack(self._honeypots[0]._ip_address, self._honeypots[0]._port, attacker_ip, attacker_port, DEFAULT_NUM_THREADS, DEFAULT_NUM_REQUESTS)

    def _initialize_deadman_switch(self):
        self._deadman_switch = DeadmanSwitch()

    def run(self):
        self._initialize_honeypots()
        self._initialize_ids()
        logging.info("Importing modules...")
        attacker_ip = self._honeypots[0]._ip_address
        attacker_port = self._honeypots[0]._port 
    if self._is_attacker_detected(attacker_ip): 
           self._initialize_ddos_attack(attacker_ip, attacker_port)
           self._ddos_attack.start()  
    else  self._initialize_deadman_switch() 
           self._deadman_switch.start()  

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    defense_framework = DefenseFramework()
    defense_framework.run()
