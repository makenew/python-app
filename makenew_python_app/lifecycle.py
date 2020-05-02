class Lifecycle:
    def __init__(self, log, flags):
        self._log = log
        self._flags = flags

    def on_start(self):
        self._log.info("On Start")
