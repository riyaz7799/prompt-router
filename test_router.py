#!/usr/bin/env python3
# ============================================================
#  test_router.py  –  Full Test Suite (20 test messages)
# ============================================================

import json
import os
import sys
import time
from router import handle_message

# ── ANSI colors ──────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[92m"
RED    = "\033[91m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GRAY   = "\033[90m"

# ============================================================
#  Test Cases
#  Each entry: (message, expected_intent_or_None_to_skip)
# ============================================================
TEST_CASES = [
    # ── Clear code intent ──
    ("how do i sort a list of objects in python?",               "code"),
    ("explain this sql query for me",                             "code"),
    ("fxi thsi bug pls: for i in range(10) print(i)",            "code"),

    # ── Clear data intent ──
    ("what's the average of these numbers: 12, 45, 23, 67, 34", "data"),
    ("what is a pivot table",                                     "data"),

    # ── Clear writing intent ──
    ("This paragraph sounds awkward, can you help me fix it?",   "writing"),
    ("Rewrite this sentence to be more professional.",            "writing"),
    ("My boss says my writing is too verbose.",                   "writing"),

    # ── Clear career intent ──
    ("I'm preparing for a job interview, any tips?",             "career"),
    ("How do I structure a cover letter?",                        "career"),
    ("I'm not sure what to do with my career.",                  "career"),

    # ── Ambiguous ──
    ("Help me make this better.",                                 None),
    ("hey",                                                       "unclear"),
    ("Can you write me a poem about clouds?",                    "unclear"),

    # ── Multi-intent ──
    (
        "I need to write a function that takes a user id and returns "
        "their profile, but also i need help with my resume.",
        None,
    ),

    # ── Edge cases ──
    ("",                                                          "unclear"),
    ("x",                                                         "unclear"),
    (
        "I have a dataset of 50,000 rows with sales figures across "
        "regions. The numbers look off. Some entries show negative "
        "revenue which shouldn't be possible. How should I investigate?",
        "data",
    ),

    # ── Manual override ──
    ("@code Fix this: print('hello world'",                      "code"),
    ("@career How do I negotiate my salary?",                    "career"),
]

# ============================================================
#  Runner
# ============================================================
def run_tests():
    print(f"\n{CYAN}{BOLD}{'═'*60}")
    print("  LLM Prompt Router — Full Test Suite")
    print(f"{'═'*60}{RESET}\n")

    passed  = 0
    failed  = 0
    skipped = 0
    results = []

    for i, (message, expected) in enumerate(TEST_CASES, 1):
        display_msg = message[:60] + "..." if len(message) > 60 else message
        print(f"{BOLD}[{i:02d}]{RESET} {display_msg}")

        try:
            msg_to_send = message if message else "hey"
            result = handle_message(msg_to_send)
            intent     = result["intent"]
            confidence = result["confidence"]

            if expected is None:
                status = f"{YELLOW}SKIP (no expected){RESET}"
                skipped += 1
            elif intent == expected:
                status = f"{GREEN}PASS ✓{RESET}"
                passed += 1
            else:
                status = f"{RED}FAIL ✗  (expected: {expected}, got: {intent}){RESET}"
                failed += 1

            print(f"     Intent: {intent} | Confidence: {confidence:.0%} | {status}")
            print(f"     Response preview: {result['response'][:100]}...")

            results.append({
                "test":       i,
                "message":    message,
                "expected":   expected,
                "got":        intent,
                "confidence": confidence,
                "passed":     expected is None or intent == expected,
            })

        except Exception as e:
            print(f"     {RED}ERROR: {e}{RESET}")
            failed += 1

        print()

        # ── Small delay to avoid rate limits ──
        time.sleep(0.5)

    # ── Summary ──
    total = len(TEST_CASES)
    print(f"{CYAN}{BOLD}{'═'*60}")
    print(f"  Results:  {GREEN}{passed} passed{RESET}  |  "
          f"{RED}{failed} failed{RESET}  |  "
          f"{YELLOW}{skipped} skipped{RESET}  |  {total} total")
    print(f"{CYAN}{BOLD}{'═'*60}{RESET}\n")

    # ── Save results ──
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"{GRAY}Full test results saved to test_results.json{RESET}")
    print(f"{GRAY}Route log saved to route_log.jsonl{RESET}\n")

    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)