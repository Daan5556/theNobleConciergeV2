import os
import unittest

from testcontainers.mongodb import MongoDbContainer

from src.config.database import get_database
from src.models.Task import Task

class TestIntegrationTask(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mongo_container = MongoDbContainer("mongo")
        cls.mongo_container.start()
        cls.client = cls.mongo_container.get_connection_client()
        cls.db = cls.client.test
        os.environ["MONGO_CONNECTION_STRING"] = cls.mongo_container.get_connection_url()

    @classmethod
    def tearDownClass(cls):
        cls.mongo_container.stop()

    def tearDown(self):
        for name in self.db.list_collection_names():
            self.db.drop_collection(name)

    def test_task(self):
        task = Task("task1", 1, [1, 2])

        db = get_database()
        tasks_collection = db["tasks"]

        tasks_collection.insert_one(task.to_dict())

        self.assertTrue(tasks_collection.count_documents({}) == 1)

    def test_should_be_emtpy(self):
        db = get_database()
        tasks_collection = db["tasks"]

        self.assertTrue(tasks_collection.count_documents({}) == 0)
