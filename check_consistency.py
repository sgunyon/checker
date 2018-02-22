class Consistency():
    def __init__(self):
        self.write_list = []
        self.nodes = 0
        self.new_nodes = 0
        self.live_nodes = 0
        self.new_live_nodes = 0

    def consistency(self, dictionary):
        time = dictionary['time']
        module = dictionary['module']
        log = dictionary['type']
        action = dictionary['action']

        output = {
            'time' : time,
            'module' : module,
        }

        if module == 'write':
            self.update_write_list(action)
            if self.check_level(action):
                output['consistency'] = 'succeeded'
            else:
                output['consistency'] = 'failed.'
            output['log validation'] = self.validate_logging(output['consistency'], log)
        elif module == 'read':
            if self.check_level(action):
                output['consistency'] = 'succeeded'
                output['data validation'] = self.validate_reads(action)
            else:
                output['consistency'] = 'failed'
        elif module == 'topology':
            if not log == 'fail':
                output['cluster state'] = self.update_topology(action[0], action[1])
                output['live nodes'] = self.new_live_nodes
            else:
                output['report'] = 'operation failed'
        elif module == 'live_nodes':
            if not log == 'fail':
                output['live nodes'] = self.update_live_nodes(action)
            else:
                output['report'] = 'operation failed'

        print(output)

    def update_topology(self, old_node_update, new_node_update):
        self.nodes = old_node_update
        self.new_nodes = new_node_update

        if self.nodes == 0 or self.new_live_nodes > self.new_nodes:
            self.new_live_nodes = self.new_nodes

        if self.new_nodes > self.nodes and self.nodes > 0:
            self.new_live_nodes = self.new_live_nodes + (self.new_nodes - self.nodes)

        return (self.nodes, self.new_nodes)

    def check_level(self, action):
        consistency_level = action[0]
        if len(action) > 2:
            if consistency_level == 'ALL':
                return self.new_nodes > 0 and self.new_nodes == self.new_live_nodes
            if consistency_level == 'QUORUM':
                return self.new_live_nodes >= ((self.new_nodes // 2) + 1)
            if consistency_level == 'ONE':
                return self.new_live_nodes >= 1
        return False

    def update_write_list(self, action):
        return self.write_list.append((action[1], action[2]))

    def validate_reads(self, action):
        read = (action[1], action[2])
        if read in self.write_list:
            return 'valid'
        return 'invalid'

    def update_live_nodes(self, live_node_update):
        if live_node_update[0] == self.new_live_nodes:
            self.new_live_nodes = live_node_update[1]
            return self.new_live_nodes
        return 'Live node count error'

    def validate_logging(self, consistency, log):
        if consistency == 'succeeded.' and log == 'ok':
            return 'valid'
        if consistency == 'failed' and log == 'fail':
            return 'valid'
        return 'invalid'
