# -*- coding: utf-8 -*-
"""
celery work file
"""
from start import app
from datum.datum import Invitation, Account
from public.initial import db
from celery import Celery


def create_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']

    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# init celery
celery_app = create_celery(app)
celery_app.config_from_object(app.config)


@celery_app.task()
def invite_record(uid, code):
    """invite_record"""

    invitation = Invitation()
    invitation.uid = uid
    invitation.share_code = code

    try:
        db.session.add(invitation)
        db.session.commit()
    except Exception as err:
        print(err)
        db.session.rollback()


@celery_app.task()
def init_account(uid, mobile):
    """init_account"""

    account = Account()
    account.uid = uid
    account.acc_no = mobile

    try:
        db.session.add(account)
        db.session.commit()
    except Exception as err:
        print(err)
        db.session.rollback()


"""
1 start celery by following command
celery -A celery_worker.celery_app worker -l info

2 use it in views by
from celery_worker import invite_record
invite_record.delay(uid, invite_code)
"""