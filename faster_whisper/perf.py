import time

class TimingHelper:
    def __init__(self):
        self.timings = {}
        self.start_times = {}

    def start(self, name_id):
        """Start timing for a code block identified by name_id."""
        self.start_times[name_id] = time.time()

    def stop(self, name_id):
        """Stop timing for a code block and calculate the elapsed time."""
        if name_id not in self.start_times:
            raise ValueError(f"Timing for {name_id} was never started or has already been stopped.")
        elapsed_time = time.time() - self.start_times.pop(name_id)
        if name_id in self.timings:
            self.timings[name_id] += elapsed_time
        else:
            self.timings[name_id] = elapsed_time

    def print(self):
        """Print the timings for all tracked code blocks."""
        for name_id, elapsed_time in self.timings.items():
            print(f"🚀🚀🚀 {name_id} took {elapsed_time:.4f} seconds.")
        self.timings.clear()  # Reset timings after printing