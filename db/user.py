import json

from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import SingletonThreadPool
import re

engine = create_engine('sqlite:///db.sqlite', poolclass=SingletonThreadPool)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    user_id = Column(Integer)

    def __str__(self):
        return str(vars(self))


Base.metadata.create_all(engine)

session = sessionmaker()
session.configure(bind=engine)



def add_user(name, surname, email, id=0):
    tester = "^[_A-zA-Z]*((-|\s)*[_A-zA-Z])*$"
    email_tester = "^\S+@\S+\.\S+$"
    s = session()
    try:
        if re.search(tester, name) and 1 < len(name) < 21 and \
                re.search(tester, surname) and 1 < len(surname) < 21 and \
                re.search(email_tester, email):

            s.add(User(name=name,
                       surname=surname,
                       email=email,
                       user_id=id
                       ))
            s.commit()
        else:
            raise Exception()
    except Exception as e:
        print(e)
    finally:
        s.close()


def find_user_id(name, surname):
    s = session()
    user = s.query(User).filter(User.name == name, User.surname == surname).first()
    print(user)

    s.close()

    if not user:
        return 0

    return user.id

def find_user(name, surname):
    s = session()
    user = s.query(User).filter(User.name == name, User.surname == surname).first()
    print(user)

    s.close()

    if not user:
        return None

    return user

def get_all_users():
    s = session()
    result = []

    for x in s.query(User).all():
        user = {
            "id": x.id,
            "name": x.name,
            "surname": x.surname,
            "email": x.email,
            "user_id": x.user_id
        }

        result.append(user)

    s.close()
    return json.dumps(result)


def delete_user_id(id):
    s = session()
    try:
        s.query(User). \
            filter(User.id == id). \
            update({'user_id': 0})
        s.commit()
    except Exception as e:
        print(e)



# add_user("test", "test", "test@test.com")
# add_user("testtt", "testtt", "test@test.com", find_user_id("test", "test"))

# print(s.query(User).all())

# for u in s.query(User).all():
#     print(u)

# print(s.query(User).filter(User.name == "test").first().id)

