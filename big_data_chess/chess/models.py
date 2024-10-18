from django.db import models
from libs.date_time_lib import next_year_month, str_replace_year_month
from typing import Tuple

DEFAULT_URL_LENGTH = 64
DEFAULT_BASE_FOLDER_LENGTH = 64
DEFAULT_FOLDER_LENGTH = 32
DEFAULT_ENV = "PROD"

class BaseFolderConfig(models.Model):
    IP = models.CharField(max_length=15, primary_key=True, default="127.0.0.1")
    local_folder = models.CharField(max_length=DEFAULT_BASE_FOLDER_LENGTH)
    big_folder = models.CharField(max_length=DEFAULT_BASE_FOLDER_LENGTH)
    target_folder = models.CharField(max_length=DEFAULT_BASE_FOLDER_LENGTH, default = "")

    def __str__(self):
        return self.IP
    
    class Meta:
        verbose_name = "Base Folder Configuration"  # Singular name
        verbose_name_plural = "Base Folder Configuration"  # Plural name

class FolderConfig(models.Model):
    env = models.CharField(max_length=4, default = DEFAULT_ENV, primary_key=True)
    download_folder  = models.CharField(max_length=DEFAULT_FOLDER_LENGTH, default = "")
    unzip_folder  = models.CharField(max_length=DEFAULT_FOLDER_LENGTH, default = "")
    split_folder  = models.CharField(max_length=DEFAULT_FOLDER_LENGTH, default = "")
    commented_folder = models.CharField(max_length=DEFAULT_FOLDER_LENGTH, default = "")
    reduced_folder = models.CharField(max_length=DEFAULT_FOLDER_LENGTH, default = "")
    archive_folder = models.CharField(max_length=DEFAULT_FOLDER_LENGTH, default = "")
    workflow_folder = models.CharField(max_length=DEFAULT_FOLDER_LENGTH, default = "")
    
    def __str__(self):
        return self.env
    
    class Meta:
        verbose_name = "Folder Configuration"  # Singular name
        verbose_name_plural = "Folder Configuration"  # Plural name


class EloCategory(models.Model):
    elo_cat_name = models.CharField(max_length=32, primary_key=True)
    low = models.SmallIntegerField()  # int8 corresponds to SmallIntegerField in Django
    high = models.SmallIntegerField()  # int8 corresponds to SmallIntegerField in Django

    def __str__(self):
        # Customize the display name for each EloCategories object
        return f"ELO Category: {self.elo_cat_name} ({self.low}-{self.high})"
    
    class Meta:
        verbose_name = "ELO Category"  # Singular name
        verbose_name_plural = "ELO Categories"  # Plural name


class LichessStatus(models.Model):
    last_year = models.SmallIntegerField()  # int8 corresponds to SmallIntegerField in Django
    last_month = models.SmallIntegerField()  # int8 corresponds to SmallIntegerField in Django
    base_url = models.URLField(default = "https://database.lichess.org/")
    pattern = models.CharField(max_length=DEFAULT_URL_LENGTH, default = "lichess_db_standard_rated_<YEAR>-<MONTH>.pgn.zst")

    def __str__(self):
        return "Lichess Config (" + str(self.last_year) + "-" + str(self.last_month) + ")"
    
    class Meta:
        verbose_name = "LICHESS Config"  # Singular name
        verbose_name_plural = "LICHESS Config"  # Plural name

def get_next_db_url() -> Tuple[str, int, int]:
    li_status = LichessStatus.objects.get()
    next_year, next_month = next_year_month(li_status.last_year, li_status.last_month)
    filename = str_replace_year_month(li_status.pattern, next_year, next_month)
    url = li_status.base_url + filename
    print(url, filename, next_year, next_month)
    return url, filename, next_year, next_month

class LichessFile(models.Model):
    DOWNLOAD = 0
    UNZIPPED = 1
    ECO_SPLIT = 2
    FILTERED = 3
    WORKFLOW = 4
    ARCHIVED = 5

    STATUS_CHOICES = [
        (DOWNLOAD, 'Download'),
        (UNZIPPED, 'Unzipped'),
        (ECO_SPLIT, 'ECO-Split'),
        (FILTERED, 'Filtered'),
        (WORKFLOW, 'Workflow processed'),
        (ARCHIVED, 'Archived')
    ]

    name = models.CharField(max_length=32, primary_key=True)
    year = models.SmallIntegerField()  # int8 corresponds to SmallIntegerField in Django
    month = models.SmallIntegerField()  # int8 corresponds to SmallIntegerField in Django
    status = models.IntegerField(choices=STATUS_CHOICES)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "LICHESS File"  # Singular name
        verbose_name_plural = "LICHESS Files"  # Plural name

class Test(models.Model):
    last_year = models.SmallIntegerField()  # int8 corresponds to SmallIntegerField in Django
    last_month = models.SmallIntegerField()  # int8 corresponds to SmallIntegerField in Django
    config_folder  = models.CharField(max_length=DEFAULT_FOLDER_LENGTH, default = "")
