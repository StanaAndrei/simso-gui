from collections import defaultdict

class GlobalData:
    enabled_fields = []
    d = {}
    name = ''
    customTaskNameToCode = {}
    selected_heuristic = ''

    EXAMPLE_CODE = r'''
    def customExec(self):
        self._init()
        if not self.period:
            self.period = 1

        print('custom')
        if self._task_info.activation_date:
            print('custom', self._sim.now())
            yield hold, self, int(self._task_info.activation_date * self._sim.cycles_per_ms) \
                - self._sim.now()
            self.create_job()

        for ndate in self.list_activation_dates:
            yield hold, self, int(self.period * ndate * self._sim.cycles_per_ms) \
                - self._sim.now()
            self.create_job()
        '''