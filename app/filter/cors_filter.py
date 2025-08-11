from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware


def setting_cors_filter(app: FastAPI):
    """
    配置CORS中间件
    :param app: FastAPI应用实例
    """
    logger.info("配置CORS中间件...")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    logger.info("CORS中间件配置完成.")
