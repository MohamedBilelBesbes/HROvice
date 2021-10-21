from django.db import models

class Intern(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    cin = models.IntegerField()
    email = models.EmailField()
    phonenumber = models.IntegerField()
    school = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Attestation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
    dateinit = models.DateField()
    dateend = models.DateField()
    title = models.CharField(max_length=200)
    signer = models.CharField(max_length=200)
    dateofsign = models.DateField()
    def __str__(self):
        return self.title