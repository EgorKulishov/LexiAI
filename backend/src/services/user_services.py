from utils.repository import AbstractRepository
from services.books_service import BooksServices
from repositories.books_repo import BooksRepository
from schemas.schemas import UserReadWithDoneBooksSchema

class UserServices:

    def __init__(self,user_repo: AbstractRepository) -> None:
        self.user_repo = user_repo()

    async def get_user_by_id(self,user_id):

        filters = [
            self.user_repo.model.id == user_id
        ]

        user = await self.user_repo.find_filter(filters)
        user_dict = user[0].model_dump()
        books = BooksServices(BooksRepository)
        books_done = await books.get_done_books(user_id)
        user_dict['done_books'] = books_done

        res = UserReadWithDoneBooksSchema.model_validate(user_dict,from_attributes=True)

        return res

        
