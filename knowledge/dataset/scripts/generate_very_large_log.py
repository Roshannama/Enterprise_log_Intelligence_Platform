"""Deterministic script to reproduce a very large (10k-50k line) healthy log file.
Usage: python generate_very_large_log.py <num_lines> <output_path>
"""

import sys, random, datetime

random.seed(7)
SERVICES = [
    "api-gateway",
    "payment-service",
    "auth-service",
    "user-service",
    "order-service",
]
BASE = datetime.datetime(2026, 9, 20, 8, 0, 0)


def ts(i):
    return (BASE + datetime.timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S")


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    out = sys.argv[2] if len(sys.argv) > 2 else "very_large_generated.log"
    with open(out, "w") as f:
        for i in range(n):
            svc = random.choice(SERVICES)
            f.write(f"{ts(i)} INFO {svc} Request completed successfully\n")


if __name__ == "__main__":
    main()
