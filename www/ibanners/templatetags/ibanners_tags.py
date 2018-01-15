# -*- coding: utf-8 -*-

from django import template
from ibanners.views import gen_banner_code


class BannerNode(template.Node):
    def __init__(self, request, zone_id, var):
        self.request = template.Variable(request)
        self.zone_id = zone_id

        if var:
            try:
                self.var = template.Variable(var)
            except:
                self.var = False
        else: self.var = False

    def render(self, context):
        if self.var:
            self.var = str(self.var.resolve(context))
        try:
            return gen_banner_code(self.request.resolve(context), \
                                   self.zone_id, self.var)
        except template.VariableDoesNotExist:
            return ''

# Тег для загрузки баннеров
def do_banner(parser, token):
    try:
        tokens = token.split_contents()
        if tokens.__len__() == 3:
            tag_name, request, zone_id = token.split_contents()
            var = False
        elif tokens.__len__() == 4:
            tag_name, request, zone_id,var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a 2 or 3 arguments" % token.contents.split()[0]
    return BannerNode(request, zone_id, var)

register = template.Library()
register.tag('banner', do_banner)
