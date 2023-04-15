from django.db import models

class Loan(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    ]
    dni = models.CharField(max_length=8)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    genre = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    approved = models.BooleanField(default=False)

    class Meta:
        app_label = 'loans'

    def __str__(self):
        return f"{self.name} {self.last_name}´s Loan"
