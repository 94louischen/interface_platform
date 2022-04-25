from django.db import models


# Create your models here.
class BaseModel(models.Model):
    """
    基类
    """
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # 指定这个属性后，不会生成迁移表
