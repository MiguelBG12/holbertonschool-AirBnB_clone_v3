#!/usr/bin/python3
"""Defines the DBStorage engine."""
import os
from models.base_model import BaseModel, Base
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData


class DBStorage():
    """connect to MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine("{}+{}://{}:{}@{}/{}".
                                      format("mysql", "mysqldb",
                                             os.getenv("HBNB_MYSQL_USER"),
                                             os.getenv("HBNB_MYSQL_PWD"),
                                             os.getenv("HBNB_MYSQL_HOST"),
                                             os.getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on current database for all o specify class"""
        dic = {}
        types_obj = [State, City, User, Place, Amenity, Review]
        if type(cls) == str:
            return dic
        if cls is not None and cls in types_obj:
            query_list = self.__session.query(cls).all()
            for el in query_list:
                key = "{}.{}".format(type(el).__name__, el.id)
                dic[key] = el
        else:
            for typ in types_obj:
                query_list2 = self.__session.query(typ)
                for el in query_list2:
                    key = "{}.{}".format(type(el).__name__, el.id)
                    dic[key] = el
        return dic

    def new(self, obj):
        """add the object to the current DB session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current DB session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current DB session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)
        else:
            pass

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes the current session and commits any changes to database"""
        self.__session.close()