import time

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class RequestCostTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response: Response = await call_next(request)
        cost_time = (time.perf_counter() - start_time) * 1000
        response.headers["X-Process-Time"] = f"{cost_time:.2f}ms"
        logger.info(f"{request.method} {request.url.path} 耗时: {cost_time:.2f}ms")
        return response


def setting_request_cost_time_filter(app):
    logger.info("配置请求耗时中间件...")
    app.add_middleware(RequestCostTimeMiddleware)
    logger.info("请求耗时中间件配置完成.")
