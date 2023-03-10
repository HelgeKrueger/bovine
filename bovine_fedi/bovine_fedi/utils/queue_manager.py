import asyncio
import uuid
from collections import defaultdict


class QueueManager:
    def __init__(self):
        self.queues = defaultdict(dict)

    def get_queues_for_actor(self, actor_name):
        return self.queues[actor_name].values()

    def new_queue_for_actor(self, actor_name):
        queue_id = uuid.uuid4()
        queue = asyncio.Queue()

        self.queues[actor_name][queue_id] = queue

        return queue_id, queue

    def remove_queue_for_actor(self, actor_name, queue_id):
        del self.queues[actor_name][queue_id]
