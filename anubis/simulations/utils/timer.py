import time

class Timer:
    def __init__(self):
        self.start_time = time.time()
        print("⏱️  Timer started...")

    def done(self):
        elapsed = time.time() - self.start_time
        minutes, seconds = divmod(elapsed, 60)
        print(f"✅ Done in {int(minutes)}m {int(seconds)}s")
