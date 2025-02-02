import hashlib
import json
from datetime import datetime
from typing import List, Dict, Optional
from cryptography.fernet import Fernet
from abc import ABC, abstractmethod
import tensorflow as tf
import numpy as np

# Blockchain Implementation
class Block:
    def __init__(self, timestamp: datetime, data: Dict, previous_hash: str):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            "timestamp": str(self.timestamp),
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions: List[Dict] = []

    def create_genesis_block(self) -> Block:
        return Block(datetime.now(), {"message": "Genesis Block"}, "0")

    def add_block(self, data: Dict):
        previous_block = self.chain[-1]
        new_block = Block(datetime.now(), data, previous_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

# Smart Contract Interface
class SmartContract(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        pass

class OrganMatchingContract(SmartContract):
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt_data(self, data: str) -> bytes:
        return self.cipher_suite.encrypt(data.encode())

    def decrypt_data(self, encrypted_data: bytes) -> str:
        return self.cipher_suite.decrypt(encrypted_data).decode()

    def execute(self, recipient_data: Dict, donor_data: Dict) -> Optional[Dict]:
        compatibility_score = self._calculate_compatibility(recipient_data, donor_data)
        
        if compatibility_score >= 0.8:  # Threshold for compatibility
            match_data = {
                "recipient_id": recipient_data["patient_id"],
                "donor_id": donor_data["donor_id"],
                "compatibility_score": compatibility_score,
                "timestamp": str(datetime.now())
            }
            
            # Add match to blockchain
            self.blockchain.add_block(match_data)
            return match_data
        return None

    def _calculate_compatibility(self, recipient: Dict, donor: Dict) -> float:
        blood_match = recipient["blood_type"] == donor["blood_type"]
        organ_match = recipient["organ_type"] == donor["organ_type"]
        
        if not (blood_match and organ_match):
            return 0.0
        
        hla_score = self._calculate_hla_compatibility(
            recipient["hla_typing"],
            donor["hla_typing"]
        )
        
        return hla_score

    def _calculate_hla_compatibility(self, hla_recipient: str, hla_donor: str) -> float:
        recipient_set = set(hla_recipient.split(','))
        donor_set = set(hla_donor.split(','))
        matches = len(recipient_set.intersection(donor_set))
        total = len(recipient_set.union(donor_set))
        return matches / total

# AI-based Intrusion Detection System
class MLIDS:
    def __init__(self):
        self.model = self._build_model()
        
    def _build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(10,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def detect_anomaly(self, transaction_data: Dict) -> bool:
        # Convert transaction data to feature vector
        features = self._extract_features(transaction_data)
        prediction = self.model.predict(np.array([features]))
        return bool(prediction[0] > 0.5)

    def _extract_features(self, transaction_data: Dict) -> List[float]:
        # Feature engineering from transaction data
        # This is a simplified version - in production, this would be more comprehensive
        features = [
            len(str(transaction_data)),  # Size of transaction
            transaction_data.get("timestamp", 0),  # Timestamp
            hash(str(transaction_data)) % 1000,  # Hash-based feature
            # Add more relevant features...
        ]
        # Pad to 10 features
        return features + [0] * (10 - len(features))

class SecureOrganDonationNetwork:
    def __init__(self):
        self.blockchain = Blockchain()
        self.smart_contract = OrganMatchingContract(self.blockchain)
        self.ids = MLIDS()

    def process_donation_request(self, recipient_data: Dict, donor_data: Dict) -> Optional[Dict]:
        # Check for suspicious activity
        if self.ids.detect_anomaly(recipient_data) or self.ids.detect_anomaly(donor_data):
            print("Warning: Suspicious activity detected!")
            return None

        # Execute matching through smart contract
        match_result = self.smart_contract.execute(recipient_data, donor_data)
        
        if match_result:
            # Encrypt sensitive data before storing
            match_result["encrypted_medical_data"] = self.smart_contract.encrypt_data(
                json.dumps({
                    "recipient_hla": recipient_data["hla_typing"],
                    "donor_hla": donor_data["hla_typing"]
                })
            )
            
        return match_result

# Example usage
if __name__ == "__main__":
    network = SecureOrganDonationNetwork()
    
    # Example donation request
    recipient = {
        "patient_id": "P123",
        "organ_type": "Kidney",
        "blood_type": "O+",
        "hla_typing": "A1,B8,DR3"
    }
    
    donor = {
        "donor_id": "D456",
        "organ_type": "Kidney",
        "blood_type": "O+",
        "hla_typing": "A1,B8,DR3"
    }
    
    result = network.process_donation_request(recipient, donor)
    
    if result:
        print(f"Match found! Compatibility score: {result['compatibility_score']}")
        print(f"Match recorded in block with hash: {network.blockchain.chain[-1].hash}")
    else:
        print("No suitable match found or suspicious activity detected.")