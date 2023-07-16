from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

@plugin_pool.register_plugin
class NavbarPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Navbar Plugin")
    render_template = "navbar.html"
    cache = False

    def render(self, context, instance, placeholder):

        context = super(NavbarPlugin, self).render(context, instance, placeholder)
        return context
