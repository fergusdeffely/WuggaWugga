import datetime

class TimelineLogger():

    def __init__(self):
        self._entries = []
        self.open_logfile()
        self._cycle = 0


    def log(self, data, cycle=-1):
        if cycle != self._cycle and cycle != -1:
            self.write()
            self._entries.clear()
            self._entries.append(data)
            self._cycle = cycle
        else:
            self._entries.append(data)


    def open_logfile(self):
        now = datetime.datetime.now()
        timestring = f"{now.hour:02d}{now.minute:02d}{now.second:02d}"
        self._f = open(f"./logs/timeline-{timestring}.log", "wt")


    def write(self):
        msg = f"{self._cycle:08d}"
        for entry in self._entries:
            msg += f": {entry}"
        msg+= '\n'
        self._f.write(msg)
       

# singleton
timeline_logger = TimelineLogger()
