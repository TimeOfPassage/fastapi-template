import sys

from fastapi import Request, Response, FastAPI
from loguru import logger

from app.core.config import Settings
from app.utils.md5_utils import MD5Utils

white_list = ['/', '/favicon.ico', '/docs', '/openapi.json', '/demo']


def setting_signature_filter(app: FastAPI):
    """
    配置签名校验中间件
    :param app: FastAPI应用实例
    """
    ak = Settings.ACCESS_KEY
    sk = Settings.SECRET_KEY
    if ak is None or sk is None or len(ak) == 0 or len(sk) == 0:
        logger.error("如果配置了签名校验，ACCESS_KEY or SECRET_KEY 不能为空")
        sys.exit(-1)

    @app.middleware("http")
    async def middleware(request: Request, call_next):
        path = request.url.path
        if path in white_list:
            return await call_next(request)
        query_params = dict(request.query_params) if request.query_params else {}
        nonce = query_params['nonce'] if 'nonce' in query_params else ''
        timestamp = query_params['timestamp'] if 'timestamp' in query_params else ''
        signature = query_params['signature'] if 'signature' in query_params else ''
        sign = MD5Utils.calc(f"{ak}{path}{timestamp}{nonce}{sk}")
        if signature != sign:
            logger.error(f"签名校验失败: 计算签名{sign} != 传入签名{signature}")
            return Response(content="签名校验失败", status_code=403)
        return await call_next(request)
