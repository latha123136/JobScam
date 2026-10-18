"""
Database Connection Module
MongoDB Atlas connection with Motor async driver
Falls back gracefully if MongoDB is not available
"""

from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fake_job_detection")

# Try to import motor, fall back to mock if not available
try:
    from motor.motor_asyncio import AsyncIOMotorClient
    client = AsyncIOMotorClient(MONGODB_URL)
    database = client[DATABASE_NAME]
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    database = None


class MockCollection:
    """Mock collection for when MongoDB is not available"""
    async def insert_one(self, doc):
        return type('obj', (object,), {'inserted_id': 'mock_id'})()

    async def find_one(self, query):
        return None

    async def count_documents(self, query):
        return 0

    def find(self):
        return MockCursor()


class MockCursor:
    """Mock cursor for iteration"""
    def sort(self, *args, **kwargs):
        return self

    def skip(self, *args):
        return self

    def limit(self, *args):
        return self

    def __aiter__(self):
        return self

    async def __anext__(self):
        raise StopAsyncIteration


# Collections - use real or mock
if DB_AVAILABLE:
    users_collection = database["users"]
    predictions_collection = database["scam_predictions"]
    history_collection = database["scan_history"]
    company_collection = database["company_verification"]
    feedback_collection = database["feedback"]
    chatbot_collection = database["chatbot_logs"]
    analytics_collection = database["analytics"]
    retraining_logs_collection = database["retraining_logs"]
else:
    users_collection = MockCollection()
    predictions_collection = MockCollection()
    history_collection = MockCollection()
    company_collection = MockCollection()
    feedback_collection = MockCollection()
    chatbot_collection = MockCollection()
    analytics_collection = MockCollection()
    retraining_logs_collection = MockCollection()


async def get_database():
    """Get database instance"""
    return database


async def check_connection():
    """Verify database connectivity"""
    if not DB_AVAILABLE:
        return False
    try:
        await client.admin.command("ping")
        return True
    except Exception:
        return False
