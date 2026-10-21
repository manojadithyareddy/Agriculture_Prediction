import os
import sys
import logging

log_file = os.path.join(os.path.dirname(__file__), "server.log")
logging.basicConfig(
    filename=log_file,
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logging.info("start_server.py invoked.")

try:
    import uvicorn
    logging.info("uvicorn imported.")
    import main
    logging.info("main imported successfully.")
    logging.info("Starting uvicorn server on http://127.0.0.1:8000 ...")
    uvicorn.run(main.app, host="127.0.0.1", port=8000, log_level="info")
except Exception as e:
    logging.exception(f"Startup error: {e}")
