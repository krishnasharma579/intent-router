"""
Test script for the Clob Intent Router.

This script runs a series of test queries through the intent classifier
to verify that the routing logic functions correctly and measures latency
before integrating it into the main LangGraph application.
"""

import time
import logging
from router import classify_intent

# Suppress the detailed logs from our classifier for a cleaner test output
# In production, you would keep these on.
logging.getLogger("router.classifier").setLevel(logging.WARNING)

def run_tests():
    """
    Executes a suite of test queries against the intent router, 
    calculates latency, and prints the results in a formatted structure.
    """
    # A comprehensive mix of queries to test all three defined categories
    test_queries = [
        # Expected: hardware_query
        "What are the specifications of the ESP32 microcontroller?",
        "Explain the input-only pins on an ESP32 board.",
        
        # Expected: code_generation
        "Can you write a C++ code for blinking an LED on Arduino?",
        "Fix the syntax error in my smart irrigation stepper motor script.",
        
        # Expected: general_chat
        "Hi, what is your name and what can you do?",
        "Are you an AI?"
    ]

    print("=" * 60)
    print("STARTING CLOB INTENT ROUTER TEST SUITE")
    print("=" * 60 + "\n")

    success_count = 0

    for idx, query in enumerate(test_queries, 1):
        print(f"Test Case #{idx}")
        print(f"User Input:  '{query}'")
        
        try:
            # Track execution time (Latency)
            start_time = time.time()
            
            # Call the core routing engine
            intent = classify_intent(query)
            
            execution_time = time.time() - start_time
            
            # Print the formatted result
            print(f"Routed To:   [ {intent} ]")
            print(f"Latency:     {execution_time:.2f} seconds")
            success_count += 1
            
        except Exception as e:
            print(f"Error processing query: {e}")
            
        print("-" * 60)

    print(f"\nTest Suite Completed! ({success_count}/{len(test_queries)} queries processed successfully)")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()