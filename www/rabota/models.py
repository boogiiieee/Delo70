# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.conf import settings
import datetime
import re, os


from pytils.translit import slugify
from sorl.thumbnail import ImageField as SorlImageField

from geo.models import CustomLocation

##########################################################################
##########################################################################

User.add_to_class('phone',
	models.CharField(max_length=20, verbose_name=u'телефон', blank=True)
)

def get_user_name(self):
	return self.get_full_name() if self.get_full_name() else self.username

User.add_to_class('get_user_name', get_user_name)
User.add_to_class('__unicode__', get_user_name)

##########################################################################
##########################################################################

class ActiveManager(models.Manager): 
	def get_query_set(self): 
		return super(ActiveManager, self).get_query_set().filter(is_active=True)
		
##########################################################################
##########################################################################

#График работы
class Schedule(models.Model):
	title = models.CharField(max_length=100, verbose_name=u'название')
	is_active = models.BooleanField(verbose_name=u'активно', default=True)
	order = models.IntegerField(verbose_name=u'сортировка', default=0)
	
	def get_title(self): return self.title
	
	def __unicode__(self):
		return self.get_title()
		
	objects = models.Manager()
	activs = ActiveManager()
		
	class Meta: 
		verbose_name = u'график работы' 
		verbose_name_plural = u'график работы'
		ordering = ['order', 'title']
		
#Тип занятости
class TypeEmployment(models.Model):
	title = models.CharField(max_length=100, verbose_name=u'название')
	is_active = models.BooleanField(verbose_name=u'активно', default=True)
	order = models.IntegerField(verbose_name=u'сортировка', default=0)
	
	def get_title(self): return self.title
	
	def __unicode__(self):
		return self.get_title()
		
	objects = models.Manager()
	activs = ActiveManager()
		
	class Meta: 
		verbose_name = u'тип занятости' 
		verbose_name_plural = u'тип занятости'
		ordering = ['order', 'title']
		
#Тип ЗП
class TypeWages(models.Model):
	title = models.CharField(max_length=100, verbose_name=u'название')
	is_active = models.BooleanField(verbose_name=u'активно', default=True)
	order = models.IntegerField(verbose_name=u'сортировка', default=0)
	
	def get_title(self): return self.title
	
	def __unicode__(self):
		return self.get_title()
		
	objects = models.Manager()
	activs = ActiveManager()
		
	class Meta: 
		verbose_name = u'тип ЗП' 
		verbose_name_plural = u'тип ЗП'
		ordering = ['order', 'title']

#Образование
class Education(models.Model):
	title = models.CharField(max_length=100, verbose_name=u'название')
	is_active = models.BooleanField(verbose_name=u'активно', default=True)
	order = models.IntegerField(verbose_name=u'сортировка', default=0)
	
	def get_title(self): return self.title
	
	def __unicode__(self):
		return self.get_title()
		
	objects = models.Manager()
	activs = ActiveManager()
		
	class Meta: 
		verbose_name = u'образование' 
		verbose_name_plural = u'образование'
		ordering = ['order', 'title']
		
#Стаж
class Experience(models.Model):
	title = models.CharField(max_length=100, verbose_name=u'название')
	is_active = models.BooleanField(verbose_name=u'активно', default=True)
	order = models.IntegerField(verbose_name=u'сортировка', default=0)
	
	def get_title(self): return self.title
	
	def __unicode__(self):
		return self.get_title()
		
	objects = models.Manager()
	activs = ActiveManager()
		
	class Meta: 
		verbose_name = u'стаж' 
		verbose_name_plural = u'стаж'
		ordering = ['order', 'title']

##########################################################################
##########################################################################

#Категории
class Category(models.Model):
	title = models.CharField(max_length=100, verbose_name=u'название')
	slug = models.CharField(max_length=500, verbose_name=u'псевдоним', blank=True)
	
	is_active = models.BooleanField(verbose_name=u'активно', default=True)
	order = models.IntegerField(verbose_name=u'сортировка', default=0)
	
	meta_title = models.TextField(verbose_name=u'title', blank=True)
	meta_description = models.TextField(verbose_name=u'description', blank=True)
	meta_keywords = models.TextField(verbose_name=u'keywords', blank=True)
	
	def get_title(self): return self.title
	def get_meta_title(self): return self.meta_title
	def get_meta_description(self): return self.meta_description
	def get_meta_keywords(self): return self.meta_keywords
	
	def get_count_vacancy(self, location=None):
		q = {'is_active': True, 'in_archive': False}
		if location:
			q['city'] = location
		return self.vacancy_category_rel.filter(**q).count()
		
	def get_count_resume(self, location=None):
		q = {'is_active': True, 'in_archive': False}
		if location:
			q['city'] = location
		return self.resume_category_rel.filter(**q).count()
	
	def __unicode__(self):
		return self.get_title()
		
	def get_absolute_vacancy_url(self, location):
		return reverse('category_vacancy_url', args=[], kwargs={'slug_city':location, 'id':self.id, 'slug':self.slug})
		
	def get_absolute_resume_url(self, location):
		return reverse('category_resume_url', args=[], kwargs={'slug_city':location, 'id':self.id, 'slug':self.slug})
		
	objects = models.Manager()
	activs = ActiveManager()
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Category, self).save(*args, **kwargs)
	
	class Meta: 
		verbose_name = u'категория' 
		verbose_name_plural = u'категории'
		ordering = ['order', 'title']

##########################################################################
##########################################################################

#Вакансия
class VacancyActiveManager(models.Manager): 
	def get_query_set(self): 
		return super(VacancyActiveManager, self).get_query_set().filter(is_active=True, in_archive=False).filter(Q(phone1__isnull=False) | Q(phone2__isnull=False) | Q(email__isnull=False))	
		
class OldVacanciesManager(models.Manager): 
	def get_query_set(self): 
		month_ago = datetime.datetime.now() - datetime.timedelta(days=90)
		return super(OldVacanciesManager, self).get_query_set().filter( modified__lte=month_ago)

class Vacancy(models.Model):
	def make_upload_path(instance, filename):
		if instance.user: return u'upload/%d/vacancy/%s' % (instance.user.id, filename.lower())
		else: return u'upload/vacancy/%s' % filename.lower()
		
	user = models.ForeignKey(User, verbose_name=u'пользователь', related_name='vacancy_rel', blank=True, null=True)
	
	post = models.CharField(max_length=100, verbose_name=u'должность')
	slug = models.CharField(max_length=500, verbose_name=u'псевдоним должности', blank=True)	
	
	brief = models.CharField(max_length=250, verbose_name=u'краткое описание')
	category = models.ManyToManyField(Category, verbose_name=u'рубрика', related_name='vacancy_category_rel')
	
	schedule = models.ForeignKey(Schedule, verbose_name=u'график работы', related_name='vacancy_schedule_rel', blank=True, null=True)
	type_employment = models.ForeignKey(TypeEmployment, verbose_name=u'тип занятости', related_name='vacancy_type_employment_rel', blank=True, null=True)
	wage_min = models.IntegerField(verbose_name=u'Зарплата от', blank=True, null=True)
	wage_max = models.IntegerField(verbose_name=u'Зарплата до', blank=True, null=True)
	type_wages = models.ForeignKey(TypeWages, verbose_name=u'тип ЗП', related_name='vacancy_type_wages_rel', blank=True, null=True)
	description = models.TextField(max_length=10000, verbose_name=u'описание')
	
	education = models.ForeignKey(Education, verbose_name=u'образование', related_name='vacancy_education_rel', blank=True, null=True)
	experience = models.ForeignKey(Experience, verbose_name=u'стаж работы', related_name='vacancy_experience_rel', blank=True, null=True)
	professional_skills = models.TextField(max_length=10000, verbose_name=u'навыки и опыт работы', blank=True)
	
	company = models.CharField(max_length=100, verbose_name=u'название компании')
	fio = models.CharField(max_length=100, verbose_name=u'контактное лицо')
	phone1 = models.CharField(max_length=100, verbose_name=u'телефон 1')
	other_phone1 = models.CharField(max_length=100, verbose_name=u'комментарий к телефону 1', blank=True)
	phone2 = models.CharField(max_length=100, verbose_name=u'телефон 2', blank=True)
	other_phone2 = models.CharField(max_length=100, verbose_name=u'комментарий к телефону2', blank=True)
	email = models.EmailField(max_length=100, verbose_name=u'e-mail', blank=True)
	icq = models.CharField(max_length=100, verbose_name=u'ICQ', blank=True)
	skype = models.CharField(max_length=100, verbose_name=u'skype', blank=True)
	site = models.URLField(max_length=100, verbose_name=u'сайт', verify_exists=False, blank=True)
	city = models.ForeignKey(CustomLocation, verbose_name=u'город')
	street = models.CharField(max_length=100, verbose_name=u'улица', blank=True)
	home = models.CharField(max_length=100, verbose_name=u'№ дома', blank=True)
	other_address = models.CharField(max_length=100, verbose_name=u'комментарий к адресу', blank=True)
	logo = SorlImageField(max_length=300, upload_to=make_upload_path, verbose_name=u'логотип', blank=True, null=True)
	
	views_count = models.IntegerField(verbose_name=u'просмотры', default=0)	
	
	created = models.DateTimeField(verbose_name=u'дата создания', default=datetime.datetime.now())
	modified = models.DateTimeField(verbose_name=u'дата обновления', auto_now=True)
	
	stick_date = models.DateTimeField(verbose_name=u'прилеплено до', default=datetime.datetime.now(), help_text=u'До какой даты считать сообщение прилепленным.')
	
	is_active = models.BooleanField(verbose_name=u'активно', default=True)
	in_archive = models.BooleanField(verbose_name=u'в архиве', default=False)
	order = models.IntegerField(verbose_name=u'сортировка', default=0)	
	
	def get_post(self): return self.post
	def get_fio(self):
		return self.fio
		
	def get_wage(self):
		if self.wage_min or self.wage_max:
			wage = u''
			if self.wage_min:
				wage +=u'от %s' % self.wage_min
			if self.wage_max:
				wage +=u' до %s' % self.wage_max
			if self.type_wages:
				wage +=u' %s' % self.type_wages
			return wage
		else: return u'не указан'
		
	def get_phones(self):
		if self.phone1 and self.other_phone1:
			return u'%s, %s' % (self.phone1, self.other_phone1)
		else:
			return self.phone1
	
	def get_address(self):
		address = u''
		if self.city: 
			address += u'%s' % self.city
			if self.street: 
				address += u', %s' % self.street
				if self.home: 
					address += u', %s' % self.home
		else:
			if self.street: 
				address += u', %s' % self.street
				if self.home: 
					address += u', %s' % self.home
		if self.other_address:
			address += u'(%s)' % self.other_address
		return address
			
	def __unicode__(self):
		return self.get_post()
		
	objects = models.Manager()
	activs = VacancyActiveManager()
	old_vacancies = OldVacanciesManager()
		
	class Meta: 
		verbose_name = u'вакансия' 
		verbose_name_plural = u'вакансии'
		ordering = ['order', '-stick_date', '-created', '-id']
		
	def get_absolute_url(self):
		return reverse('vacancy_item', args=[], kwargs={'slug_city':self.city.slug, 'id':self.id, 'slug':self.slug})
		
	def get_edit_url(self):
		if self.user:
			return reverse('account_vacancy_item', args=[], kwargs={'username':self.user.username, 'id':self.id})
		return None
		
	def get_del_url(self):
		if self.user:
			return reverse('vacancy_del', args=[], kwargs={'username':self.user.username, 'id':self.id})
		return None
		
	def save(self, *args, **kwargs):
		self.slug = slugify(self.post)
		super(Vacancy, self).save(*args, **kwargs)

	def get_ret_url(self):
		if self.user:
			return reverse('vacancy_ret', args=[], kwargs={'username':self.user.username, 'id':self.id})
		return None
		
##########################################################################
##########################################################################

SEX_CHOICES = [
	(10, u'мужской'),
	(20, u'женский'),
]

#Резюме
class ResumeActiveManager(models.Manager): 
	def get_query_set(self): 
		return super(ResumeActiveManager, self).get_query_set().filter(is_active=True, in_archive=False)

class OldResumesManager(models.Manager): 
	def get_query_set(self): 
		month_ago = datetime.datetime.now() - datetime.timedelta(days=90)
		return super(OldResumesManager, self).get_query_set().filter( modified__lte=month_ago)

class Resume(models.Model):
	def make_upload_path(instance, filename):
		if instance.user: return u'upload/%d/resume/%s' % (instance.user.id, filename.lower())
		else: return u'upload/resume/%s' % filename.lower()
		
	user = models.ForeignKey(User, verbose_name=u'пользователь', related_name='resume_rel', blank=True, null=True)
	
	post = models.CharField(max_length=100, verbose_name=u'должность')
	slug = models.CharField(max_length=500, verbose_name=u'псевдоним должности', blank=True)	
	
	category = models.ManyToManyField(Category, verbose_name=u'рубрика', related_name='resume_category_rel')
	
	schedule = models.ForeignKey(Schedule, verbose_name=u'график работы', related_name='resume_schedule_rel', blank=True, null=True)
	type_employment = models.ForeignKey(TypeEmployment, verbose_name=u'тип занятости', related_name='resume_type_employment_rel', blank=True, null=True)
	wage_min = models.IntegerField(verbose_name=u'Зарплата от', blank=True, null=True)
	type_wages = models.ForeignKey(TypeWages, verbose_name=u'тип ЗП', related_name='resume_type_wages_rel', blank=True, null=True)
	
	fio = models.CharField(max_length=100, verbose_name=u'контактное лицо')
	photo = SorlImageField(max_length=300, upload_to=make_upload_path, verbose_name=u'фотография', blank=True, null=True)
	dob = models.DateField(verbose_name=u'дата рождения')
	sex = models.IntegerField(verbose_name=u'пол', choices=SEX_CHOICES)
	marital_status = models.NullBooleanField(verbose_name=u'женат / замужем', blank=True, null=True)
	experience = models.ForeignKey(Experience, verbose_name=u'стаж работы', related_name='resume_experience_rel', blank=True, null=True)
	professional_skills = models.TextField(max_length=10000, verbose_name=u'навыки и опыт работы', blank=True)
	education = models.ForeignKey(Education, verbose_name=u'образование', related_name='resume_education_rel', blank=True, null=True)
	educational_institution = models.CharField(max_length=100, verbose_name=u'учебное заведение', blank=True)
	major_subject = models.CharField(max_length=100, verbose_name=u'основная специальность', blank=True)
	extras_education = models.TextField(max_length=10000, verbose_name=u'доп. образование', blank=True)
	personal_qualities = models.TextField(max_length=10000, verbose_name=u'личные качества', blank=True)
	driver_license = models.NullBooleanField(verbose_name=u'есть водительские права')
	willing_travel = models.NullBooleanField(verbose_name=u'готов к командировкам')
	smoke = models.NullBooleanField(verbose_name=u'курю')
	summary = models.FileField(max_length=300, upload_to=make_upload_path, verbose_name=u'резюме', blank=True, null=True)
	
	phone1 = models.CharField(max_length=100, verbose_name=u'телефон')
	other_phone1 = models.CharField(max_length=100, verbose_name=u'комментарий к телефону', blank=True)
	email = models.EmailField(max_length=100, verbose_name=u'e-mail', blank=True)
	icq = models.CharField(max_length=100, verbose_name=u'ICQ', blank=True)
	skype = models.CharField(max_length=100, verbose_name=u'skype', blank=True)
	city = models.ForeignKey(CustomLocation, verbose_name=u'город')
	
	views_count = models.IntegerField(verbose_name=u'просмотры', default=0)	
	
	created = models.DateTimeField(verbose_name=u'дата создания', auto_now_add=True)
	modified = models.DateTimeField(verbose_name=u'дата обновления', auto_now=True)
	
	is_active = models.BooleanField(verbose_name=u'активно', default=True)
	in_archive = models.BooleanField(verbose_name=u'в архиве', default=False)
	order = models.IntegerField(verbose_name=u'сортировка', default=0)

	def get_post(self): return self.post
	
	def __unicode__(self):
		return self.get_post()
		
	objects = models.Manager()
	old_resumes = OldResumesManager()
	activs = ResumeActiveManager()
		
	class Meta: 
		verbose_name = u'резюме' 
		verbose_name_plural = u'резюме'
		ordering = ['order', '-id']
	
	def get_fio(self):
		return self.fio
		
	def get_dob(self):
		return self.dob
		
	def get_age(self):
		return datetime.datetime.now().year -self.dob.year
		
	def get_phones(self):
		if self.phone1 and self.other_phone1:
			return u'%s, %s' % (self.phone1, self.other_phone1)
		else:
			return self.phone1
			
	def get_marital_status(self):
		if self.marital_status == '': return False
		else:
			if self.sex == 10:
				if self.marital_status: return u'женат'
				else: return u'не женат'
			elif self.sex == 20:
				if self.marital_status: return u'замужем'
				else: return u'не замужем'
				
	def get_driver_license(self):
		if self.driver_license == '': return False 
		else:
			if self.driver_license: return u'да'
			else: return u'нет'
			
	def get_willing_travel(self):
		if self.willing_travel == '': return False 
		else:
			if self.willing_travel: return u'да'
			else: return u'нет'
				
	def get_wage(self):
		if self.wage_min:
			if self.type_wages:	return '%d %s' % (self.wage_min, self.type_wages)
			else:
				return '%d руб.' % self.wage_min
		return None
			
	def get_no_foto(self):
		if self.sex == 20:
			return u'<img class="img-polaroid" style="max-width:100px; max-height:85px" src="%simg/no-foto.png" alt="Нет фото" />' % settings.MEDIA_URL
		return u'<img class="img-polaroid" style="max-width:100px;max-height:85px" src="%simg/no-foto.gif" alt="Нет фото" />' % settings.MEDIA_URL
	
	def get_absolute_url(self):
		return reverse('resume_item', args=[], kwargs={'slug_city':self.city.slug, 'id':self.id, 'slug':self.slug})
		
	def get_edit_url(self):
		if self.user:
			return reverse('account_resume_item', args=[], kwargs={'username':self.user.username, 'id':self.id})
		return None
		
	def get_del_url(self):
		if self.user:
			return reverse('resume_del', args=[], kwargs={'username':self.user.username, 'id':self.id})
		return None
		
	def save(self, *args, **kwargs):
		self.slug = slugify(self.post)
		super(Resume, self).save(*args, **kwargs)

	def get_ret_url(self):
		if self.user:
			return reverse('resume_ret', args=[], kwargs={'username':self.user.username, 'id':self.id})
		return None
		
##########################################################################
##########################################################################

#Подписаться  на вакансии
class SubscribeVacancy(models.Model):
	user = models.OneToOneField(User, verbose_name=u'пользователь', related_name='subscribe_vacancy_rel')
	
	category = models.ManyToManyField(Category, verbose_name=u'рубрика')
	
	schedule = models.ForeignKey(Schedule, verbose_name=u'график работы', blank=True, null=True)
	type_employment = models.ForeignKey(TypeEmployment, verbose_name=u'тип занятости', blank=True, null=True)
	wage_min = models.IntegerField(verbose_name=u'Зарплата от', blank=True, null=True)
	wage_max = models.IntegerField(verbose_name=u'Зарплата до', blank=True, null=True)
	type_wages = models.ForeignKey(TypeWages, verbose_name=u'тип ЗП', blank=True, null=True)
	
	education = models.ForeignKey(Education, verbose_name=u'образование', blank=True, null=True)
	experience = models.ForeignKey(Experience, verbose_name=u'стаж работы', blank=True, null=True)
	
	city = models.ForeignKey(CustomLocation, verbose_name=u'город')
	
	created = models.DateTimeField(verbose_name=u'дата создания', auto_now_add=True)
	modified = models.DateTimeField(verbose_name=u'дата обновления', auto_now=True)
	
	is_active = models.BooleanField(verbose_name=u'активно', default=True)
	
	def __unicode__(self):
		return self.user.get_full_name()
		
	objects = models.Manager()
	activs = ActiveManager()
		
	class Meta: 
		verbose_name = u'подписка на вакансии' 
		verbose_name_plural = u'подписка на вакансии'
		ordering = ['id']

##########################################################################
##########################################################################

#Подписаться  на резюме
class SubscribeResume(models.Model):
	user = models.OneToOneField(User, verbose_name=u'пользователь', related_name='subscribe_resume_rel')
	
	category = models.ManyToManyField(Category, verbose_name=u'рубрика')
	
	schedule = models.ForeignKey(Schedule, verbose_name=u'график работы', blank=True, null=True)
	type_employment = models.ForeignKey(TypeEmployment, verbose_name=u'тип занятости', blank=True, null=True)
	wage_min = models.IntegerField(verbose_name=u'Зарплата от', blank=True, null=True)
	type_wages = models.ForeignKey(TypeWages, verbose_name=u'тип ЗП', blank=True, null=True)
	
	experience = models.ForeignKey(Experience, verbose_name=u'стаж работы', blank=True, null=True)
	education = models.ForeignKey(Education, verbose_name=u'образование', blank=True, null=True)
	
	city = models.ForeignKey(CustomLocation, verbose_name=u'город')
	
	created = models.DateTimeField(verbose_name=u'дата создания', auto_now_add=True)
	modified = models.DateTimeField(verbose_name=u'дата обновления', auto_now=True)
	
	is_active = models.BooleanField(verbose_name=u'активно', default=True)
	
	def __unicode__(self):
		return self.user.get_full_name()
		
	objects = models.Manager()
	activs = ActiveManager()
		
	class Meta: 
		verbose_name = u'подписка на резюме' 
		verbose_name_plural = u'подписка на резюме'
		ordering = ['id']

##########################################################################
##########################################################################