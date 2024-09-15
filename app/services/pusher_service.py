from flask import current_app

def send_pusher_event(channel, event, data):
    # Acceder a Pusher desde el contexto de la app
    pusher_client = current_app.config['PUSHER']
    pusher_client.trigger(channel, event, data)
