from django.shortcuts import redirect, get_object_or_404

from banner_rotator.models import Banner, Region


def click(request, region_id, banner_id):
    banner = get_object_or_404(Banner, pk=banner_id)
    region = get_object_or_404(Region, pk=region_id)
    banner.click(request, region)

    return redirect(banner.url)
