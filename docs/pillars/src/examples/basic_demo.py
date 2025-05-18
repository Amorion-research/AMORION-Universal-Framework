"""
DEVUS Universal Framework - Basic Demonstration
This file demonstrates a simple implementation of DEVUS concepts.
"""

import sys
import time
import random
from pathlib import Path

# Add the src directory to the path so we can import the DEVUS core
sys.path.append(str(Path(__file__).parent.parent / "src"))

from devus_core import DEVUSCore

class SimplePhysicalDevice:
    """A simple physical device used to demonstrate DEVUS principles."""
    
    def __init__(self, device_id, oscillator_drift=0.0001):
        self.device_id = device_id
        self.creation_time = time.time()
        self.oscillator_drift = oscillator_drift
        self.temperature = 20.0 + random.random() * 5.0
        
        # Unique physical characteristics
        self.propagation_delay = 0.000001 * (1 + random.random() * 0.1)
        
        # Internal state
        self.operation_count = 0
    
    def perform_operation(self):
        """Perform a simple operation that affects the device's physical state."""
        # Simulate work
        time.sleep(0.01 * (1 + random.random() * 0.1))
        
        # Update internal state
        self.operation_count += 1
        self.temperature += 0.01 * random.random()
        
        # Return operation result
        return {"timestamp": time.time(), "operation_id": self.operation_count}
    
    def get_physical_properties(self):
        """Return the current physical properties of the device."""
        # Calculate time-dependent jitter (affected by oscillator drift)
        time_since_creation = time.time() - self.creation_time
        current_jitter = 0.0001 * (1 + self.oscillator_drift * time_since_creation)
        
        return {
            "device_id": self.device_id,
            "temperature": self.temperature,
            "propagation_delay": self.propagation_delay,
            "jitter": current_jitter,
            "age": time_since_creation,
            "operations": self.operation_count
        }


class DEVUSDemo:
    """Demonstration of DEVUS principles with simple physical devices."""
    
    def __init__(self):
        self.devus = DEVUSCore()
        self.devices = {}
    
    def create_device(self, device_id):
        """Create a new physical device."""
        self.devices[device_id] = SimplePhysicalDevice(device_id)
        return self.devices[device_id]
    
    def authenticate_device(self, device_id):
        """Authenticate a device using DEVUS principles."""
        if device_id not in self.devices:
            return {"authenticated": False, "reason": "Device not found"}
        
        device = self.devices[device_id]
        properties = device.get_physical_properties()
        
        # Use DEVUS to validate the device's physical-temporal properties
        validation_result = self.devus.validate_physical_temporal_topology(
            properties, 
            t=time.time()
        )
        
        return {
            "authenticated": validation_result.is_valid,
            "device_properties": properties,
            "proof": validation_result.proof if validation_result.is_valid else None
        }
    
    def run_demo(self):
        """Run a demonstration of DEVUS authentication."""
        print("DEVUS Universal Framework - Basic Demonstration")
        print("==============================================")
        
        # Create some devices
        print("\nCreating devices...")
        for i in range(3):
            device_id = f"device_{i}"
            device = self.create_device(device_id)
            print(f"  Created {device_id} with initial properties:")
            for key, value in device.get_physical_properties().items():
                print(f"    {key}: {value}")
        
        # Perform some operations
        print("\nPerforming operations...")
        for _ in range(5):
            for device_id, device in self.devices.items():
                result = device.perform_operation()
                print(f"  {device_id} performed operation {result['operation_id']}")
            time.sleep(0.1)
        
        # Authenticate devices
        print("\nAuthenticating devices...")
        for device_id in self.devices:
            result = self.authenticate_device(device_id)
            print(f"  {device_id}: {'Authenticated' if result['authenticated'] else 'Not authenticated'}")
            if result['authenticated']:
                print(f"    Proof exists with length: {len(str(result['proof']))}")
        
        print("\nDemonstration complete.")


if __name__ == "__main__":
    demo = DEVUSDemo()
    demo.run_demo()
