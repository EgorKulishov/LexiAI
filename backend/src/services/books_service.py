from utils.repository import AbstractRepository
import aiohttp
import asyncio
from gemini import request_to_model
from datetime import *
from schemas.schemas import BooksInfoWithDeadlineSchema,BooksInfoSchema

class BooksServices:

    def __init__(self,books_repo: AbstractRepository) -> None:
        self.books_repo = books_repo()

    async def add_books(self,book,file,user_id,deadline):

        
        book['user_id'] = user_id
        book['done'] = False
        text = file.read()

        promtt = f'''{text} твоя задача сделать выжимку данного текста чтобы его было можно прочитать за данное количество дней, если каждый день человек читает по 2 часа, а в час он прочитывает 9000 слов, если что его точно можно прочитать за данное количество дней
        количество дней={deadline}
        '''

        created_date = datetime.now()
        book['created_date'] = created_date

        deadline_date = created_date + timedelta(days=deadline)
        book['deadline_date'] = deadline_date
        text_new = await request_to_model(promtt,0)
        #book['text'] = text_new
        book['text'] = "ТЕСТОВЫЙ ТЕКСТ!"
        book_id = await self.books_repo.add_one(book)
        #return text_new
        return book['text']

    async def get_books_true_deadline(self,books):
        res_books = []
        for book in books:
            deadline: timedelta = book.deadline_date - datetime.now()
            if  deadline.days >= 0:
                n = book.model_dump()
                n['deadline'] = deadline.days
                b = BooksInfoWithDeadlineSchema.model_validate(n,from_attributes=True)
                res_books.append(b)

            
        return res_books
        

    async def findBooksWithDeadline(self,user_id):

        filters = [
            self.books_repo.model.user_id == user_id,
            self.books_repo.model.done == False,
        ]

        books = await self.books_repo.find_filter(filters)
        print(books)
        res = await self.get_books_true_deadline(books)
        return res

    async def findBooksWithMotivation(self,user_id):

        filters = [
            self.books_repo.model.user_id == user_id,
            self.books_repo.model.motivation != None,
            self.books_repo.model.done == False,
        ]

        books = await self.books_repo.find_filter(filters)
        res = await self.get_books_true_deadline(books)
        return res

    async def delete_book(self,book_id):

        book_id = await self.books_repo.delete_one(book_id)

        return book_id

    async def get_all_books(self,user_id):

        filters = [
            self.books_repo.model.user_id == user_id,
        ]

        books = await self.books_repo.find_filter(filters)

        return books


    async def get_books_by_name(self,name,user_id):

        filters = [
            self.books_repo.model.user_id == user_id,
            self.books_repo.model.book_name == name,
        ]

        book = await self.books_repo.find_filter(filters)

        return book


    async def get_done_books(self,user_id):

        filters = [
            self.books_repo.model.user_id == user_id,
            self.books_repo.model.done == True,
        ]

        books = await self.books_repo.find_filter(filters)

        return books

    async def done_book(self,id):

        values = {
            'done' : True
        }

        book = await self.books_repo.update(id,values)

        return book


