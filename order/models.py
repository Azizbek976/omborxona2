from main.models import *
from cities_light.models import Country

class Favorite(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} -- {self.product}"

class Cartitem(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant , on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1 , validators=[MinValueValidator(1) , MaxValueValidator(100)])
    crtime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} --- {self.product} --- {self.variant} --- {self.quantity} --- {self.crtime}"

class Order(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    country = models.ForeignKey(Country , on_delete=models.CASCADE , blank=True , null=True)
    address = models.TextField(blank=True , null=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=20 , blank=True , null=True)
    email = models.EmailField(max_length=100 , blank=True , null=True)
    deliverytime = models.CharField(max_length=100 , blank=True , null=True)
    paymenttime = models.CharField(max_length=100 , blank=True , null=True)
    crtime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50 , default="Kutilmoqda")

    def __str__(self):
        return f"{self.user} --- {self.country} --- {self.crtime} --- {self.status}"





























