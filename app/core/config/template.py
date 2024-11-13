# core/config/template.py

# lib
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader

# module


# define
TEMPLATE = Jinja2Templates(directory="app/core/template")
TEMPLATE.env.loader = ChoiceLoader([
    FileSystemLoader("app/core/template"),
    FileSystemLoader("app/common/template"),
    FileSystemLoader("app/post/template"),
    FileSystemLoader("app/profile/template"),
])