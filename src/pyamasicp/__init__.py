import logging
import sys

stdout_handler = logging.StreamHandler(sys.stdout)
stderr_handler = logging.StreamHandler(sys.stderr)

# Set levels for handlers
stdout_handler.setLevel(logging.DEBUG)
stderr_handler.setLevel(logging.WARNING)

# Create formatters and add it to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)
stderr_handler.setFormatter(formatter)

logging.basicConfig(handlers=[stdout_handler, stderr_handler])
