import mido
from mido import Message
from mido.backends.rtmidi import Input
from threading import Event
from scoring import score_note

from base_classes import RealTime, Threaded

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

class ControlPianoReader(Threaded):


    callbacks:dict[str,list[str,callable]] = None

    
    def __init__(self, piano_name = PIANO_NAME, keys_offset = 0):
        
        self._input_port:Input = mido.open_input(piano_name)
        self._pressed_keys = set()
        self._pressed_btns = set()
        self.vol_knob_position = 0
        self.left_knob_position = 0
        self.right_knob_position = 0

        self.callbacks = {}

        self.keys_offset = keys_offset
        
    def close(self):
        """ End thread and close port """
        super(self, Threaded).close()
        self._input_port.close()
            
    def loop(self):
        """ Mian monitoring loop """
        for msg in self._input_port.iter_pending():
                self.read_msg(msg)

    def read_msg(self, msg: Message):
        # A note on message, add the note to the pressed keys set
        # and run callbacks
        if msg.type == "note_on": 
            note_num = msg.note - self.keys_offset
            self._pressed_keys.add(note_num)
            self.run_callbacks(f"key {note_num}",[PRESSED,BOTH], note_num)

        # A note off message, remove the note from the pressed keys set
        # and run callbacks
        elif msg.type == "note_off":
            note_num = msg.note - self.keys_offset
            self._pressed_keys.discard(note_num)
            self.run_callbacks(f"key {note_num}",[RELEASED,BOTH], note_num)

        # A pitchwheel message, the left knob is the pitch wheel 
        # Determine if the value was increasing or decreasing
        # Save value and run callbacks
        elif msg.type == "pitchwheel":
            if msg.pitch > self.left_knob_position: edge = RISING
            elif msg.pitch < self.left_knob_position: edge = FALLING
            else: edge = None
            self.left_knob_position = msg.pitch
            self.run_callbacks("left knob",[edge,BOTH], self.left_knob_position)

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
                self.run_callbacks("right knob",[edge,BOTH], self.right_knob_position)

            # A vol knob message
            # Determine if the value was increasing or decreasing
            # Save value and run callbacks
            elif msg.control == VOL_KNOB:
                if msg.value > self.vol_knob_position: edge = RISING
                elif msg.value < self.vol_knob_position: edge = FALLING
                else: edge = None
                self.vol_knob_position = msg.value
                self.run_callbacks("vol knob",[edge,BOTH], self.vol_knob_position)

            # Any other controls, these are the other buttons
            # TODO: Implement button specific names? 
            else:
                # If the value is non-zero the button was pressed
                # Add it to the set and run callbacks
                if msg.value != 0:
                    self._pressed_btns.add(msg.control)
                    self.run_callbacks(f"btn {msg.control}",[PRESSED,BOTH], msg.control)
                
                # If the value is zero the button was releases
                # Remove it from the set and run callbacks
                else:
                    self._pressed_btns.discard(msg.control)
                    self.run_callbacks(f"btn {msg.control}",[RELEASED,BOTH], msg.control)

        # print(
        #     f"Keys Pressed: {self.pressed_keys}\n"
        #     f"Btns Pressed: {self.pressed_btns}\n"
        #     f"Volume Knob:  {self.vol_knob_position}\n"
        #     f"Left Knob:    {self.left_knob_position}\n"
        #     f"Right Knob:   {self.right_knob_position}\n"
        # )
    

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


    def run_callbacks(self, name, valid_edges = None, *args):
        """ 
        Execute any callbacks from control `name` if the edge type is in `valid_edges`.
        If `valid_edges` is None, execute all associated callbacks.
        """
        callback_list = self.callbacks.get(name, [])
        if  isinstance(valid_edges, str):
            valid_edges = [valid_edges]
        for edge,callback in callback_list:
            if valid_edges is None or edge in valid_edges:
                callback(*args)



class NotesPianoReader(ControlPianoReader, RealTime):
    '''
    Needs to change the way we look at pressed keys.
    Should it just maintain a list of all the note_on/off commands?
    Or should it be an along the way kind of thing? Maybe a blocking generator? 
    Yea i think a generator would work well. 
    But it should also maintain a list probably for looking at later
    '''

    

    def __init__(self, piano_name = PIANO_NAME, time_zero = None, keys_offset = 0):
        self.set_time_zero()
        super().__init__(piano_name, keys_offset)
        self._in_progress_notes: list[int, float, int] = []
        self._played_notes: list[int,float,float, int] = []
        self._new_notes_event = Event()
        self._new_notes_event.clear()
        self._note_index = 0


    def read_note_msg(self, msg: Message, now = None):
        if now is None:
            now = self.time_since_zero
        if msg.type == "note_on": 
            note_num = msg.note - self.keys_offset
            self._in_progress_notes.append([note_num, now, msg.velocity])

        elif msg.type == "note_off":
            note_num = msg.note - self.keys_offset
            for i,entry in enumerate(self._in_progress_notes):
                if entry[0] == note_num:
                    note, start, velocity = self._in_progress_notes.pop(i)
                    self._played_notes.append([note,
                                               start,
                                               now - start,
                                               velocity])
                    self._new_notes_event.set()
                    break         

    def get_notes(self):
        '''
        '''
        if self.notes_available():
            notes = self._played_notes[self._note_index:]
            self._note_index += len(notes)
            self._new_notes_event.clear()
            return notes
        else:
            return []

    def notes_available(self):
        return self._new_notes_event.is_set()
            
                    

    def loop(self):
        for msg in self._input_port.iter_pending():
            print(msg)
            self.read_msg(msg)
            now = self.time_since_zero
            self.read_note_msg(msg, now)

class PianoScorer(NotesPianoReader):
    def __init__(self, piano_name = PIANO_NAME, time_zero = None, keys_offset = 0, notes_dict:dict = None):
        self.set_time_zero()
        super().__init__(piano_name, keys_offset)
        self._in_progress_notes: list[int, float, int] = []
        self._played_notes: list[int,float,float, int] = []
        self._new_notes_event = Event()
        self._new_notes_event.clear()
        self.correct_notes_dict = notes_dict
        

    def loop(self):
        super().loop()
        while self.notes_available():
            print(score_note(self.correct_notes_dict, next(self.notes)))


    



if __name__ == '__main__':
    midi = NotesPianoReader()
    l = lambda x: print("Vol Changed!")
    midi.attach_vol_knob_callback(l)
    midi.attach_vol_knob_callback(lambda x: print("Vol Decreased!"),edge = FALLING)
    midi.attach_key_callback(80, lambda x:print("Key 80 pressed!"), edge = PRESSED)
    midi.attach_key_callback(80, lambda x:print("Key 80 released!"),edge = RELEASED)
    midi.attach_key_callback(81, lambda x:midi.remove_vol_knob_callback(l),edge = PRESSED)
    midi.attach_key_callback(97, lambda x:midi._end(),edge = RELEASED)
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







