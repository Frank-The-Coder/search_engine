import os

IS_DEPLOY = os.getenv("DEPLOY_MODE") == "true"
MAIN_URL = "http://ec2-23-22-39-109.compute-1.amazonaws.com" if IS_DEPLOY else "http://localhost:8080"
