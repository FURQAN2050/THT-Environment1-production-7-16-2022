from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

@plugin_pool.register_plugin
class FooterPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Footer Plugin")
    render_template = "footerMain.html"
    cache = False

    def render(self, context, instance, placeholder):

        context = super(FooterPlugin, self).render(context, instance, placeholder)
        return context
