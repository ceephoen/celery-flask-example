# -*- coding: utf-8 -*-
"""
about datum
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from public.initial import db


class BaseModel(object):
    """BaseModel"""
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class User(BaseModel, db.Model):
    """User"""

    __table__ = "uc_user"

    # base info
    id = db.Column(db.Integer, primary_key=True, index=True)
    cell_phone = db.Column(db.String(11), unique=True, nullable=False)
    payment_pwd = db.Column(db.String(128))
    share_code = db.Column(db.String(16), unique=True)
    normal = db.Column(db.Boolean, default=True)

    # payment_pwd
    @property
    def pay_pwd(self):
        raise AttributeError('Attribution Read Error')

    @pay_pwd.setter
    def pay_pwd(self, value):
        self.payment_pwd = generate_password_hash(value)

    def check_ppwd(self, value):
        return check_password_hash(self.payment_pwd, value)


class Invitation(BaseModel, db.Model):
    """Invitation"""

    __table__ = "uc_invite"

    id = db.Column(db.Integer, primary_key=True, index=True)
    share_code = db.Column(db.String(8))
    uid = db.Column(db.Integer)


class Account(BaseModel, db.Model):
    """Account"""

    __table__ = "uc_account"

    id = db.Column(db.Integer, primary_key=True, index=True)
    uid = db.Column(db.Integer)
    acc_no = db.Column(db.String(11), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.00)
    integral = db.Column(db.SmallInteger, default=0)
    rebate = db.Column(db.SmallInteger, default=0)
