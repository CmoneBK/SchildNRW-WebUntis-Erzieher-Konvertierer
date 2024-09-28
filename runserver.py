"""
This script runs the ErzieherKonverter application using a development server.
"""

from os import environ
from ErzieherKonvertierer import app
import logging

# Configure logging to display DEBUG messages
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '127.0.0.1')  # Ensure we're using 127.0.0.1
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))  # Use the default Flask port
    except ValueError:
        PORT = 5000

    app.logger.info(f"Starting Flask app on {HOST}:{PORT} with debug mode enabled (reloader disabled)")

    # Start the Flask application with debug mode enabled but disable the auto-reloader
    app.run(host=HOST, port=PORT, debug=True, use_reloader=False)
