from django.db import models
from django.contrib.auth.models import User

from finance.authentication.models import UserProfile


class Balance(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Balance for {self.user_profile.user.username}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('income', 'Income'), ('expense', 'Expense')])
    date = models.DateField()

    def __str__(self):
        return f"{self.description} ({self.amount})"
