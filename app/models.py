from enum import unique
from operator import index
from re import S
import re
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db
from datetime import date, datetime

#Este decorador es usado para registrar la funcion con Flask-Login, el cual va a llamara cuando se necesite devolver informacion acerca del usuario
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Permission:

    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
        #self.insert_roles()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
        }
        default_role = 'User'

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    #member_since = db.Column(db.DateTime(datetime.utcnow), default = datetime.utcnow)
    #last_seen = db.Column(db.DateTime(datetime.utcnow), default = datetime.utcnow)
    
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        for u in User.query.all():
            if self.role is None:
                if self.email == current_app.config['FLASKY_ADMIN']:
                    self.role = Role.query.filter_by(name='Administrator').first()
                if self.role is None:
                    self.role = Role.query.filter_by(default=True).first()
                    print(self.role)
        db.session.commit()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow
        db.session.add(self)
        db.session.commit()
    #Se hace un atributo en el cual se guarda la clave en cadena sencilla
    
    #Si se intenta leer no se va a poder porque va a dar un error
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    #Entonces cuando se establece o se pone un valor en el atributo, se da la siguiente funcion
    @password.setter
    #La funcion con el mismo nombre del metodo, pero con la unica diferencia de que el parametro "password" es un atributo
    #Entonces cuando se sobreescribe el atributo, este sobreescribe otro atributo que sería el password_hash y lo que mete ahi es la contraseña de hash
    #que sería el atributo password que se genera un hash
    def password(self, password):
        #Guarda en su espacio/variable el hash del atributo password
        self.password_hash = generate_password_hash(password)

    #Este metodo lo que hace es tomar  la palabra para verificar si es la misma, si son iguales los hash entonces es correcto
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser