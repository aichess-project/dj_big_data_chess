from django.apps import AppConfig as DjangoAppConfig

class ChessConfig(DjangoAppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chess'

    def ready(self):
        from .config import ChessConfigManager
        ChessConfigManager.load_config()


