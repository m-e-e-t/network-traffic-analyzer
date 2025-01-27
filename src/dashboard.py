# src/dashboard.py
from flask import Flask, render_template
from flask_socketio import SocketIO
import json
import threading
import time
import random
from datetime import datetime
import os
import logging

class Dashboard:
    def __init__(self):
        template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
        static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
        
        self.app = Flask(__name__, 
                        template_folder=template_dir,
                        static_folder=static_dir)
        
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.setup_routes()
        self.setup_logging()
    
    def setup_routes(self):
        @self.app.route('/')
        @self.app.route('/index')
        def index():
            return render_template('dashboard.html')
    
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('Dashboard')
    
    def generate_mock_data(self):
        """Generate mock data for demonstration"""
        threats = [
            {'type': 'DDoS Attempt', 'severity': 'High'},
            {'type': 'Port Scan', 'severity': 'Medium'},
            {'type': 'Malware', 'severity': 'Low'}
        ]
        traffic = {
            'packetCount': random.randint(50, 500),
            'dataTransferred': random.uniform(1.0, 100.0)  # in MB
        }
        connections = [
            {
                'sourceIP': f'192.168.1.{random.randint(1, 255)}',
                'destination': f'10.0.0.{random.randint(1, 255)}',
                'status': self.determine_connection_status(f'192.168.1.{random.randint(1, 255)}')
            } for _ in range(5)
        ]
        logs = [
            {
                'timestamp': datetime.now().strftime("%H:%M:%S"),
                'source': f'192.168.1.{random.randint(1, 255)}',
                'destination': f'10.0.0.{random.randint(1, 255)}',
                'protocol': random.choice(['TCP', 'UDP', 'ICMP']),
                'severity': random.choice(['Low', 'Medium', 'High']),
                'message': 'Sample log message'
            } for _ in range(10)
        ]
        
        # Determine if there are any attacks
        has_attacks = any(threat['severity'] == 'High' for threat in threats) or \
                      any(connection['status'] == 'Suspicious' for connection in connections)
        
        return {
            'threats': threats,
            'traffic': traffic,
            'connections': connections,
            'logs': logs,
            'has_attacks': has_attacks
        }
    
    def determine_connection_status(self, source_ip):
        """Determine if a connection is secure or suspicious based on the source IP"""
        suspicious_ips = ['192.168.1.100', '192.168.1.200']
        if source_ip in suspicious_ips:
            return 'Suspicious'
        return 'Secure'
    
    def send_updates(self):
        """Background thread to emit updates"""
        while True:
            try:
                data = self.generate_mock_data()
                self.socketio.emit('dashboard_update', json.dumps(data))
                self.logger.info('Sent dashboard update')
                time.sleep(5)  # Update every 5 seconds
            except Exception as e:
                self.logger.error(f'Error in send_updates: {e}')
    
    def run(self):
        # Start the background thread for updates
        update_thread = threading.Thread(target=self.send_updates)
        update_thread.daemon = True
        update_thread.start()
        
        # Run the application
        self.socketio.run(self.app, debug=True)

if __name__ == '__main__':
    dashboard = Dashboard()
    dashboard.run()