from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

@plugin_pool.register_plugin
class WorkoutGames(CMSPluginBase):
    model = CMSPlugin
    name = _("Workouts Plugin")
    render_template = "workouts.html"
    cache = False

