#!/usr/bin/env python3
"""
Test script to debug role selection issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.auth_service import auth_service

def test_role_mapping():
    """Test the role mapping functionality directly"""
    print("Testing role mapping...")
    
    # Test vendor role
    print("\n1. Testing 'vendor' role:")
    print(f"   Input role: 'vendor'")
    
    try:
        result = auth_service.api_register_user(
            email="test_vendor@example.com",
            password="testpass123",
            name="Test Vendor",
            role="vendor"
        )
        print(f"   Registration result: {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test job_seeker role
    print("\n2. Testing 'job_seeker' role:")
    print(f"   Input role: 'job_seeker'")
    
    try:
        result = auth_service.api_register_user(
            email="test_jobseeker@example.com",
            password="testpass123", 
            name="Test Job Seeker",
            role="job_seeker"
        )
        print(f"   Registration result: {result}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_role_mapping()