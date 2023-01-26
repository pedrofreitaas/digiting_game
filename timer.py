from time import time as tm

class Timer():

    class pausedDeactivatedClock(AssertionError):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)
    class unpausingNotPausedClock(AssertionError):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)
    
    timers : list['Timer'] = []
    id = 1
    
    def unpauseAllTimers() -> None:
        '''Unpausing all the registered timers.\n
           Won't throw.\n'''
        for timer in Timer.timers:
            try: timer.unpause()
            except Timer.unpausingNotPausedClock: pass
            except Timer.unpausingNotPausedClock: pass

    def pauseAllTimers() -> None:
        '''Pausing all the registered timers.\n
           Won't throw.\n'''
        for timer in Timer.timers:
            try: timer.pause()
            except Timer.pausedDeactivatedClock: pass

    def updAllTimers() -> None:
        '''Updates all the registered timers in the game.\n
           If it's defined to work only once, deletes the timer afterwards.\n'''
        
        for timer in Timer.timers:

            if not timer.activated:
                continue

            if timer.destroyed:
                Timer.timers.remove(timer)
                continue

            if tm() - timer.trigger_time >= timer.how_long:
                timer.procedure()
                
                if timer.once: Timer.timers.remove(timer)

                timer.trigger_time = tm()

    def __eq__(self, __o: object) -> bool:
        if type(self) == type(__o) and self.id == __o.id:
            return True
        return False

    def __init__(self, howLong: float, procedure: callable, once: bool) -> None:
        '''Creates a timer instance.\n
           howLong: the amount of time for the timer.\n
           procedure: the method to be called after the timer expires.\n
           once: bool to define if the timer is going to be used once or many times.\n'''
        
        self.id = Timer.id
        Timer.id += 1

        self.trigger_time = tm()
        self.how_long = howLong
        self.procedure = procedure
        self.once = once

        self.destroyed = False
        self.activated = True
        self.paused = False

        Timer.timers.append(self)

        #aux.
        self.time_spent_before_pause = 0

    def changeTime(self, cycleTime: float, reset: bool = False) -> None:
        '''Changes the cycle time to the new value.\n'''

        self.how_long = cycleTime

        if reset:
            self.trigger_time = tm()

    def reconfig(self, howLong: float) -> None:
        '''Reconfigs the timer to conclude after a new time.\n
           Doesn't activates the timer if it's deactivated.\n'''

        self.how_long = howLong
        self.trigger_time = tm()

    def destroyTimer(self) -> None:
        '''Timer will be destroyed and won't conclude any other time.\n'''

        self.destroyed = True

    def pause(self) -> None:
        '''Pauses the instance.\n
           Different from deactivation, when paused, a clock has to be unpaused by the unpause function.\n
           When unpaused, the timer will consider the time that past in the last cyle (before it was paused).\n
           Pausing a deactivated clock will throw.\n
           Pausing a paused clock will do nothing.\n'''

        if not self.activated:
            raise Timer.pausedDeactivatedClock

        if self.paused:
            return 

        self.paused = True
        self.time_spent_before_pause = self.how_long - (tm() - self.trigger_time)

        if self.time_spent_before_pause <= 0:
            self.time_spent_before_pause = 0

    def unpause(self) -> None:
        '''Unpauses the instance.\n
           The instance will start counting the time that alredy passed in the last cycle.\n
           Unpausing a deactivated clock will throw.\n
           Unpausing a not paused clock will throw.\n'''

        if not self.activated:
            raise Timer.pausedDeactivatedClock

        if not self.paused:
            raise Timer.unpausingNotPausedClock

        self.paused = False
        self.trigger_time = tm() - self.time_spent_before_pause

    def deactiveTimer(self) -> None:
        '''Timer will be deactivated, so it won't take effect.\n
           Different from pausing.\n
           If instance is paused, does nothing.\n
           If instance alredy deactivated, does nothing.\n'''

        if self.paused:
            return

        if not self.activated:
            return

        self.activated = False
    
    def activateTimer(self) -> None:
        '''Timer will take effect after the time it was set to conclude.\n
           Trigger time is set to the moment of the call.\n
           With the instance is paused, won't do anything.\n
           If instance is alredy active, does nothing.\n'''

        if self.paused:
            return

        if self.activated:
            return

        self.activated = True
        self.trigger_time = tm()
