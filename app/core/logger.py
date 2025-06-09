import logging
import sys
from typing import List

from app.core.config import settings

# Configurar formato do log
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

# Configurar nível de log
log_level = getattr(logging, settings.LOG_LEVEL.upper())

# Configurar handlers
handlers: List[logging.Handler] = [
    logging.StreamHandler(sys.stdout)
]

# Configurar logging
logging.basicConfig(
    level=log_level,
    format=log_format,
    datefmt=date_format,
    handlers=handlers
)

# Criar logger para a aplicação
logger = logging.getLogger("app")
