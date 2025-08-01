# run.py
from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    # Use socketio.run() to start the development server
    socketio.run(app, debug=True)