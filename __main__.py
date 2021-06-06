import random
import time

from SpotChecker import SpotChecker

WAITING_TIME_NEXT_TRY = 600  # How long to wait before trying again?

def main():
    while True:
        checker = SpotChecker()
        checker.check_for_spot()

        time.sleep(WAITING_TIME_NEXT_TRY + random.uniform(1, 50))  # Wait till checking again.

if __name__ == "__main__":
    main()
