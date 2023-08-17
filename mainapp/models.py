from django.db import models

class UserRegistration(models.Model):
    full_name = models.CharField(max_length = 50)
    mobile_num = models.IntegerField()
    email_id = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.email_id


class ListingModel(models.Model):
    #details
    email_id = models.CharField(max_length=50)
    view_count = models.IntegerField(default = 0)
    title = models.CharField(max_length=50)
    address = models.TextField(max_length=200)
    beds_qty = models.IntegerField(default=0)
    baths_qty = models.IntegerField(default=0)
    sqrft = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to = "images/")
    description = models.TextField(max_length=500)
    country = models.CharField(max_length=50)
    apartment_type = models.CharField(max_length=50)
    #property
    property_id = models.IntegerField(default=0)
    rooms = models.IntegerField(default=0)
    #Amenities
    AC = models.BooleanField(default=False)
    builtin_wardrobe = models.BooleanField(default=False)
    dish_washer = models.BooleanField(default=False)
    floor_covering = models.BooleanField(default=False)
    medical = models.BooleanField(default=False)
    fencing = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    is_avaliable=models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ContactModel(models.Model):
    Name=models.CharField(max_length=20)
    Email=models.EmailField()
    Phone=models.PositiveIntegerField()
    Message=models.TextField()


    def __str__(self):
        return self.Name

class BookingModel(models.Model):
    user=models.ForeignKey(UserRegistration,on_delete=models.CASCADE)
    estate=models.ForeignKey(ListingModel,on_delete=models.CASCADE)
    Cost=models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + "   " + str(self.estate)