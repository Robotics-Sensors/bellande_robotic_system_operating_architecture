from common_msgs import *
import time

class Example_python:
    def run(self):
        while True:
            # TODO: Implement node logic
            print(f"Running example_python")
            time.sleep(1)

if __name__ == "__main__":
    node = Example_python()
    node.run()
