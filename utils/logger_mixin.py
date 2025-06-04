import logging # Para registrar eventos en lugar de usar print

class LoggerMixin:
    """
    Mixin que proporciona un logger configurado a cualquier clase que lo herede.
    """
    # Configurar logging para mostrar mensajes informativos y de error
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)# Crea un logger asociado al módulo actual
