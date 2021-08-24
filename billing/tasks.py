import random
from celery.decorators import task
from .models import BillingItem
# aca puede no haber algo especifico de django
# ponele que mi tarea fuera generar un pdf o xls

@task(name="sum_two_numbers")
def add(x,y):
    return x + y

@task(name="multiply_two_numbers")
def mult(x,y):
    number1 = x
    number2 = y * random.randint(3,100)
    total = number1 * number2
    new_obj = BillingItem.objects.create(
        item_name="Some item",
        number_1=number1, 
        number_2=number2, 
        total=total)

    return total

@task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)