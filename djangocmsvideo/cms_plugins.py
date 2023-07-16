from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import Data
from .models import Video

class VideoInlineAdmin(admin.StackedInline):
    model = Video

@plugin_pool.register_plugin
class VideoPlugin(CMSPluginBase):
    model = Data
    name = _("Video Plugin")
    render_template = "hello.html"
    cache = False
    inlines = (VideoInlineAdmin,)


    def render(self, context, instance, placeholder):
        context = super(VideoPlugin, self).render(context, instance, placeholder)
        items = list(instance.associated_item.all().values())
        context.update({
            'items': items,
        })
        print(instance)
        return context