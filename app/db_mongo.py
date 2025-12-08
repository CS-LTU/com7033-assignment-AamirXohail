from datetime import datetime

from flask import current_app, g
from pymongo import MongoClient


def _get_mongo_client() -> MongoClient:
    """
    Lazily create and cache a MongoDB client on the Flask 'g' object.
    """
    if "mongo_client" not in g:
        uri = current_app.config["MONGO_URI"]
        g.mongo_client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    return g.mongo_client


def _get_db():
    client = _get_mongo_client()
    db_name = current_app.config.get("MONGO_DB_NAME", "hospital_management_db")
    return client[db_name]


def get_patient_collection():
    """
    Collection for patient records.
    """
    return _get_db()["patients"]


def get_activity_collection():
    """
    Collection for audit / activity logs.
    """
    return _get_db()["activity_logs"]


def log_activity(username: str, action: str, details: str | None = None) -> None:
    """
    Write a simple audit entry to MongoDB.

    :param username: user who triggered the action
    :param action: short code such as CREATE_PATIENT, UPDATE_PATIENT,
                   DELETE_PATIENT, UPLOAD_DATASET
    :param details: free-text description of what happened
    """
    coll = get_activity_collection()
    doc = {
        "username": username,
        "action": action,
        "details": details,
        "timestamp": datetime.utcnow(),
    }
    try:
        coll.insert_one(doc)
    except Exception as exc:  # pragma: no cover
        # Do not break the app just because logging failed
        current_app.logger.warning("Failed to write activity log: %s", exc)


def close_mongo_client(exception=None):
    """
    Close the Mongo client at the end of the request/app context.
    """
    client: MongoClient | None = g.pop("mongo_client", None)
    if client is not None:
        client.close()
