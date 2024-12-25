## conn.py


## models.py
- Difference between Declarative and Imperative Mapping
- Frequently used imports and where these get imported from
- What is Mapped and how is it related to the Python Descriptor Concept
- mapping_column() function, frequently used arguments, what basically it returns etc
- `ForeignKey()` constructor
- Difference between `Numeric` and `Float`
- relationship in sql-alchemy






**Approach 1:**
```python
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
```
- Creates a `sessionmaker` factory
- The `sessionmaker` returns a new session class that is bound to a specific engine
- You first create a session class with `Session = sessionmaker(bind=engine)`
- Then you create an actual session instance by calling `Session()`
- This approach is more flexible as you can create multiple session classes with different configurations
- Useful when you want to create multiple session types or configure sessions differently

**Approach 2:**
```python
from sqlalchemy.orm import Session
session = Session(bind=engine)
```
- Directly creates a session instance
- Instantiates the `Session` class directly with the engine
- More concise and direct
- Less flexible compared to the first approach