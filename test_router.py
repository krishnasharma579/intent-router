"""
Smoke test runner for the Clob Intent Router.

This script executes a series of benchmark queries to verify routing 
accuracy and measure latency under the current LLM configuration.
"""

import logging
import time
from typing import Callable

# Setting up a cleaner type alias for our classifier function
QueryClassifier = Callable[[str], str]

# Core test dataset reflecting the three main intents
TEST_QUERIES: tuple[str, ...] = (
    "What are the specifications of the ESP32 microcontroller?",
    "Explain the input-only pins on an ESP32 board.",
    "Can you write a C++ code for blinking an LED on Arduino?",
    "Fix the syntax error in my smart irrigation stepper motor script.",
    "Hi, what is your name and what can you do?",
    "Are you an AI?",
)

def run_tests(classify_fn: QueryClassifier) -> int:
    """
    Executes benchmark queries and prints performance metrics.
    
    Returns:
        int: The number of successful classification cycles.
    """
    print("\n" + "=" * 60)
    print("🚀 CLOB INTENT ROUTER: BENCHMARK SUITE")
    print("=" * 60 + "\n")

    success_count = 0
    total_queries = len(TEST_QUERIES)

    for idx, query in enumerate(TEST_QUERIES, 1):
        print(f"Test Case #{idx}/{total_queries}")
        print(f"Input   : '{query}'")

        start_time = time.perf_counter() # More precise for latency than time.time()
        try:
            intent = classify_fn(query)
            latency = time.perf_counter() - start_time
            
            print(f"Intent  : [ {intent} ]")
            print(f"Latency : {latency:.3f}s") # 3 decimal places for milliseconds
            success_count += 1
        except (RuntimeError, ValueError, TypeError) as exc:
            print(f"❌ Failed: {exc}")

        print("-" * 40)

    print(f"\n✅ Suite Finished: {success_count}/{total_queries} Successful")
    print("=" * 60 + "\n")
    return success_count


if __name__ == "__main__":
    # Configure logging to be less noisy during testing
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
    
    # Import here to ensure environment is loaded via core/config
    try:
        from router import classify_intent
        run_tests(classify_intent)
    except Exception as e:
        print(f"CRITICAL: Could not start test suite. {e}")