class Consistency():
    def __init__(self):
        self.output = {}
        self.write_list = []
        self.old_nodes = 0
        self.new_nodes = 0
        self.live_nodes = 0

    def consistency(self, dictionary):
        time = dictionary['time']
        module = dictionary['module']
        log = dictionary['type']
        action = dictionary['action']

        self.output = {
            'time' : time,
            'module' : module,
        }

        if module == 'topology':
            self.output['node state'] = self.update_topology(action[0], action[1])

        if module == 'write':
            self.update_write_list(action)
            if self.check_level(action):
                 self.output['consistency'] = 'Consistency check succeeded.'
            else:
                self.output['consistency'] = 'Consistency check failed.'
            self.output['logging'] = self.validate_logging(self.output['consistency'], log)

        if module == 'read':
            if self.check_level(action):
                self.output['consistency'] = 'Consistency check succeeded.'
                self.output['data validation'] = self.validate_reads(action)
            else:
                self.output['consistency'] = 'Consistency check failed.'

        if module == 'live_nodes':
            self.output['live nodes'] = self.update_live_nodes(action[1])

        self.create_output(self.output)

    def update_topology(self, old_node_update, new_node_update):
        self.old_nodes = old_node_update
        self.new_nodes = new_node_update

        if self.old_nodes == 0 or self.live_nodes > self.new_nodes:
            self.live_nodes = self.new_nodes

        if self.new_nodes > self.old_nodes and self.old_nodes > 0:
            self.live_nodes = self.live_nodes + (self.new_nodes - self.old_nodes)

        return (self.old_nodes, self.new_nodes)

    def check_level(self, action):
        consistency_level = action[0]
        if len(action) > 2:
            if consistency_level == 'ALL':
                return self.new_nodes > 0 and self.new_nodes == self.live_nodes
            if consistency_level == 'QUORUM':
                return self.live_nodes >= ((self.new_nodes // 2) + 1)
            if consistency_level == 'ONE':
                return self.live_nodes >= 1
        return False

    def update_write_list(self, action):
        return self.write_list.append((action[1], action[2]))

    def validate_reads(self, action):
        read = (action[1], action[2])
        if read in self.write_list:
            return 'Found corresponding write.'
        return 'No correpsonding write.'

    def update_live_nodes(self, live_node_update):
        self.live_nodes = live_node_update
        return self.live_nodes

    def validate_logging(self, consistency, log):
        if consistency == 'Consistency check succeeded.' and log == 'ok':
            return 'Logging confirmed'
        if consistency == 'Consistency check failed.' and log == 'failed':
            return 'Logging confirmed'
        return 'Logging failed'

    def create_output(self, input):
        print(input)
