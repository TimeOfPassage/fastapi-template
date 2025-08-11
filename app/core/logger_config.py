import sys

from loguru import logger

from app.core.config import settings
from app.filter.trace_id_filter import get_trace_id


def trace_id_filter(record):
    record['trace_id'] = get_trace_id() or ""
    return True  # 永远允许输出日志


# 清空所有设置
logger.remove()
# 日志输出格式
# formatter = "{time:YYYY-MM-DD HH:mm:ss.SSS} {level: <8} {trace_id} {thread.id} [{thread.name}] - {module}.{function}:{line} - {message}"
formatter = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "  # 时间使用绿色
    "<level>{level: <8}</level> "  # 等级使用 loguru 默认颜色
    "{trace_id} {thread.id} [{thread.name}] - "
    "<cyan>{module}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan> - "  # 模块、函数、行号使用青色
    "<level>{message}</level>"  # 消息内容使用等级对应颜色
)
# 输出到控制台
logger.add(sink=sys.stdout, format=formatter, filter=trace_id_filter, level=settings.LOG_LEVEL)
# 根据Settings.LOG_LEVEL配置日志等级
# "logs/app.log"：指定日志输出的文件路径。这里表示将日志写入项目目录下 logs 文件夹中的 app.log 文件。
# format=formatter：设置日志的输出格式。formatter 是一个定义好的字符串，用于指定日志记录的样式，包含时间、日志级别、追踪 ID、线程信息等。
# filter=_logger_filter：指定日志过滤函数。_logger_filter 函数会在每条日志记录输出前执行，这里会给日志记录添加 trace_id 字段，并根据 trace_id 决定是否输出该日志。
# level=Settings.LOG_LEVEL：设置日志记录的最低级别。Settings.LOG_LEVEL 从配置文件中获取，只有日志级别等于或高于该值的日志才会被记录。
# encoding='utf-8'：指定日志文件的编码格式为 UTF-8，确保可以正确处理各种字符。
# retention='7 days'：设置日志文件的保留策略。这里表示只保留最近 7 天的日志文件，旧的日志文件会被自动删除。
# backtrace=True：开启回溯功能。当捕获到异常时，会显示完整的调用栈信息，有助于调试。
# diagnose=True：开启诊断功能。在捕获到异常时，会显示详细的变量值和局部状态信息，方便定位问题。
# enqueue=True：开启异步写入模式。日志记录会先放入队列，然后由单独的线程异步写入文件，这样可以避免阻塞主线程。
# rotation="100 MB"：设置日志文件的轮转策略。当日志文件大小达到 100 MB 时，会自动创建一个新的日志文件继续记录。
logger.add(settings.LOG_FILE, format=formatter, filter=trace_id_filter, level=settings.LOG_LEVEL, encoding='utf-8', retention='7 days', backtrace=False, diagnose=False, enqueue=True, rotation="100 MB")

__all__ = ["logger"]
