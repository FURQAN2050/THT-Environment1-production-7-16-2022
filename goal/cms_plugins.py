from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

@plugin_pool.register_plugin
class GoalPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Goal Plugin")
    render_template = "goal.html"
    cache = False
