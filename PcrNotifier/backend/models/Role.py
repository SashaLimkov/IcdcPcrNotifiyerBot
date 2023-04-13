from django.db import models


class Role(models.Model):
    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    name = models.CharField("Название роли", max_length=100, unique=True)

    def __str__(self):
        return self.name
