from .models import BaseFolderConfig, FolderConfig, DEFAULT_ENV
from libs.net_lib import get_local_ip
import os
import logging

logger = logging.getLogger('django')

class ChessConfigManager:
    _config_cache = {}

    @classmethod
    def load_config(cls, environment=DEFAULT_ENV):
        """Load configuration from the database into cache."""
        config_entries = []
        folder = FolderConfig.objects.get(env=environment)
        logger.info(f'Folder: {folder}', extra={'status':'ok'})
        base_folder = BaseFolderConfig.objects.get(IP=get_local_ip())
        logger.info(f'Base Folder: {base_folder, base_folder.big_folder}', extra={'status':'ok'})
        folder_entries = [
            {'key': 'download_folder', 'value': os.path.join(base_folder.local_folder, folder.download_folder)},
            {'key': 'unzip_folder', 'value': os.path.join(base_folder.local_folder, folder.unzip_folder)},
#            {'key': 'config_folder', 'value': os.path.join(base_folder.big_folder, folder.config_folder)},
            {'key': 'split_folder', 'value': os.path.join(base_folder.big_folder, folder.split_folder)},
            {'key': 'commented_folder', 'value': os.path.join(base_folder.big_folder, folder.commented_folder)},
            {'key': 'reduced_folder', 'value': os.path.join(base_folder.big_folder, folder.reduced_folder)},
            {'key': 'archive_folder', 'value': os.path.join(base_folder.big_folder, folder.archive_folder)},
            {'key': 'workflow_folder', 'value': os.path.join(base_folder.target_folder, folder.workflow_folder)},
        ]
        config_entries.extend(folder_entries)
        logger_entries = [
            {'key': 'logger', 'value': logging.getLogger('django')},
        ]
        config_entries.extend(logger_entries)
        cls._config_cache = {entry['key']: entry['value'] for entry in config_entries}
        logger.info('Config Cache', extra={'status':'ok', 'operation':str(cls._config_cache)})


    @classmethod
    def get(cls, key, default=None):
        """Retrieve a configuration value by key."""
        if not cls._config_cache:
            cls.load_config()
        return cls._config_cache.get(key, default)
