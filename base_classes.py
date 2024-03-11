from time import time
from threading import Thread
from multiprocessing import Process, Event

class RealTime:

    time_zero = 0

    
    @staticmethod
    def now():
        ''' Change the value of this function to make objects not realtime '''
        return time()

    @property
    def time_since_zero(self):
        """ Return the time since time_zero"""
        return self.now() - self.time_zero
    
    def set_time_zero(self, time_zero=None):
        """ Reset time_zero to the current time or the specified value """
        self.time_zero = time_zero or self.now()

    def sync(self, list_of_objects):
        """ Sync the time zero of the objects in the list to the calling object """
        if not isinstance(list_of_objects, (list, tuple)):
            list_of_objects = [list_of_objects]
        for object in list_of_objects:
            if not isinstance(object, RealTime):
                raise TypeError("Can only sync Real Time objects")
            object.set_time_zero(self.time_zero)


class Threaded:

    thread: Thread = None
    running = False

    def begin(self, threaded = True, multithreaded = False):
        """ End any previous thread. Begin a new one """
        self._end()
        if threaded:
            if multithreaded: 
                self.thread = Process(target = self._run_loop)
            else:
                self.thread = Thread(target = self._run_loop)
            self.running = True
            self.thread.start()
        else:
            self.running = True
            self._run_loop

    def _end(self):
        """ End the thread if one is running """
        self.running = False
        if self.thread is not None:
            if isinstance(self.thread, Process):
                self.thread.terminate()
            try:
                self.thread.join()
            except:
                pass

    def close(self):
        """ End thread and close port """
        self._end()

    def _run_loop(self):
        """ Runs loop until canceled. Should only be run in a thread using .begin() """
        prev = time()
        while self.running:
            self.loop()
            # now = time()
            # print(prev-now)
            # prev = now
            
    def loop(self):
        """ The function that is looped """
        return

    
