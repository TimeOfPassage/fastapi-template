import uuid
from contextvars import ContextVar

from fastapi import Request, FastAPI
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# 上下文变量，全局唯一 trace_id
trace_id_ctx_var: ContextVar[str] = ContextVar("trace_id", default=None)


def get_trace_id():
    return trace_id_ctx_var.get()


class TraceIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = request.headers.get("X-Trace-Id", str(uuid.uuid4()))
        trace_id_ctx_var.set(trace_id)
        response: Response = await call_next(request)
        response.headers["X-Trace-Id"] = trace_id
        return response


def setting_trace_id_filter(app: FastAPI):
    logger.info("配置全链路追踪中间件...")
    app.add_middleware(TraceIDMiddleware)
    logger.info("全链路追踪中间件配置完成.")
