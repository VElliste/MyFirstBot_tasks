# connect to mongo
from pymongo import MongoClient
import os

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "DatabaseBot"

client = MongoClient(MONGO_URL)
db = client[DB_NAME]


async def insert_users(user):
    db.Users.insert_one(user)
    # collection= db['Users']
    # collection.count_documents({})

async def insert_task(task):
    db.Tasks.insert_one(task)

async def check_user_registration(user_id):
    user = db.Users.find_one({"id": int(user_id)})
    if user is not None:
        return user
    else:
        return False


async def all_tasks(user_id):
    return db.Tasks.find({"idFrom": int(user_id)})

async def one_task(task_id):
    return db.Tasks.find_one({"idTask": str(task_id)})

async def all_tasks_for_executer(user_id):
    return db.Tasks.find({"idExecuter": int(user_id)})


async def get_all_users():
    return db.Users.find()

async def update_status_executer(taskId):
    tasks_collection = db["Tasks"]
    tasks_collection.update_one(
        {"idTask": taskId},
        {"$set": {"status": "Выполнена"}}
    )

async def update_name(taskId, taskName):
    tasks_collection = db["Tasks"]
    tasks_collection.update_one(
        {"idTask": taskId},
        {"$set": {"nameTask": taskName}}
    )

async def update_info(taskId, taskInfo):
    tasks_collection = db["Tasks"]
    tasks_collection.update_one(
        {"idTask": taskId},
        {"$set": {"taskInfo": taskInfo}}
    )

async def update_deadline(taskId, taskDeadline):
    tasks_collection = db["Tasks"]
    tasks_collection.update_one(
        {"idTask": taskId},
        {"$set": {"taskDeadline": taskDeadline}}
    )

async def update_status(taskId, status):
    tasks_collection = db["Tasks"]
    if status == "Выполнена":
        tasks_collection.update_one(
            {"idTask": taskId},
            {"$set": {"status": "Не выполнена"}}
        )
    else:
        tasks_collection.update_one(
            {"idTask": taskId},
            {"$set": {"status": "Выполнена"}}
        )