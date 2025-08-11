from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.requests import Request

from app.common.exceptions.app_exception import AppException


# 自定义全局异常处理逻辑
def setting_global_exception_filter(app):
    # 处理 FastAPI 内部抛出的 HTTP 异常
    @app.exception_handler(AppException)
    async def http_exception_handler(request: Request, exc: AppException):
        logger.error(f"【业务操作失败】: {request.method} {request.url.path} - {exc}")
        return JSONResponse(status_code=200, content={"code": exc.code, "message": exc.message})

    # 处理请求验证错误（如 Pydantic 校验失败）
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"【参数验证失败】: {request.method} {request.url.path} - {exc.errors()}")
        return JSONResponse(status_code=422, content={"code": 422, "message": "参数验证失败", "errors": exc.errors()})

    # 捕获所有未处理的其他异常
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"【系统异常】: {request.method} {request.url.path} - {exc}")
        return JSONResponse(status_code=500, content={"code": 500, "message": "服务器内部错误"})
