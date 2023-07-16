from storages.backends.s3boto3 import S3Boto3Storage

# define a storage location for media files on aws s3 bucket
class MediaStore(S3Boto3Storage):
    location = 'media'
    file_overwrite = False