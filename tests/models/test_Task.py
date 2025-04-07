from src.models.Task import Task
import unittest


class TestTask(unittest.TestCase):
    def test_TaskShouldBeCreatedCorrectly(self):
        task = Task("task_1", 1, [1, 2])

        self.assertEqual("Task 1", task.name)
        self.assertEqual(1, task.weeks_interval)
        self.assertEqual([1, 2], task.members)

    def test_shouldReturnDict(self):
        task = Task("task_1", 1, [1, 2])

        expected = {
            "name": "Task 1",
            "weeks_interval": 1,
            "members": [1, 2],
            "active_member_pool": [],
            "weeks_until_due": 0,
        }
        task_dict = task.to_dict()

        self.assertEqual(expected, task_dict)
