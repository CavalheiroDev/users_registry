from chalicelib.contracts.repository import Repository


class UserRepository(Repository):
    table_name = 'users'


user_repository = UserRepository()
