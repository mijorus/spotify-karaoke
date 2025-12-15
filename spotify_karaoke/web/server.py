from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import os

from spotify_karaoke.constants import templates_dir, storage_dir
from spotify_karaoke.State import State

app = Flask(__name__, template_folder=templates_dir)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/storage/<path:filename>')
def serve_storage(filename):
    return send_from_directory(storage_dir, filename)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('track_change',  dict(State.state), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def track_change(state):
    print('Received event track_change', state)
    socketio.emit('track_change', dict(state))

def start():
    socketio.run(app, debug=True, host='127.0.0.1', port=os.getenv('HTTP_PORT', 8080))
