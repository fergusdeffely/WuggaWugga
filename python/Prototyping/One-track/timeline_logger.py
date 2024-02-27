import datetime

class TimelineLogger():

    def __init__(self):
        self._entries = []
        self.open_logfile()


    def start(self, t):
        self._t = t


    def log(self, data, t=-1):
        if t != self._t and t != -1:
            self.write()
            self._entries.clear()
            self._entries.append(data)
            self._t = t
        else:
            self._entries.append(data)


    def open_logfile(self):
        now = datetime.datetime.now()
        timestring = f"{now.hour:02d}{now.minute:02d}{now.second:02d}"
        self._f = open(f"./logs/timeline-{timestring}.log", "wt")


    def write(self):
        msg = f"{self._t}"
        for entry in self._entries:
            msg += f": {entry}"
        msg+= '\n'
        self._f.write(msg)
        

# singleton
timeline_logger = TimelineLogger()
