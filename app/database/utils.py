from motor.motor_asyncio import AsyncIOMotorClient as AIOMC

DB_NAME = 'fastapi'
MONGO_URI = f"mongodb://mongoadmin:P%40ssw0rd@localhost:27017/{DB_NAME}?authSource=admin"

todos_db = DB_NAME
todos_coll = 'todos'


class DB:
	client: AIOMC = None


db = DB()

def connect_mongo():

	db.client = AIOMC(MONGO_URI)


def disconnect_mongo():

	db.client.close()


def get_database():

	return db.client
