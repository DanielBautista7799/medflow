# Lambda = where our FastAPI backend runs in AWS
# Mangum = translator inside Lambda that passes requests between Lambda and FastAPI
# React sends a request -> Lambda receives it -> Mangum gives it to FastAPI -> FastAPI talks to RDS
# The response comes back RDS -> FastAPI -> Mangum -> Lambda -> React

from mangum import Mangum

from app.main import app

handler = Mangum(app)