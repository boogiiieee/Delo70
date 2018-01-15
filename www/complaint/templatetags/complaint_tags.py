from django import template
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import Node, NodeList, Template, Context, Variable
from django.conf import settings


from complaint.forms import ComplaintForm

register = template.Library()

###########################################################################################
###########################################################################################

class GetComplaintNode(Node):

	def render(self, context):
		form = ComplaintForm()
		t = get_template('complaint_temp.html')
		c = Context({'form' : form })
		html = t.render(c)
		return html

def get_complaint(parser, token):
	return GetComplaintNode()

get_complaint = register.tag(get_complaint)


###########################################################################################
###########################################################################################

class GetComplaintJs(Node):
	def render(self, context):
		complaint_js = u'<script src="' + settings.STATIC_URL + 'complaint/js/complaint.js"></script>'		
		return complaint_js

def get_comlaint_js(parser, token):
	return GetComplaintJs()

get_comlaint_js = register.tag(get_comlaint_js)

###########################################################################################
###########################################################################################