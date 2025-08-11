from fastapi import FastAPI
from loguru import logger

from app.api.v1 import user_api
from app.core.config import settings
from app.core.database import DatabaseBaseModel, engine
from app.filter.cors_filter import setting_cors_filter
from app.filter.global_exception_filter import setting_global_exception_filter
from app.filter.request_cost_time_filter import setting_request_cost_time_filter
from app.filter.trace_id_filter import setting_trace_id_filter


def init_database():
    try:
        import app.models
        logger.info(f"初始化数据库...")
        for t in DatabaseBaseModel.metadata.tables:
            logger.info(f"初始化表【{t}】")
        from sqlalchemy import text
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info(f"数据库链接: {'🟢' if result.scalar() == 1 else '🛑'}")  # 输出 1
        # 创建所有表
        DatabaseBaseModel.metadata.create_all(bind=engine)
        logger.info("数据库初始化完成")
    except Exception as e:
        logger.error(f"初始化数据库失败...{e}")


def init_router(app: FastAPI):
    app.include_router(user_api.router, prefix="/api/v1/users", tags=["users"])
    logger.info("注册路由... 【/api/v1/users】")


def config_middleware(_app: FastAPI):
    # 配置跨域中间件
    setting_cors_filter(_app)
    # 配置全局异常拦截器
    setting_global_exception_filter(_app)
    # 配置全链路追踪中间件
    setting_trace_id_filter(_app)
    # 配置请求耗时中间件
    setting_request_cost_time_filter(_app)


def startup():
    logger.info("应用启动中...")
    init_database()
    init_router(app)
    logger.info("🚀 应用启动完成.")


def shutdown():
    logger.info("🛑 应用关闭...")


app = FastAPI(title=settings.PROJECT_NAME)
config_middleware(app)
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)
__all__ = ["app"]
