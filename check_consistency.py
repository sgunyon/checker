class Consistency():
    def __init__(self):
        self.write_list = []
        self.old_nodes = 0
        self.new_nodes = 0
        self.live_nodes = 0

    def route_modules(self, dictionary):
        module = dictionary['module']
        action = dictionary['action']
        log = dictionary['type']
        #time = dictionary['time']

        if module == 'topology':
            old_node_update = action[0]
            new_node_update = action[1]
            self.update_topology(old_node_update, new_node_update)

        if module == 'write':
            if self.check_level(action[0]):
                #print("Consistency met")
                write = (action[1], action[2])
                return self.write_list.append(write)

        if module == 'read':
            if self.check_level(action[0]):
                return self.validate_reads(action)

        if module == 'live_nodes':
            #self.old_live_nodes = action[0]
            self.live_nodes = action[1]
            self.update_live_nodes(self.live_nodes)

    def update_topology(self, old_node_update, new_node_update):
        self.old_nodes = old_node_update
        self.new_nodes = new_node_update

        if self.old_nodes == 0 or self.live_nodes > self.new_nodes:
            self.live_nodes = self.new_nodes

        if self.new_nodes > self.old_nodes and self.old_nodes > 0:
            self.live_nodes = self.live_nodes + (self.new_nodes - self.old_nodes)

        # Troubleshooting
        print(self.old_nodes, self.new_nodes, self.live_nodes)

    def update_live_nodes(self, live_node_update):
        self.live_nodes = live_node_update
        print(self.old_nodes, self.new_nodes, self.live_nodes)

    def check_level(self, consistency_level):
        if consistency_level == 'ALL':
            return self.new_nodes > 0 and self.new_nodes == self.live_nodes
        if consistency_level == 'QUORUM':
            return self.live_nodes >= ((self.new_nodes // 2) + 1)
        if consistency_level == 'ONE':
            return self.live_nodes >= 1
        print('Consistency_level not met')

    def validate_reads(self, action):
            read = (action[1], action[2])
            if read in self.write_list:
                return
                #self.validate_logging(log)
            print('Value never written')

    def validate_logging(self, type):
        pass

    def logging_output(self):
        pass
