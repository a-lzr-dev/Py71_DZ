from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()

def validate_not_past(value):
    if value < timezone.now().date():
        raise ValidationError('Дата бронирования не может быть в прошлом.')

class Table(models.Model):
    number = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(10000)], verbose_name="Номер столика", help_text="от 1 до 10000")
    image = models.ImageField(upload_to='table/%Y/%m', blank=True, null=True, verbose_name="Изображение столика", max_length=256)
    seats = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(100)], verbose_name="Кол-во мест за столиком", help_text="от 0 до 100")

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.RESTRICT)
    user = models.ForeignKey(USER_MODEL, on_delete=models.RESTRICT)
    date = models.DateField(validators=[validate_not_past], verbose_name="Дата бронирования")
    hour_start = models.IntegerField(validators = [MinValueValidator(8), MaxValueValidator(17)], verbose_name="Час начала бронирования", help_text="от 8 до 17")
    hour_end = models.IntegerField(validators = [MinValueValidator(9), MaxValueValidator(18)], verbose_name="Час окончания бронирования", help_text="от 9 до 18")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания бронирования")
#    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

# class Note(models.Model):
#
#     user = models.ForeignKey(USER_MODEL, on_delete=models.RESTRICT)
#     title = models.CharField(max_length=128, verbose_name="Заголовок", help_text="Не более 128 символов")
#     content = models.TextField(verbose_name="Содержимое")
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     image = models.ImageField(upload_to='notes/%Y/%m', blank=True, null=True, verbose_name="Картинка", max_length=256)
#
#     class Meta:
#         ordering = ['-created_at']
