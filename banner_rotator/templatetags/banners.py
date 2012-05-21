from django import template

from banner_rotator.models import Banner

register = template.Library()


class BannerNode(template.Node):

    def __init__(self, varname='banner', region_key=None):
        self.varname, self.region_key = varname, region_key

    def render(self, context):
        kwargs = {}
        if self.region_key:
            kwargs['region__key'] = self.region_key
        try:
            banner = Banner.objects.biased_choice(**kwargs)
        except Banner.DoesNotExist:
            context[self.varname] = None
            return ''
        else:
            banner.view()
            context[self.varname] = banner
            return ''


@register.tag
def banner(parser, token):
    """
    Use: {% banner left as banner %}

    Pick a banner using the biased / weighting manager, with an region key
    """
    bits = token.contents.split()

    if len(bits) != 4:
        raise template.TemplateSyntaxError, "pick_banner tag takes four arguments"

    region = bits[1]
    varname = bits[3]

    return BannerNode(varname, region)
