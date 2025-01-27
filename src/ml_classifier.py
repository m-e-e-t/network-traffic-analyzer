import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class TrafficClassifier:
    def __init__(self, n_estimators=100, test_size=0.2, random_state=42):
        self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
        self.scaler = StandardScaler()
        self.test_size = test_size
        self.random_state = random_state
    
    def prepare_data(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        return train_test_split(X_scaled, y, test_size=self.test_size, random_state=self.random_state)
    
    def train(self, X, y):
        X_train, X_test, y_train, y_test = self.prepare_data(X, y)
        self.model.fit(X_train, y_train)
        accuracy = self.model.score(X_test, y_test)
        print(f"Model Accuracy: {accuracy:.4f}")
    
    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
