'''The below 2 imports are required for type hinting'''
from typing import Optional

'''SQL Alchemy ORM Specific Imports'''
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationships # Understand the use of this [https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html]
from sqlalchemy import String, Integer, Float, Date
from sqlalchemy import ForeignKey, UniqueConstraint

from .conn import engine

"""
Difference between Declarative and Imperative Mapping?
We can inherit DeclarativeBase class in Transaction, Personal etc classes. But instead went with below way why?
"""
class Base(DeclarativeBase):
    pass

"""
Mapped concept came in sqlalchemy 1.4
Mapped[int] or Mapped[str] or Mapped[Optional[str]] these are just type hint
Why are we doing this type hinting? This has something to do with the descriptors in python

- mapped_column concept came in sqlalchemy 2.0
- First 2 arguments of mapped_column() function are __name_pos and __type_pos.
- __name_pos and __type_pos are positional-only arguments and must be passed positionally.
- If __name_pos argument is omitted, If omitted, the attribute name to which the mapped_column() is mapped will be used as the SQL column name.
- If __type_pos argument is omitted, the ultimate type for the column may be derived either from the annotated type, or if a ForeignKey is present, from the datatype of the referenced column.
- nullable is Optional bool argument shows whether the column should be “NULL” or “NOT NULL”. If omitted, the nullability is derived from the type annotation based on whether or not typing.Optional is present. nullable defaults to True otherwise for non-primary key columns, and False for primary key columns.
"""

class Transaction:
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[date] = mapped_column(Date, nullable=False) # type: ignore
    category_id: Mapped[ForeignKey] = mapped_column(ForeignKey('category.id'))
    sub_category_id: Mapped[ForeignKey] = mapped_column(ForeignKey('sub_category.id'))
    product_or_service: Mapped[str] = mapped_column(String(length=7), nullable=False)
    product_or_service_name: Mapped[str] = mapped_column(String(length=128), nullable=False)
    brand: Mapped[Optional[str]] = mapped_column(String(length=128))
    # Quantity Or Duration has mixed data types (e.g., "1 Unit" vs. "2 Months"). Split in 2 different columns
    # Composite column concept probably
    quantity_or_duration: Mapped[Optional[str]] = mapped_column(String(length=20), nullable=True) # Should not be NULL    
    # The Price field contains monetary values
    price: Mapped[float] = mapped_column(Float, nullable=False) # Float(precision=2)understand this
    transaction_mode: Mapped[str] = mapped_column(String(7), nullable=False)
    details: Mapped[Optional[str]] = mapped_column(String)

    def __repr__(self):
        return f'Transaction(id={self.id}, date={self.date}, \
            category_id={self.category_id}, sub_category_id={self.sub_category_id}), \
            product_or_service = {self.product_or_service}, product_or_service_name={self.product_or_service_name}, brand={self.brand} \
            quantity_or_duration={self.quantity_or_duration}, price={self.price}, transaction_mode={self.transaction_mode} \
            details={self.details}'


class Personal(Base, Transaction):
    __tablename__ = 'personal'

class Dearness(Base, Transaction):
    __tablename__ = 'dearness'
    relation :Mapped[str] = mapped_column(String(32), nullable=True) # Once the data is corrected, I can make this false

    def __repr__(self):
        pass

class Category(Base):
    __tablename__ = 'category'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

    def __repr__(self):
        return f'Category(id={self.id}, name={self.name})'

class SubCategory(Base):
    __tablename__ = 'sub_category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    category_id: Mapped[ForeignKey] = mapped_column(ForeignKey('category.id'))

    UniqueConstraint(name, category_id, name='uc_sub_category_name_category_id')

    def __repr__(self):
        return f'SubCategory(id={self.id}, name={self.name}, category_id={self.category_id})'


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)