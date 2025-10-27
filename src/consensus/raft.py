class RaftNode:
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers
        self.state = "follower"  # follower, candidate, leader
        self.current_term = 0
        self.voted_for = None
        self.log = []

    def request_vote(self):
        # nanti kita isi di tahap implementasi Raft
        pass

    def append_entries(self):
        # nanti diisi untuk replicate log
        pass
