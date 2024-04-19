from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import Permission

class SoftDeleteQuerySet(QuerySet):
    def delete(self):
        self.update(is_deleted=True)

class BaseModelManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    objects = BaseModelManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

class CustomUserPermissions:
    class Meta:
        permissions = (
            ("edit_or_add_category", "Can edit or add category"),
            ("edit_or_add_product", "Can edit or add products"),
        )
        
        
class Colors(BaseModel):
    color = models.CharField(max_length=50)
    hex = models.CharField(max_length=7)
    
    def __str__(self):
        return self.color