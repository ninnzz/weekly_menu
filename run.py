"""
Script to run Flask server.

This is for development purpose only.
For production, use proper server such as WSGU, gUnicorn, etc
"""

from app.server import create_app

# Create application
app = create_app()

# For development use only
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port='5000',
        use_reloader=True,
        threaded=True,
        debug=True)
