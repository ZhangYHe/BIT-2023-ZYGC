import logging.config as log_config
import logging
import yaml

'''
使用时：
    from utils.logger import logger

需要调试：
    logger.info("xxx)
    logger.debug("xxx")
    logger.warning("xxx")
    logger.error("xxx")
    
    try:
        xxx    
    except Exception as e:
        logger.info('Exception %s happened , xxx !' % e)
        
在 code/back_end/config/logging_config.yaml 中更改显示等级
'''

logging_config_file = './config/logging_config.yaml'

# 设置日志
with open(logging_config_file, 'r') as f:
    config = yaml.safe_load(f.read())
    #print(config)
    log_config.dictConfig(config)
    f.close()
logger = logging.getLogger(__name__)