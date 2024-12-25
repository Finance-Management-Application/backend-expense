from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import insert
from sqlalchemy import select

from .conn import engine
from .models import Category, SubCategory, Personal, Dearness

def bulk_insert_categories(categories: List[dict]) -> None:
    with Session(engine) as session:
        session.execute(insert(Category),categories)
        session.commit()

def bulk_insert_sub_category(sub_categories: List[dict]) -> None:
    with Session(engine) as session:
        # I already know that this function is only performed after bulk_insert_categories
        # I already have a session object which is used in bulk_insert_categories
        # Below I am creating another session and getting one result at a time with the new session
        # Can I optimize this further?
        for sub_category in sub_categories:
            stmt = select(Category.id).where(Category.name == sub_category['category_name'])
            category_id = session.scalar(stmt) # Why I don't have to use session.execute method?
            # result = session.execute(stmt).scalar() # scaler() is going to return the first column of the first row in the result
            del sub_category['category_name']
            sub_category['category_id'] = category_id
            stmt = insert(SubCategory).values(**sub_category)
            session.execute(stmt)
        session.commit()


def bulk_insert_transactions(transactions: List[dict], table: str) -> None:
    with Session(engine) as session:
        for transaction in transactions:
            stmt = select(Category.id).where(Category.name == transaction['category'])
            category_id = session.scalar(stmt)
            stmt = select(SubCategory.id).where(SubCategory.category_id==category_id and SubCategory.name == transaction['sub_category'])
            sub_category_id = session.scalar(stmt)
            del transaction['category']; transaction['category_id'] = category_id
            del transaction['sub_category']; transaction['sub_category_id'] = sub_category_id
            stmt = insert(Personal).values(**transaction) if(table=='personal') else insert(Dearness).values(**transaction)
            session.execute(stmt)
        session.commit()

# Not required to create separate method as of now
# def bulk_insert_dearness_transactions(transactions: List[dict]) -> None:
#     pass

def insert_personal_transaction(transaction: dict) -> None:
    pass

def insert_dearness_transaction(transaction: dict) -> None:
    pass

def insert_category(category: dict) -> None:
    pass

def insert_sub_category(sub_category: dict) -> None:
    pass