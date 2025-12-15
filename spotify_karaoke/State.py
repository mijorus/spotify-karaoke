import multiprocessing

class State():
    state = None

    listeners = []

    @staticmethod
    def update_state(status='', track_name='', scale='', vocals_track=None, inst_track=None):
        State.state['status'] = status
        State.state['track_name'] = track_name
        State.state['scale'] = scale
        State.state['vocals_track'] = vocals_track
        State.state['inst_track'] = inst_track

    @staticmethod
    def update_track(vocals_track=None, inst_track=None):
        State.state['vocals_track'] = vocals_track
        State.state['inst_track'] = inst_track

        for l in State.listeners:
            l(State.state)

    @staticmethod
    def add_listener(func):
        State.listeners.append(func)