from django.db import models


class Donor(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)
    dob = models.DateField()
    blood_type = models.CharField(max_length=3)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.email
class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name
class BloodRequest(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    blood_type = models.CharField(max_length=3)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Request by {self.donor.email} for {self.blood_type} at {self.hospital.name}"