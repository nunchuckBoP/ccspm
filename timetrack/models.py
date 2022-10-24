from django.db import models
from accounts.models import CustomUser
from django.conf import settings

# Create your models here.

class Project(models.Model):
    number = models.CharField(verbose_name="Number", max_length=6, primary_key=True, unique=True)
    desc = models.CharField(verbose_name="Description", max_length=256)
    pm = models.ForeignKey(CustomUser, verbose_name="Project Manager", on_delete=models.SET_NULL, null=True, blank=True)
    created_on = models.DateField(verbose_name="Created On")
    
class Timesheet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_on = models.DateField(verbose_name="Created On")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    mileage_rate = models.DecimalField(verbose_name="Mileage Rate", default=settings.DEFAULT_MILAGE_RATE)
    sumbitted_on = models.DateField(verbose_name="Submitted On", null=True, blank=True)
    
    @property
    def submitted(self):
        if submitted is not None:
            return True
        else:
            return False

class TimeEntry(models.Model):
    sheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE)
    date = models.DateField()
    job = models.ForeignKey(Project, on_delete=models.DO_NOTHING, null=True, blank=True)
    work_code = models.IntegerField(verbose_name="Work Code", choices=settings.WORK_CODES)
    reg_hrs = models.DecimalField(verbose_name="Regular Hours", null=True, blank=True)
    ovt_hrs = models.DecimalField(verbose_name="Overtime Hours", null=True, blank=True)
    dbl_hrs = models.DecimalField(verbose_name="Doubletime Hours", null=True, blank=True)
    desc = models.CharField(max_length=1024, verbose_name="Description of Work")
    
    @property
    def total_hours(self):
        return self.reg_hrs + (self.ovt_hrs * 1.5) + (self.dbl_hrs * 2)
    
class ExpenseEntry(models.Model):
    sheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE)
    date = models.DateField()
    job = models.ForeignKey(Project, on_delete=models.DO_NOTHING, null=True, blank=True)
    mileage_rate = models.DecimalField(verbose_name="Mileage Rate", default=settings.DEFAULT_MILEAGE_RATE, null=False, blank=False)
    miles = models.DecimalField(null=True, blank=True)
    food = models.DecimalField(verbose_name="Per Diem Food", null=True, blank=True)
    air = models.DecimalField(verbose_name="Air Fare", null=True, blank=True)
    parking = models.DecimalField(verbose_name="Tolls / Parking", null=True, blank=True)
    meals = models.DecimalField(verbose_name="Business Meals", null=True, blank=True)
    other = models.DecimalField(verbose_name="Other Expenses", null=True, blank=True)
    other_explain = models.CharField(verbose_name="Explanation of Expenses", max_length=1024, null=True, blank=True)
    
    @property
    def mileage_amount(self):
        if self.miles is not None:
            return self.miles * self.mileage_rate
        else:
            return 0.0
    
    @property
    def daily_total(self):
        total = self.mileage_amount()
        if self.food is not None:
            total = total + self.food
        if self.air is not None:
            total = total + self.air
        if self.parking is not None:
            total = total + self.parking
        if self.meals is not None:
            total = total + self.meals
        if self.other is not None:
            total = total + self.other
        
        return total
    
class PartEntry(models.Model):
    sheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE)
    job = models.ForeignKey(Project, on_delete=models.DO_NOTHING, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    desc = models.CharField(max_length=256, verbose_name="Part Description / Part Number")
    notes = models.CharField(max_length=256, verbose_name="Additional Notes for Customer")
    reorder = models.CharField(max_length=3, verbose_name="Re-Order Part Yes/No", choices=(("Yes", "Yes"), ("No", "No")))
    