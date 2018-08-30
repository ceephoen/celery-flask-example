# -*- coding: utf-8 -*-
"""
api
"""
import uuid
from flask import request, jsonify
from . import router
from public.initial import redis_db, db
from datum.datum import User
from public.respond import RET


@router.route('/login', methods=['POST'])
def login():
    """
    ret = db.session.query(exists().where(User.cell_phone == mobile)).scalar()
    :return: resp
    """
    # 1 param
    data = request.get_json()

    cell_phone = data.get('cellPhone')
    login_code = data.get('loginCode')
    invite_code = data.get('inviteCode')

    # 2 sms code
    try:
        code = redis_db.get("{}:{}".format(cell_phone,'loginCode'))  # None
    except Exception as err:
        print(err)
        return jsonify({'result': RET.DBERR, 'data': ''})

    if code is None:
        return jsonify({'result': RET.INVALIDCODE, 'data': ''})

    if login_code != code.decode('utf-8'):
        return jsonify({'result': RET.INVALIDCODE, 'data': ''})

    # 3 verify user
    try:
        user = User.query.filter(User.cell_phone == cell_phone).first()
    except Exception as err:
        print(err)
        return jsonify({'result': RET.DBERR, 'data': ''})

    # 4 user
    if user is None:
        client_id = uuid.uuid5(uuid.NAMESPACE_DNS, cell_phone).hex
        # instance user
        user = User()
        user.cell_phone = cell_phone
        # save
        try:
            db.session.add(user)
            db.session.flush()
            uid = user.id  # uid

            # share_code
            user.share_code = client_id.upper()[0: 8]
            db.session.commit()
        except Exception as err:
            print(err)
            db.session.rollback()
            return jsonify({'result': RET.DBERR, 'data': ''})

        # invite_code
        if invite_code:
            from celery_worker import invite_record
            invite_record.delay(uid, invite_code)

        # init_account
        from celery_worker import init_account
        init_account.delay(uid, cell_phone)
    else:
        uid = user.id

    if not user.normal:
        return jsonify({'result': RET.ABNORMAL, 'data': ''})

    # user uid to generate token, like itsdangerous
    token = uid

    # 8 return resp
    return jsonify({'result': RET.OK, 'data': token})
