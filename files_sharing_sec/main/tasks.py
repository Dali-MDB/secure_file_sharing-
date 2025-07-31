from celery import shared_task
from .models import DownloadLink,UploadedFile
from django.utils import timezone
from django.db.models import Q, F
from datetime import timedelta
from django.conf import settings
import os



@shared_task
def delete_expired_tokens():
    deleted_count,_ = DownloadLink.objects.filter(
        Q(expires_at__lt=timezone.now()) |
        Q(current_uses__gte=F('max_uses'))       # F for refering to the attribute directly
    ).delete()
    return deleted_count



@shared_task
def delete_expired_files():
    deleted_files = UploadedFile.objects.filter(
        last_visited__lt=(timezone.now() - timedelta(days=30)),    #a month without visits
        auto_delete=True     #only the ones set to be auto deleted
    )
    count = deleted_files.count()
    for file in deleted_files:
        file.file.delete(save=False)
        file.delete()
    return count


@shared_task
def cleanup_orphaned_files():
    base_folder = settings.MEDIA_ROOT
    db_files = set(UploadedFile.objects.exclude(file='').values_list('file', flat=True))   #extract files urls of set uploaded files
    deleted_count = 0

    for root, dirs, files in os.walk(base_folder):  
        for name in files:
            full_path = os.path.join(root, name)
            # Get the relative path from MEDIA_ROOT
            rel_path = os.path.relpath(full_path, base_folder).replace("\\", "/")

            if rel_path not in db_files:
                try:
                    os.remove(full_path)
                    deleted_count += 1
                except Exception as e:
                    pass  

    return deleted_count 