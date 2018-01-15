# -*- coding: utf-8 -*-

from django import template
from django.template import Node, NodeList, Template, Context, RequestContext, Variable
from django.template import TemplateSyntaxError
from django.template import loader, get_library, Library, InvalidTemplateLibrary

from simpleblocks.models import Block

register = template.Library()

#######################################################################################################################
#######################################################################################################################

class GetSimpleBlockNode(Node):
	def __init__(self, ident, template):
		self.ident = ident
		self.template = str(template) if template else 'simpleblocks/simpleblocks.html'

	def render(self, context):
		try: item = Block.objects.get(ident=self.ident, location=context['request'].location)
		except:
			try: item = Block.objects.get(ident=self.ident, location__isnull=True)
			except: item = None
			
		if item:
			t = Template(item.get_text())
			c = RequestContext(context['request'], {})
			content = t.render(c)
		else:
			content = u''
			
		t = loader.get_template(self.template)
		c = RequestContext(context['request'], {'content':content})
		return t.render(c)
		
def get_simpleblock(parser, token):
	bits = token.split_contents()
	if len(bits) < 2 or len(bits) > 3: raise TemplateSyntaxError('Error token tag "get_simpleblock"')

	template = bits[2][1:-1] if len(bits) >= 3 and bits[2] and len(bits[2]) >= 3 else ''
	
	return GetSimpleBlockNode(bits[1][1:-1], template)
	
get_simpleblock = register.tag(get_simpleblock)

#######################################################################################################################
#######################################################################################################################