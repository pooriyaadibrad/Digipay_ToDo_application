from django.db import models
from django_jalali.db import models as jalali_models
import uuid

class Todo(models.Model):
    """
    this model use for stored _todo_ information in database
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = jalali_models.jDateTimeField()
    completed = models.BooleanField(default=False)
    created_at = jalali_models.jDateTimeField(auto_now_add=True)
    updated_at = jalali_models.jDateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'ToDO_list'
