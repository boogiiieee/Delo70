# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
import datetime

from rabota.models import Vacancy, Resume, Category

#######################################################################################################################
#######################################################################################################################

#Менеджер помещает старые вакансии и резюме в архив и обновляет категории
class Command(NoArgsCommand):
	help = "Сommand places the vacancies and resumes older than a week to the archive."

	def handle_noargs(self, **options):		
		Vacancy.old_vacancies.all().update(in_archive = True)		
		Resume.old_resumes.all().update(in_archive = True)	
		
		return

#######################################################################################################################
#######################################################################################################################