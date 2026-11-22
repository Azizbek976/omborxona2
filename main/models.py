from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import SET_NULL, CharField, TextField
from django.utils.text import slugify

# from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50 , blank=True , null=True)
    slug = models.SlugField(max_length=60 , unique=True)
    image = models.ImageField(upload_to="category/" , blank=True , null=True)

    def __str__(self):
        return self.name

    def save(self , *args , **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    name = models.CharField(max_length=50 , blank=True , null=True)
    slug = models.SlugField(max_length=60 , blank=True , null=True)
    image = models.ImageField(upload_to='subimage/' , blank=True , null=True)
    category = models.ForeignKey(Category , on_delete=SET_NULL , blank=True , null=True)

    def __str__(self):
        return self.name

    def save(self , *args , **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while SubCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Seller(models.Model):
    name = models.CharField(max_length=20 , blank=True , null=True)
    image = models.ImageField(upload_to="seller/" , blank=True , null=True)

class Product(models.Model):
    name = models.CharField(max_length=50 , blank=True , null=True)
    slug = models.SlugField(max_length=100)
    country = models.CharField(max_length=50 , default="Uzbekistan")
    brand = models.CharField(max_length=50 , blank=True , null=True)
    details = models.TextField(blank=True , null=True)
    price = models.FloatField(max_length=12 , default=0)
    amount = models.PositiveSmallIntegerField(max_length=6 , blank=True , null=True)
    delivery = models.CharField(max_length=100 , blank=True , null=True)
    image = models.ImageField(upload_to="product/" , blank=True , null=True)
    sub_category = models.ForeignKey(SubCategory , on_delete=SET_NULL , blank=True , null=True)
    order = models.PositiveIntegerField(max_length=6 , blank=True , null=True)

    def save(self , *args , **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args , **kwargs)

    @property
    def get_main_media(self):
        medias = self.media_set.all()
        if medias.exists():
            media = medias.order_by("-main").first()
            return media
        return None

    def __str__(self):
        return (f"{self.name} --- {self.brand} --- {self.details} --- {self.price} --- "
                f"{self.amount} --- {self.delivery} --- {self.sub_category}")

class Media(models.Model):
    image = models.ImageField(upload_to="media" , blank=True , null=True)
    main = models.BooleanField(default=False)
    product = models.ForeignKey(Product , on_delete=models.CASCADE, blank=True , null=True)

    def __str__(self):
        return f"{self.product}"

class Property(models.Model):
    name = CharField(max_length=100)
    value = TextField()
    product = models.ForeignKey(Product , on_delete=models.CASCADE, blank=True , null=True)

    def __str__(self):
        return f"{self.name} --- {self.value} --- {self.product}"

class Choice(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product , on_delete=models.CASCADE , blank=True , null=True)

    def __str__(self):
        return f"{self.name} --- {self.product}"

class Variant(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="variant/" , blank=True , null=True)
    deltaprice = models.FloatField(default=0)
    choice = models.ForeignKey(Choice , on_delete=models.CASCADE , blank=True , null=True)

    @property
    def nextprice(self):
        return self.choice.product.price + self.deltaprice

    def __str__(self):
        return f"{self.name} --- {self.deltaprice} --- {self.choice}"

class Discount(models.Model):
    percentage = models.FloatField(blank=True , null=True)
    disprice = models.FloatField(blank=True , null=True)
    newprice = models.FloatField(blank=True , null=True)

    endtime = models.DateTimeField(blank=True , null=True)
    product = models.ForeignKey(Product , on_delete=models.CASCADE , blank=True , null=True)

    def __str__(self):
        return f"{self.percentage}% --- {self.disprice} --- {self.newprice} --- {self.endtime}"

    def save(self , *args , **kwargs):
        price = self.product.price
        if self.price==0:
            return
        if self.percentage is not None:
            self.newprice = price/100*(100-self.percentage)
            self.disprice = price - self.newprice
        elif self.disprice is not None:
            self.percentage = (self.disprice / price) * 100
            self.newprice = price - self.disprice
        elif self.newprice is not None:
            self.percentage = ((price - self.newprice) / price ) * 100
            self.disprice = price - self.newprice

        super().save(*args , **kwargs)

class Review(models.Model):
    text = models.TextField(blank=True , null=True)
    rate = models.PositiveSmallIntegerField(blank=True , null=True ,
                                            validators=[MinValueValidator(1) , MaxValueValidator(5)])
    crtime = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product , on_delete=models.CASCADE, blank=True , null=True)
    user = models.ForeignKey(User , on_delete=models.SET_NULL, blank=True , null=True)

class ADbanner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="adbanner/" , blank=True , null=True)
    url = models.URLField(blank=True , null=True)
    active = models.BooleanField(default=False)
    endtime = models.DateField(blank=True , null=True)

    def __str__(self):
        return f"{self.title} --- {self.url} --- {self.active} --- {self.endtime}"










