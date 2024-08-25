from django.db import models

class FolderConfig(models.Model):
    base_folder = models.CharField(max_length=192)
    zip_sub_folder = models.CharField(max_length=32)
    unzip_sub_folder = models.CharField(max_length=32)

    def __str__(self):
        return self.base_folder
    
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


class LichessFile(models.Model):
    DOWNLOAD = 0
    UNZIPPED = 1
    ECO_SPLIT = 2
    FILTERED = 3
    DB_UPDATE = 4

    STATUS_CHOICES = [
        (DOWNLOAD, 'Download'),
        (UNZIPPED, 'Unzipped'),
        (ECO_SPLIT, 'ECO-Split'),
        (FILTERED, 'Filtered'),
        (DB_UPDATE, 'DB-Update'),
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

