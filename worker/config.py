broker_url = 'redis://127.0.0.1:6379/0'
broker_pool_limit = 200  # Borker 连接池, 默认是10

timezone = 'Asia/Shanghai'
accept_content = ['pickle', 'json']  #接受的任务格式

task_serializer = 'pickle'  #解析数据

result_backend = 'redis://127.0.0.1:6379/0'
result_serializer = 'pickle'
result_cache_max = 10000  # 任务结果最大缓存数量
result_expires = 3600  # 任务过期时间

worker_redirect_stdouts_level = 'INFO'


#celery的启动方式celery worker -A tasks -- loglevel=info