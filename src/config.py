import os

IS_DEPLOY = os.getenv("DEPLOY_MODE") == "true"
MAIN_URL = "http://localhost:8080"
USE_DB = True
DB_LOCATION = "src/search_engine.db"