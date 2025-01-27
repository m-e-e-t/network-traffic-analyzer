import json
import datetime
from collections import defaultdict

class ThreatDetector:
    def __init__(self, model):
        self.model = model
        self.threat_patterns = self.load_threat_patterns()
        self.packet_log = defaultdict(list)
        
    def load_threat_patterns(self):
        with open('./data/threat_signatures.json', 'r') as f:
            return json.load(f)
    
    def analyze_traffic(self, packet_data):
        threats = []
        
        if self.detect_ddos(packet_data):
            threats.append({
                'type': 'DDoS',
                'severity': 'High',
                'timestamp': datetime.datetime.now()
            })
            
        if self.detect_port_scan(packet_data):
            threats.append({
                'type': 'Port Scan',
                'severity': 'Medium',
                'timestamp': datetime.datetime.now()
            })
        
        if self.detect_suspicious_payload(packet_data):
            threats.append({
                'type': 'Suspicious Payload',
                'severity': 'High',
                'timestamp': datetime.datetime.now()
            })
            
        return threats
    
    def detect_ddos(self, packet_data):
        current_time = datetime.datetime.now()
        self.packet_log['ddos'].append(current_time)
        
        timeframe = self.threat_patterns.get('ddos_pattern', {}).get('timeframe', 60)
        threshold = self.threat_patterns.get('ddos_pattern', {}).get('threshold', 1000)
        
        self.packet_log['ddos'] = [
            timestamp for timestamp in self.packet_log['ddos']
            if (current_time - timestamp).seconds <= timeframe
        ]
        
        return len(self.packet_log['ddos']) > threshold
    
    def detect_port_scan(self, packet_data):
        current_time = datetime.datetime.now()
        src_ip = packet_data.get('src_ip')
        self.packet_log[src_ip].append(current_time)
        
        timeframe = self.threat_patterns.get('port_scan', {}).get('timeframe', 10)
        threshold = self.threat_patterns.get('port_scan', {}).get('threshold', 20)
        
        self.packet_log[src_ip] = [
            timestamp for timestamp in self.packet_log[src_ip]
            if (current_time - timestamp).seconds <= timeframe
        ]
        
        return len(self.packet_log[src_ip]) > threshold
    
    def detect_suspicious_payload(self, packet_data):
        payload = packet_data.get('payload', '')
        suspicious_list = self.threat_patterns.get('suspicious_payload', [])
        
        return any(pattern in payload for pattern in suspicious_list)
