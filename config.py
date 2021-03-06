# 引用方式: app.config.from_object('config'), config.py里面的

# key必须是大写的,
# 很多地方就不用写配置了, 比如debug=True, SECRET_KEY等,系统自动从下面取值
DEBUG = False

# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://energy:energy168@localhost/commodity?charset=utf8'
DATABASE_CONNECT_OPTIONS = {}

# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 如果设置成 True，SQLAlchemy 将会记录所有 发到标准输出(stderr)的语句，这对调试很有帮助
SQLALCHEMY_ECHO = True

# mysql connettion ,use Mysql's original connector from Oracle,
# SQLALCHEMY_MYSQL_URI = 'mysql+mysqlconnector://energy:energy168@localhost/clouddata?charset=utf8'

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
# CSRF_SESSION_KEY = "admin168."

# Secret key for signing cookies
# SECRET_KEY = "admin168."

# Json config
# app_path = os.path.realpath(os.path.dirname(__file__))
# JSON_CONFIG_PATH = BASE_DIR + "\\app\\data\\appconfig.json"

# 为了加载这些配置变量，通常使用app.config.from_object()

# # 远程服务器配置
# # ZMQ Config
SERVER = '192.144.156.204'
PRIVATE_SERVER = '127.0.0.1'
PORT = '8080'
WRITE_PORT = '2929'
#
# # Mysql config
MYSQL_URL = '192.144.156.204'
MYSQL_USERNAME = 'blockchain'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'blockchain'

# 本机测试
# # ZMQ Config
# SERVER = '127.0.0.1'
# PRIVATE_SERVER = '127.0.0.1'
# PORT = '8080'
# WRITE_PORT = '2929'

# Mysql config
# MYSQL_URL = '127.0.0.1'
# MYSQL_USERNAME = 'root'
# MYSQL_PASSWORD = '123456'
# MYSQL_DATABASE = 'blockchain'