from db.mongodb import get_database
from bson.objectid import ObjectId

from model.step import Step


class StepCRUD:

    def __init__(self):
        self.collection = "step"
        self.db = get_database()

    def insert(self, steps):
        result = {}
        document_id = str(self.db[self.collection].insert_one(steps.dict(by_alias=True)).inserted_id)
        result["_id"] = document_id
        result.update(steps)
        return Step(**result)

    def get_all(self):
        documents = self.db[self.collection].find()
        return [Step(**document) for document in documents]

    def get_by_id(self, _id):
        result = self.db[self.collection].find_one({"_id": ObjectId(_id)})
        if result:
            return Step(**result)

    def delete(self, _id):
        document = self.db[self.collection].find_one({"_id": ObjectId(_id)})
        if document:
            self.db[self.collection].delete_one({"_id": ObjectId(_id)})
            return Step(**document)

    def update(self, _id, step):
        self.db[self.collection].update_one({"_id": ObjectId(_id)}, {"$set": step.dict(by_alias=True)})
        document = self.db[self.collection].find_one({"_id": ObjectId(_id)})
        if document:
            return Step(**document)

