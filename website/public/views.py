from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse

from core.models import has_group


def index(request):
    return render(request, "public/index.html")


def media(request):
    stories = [
        {
            'title': "The People's Pantry in Toronto provides free home-cooked meals to those in need",
            'author': 'Olivia Little',
            'date': '2021-01-11',
            'link': 'https://www.blogto.com/eat_drink/2021/01/peoples-pantry-toronto-provides-free-home-cooked-meals-those-need/',
            'image': 'media/blogto.png',
            'outlet': 'BlogTO'
        },
        {
            'title': 'The Peoples Pantry is Helping Combat Food Insecurity',
            'author': 'Stella Acquisto',
            'date': '2020-07-28',
            'link': 'https://toronto.citynews.ca/video/2020/07/28/peoples-pantry-helping-combat-food-insecurity/#:~:text=combat%20food%20insecurity',
            'image': 'media/citynews-1.jpg',
            'outlet': 'CityNews Toronto'
        },
        {
            'title': 'Food is Love: Volunteers look to continue feeding Toronto with The People’s Pantry',
            'author': 'Lyndsay Morrison',
            'date': '2020-10-14',
            'link': 'https://toronto.ctvnews.ca/food-is-love-volunteers-look-to-continue-feeding-toronto-with-the-people-s-pantry-1.5145374',
            'image': 'media/citynews-2.jpg',
            'outlet': 'CityNews Toronto'
        },
        {
            'title': 'The Exception as the Rule: Toronto’s social reproduction organizing in the age of COVID-19',
            'author': 'Lina Nasr, El Hag Ali, and Olena Lyubchienko',
            'date': '2020-10-14',
            'link': 'https://spectrejournal.com/the-exception-as-the-rule/',
            'image': 'media/spectre.jpg',
            'outlet': 'Spectre'
        },
        {
            'title': 'People’s Pantry and creating inclusive spaces for migrants during the pandemic (PDF).',
            'author': 'Dominik Formanowicz',
            'date': '2020-11-03',
            'link': 'https://www.ryerson.ca/content/dam/centre-for-immigration-and-settlement/RCIS/publications/spotlightonmigration/2020_3_Formanowicz_Dominik_People\'s_Pantry_and_creating_inclusive_spaces_for_migrants_during_the_pandemic.pdf',
            'image': 'media/ryerson.jpg',
            'outlet': 'Ryerson’s spotlight on migration'
        },
        {
            'title': 'Sociology students build grassroots volunteer-run initiative to help those in need during COVID-19 pandemic.',
            'author': 'Sherri Klassen',
            'date': '2020-04-24',
            'link': 'https://sociology.utoronto.ca/sociology-students-build-grassroots-volunteer-run-initiative-to-help-those-in-need-during-covid-19-pandemic/',
            'image': 'media/utoronto.jpg',
            'outlet': 'University of Toronto'
        },
        {
            'title': 'The People’s Pantry Gives Free Food to Torontonians Experiencing Food Insecurity.',
            'author': 'Al Donato',
            'date': '2020-06-03',
            'link': 'http://www.huffingtonpost.ca/entry/peoples-pantry-free-food-toronto_ca_5ed163a2c5b64d62dd502851',
            'image': 'media/huffpo.jpg',
            'outlet': 'HuffPo Canada'
        },
        {
            'title': 'Grad student addresses food insecurity in Ontario as co-founder of a grassroots community initiative.',
            'author': 'Stephanie Shaw',
            'date': '2020-08-13',
            'link': 'https://yfile.news.yorku.ca/2020/08/13/laps-student-addresses-food-insecurity-in-ontario-with-grassroots-community-initiative-note-use-they-their-pronouns/',
            'image': 'media/yfile.jpg',
            'outlet': 'York University yFile'
        },
        {
            'title': 'Reasons to Love Toronto. No. 1: Because our home chefs are feeding the hungry',
            'author': 'Caroline Aksich',
            'date': '2020-10-20',
            'link': 'https://torontolife.com/city/reasons-to-love-toronto/no-1-because-our-home-chefs-are-feeding-the-hungry/',
            'image': 'media/torontolife.jpg',
            'outlet': 'Toronto Life'
        },
        {
            'title': 'Covid-19: Food Justice and Mutual Aid in the Pandemic (Webinar)',
            'author': '',
            'date': '2020-05-19',
            'link': 'https://www.facebook.com/110190900641866/videos/2779922052293971',
            'image': 'media/mutualaid.jpg',
            'outlet': 'Toronto/Tkaronto Mutual Aid'
        },
        {
            'title': 'Organizing During a Pandemic: Lessons for the Left (Webinar)',
            'author': '',
            'date': '2020-06-23',
            'link': 'https://www.youtube.com/watch?v=s2uw5GWrTKI',
            'image': 'media/sis.jpg',
            'outlet': 'SIS Salon'
        },
    ]

    return render(request, "public/media.html", context={'stories': stories})


class GroupView(UserPassesTestMixin):
    def test_func(self):
        return has_group(self.request.user, self.permission_group) or self.request.user.is_staff

    def get_permission_group_redirect_url(self):
        default = reverse('profile')
        return getattr(self, 'permission_group_redirect_url', default)

    def handle_no_permission(self):
        return redirect(self.get_permission_group_redirect_url())
