class APIStats(object):
    def __init__(self, pid, stats):
        self.pid = pid
        self.stats = stats

class API(object):
    def __init__(self, api_obj):
        self.name = api_obj['api']
        self.return_value = api_obj['return_value']
        self.args = api_obj['arguments']
        self.flags = api_obj['flags']
        self.time = api_obj['time']
        self.category = api_obj['category']

    def __str__(self):
        return "%s(%s)"%(self.name, ', '.join(("%s=%s"%k,v) for k,v in self.args.items()))

class Process(object):
    def __init__(self, pobj):
        self.pid = pobj['pid']
        self.ppid = pobj['ppid']
        self.name = pobj['process_name']
        self.cmd_line = pobj['command_line']
        self.time = pobj['time']
        self.type = Process
        self.call = []

    def call_chain(self, api):
        self.call.append(api)

    def __str__(self):
        return "Process (name=%s, pid=%s)"%(self.name, self.pid)
