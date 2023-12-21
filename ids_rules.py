##load your ids rules here in this format of python & json.

ids_rules = [
    {
        "rule_id": 1,
        "rule_name": "Rule 1",
        "description": "Detects suspicious network traffic",
        "condition": "source_ip == '192.168.0.1' and destination_port == 8080",
        "action": "alert",
        "severity": "high"
    },
    {
        "rule_id": 2,
        "rule_name": "Rule 2",
        "description": "Detects potential SQL injection attacks",
        "condition": "request_method == 'POST' and 'SELECT' in request_data",
        "action": "block",
        "severity": "medium"
    },
    {
        "rule_id": 3,
        "rule_name": "Rule 3",
        "description": "Detects brute-force login attempts",
        "condition": "request_method == 'POST' and 'login' in request_url and response_code == 401",
        "action": "log",
        "severity": "low"
    }
]
