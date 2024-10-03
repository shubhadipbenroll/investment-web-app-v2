#!/usr/bin/python3.9
from wsgiref.handlers import CGIHandler
from app import app

CGIHandler().run(app)
