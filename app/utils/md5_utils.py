import hashlib


class MD5Utils:

    @staticmethod
    def calc(content: str):
        # 创建一个md5哈希对象
        md5 = hashlib.md5()
        # 更新哈希对象
        md5.update(content.encode('utf-8'))
        # 获取十六进制表示的哈希值
        return md5.hexdigest()
