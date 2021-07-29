from flask import Flask
from flask_restful import abort


def abort_if_not_exist(data, req):
    if req not in data:
        abort(404, message="La ressource n'existe pas")


def abort_if_alrady_exist(data, req):
    if req in data:
        abort(409, message="La ressource existe déja")
