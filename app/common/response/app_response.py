class BaseResponse:

    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

    @staticmethod
    def ok(data: object = None):
        return {
            'code': 0,
            'msg': "操作成功",
            'data': data
        }

    @staticmethod
    def error(code: int, message: str = "操作失败"):
        return {
            'code': code,
            'msg': message
        }
