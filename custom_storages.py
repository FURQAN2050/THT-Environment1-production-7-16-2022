from django.conf import settings 
from storages.backends.s3boto3 import S3Boto3Storage 
 
class StaticStorage(S3Boto3Storage):     
    location = settings.STATICFILES_LOCATION
    custom_domain = settings.STATIC_AWS_S3_CUSTOM_DOMAIN
    bucket_name = settings.STATICFILES_BUCKETNAME

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    custom_domain = settings.MEDIA_AWS_S3_CUSTOM_DOMAIN
    bucket_name = settings.MEDIAFILES_BUCKETNAME
