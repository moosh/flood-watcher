# 
# main.py
# Copyright (c) 2023 Mooshwerks
# All Rights Reserved
#

import time

class stopwatch:
    def __init__(self) -> None:
        self.start_time = 0
        self.stop_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.stop_time = time.time()

    def elapsedMilliseconds(self):
        return self.elapsedSeconds() / 1000.0

    def elapsedSeconds(self):
        return self.stop_time - self.start_time