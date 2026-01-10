import os
from pathlib import Path

CONFIG_FILE_PATH = Path(os.path.join(os.path.dirname(__file__), "..", "..", "..", "config", "config.yaml"))
PARAMS_FILE_PATH = Path(os.path.join(os.path.dirname(__file__), "..", "..", "..", "params.yaml"))