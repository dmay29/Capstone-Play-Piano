import mido
from mido import Message
from mido.backends.rtmidi import Input
from threading import Thread, Event
from time import time, sleep

PIANO_NAME = 'Impact GX61 MIDI1'

CLICK_BTN = 0 # 66 in shift
RIGHT_KNOB = 1
REWIND_BTN = 2 # 67 in shift
FAST_FORWARD_BTN = 3 # 68 in shift
LOOP_BTN = 4 # 69 in shift

STOP_BTN = 6 # 98 in shift
VOL_KNOB = 7
PLAY_BTN = 8 # 99 in shift
RECORD_BTN = 9 # 100 in shift 

RISING = "rising"
PRESSED = "pressed"
BOTH = "both"
RELEASED = "released"
FALLING = "falling"

VALID_EDGES = [RISING, PRESSED, BOTH, RELEASED, FALLING]

class ControlPianoReader():


    thread:Thread = None
    running: bool = False

    callbacks:dict[str,list[str,callable]] = None

    
    def __init__(self, piano_name = PIANO_NAME):
        
        self._input_port:Input = mido.open_input(piano_name)
        self._pressed_keys = set()
        self._pressed_btns = set()
        self.vol_knob_position = 0
        self.left_knob_position = 0
        self.right_knob_position = 0

        self.callbacks = {}
        
    def begin(self):
        """ End any previous thread. Begin a new one """
        self.end()
        self.thread = Thread(target = self._run)
        self.running = True
        self.thread.start()

    def end(self):
        """ End the thread if one is running """
        self.running = False
        if self.thread is not None:
            self.thread.join()

    def close(self):
        """ End thread and close port """
        self.end()
        self._input_port.close()

    def _run(self):
        """ Main monitoring loop. Should only be run in a thread using ControlPianoReader.begin() """
        while self.running:
            for msg in self._input_port.iter_pending():
                self.read_msg(msg)

    def read_msg(self, msg: Message):
        # A note on message, add the note to the pressed keys set
        # and run callbacks
        if msg.type == "note_on": 
            self._pressed_keys.add(msg.note)
            self.run_callbacks(f"key {msg.note}",[PRESSED,BOTH])

        # A note off message, remove the note from the pressed keys set
        # and run callbacks
        elif msg.type == "note_off":
            self._pressed_keys.discard(msg.note)
            self.run_callbacks(f"key {msg.note}",[RELEASED,BOTH])

        # A pitchwheel message, the left knob is the pitch wheel 
        # Determine if the value was increasing or decreasing
        # Save value and run callbacks
        elif msg.type == "pitchwheel":
            if msg.pitch > self.left_knob_position: edge = RISING
            elif msg.pitch < self.left_knob_position: edge = FALLING
            else: edge = None
            self.left_knob_position = msg.pitch
            self.run_callbacks("left knob",[edge,BOTH])

        # Control messages are all the other controls on the piano
        elif msg.type == "control_change":

            # A right knob message
            # Determine if the value was increasing or decreasing
            # Save value and run callbacks

            if msg.control == RIGHT_KNOB:
                if msg.value > self.right_knob_position: edge = RISING
                elif msg.value < self.right_knob_position: edge = FALLING
                else: edge = None
                self.right_knob_position = msg.value
                self.run_callbacks("right knob",[edge,BOTH])

            # A vol knob message
            # Determine if the value was increasing or decreasing
            # Save value and run callbacks
            elif msg.control == VOL_KNOB:
                if msg.value > self.vol_knob_position: edge = RISING
                elif msg.value < self.vol_knob_position: edge = FALLING
                else: edge = None
                self.vol_knob_position = msg.value
                self.run_callbacks("vol knob",[edge,BOTH])

            # Any other controls, these are the other buttons
            # TODO: Implement button specific names? 
            else:
                # If the value is non-zero the button was pressed
                # Add it to the set and run callbacks
                if msg.value != 0:
                    self._pressed_btns.add(msg.control)
                    self.run_callbacks(f"btn {msg.control}",[PRESSED,BOTH])
                
                # If the value is zero the button was releases
                # Remove it from the set and run callbacks
                else:
                    self._pressed_btns.discard(msg.control)
                    self.run_callbacks(f"btn {msg.control}",[RELEASED,BOTH])

        print(
            f"Keys Pressed: {self.pressed_keys}\n"
            f"Btns Pressed: {self.pressed_btns}\n"
            f"Volume Knob:  {self.vol_knob_position}\n"
            f"Left Knob:    {self.left_knob_position}\n"
            f"Right Knob:   {self.right_knob_position}\n"
        )
    

    # Button/Key Handlers

    @property
    def pressed_keys(self):
        """ List of currently pressed keys """
        return sorted(list(self._pressed_keys))
    
    @property
    def pressed_btns(self):
        """ List of currently pressed buttons """
        return sorted(list(self._pressed_btns))

    
    def key_is_pressed(self,key_num):
        """ Returns True if key is currently pressed """
        return (key_num in self._pressed_keys)

    def btn_is_pressed(self,btn_num):
        """ Returns True if button is currently pressed """
        return (btn_num in self._pressed_btns)


    # Callback Handlers
    def attach_callback(self, name, function: callable, edge: str):
        """ Attach a callback function to the control `name` """
        if edge not in VALID_EDGES:
            raise ValueError(f"Edge must be in {VALID_EDGES}")
        callbacks:list = self.callbacks.get(name, [])
        callbacks.append((edge, function))
        self.callbacks[name] = callbacks

    def remove_callback(self, name, callback_to_remove = None):
        """ 
        Remove the function `callback_to_remove` from the control
        `name`. If `callback_to_remove` is None, remove them all.
        """
        if callback_to_remove is None:
            self.callbacks[name] = []
        else:
            callbacks:list = self.callbacks.get(name, [])
            for i,(edge, callback) in enumerate(callbacks):
                if callback == callback_to_remove:
                    self.callbacks[name].pop(i)
                    return
                
    def attach_key_callback(self, key_num, function: callable, edge = PRESSED):
        """ Attach a callback function to the specified key """
        self.attach_callback(f"key {key_num}", function, edge)
    
    def remove_key_callback(self, key_num, callback_to_remove = None):
        """ 
        Remove the function `callback_to_remove` from the specified key.
        If `callback_to_remove` is None, remove them all.
        """
        self.remove_callback(f"key {key_num}", callback_to_remove)
    

    def attach_btn_callback(self, btn_num, function: callable, edge = PRESSED):
        """ Attach a callback function to the specified button """
        self.attach_callback(f"btn {btn_num}", function, edge)
        
    def remove_btn_callback(self, btn_num, callback_to_remove = None):
        """ 
        Remove the function `callback_to_remove` from the specified btn.
        If `callback_to_remove` is None, remove them all.
        """
        self.remove_callback(f"btn {btn_num}", callback_to_remove)
    

    def attach_vol_knob_callback(self, function: callable, edge = BOTH):
        """ Attach a callback function to the volume knob """
        self.attach_callback("vol knob", function, edge)

    def remove_vol_knob_callback(self, callback_to_remove = None):
        """ 
        Remove the function `callback_to_remove` from the volume knob.
        If `callback_to_remove` is None, remove them all.
        """
        self.remove_callback("vol knob", callback_to_remove)


    def attach_left_knob_callback(self, function: callable, edge = BOTH):
        """ Attach a callback function to the left knob """
        self.attach_callback("left knob", function, edge)

    def remove_left_knob_callback(self, callback_to_remove = None):
        """ 
        Remove the function `callback_to_remove` from the left knob.
        If `callback_to_remove` is None, remove them all.
        """
        self.remove_callback("left knob", callback_to_remove)


    def attach_right_knob_callback(self, function: callable, edge = BOTH):
        """ Attach a callback function to the right knob """
        self.attach_callback(f"right knob", function, edge)

    def remove_right_knob_callback(self, callback_to_remove = None):
        """ 
        Remove the function `callback_to_remove` from the right knob.
        If `callback_to_remove` is None, remove them all.
        """
        self.remove_callback(f"right knob", callback_to_remove)


    def run_callbacks(self, name, valid_edges = None):
        """ 
        Execute any callbacks from control `name` if the edge type is in `valid_edges`.
        If `valid_edges` is None, execute all associated callbacks.
        """
        callback_list = self.callbacks.get(name, [])
        if  isinstance(valid_edges, str):
            valid_edges = [valid_edges]
        for edge,callback in callback_list:
            if valid_edges is None or edge in valid_edges:
                callback()



class NotesPianoReader(ControlPianoReader):
    '''
    Needs to change the way we look at pressed keys.
    Should it just maintain a list of all the note_on/off commands?
    Or should it be an along the way kind of thing? Maybe a blocking generator? 
    Yea i think a generator would work well. 
    But it should also maintain a list probably for looking at later
    '''

    

    def __init__(self, piano_name = PIANO_NAME, time_zero = None):
        self.time_zero = time_zero or time()
        super().__init__(piano_name)
        self._in_progress_notes: list[int, float, int] = []
        self._played_notes: list[int,float,float, int] = []
        self._new_notes_event = Event()
        self._new_notes_event.clear()

    def read_note_msg(self, msg: Message, now = None):
        if now is None:
            now = time()
        if msg.type == "note_on": 
            self._in_progress_notes.append([msg.note, now, msg.velocity])

        elif msg.type == "note_off":
            for i,entry in enumerate(self._in_progress_notes):
                if entry[0] == msg.note:
                    note, start, velocity = self._in_progress_notes.pop(i)
                    self._played_notes.append([note,
                                               start,
                                               now - start,
                                               velocity])
                    self._new_notes_event.set()
                    break

    @property 
    def time_since_zero(self):
        return time()-self.time_zero            

    def get_notes(self):
        '''
        '''
        i = 0
        while True:
            self._new_notes_event.wait()
            while i < len(self._played_notes):
                yield self._played_notes[i]
                i+=1
            self._new_notes_event.clear()
            
                    

    def _run(self):
        while self.running:
            now = self.time_since_zero
            for msg in self._input_port.iter_pending():
                self.read_msg(msg)
                self.read_note_msg(msg, now)

    



if __name__ == '__main__':
    midi = NotesPianoReader()
    l = lambda: print("Vol Changed!")
    midi.attach_vol_knob_callback(l)
    midi.attach_vol_knob_callback(lambda: print("Vol Decreased!"),edge = FALLING)
    midi.attach_key_callback(80, lambda:print("Key 80 pressed!"), edge = PRESSED)
    midi.attach_key_callback(80, lambda:print("Key 80 released!"),edge = RELEASED)
    midi.attach_key_callback(81, lambda:midi.remove_vol_knob_callback(l),edge = PRESSED)
    midi.begin()

    for i in midi.get_notes():
        print(i)
    # try:
    #     while True:
    #         pass
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     midi.close()







