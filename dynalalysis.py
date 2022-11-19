from threading import Thread
import pythoncom
import wmi

def date_time_format(date_time):
    year = date_time[:4]
    month = date_time[4:6]
    day = date_time[6:8]
    hour = date_time[8:10]
    minutes = date_time[10:12]
    seconds = date_time[12:14]
    return '{0}/{1}/{2} {3}:{4}:{5}'.format(
        day, month, year, hour, minutes, seconds
    )
class ProcessMonitor():
    def __init__(self, notification_filter ='operation'):
        self.process_property = {
            'Caption': None,
            'CreationDate': None,
            'ProcessID': None,
        }
        self.process_watcher = wmi.WMI().Win32_Process.watch_for(
            notification_filter
        )
    def update(self):
        process = self.process_watcher()
        self.process_property['EventType'] = process.event_type
        self.process_property['Caption'] = process.Caption
        self.process_property['CreationDate'] = process.CreationDate
        self.process_property['ProcessID'] = process.ProcessID

    @property
    def event_type(self):
        return self.process_property['EventType']

    @property
    def caption(self):
        return self.process_property['Caption']

    @property
    def creation_date(self):
        return date_time_format(self.process_property['CreationDate'])

    @property
    def process_id(self):
        return self.process_property['ProcessID']

class Monitor(Thread):
    def __init__(self, action):
        self._action = action
        Thread.__init__(self)
    def run(self):
        print('Start monitoring...')
        pythoncom.CoInitialize()
        proc_mon = ProcessMonitor(self._action)
        while True:
            proc_mon.update()
            print(
                proc_mon.creation_date,
                proc_mon.event_type,
                proc_mon.caption,
                proc_mon.process_id
            )
        pythoncom.CoUnitialize()

mon_creation = Monitor('creation')
mon_creation.start()

