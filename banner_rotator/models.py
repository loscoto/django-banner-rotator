from django.db import models

from banner_rotator.managers import BiasedManager

class Region(models.Model):

    key = models.SlugField(max_length=20, unique=True)

    def __unicode__(self):
        return self.key

class Banner(models.Model):

    objects = BiasedManager()

    region = models.ForeignKey(Region, related_name="banners")

    name = models.CharField(max_length=255)
    url = models.URLField()

    impressions = models.PositiveIntegerField(default=0)

    weight = models.IntegerField(help_text="A ten will display 10 times more often that a one.",\
        choices=[[i,i] for i in range(11)])

    image = models.ImageField(upload_to='banners')

    width = models.CharField(max_length=15)
    height = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def view(self):
        self.impressions = models.F('impressions') + 1
        self.save()
        return ''

    def click(self, request, region):
        click = {
            'banner': self,
            'region': region,
            'ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'referrer': request.META.get('HTTP_REFERER'),
        }
        
        if request.user.is_authenticated():
            click['user'] = request.user

        return Click.objects.create(**click)


    #@models.permalink
    #def get_absolute_url(self):
    #    return ('banner_click', (), {'banner_id': self.pk})


class Click(models.Model):

    banner = models.ForeignKey(Banner, related_name="clicks")
    user = models.ForeignKey("auth.User", null=True, blank=True, related_name="clicks")
    region = models.ForeignKey(Region, related_name="clicks")

    datetime = models.DateTimeField("Clicked at", auto_now_add=True)
    ip = models.IPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)
