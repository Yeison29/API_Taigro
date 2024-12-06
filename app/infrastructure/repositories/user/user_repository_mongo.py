from app.utils.data_transfer.dtos.user.register_user_dto import RegisterUserMongoDTO


class UserRepositoryMongo:
    def __init__(self, mongo_db):
        self.mongo_db = mongo_db

    async def create_user(self, user_data: RegisterUserMongoDTO):
        collection = self.mongo_db['user_img']
        result = await collection.insert_one(user_data.__dict__)
        return str(result.inserted_id)
