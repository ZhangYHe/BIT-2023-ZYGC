import logging
import yaml

logging_config_file = './utils/logging_config.yaml'

# 设置日志
with open(logging_config_file, 'r') as f:
    config = yaml.safe_load(f.read())
    # config['handlers']['file']['filename'] += ".log"        # TODO
    # config['handlers']['info_file_handler']['filename'] += ".log"
    print(config)
    logging.config.dictConfig(config)
    f.close()
logger = logging.getLogger(__name__)