from src.packet_capture import NetworkTrafficAnalyzer
from src.ml_classifier import TrafficClassifier
from src.threat_detector import ThreatDetector
from src.dashboard import Dashboard
import threading

def main():
    # Initialize components
    analyzer = NetworkTrafficAnalyzer()
    classifier = TrafficClassifier()
    detector = ThreatDetector(classifier.model)
    dashboard = Dashboard()
    
    # Start capture in a separate thread
    capture_thread = threading.Thread(target=analyzer.start_capture)
    capture_thread.start()
    
    # Run dashboard
    dashboard.run()

if __name__ == "__main__":
    main()