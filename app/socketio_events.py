# app/socketio_events.py

from flask import render_template
from flask_login import current_user  # We only need current_user
from flask_socketio import emit
from . import socketio, db
from .models import Message

@socketio.on('connect')
def handle_connect():
    # This is the standard way to protect a SocketIO connection.
    # If the user is not authenticated, the connection is refused.
    if not current_user.is_authenticated:
        return False  # This rejects the connection
    
    print(f'Client connected: {current_user.username}')
    # Let the client know they are successfully connected
    emit('connection_response', {'message': f'Welcome, {current_user.username}!'})

@socketio.on('new_message')
def handle_new_message(data):
    # Always check authentication inside the handler
    if not current_user.is_authenticated:
        return # Do nothing if a rogue client sends a message

    msg_body = data.get('body')
    if msg_body:
        message = Message(body=msg_body, author=current_user)
        db.session.add(message)
        db.session.commit()
        
        rendered_message = render_template('_message.html', message=message)
        emit('message_broadcast', {'html': rendered_message}, broadcast=True)

@socketio.on('edit_message')
def handle_edit_message(data):
    if not current_user.is_authenticated:
        return
    
    msg_id = data.get('id')
    new_body = data.get('new_body')
    message = Message.query.get(msg_id)
    
    if message and message.user_id == current_user.id and new_body:
        message.body = new_body
        message.edited = True
        db.session.commit()
        emit('message_edited', {'id': msg_id, 'new_body': new_body}, broadcast=True)

@socketio.on('delete_message')
def handle_delete_message(data):
    if not current_user.is_authenticated:
        return

    msg_id = data.get('id')
    message = Message.query.get(msg_id)
    
    if message and message.user_id == current_user.id:
        db.session.delete(message)
        db.session.commit()
        emit('message_deleted', {'id': msg_id}, broadcast=True)