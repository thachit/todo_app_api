from sys import prefix
from starlette.responses import JSONResponse
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from src.core.config import Config
from src.api.api_v1.registers import register_router_v1
from src.api.api_v1.login import login_router_v1
from src.api.api_v1.refresh_token import refresh_token_router_v1
from src.api.api_v1.tasks import task_router_v1
fast_api = FastAPI()

@fast_api.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors_string = ""
    for error in exc.errors():
        loc = error.get('loc', ())
        field_name = loc[1] if len(loc) > 1 else ""
        error_ctx = error.get('ctx')
        errors_string = errors_string + \
                        f"{field_name} {error.get('msg', '')}, "

    return JSONResponse(content=jsonable_encoder({"detail": errors_string.strip()}),
                        status_code=status.HTTP_400_BAD_REQUEST)

# API V1
fast_api.include_router(register_router_v1, prefix='/api/v1')
fast_api.include_router(login_router_v1, prefix='/api/v1')
fast_api.include_router(refresh_token_router_v1, prefix='/api/v1')
fast_api.include_router(task_router_v1, prefix='/api/v1')
@fast_api.get("/health")
async def health_check():
    return {
        "status": "ok",
        "app_name": Config.APP_NAME
    }