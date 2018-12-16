from bcrypt import gensalt, hashpw
from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String

from app import db, login_manager


class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property == 'password':
                value = hashpw(value.encode('utf8'), gensalt())
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None

##DB Tables
class SentM(db.Model, UserMixin):
    
    __tablename__ = 'SentM'
    
    phoneNum = Column(String(15),primary_key=True)
    name = Column(String(50))
    text = Column(String(500))
    prodtype = Column(String(10))
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value ,= value
            setattr(self, property, value)
        
    def __repr__(self):
        return str(self.username)
    
class ReceiveM(db.Model, UserMixin):
    
    __tablename__ = 'ReceiveM'
    
    phoneNum = Column(String(15),primary_key=True)
    text = Column(String(500))
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value ,= value
            setattr(self, property, value)
        
    def __repr__(self):
        return str(self.username)
    