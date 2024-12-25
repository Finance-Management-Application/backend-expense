from sqlalchemy import create_engine
# engine = create_engine("sqlite://", echo=True)
engine = create_engine(url='postgresql+psycopg2://postgres:admin@localhost:5432/expense')

# Approach 1 - More Flexible
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# Approach 2 - Less Flexible
# from sqlalchemy.orm import Session
# session = Session(bind=engine)