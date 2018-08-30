# -*- coding: utf-8 -*-
"""
Blueprint
"""
from flask import Blueprint

# init Blueprint
router = Blueprint('router', __name__, url_prefix='/v1/api')
from api import entry
