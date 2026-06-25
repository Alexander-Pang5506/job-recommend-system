import pymysql
pymysql.install_as_MySQLdb()
# 设置 pymysql 默认字符集
pymysql.version_info = (1, 4, 3, "final", 0)
pymysql.connections.DEFAULT_CHARSET = 'utf8mb4'