# config.py

# lib
from os import getenv
from dotenv import load_dotenv

# module


# define
load_dotenv()
SETTING = {
    "project":{
        "name":getenv("PROJECT_NAME"),
    },
    "app":{
        "core":{
            "database":{
                "session":{
                    "name":getenv("APP_CORE_DATABASE_NAME"),
                    "id":getenv("APP_CORE_DATABASE_ID"),
                    "pw":getenv("APP_CORE_DATABASE_PW"),
                    "ip":getenv("APP_CORE_DATABASE_IP"),
                    "port":int(getenv("APP_CORE_DATABASE_PORT")),
                },
                "orm":{

                },
            },
            "security":{
                "auth":{
                    "url":getenv("APP_CORE_SECURITY_AUTH_URL"),
                },
                "access":{
                    "key":getenv("APP_CORE_SECURITY_ACCESS_KEY"),
                    "secretkey":getenv("APP_CORE_SECURITY_ACCESS_SECRETKEY"),
                    "algorithm":getenv("APP_CORE_SECURITY_ACCESS_ALGORITHM"),
                    "expmin":int(getenv("APP_CORE_SECURITY_ACCESS_EXPMIN")),
                },
            },
        },
        "post":{
            "pagesize":int( getenv("APP_POST_PAGESIZE") )
        },
    }
}