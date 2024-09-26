import logging
import sys


class Logger(logging.Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        stdout_stream_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s.%(msecs)03d] [%(levelname)s],[%(filename)s:%(lineno)d], %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        stdout_stream_handler.setFormatter(formatter)
        self.addHandler(stdout_stream_handler)
        self.setLevel(logging.INFO)
