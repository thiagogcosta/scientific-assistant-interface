from chat import ScientificAssistantChat
from configs.config import Config
from configs.logger import Logger
from utils import set_name_page, set_title, set_title_alignment

# ----------
# DESC: config the Logger
logger = Logger().get_logger()
# ----------

set_name_page()

set_title()

set_title_alignment()

ScientificAssistantChat(config=Config())
