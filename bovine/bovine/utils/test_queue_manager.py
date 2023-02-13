from .queue_manager import QueueManager


def test_get_queues_for_actor():
    manager = QueueManager()

    queues = manager.get_queues_for_actor("actor_name")

    assert list(queues) == []


def test_get_queues_for_actor_with_queues():
    manager = QueueManager()

    _, queue1 = manager.new_queue_for_actor("actor_name")
    _, queue2 = manager.new_queue_for_actor("actor_name")

    queues = manager.get_queues_for_actor("actor_name")

    assert set(queues) == {queue1, queue2}


def test_removing_queues():
    manager = QueueManager()

    id1, queue1 = manager.new_queue_for_actor("actor_name")
    id2, queue2 = manager.new_queue_for_actor("actor_name")

    manager.remove_queue_for_actor("actor_name", id1)

    queues = manager.get_queues_for_actor("actor_name")

    assert set(queues) == {queue2}

    manager.remove_queue_for_actor("actor_name", id2)

    queues = manager.get_queues_for_actor("actor_name")

    assert len(queues) == 0
