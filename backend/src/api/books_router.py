from fastapi import APIRouter,Depends,UploadFile,HTTPException
from auth.auth import current_user
from schemas.schemas import BooksAddSchema
from .dependencies import books_service
from services.books_service import BooksServices
from models.models import User
from typing import Optional
from pydantic import Field

router = APIRouter(
    tags=['books'],
    prefix='/books'
)


    

@router.post('')
async def create_book(
    file: UploadFile,
    name: str,
    deadline: int,
    motivation: Optional[str] = None,
    user: User = Depends(current_user),
    book_service: BooksServices = Depends(books_service),
):
    if deadline < 1:
        raise HTTPException(status_code=403,detail='deadline cannot be less than 1')
    book = {}
    book['book_name'] = name
    book['motivation'] = motivation
    text = await book_service.add_books(book,file,user.id,deadline)
    return text


@router.post('/dones/{id}')
async def done_book(
    id:int,
    user: User = Depends(current_user),
    books_service: BooksServices = Depends(books_service)
):

    book = await books_service.done_book(id)
    return book



@router.get('/dones')
async def dones_book(
    user: User = Depends(current_user),
    books_service: BooksServices = Depends(books_service)
):

    books= await books_service.get_done_books(user.id)
    return books

@router.get('/deadlines')
async def deadlines(
    user: User = Depends(current_user),
    books_service: BooksServices = Depends(books_service)
):

    books = await books_service.findBooksWithDeadline(user.id)
    return books

@router.get('')
async def get_all_books(
    user: User = Depends(current_user),
    books_service: BooksServices = Depends(books_service)
):

    books = await books_service.get_all_books(user.id)
    return books


@router.get('/motivations')
async def motivations(
    user: User = Depends(current_user),
    books_service: BooksServices = Depends(books_service)
):

    books = await books_service.findBooksWithMotivation(user.id)
    return books


@router.delete('/{id}')
async def delete_book(
    book_id:int,
    user: User = Depends(current_user),
    books_service: BooksServices = Depends(books_service)
):

    bk_id = await books_service.delete_book(book_id)
    return {'delete_book': bk_id}




@router.get('/{name}')
async def get_book_by_name(
    book_name:str,
    user: User = Depends(current_user),
    books_service: BooksServices = Depends(books_service)
):

    book= await books_service.get_books_by_name(book_name,user.id)
    return book







