"""Simple runner for manual intent-router smoke testing."""

import logging
import time
from typing import Callable

QueryClassifier = Callable[[str], str]

TEST_QUERIES: tuple[str, ...] = (
    "What are the specifications of the ESP32 microcontroller?",
    "Explain the input-only pins on an ESP32 board.",
    "Can you write a C++ code for blinking an LED on Arduino?",
    "Fix the syntax error in my smart irrigation stepper motor script.",
    "Hi, what is your name and what can you do?",
    "Are you an AI?",
)


def run_tests(classify_fn: QueryClassifier) -> int:
    """Run smoke tests against a classifier and return successful case count."""
    print("=" * 60)
    print("STARTING CLOB INTENT ROUTER TEST SUITE")
    print("=" * 60 + "\n")

    success_count = 0

    for idx, query in enumerate(TEST_QUERIES, 1):
        print(f"Test Case #{idx}")
        print(f"User Input:  '{query}'")

        start_time = time.time()
        try:
            intent = classify_fn(query)
            execution_time = time.time() - start_time
            print(f"Routed To:   [ {intent} ]")
            print(f"Latency:     {execution_time:.2f} seconds")
            success_count += 1
        except (RuntimeError, ValueError, TypeError) as exc:
            print(f"Error processing query '{query}': {exc}")

        print("-" * 60)

    print(
        f"\nTest Suite Completed! ({success_count}/{len(TEST_QUERIES)} queries processed successfully)"
    )
    print("=" * 60)
    return success_count


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.getLogger("router.classifier").setLevel(logging.WARNING)

    from router import classify_intent

    run_tests(classify_intent)
