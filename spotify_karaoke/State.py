class State():
    state = {}

    listeners = []
    
    @staticmethod
    def _send_notif():
        for l in State.listeners:
            l(State.state)

    @staticmethod
    def update_state(status='', track_name='', scale='', vocals_track=None, inst_track=None):
        State.state['status'] = status
        State.state['track_name'] = track_name
        State.state['scale'] = scale
        State.state['vocals_track'] = vocals_track
        State.state['inst_track'] = inst_track
        State.state['progress'] = 0
        State._send_notif()

    @staticmethod
    def update_track(vocals_track=None, inst_track=None):
        State.state['vocals_track'] = vocals_track
        State.state['inst_track'] = inst_track
        State._send_notif()
    
    @staticmethod
    def update_track_progress(p):
        State.state['progress'] = p
        State._send_notif()

    @staticmethod
    def add_listener(func):
        State.listeners.append(func)