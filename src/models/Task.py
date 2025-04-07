import random

from bson import ObjectId

from src.config.database import get_database

from pymongo import collection


class Task:
    collection: collection = get_database().tasks

    def __init__(self, name: str = "Task", weeks_interval: int = 0, members: [int] = None,
                 active_member_pool: [int] = None, weeks_until_due: int = None, _id=None):
        if members is None:
            members = []
        if active_member_pool is None:
            active_member_pool = []
        if int(weeks_interval) < 0:
            weeks_interval = 0
        if weeks_until_due is None:
            weeks_until_due = 0
        self._id = _id
        self.name: str = name.casefold().replace("_", " ").capitalize()
        self.weeks_interval: int = int(weeks_interval)
        self.members: [int] = members
        self.active_member_pool: [int] = active_member_pool
        self.weeks_until_due: int = weeks_until_due

    def to_dict(self):
        return {
            "name": self.name,
            "weeks_interval": self.weeks_interval,
            "members": self.members,
            "active_member_pool": self.active_member_pool,
            "weeks_until_due": self.weeks_until_due,
        }

    def save(self):
        if self._id:
            Task.collection.update_one(
                {"_id": ObjectId(self._id)},
                {"$set": self.to_dict()}
            )
        else:
            result = Task.collection.insert_one(self.to_dict())
            self._id = result.inserted_id

    @classmethod
    def get(cls, task_id):
        data = cls.collection.find_one({"_id": ObjectId(task_id)})
        return cls(**data)

    def is_due(self):
        return self.weeks_until_due == 0

    def assign(self):
        if not self.is_due():
            self.weeks_until_due -= 1
            self.save()
            return None

        if not self.active_member_pool:
            self.active_member_pool = self.members

        assignee = random.choice(self.active_member_pool)
        self.active_member_pool.remove(assignee)

        self.weeks_until_due = self.weeks_until_due
        self.save()

        return assignee
