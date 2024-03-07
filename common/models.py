from django.db import models
import uuid
# Create your models here.


class BaseModel(models.Model):
    """
    This is an abstract base model for other models
    it provides common fields that most models need
    Every class must inherit from this base model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        # Marked as an abstract model so that it cannot be used to create tables in the database
        abstract = True

