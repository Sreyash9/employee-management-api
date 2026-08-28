from fastapi import FastAPI

from api.employee import router as employee_router


app = FastAPI()


app.include_router(employee_router)