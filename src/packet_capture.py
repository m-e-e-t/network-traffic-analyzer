# Required Libraries
from scapy.all import * 
from scapy.layers.inet import IP, TCP
import sqlite3
import datetime
import signal
import sys

class NetworkTrafficAnalyzer:
    def __init__(self):
        self.packet_buffer = []
        self.db_connection = sqlite3.connect('traffic_analysis.db')
        self.initialize_database()
    
    def initialize_database(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS packet_data (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                source_ip TEXT,
                dest_ip TEXT,
                protocol TEXT,
                length INTEGER,
                flags TEXT,
                payload_data TEXT
            )
        ''')
        self.db_connection.commit()

    def packet_callback(self, packet):
        if IP in packet:
            packet_info = {
                'timestamp': datetime.datetime.now(),
                'source_ip': packet[IP].src,
                'dest_ip': packet[IP].dst,
                'protocol': packet[IP].proto,
                'length': len(packet),
                'flags': packet[TCP].flags if TCP in packet else None,
                'payload': str(packet.payload)
            }
            self.packet_buffer.append(packet_info)
            
            # Buffer management
            if len(self.packet_buffer) >= 1000:
                self.save_to_database()

    def start_capture(self, interface="Wi-Fi"):
        print(f"Starting packet capture on {interface}")
        sniff(iface=interface, prn=self.packet_callback, store=False)

    def save_to_database(self):
        cursor = self.db_connection.cursor()
        for packet in self.packet_buffer:
            cursor.execute('''
                INSERT INTO packet_data 
                (timestamp, source_ip, dest_ip, protocol, length, flags, payload_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                packet['timestamp'],
                packet['source_ip'],
                packet['dest_ip'],
                packet['protocol'],
                packet['length'],
                packet['flags'],
                packet['payload']
            ))
        self.db_connection.commit()
        self.packet_buffer = []

    def stop_capture(self, signum, frame):
        print("Stopping packet capture")
        self.save_to_database()
        self.db_connection.close()
        sys.exit(0)

if __name__ == "__main__":
    analyzer = NetworkTrafficAnalyzer()
    signal.signal(signal.SIGINT, analyzer.stop_capture)
    analyzer.start_capture(interface="Wi-Fi")