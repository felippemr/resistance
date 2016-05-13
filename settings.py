# coding: utf-8
import motor
import os


def _get_mongodb_client():
    return motor.motor_tornado.MotorClient(DATABASE_HOST, DATABASE_PORT)


def _setup_db():
    return getattr(_get_mongodb_client(), DATABASE_NAME)

DATABASE_NAME = os.getenv("RESISTANCE_DATABASE_NAME", 'resistance')
DATABASE_HOST = os.getenv("RESISTANCE_DATABASE_HOST", 'localhost')
DATABASE_PORT = int(os.getenv("RESISTANCE_DATABASE_PORT", 27017))
DATABASE_CONNECTION = _setup_db()

APP_PORT = os.getenv("RESISTANCE_API_PORT", 8888)
DEBUG = bool(os.getenv("RESISTANCE_DEBUG", False))


def get_app_settings():
    return {"db": DATABASE_CONNECTION, "debug": DEBUG}
