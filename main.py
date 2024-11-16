# main.py

# lib

from fastapi import FastAPI

# module
from app import core as CORE
from app import common as COMMON
from app import post as POST
from app import profile as PROFILE


# define
"""
uvicorn main:app --host 0.0.0.0 --port 9000 --reload

"""


# app
app = FastAPI()

# setting
CORE.setup(app)
COMMON.setup(app)
POST.setup(app)
PROFILE.setup(app)






# async def startup():
#     await CORE.ORM.create_tables()


# app.add_event_handler( event_type="startup", func=startup )




