import random
from datetime import date
from django.shortcuts import redirect
from django.templatetags.static import static
from django.views.generic import TemplateView

from recipients.models import MealRequest, GroceryRequest


def logo(request):
    return redirect(static('logo-black.png'))


class IndexView(TemplateView):
    template_name = "public/index.html"
    MEAL_REQUESTS_COUNT_PRIOR_TO_WEBSITE = 15_000
    GROCERY_REQUESTS_COUNT_PRIOR_TO_WEBSITE = 1_988

    @property
    def extra_context(self):
        return {
            'volunteers_lower_bound': 500,
            'meal_requests_count': self.MEAL_REQUESTS_COUNT_PRIOR_TO_WEBSITE + MealRequest.objects.count(),
            'grocery_requests_count': self.GROCERY_REQUESTS_COUNT_PRIOR_TO_WEBSITE + GroceryRequest.objects.count(),
        }


class MediaView(TemplateView):
    template_name = "public/media.html"
    extra_context = {
        "stories": sorted([
            {
                'title': 'Food Justice, Sovereignty, & Security',
                'author': "The People's Pantry",
                'date': date.fromisoformat('2021-03-05'),
                'link': 'https://www.youtube.com/watch?v=DR6SMDL4jYo',
                'image': 'media/food-justice-panel.png',
                'alt_text': 'Several people on a video conference call.',
                'outlet': 'YouTube'
            },
            {
                'title': "The People's Pantry in Toronto provides free home-cooked meals to those in need",
                'author': 'Olivia Little',
                'date': date.fromisoformat('2021-01-11'),
                'link': 'https://www.blogto.com/eat_drink/2021/01/peoples-pantry-toronto-provides-free-home-cooked-meals-those-need/',
                'image': 'media/blogto.png',
                'alt_text': 'A delivery volunteer pointing to a trunk full of meal deliveries.',
                'outlet': 'BlogTO'
            },
            {
                'title': 'The Peoples Pantry is Helping Combat Food Insecurity',
                'author': 'Stella Acquisto',
                'date': date.fromisoformat('2020-07-28'),
                'link': 'https://toronto.citynews.ca/video/2020/07/28/peoples-pantry-helping-combat-food-insecurity/#:~:text=combat%20food%20insecurity',
                'image': 'media/citynews-1.jpg',
                'alt_text': 'A knife dicing onions on a cutting board.',
                'outlet': 'CityNews Toronto'
            },
            {
                'title': 'Food is Love: Volunteers look to continue feeding Toronto with The People’s Pantry',
                'author': 'Lyndsay Morrison',
                'date': date.fromisoformat('2020-10-14'),
                'link': 'https://toronto.ctvnews.ca/food-is-love-volunteers-look-to-continue-feeding-toronto-with-the-people-s-pantry-1.5145374',
                'image': 'media/citynews-2.jpg',
                'alt_text': 'A news anchor standing in front of the CTV logo.',
                'outlet': 'CityNews Toronto'
            },
            {
                'title': 'The Exception as the Rule: Toronto’s social reproduction organizing in the age of COVID-19',
                'author': 'Lina Nasr, El Hag Ali, and Olena Lyubchienko',
                'date': date.fromisoformat('2020-10-14'),
                'link': 'https://spectrejournal.com/the-exception-as-the-rule/',
                'image': 'media/spectre.jpg',
                'alt_text': 'A photo of a public protest.',
                'outlet': 'Spectre'
            },
            {
                'title': 'People’s Pantry and creating inclusive spaces for migrants during the pandemic (PDF).',
                'author': 'Dominik Formanowicz',
                'date': date.fromisoformat('2020-11-03'),
                'link': 'https://www.ryerson.ca/content/dam/centre-for-immigration-and-settlement/RCIS/publications/spotlightonmigration/2020_3_Formanowicz_Dominik_People\'s_Pantry_and_creating_inclusive_spaces_for_migrants_during_the_pandemic.pdf',
                'image': 'media/ryerson.jpg',
                'alt_text': 'An abstract image of the world.',
                'outlet': 'Ryerson’s spotlight on migration'
            },
            {
                'title': 'Sociology students build grassroots volunteer-run initiative to help those in need during COVID-19 pandemic.',
                'author': 'Sherri Klassen',
                'date': date.fromisoformat('2020-04-24'),
                'link': 'https://sociology.utoronto.ca/sociology-students-build-grassroots-volunteer-run-initiative-to-help-those-in-need-during-covid-19-pandemic/',
                'image': 'media/utoronto.jpg',
                'alt_text': 'A variety of pantry foods like flour, oats, and spices.',
                'outlet': 'University of Toronto'
            },
            {
                'title': 'The People’s Pantry Gives Free Food to Torontonians Experiencing Food Insecurity.',
                'author': 'Al Donato',
                'date': date.fromisoformat('2020-06-03'),
                'link': 'http://www.huffingtonpost.ca/entry/peoples-pantry-free-food-toronto_ca_5ed163a2c5b64d62dd502851',
                'image': 'media/huffpo.jpg',
                'alt_text': 'Two volunteers sitting with the meal they have cooked and packaged.',
                'outlet': 'HuffPo Canada'
            },
            {
                'title': 'Grad student addresses food insecurity in Ontario as co-founder of a grassroots community initiative.',
                'author': 'Stephanie Shaw',
                'date': date.fromisoformat('2020-08-13'),
                'link': 'https://yfile.news.yorku.ca/2020/08/13/laps-student-addresses-food-insecurity-in-ontario-with-grassroots-community-initiative-note-use-they-their-pronouns/',
                'image': 'media/yfile.jpg',
                'alt_text': 'Two of our co-founders sitting in front of a trunk full of grocery bundles.',
                'outlet': 'York University yFile'
            },
            {
                'title': 'Reasons to Love Toronto. No. 1: Because our home chefs are feeding the hungry',
                'author': 'Caroline Aksich',
                'date': date.fromisoformat('2020-10-20'),
                'link': 'https://torontolife.com/city/reasons-to-love-toronto/no-1-because-our-home-chefs-are-feeding-the-hungry/',
                'image': 'media/torontolife.jpg',
                'alt_text': 'One of our co-founders sitting in their kitchen and smiling.',
                'outlet': 'Toronto Life'
            },
            {
                'title': 'Covid-19: Food Justice and Mutual Aid in the Pandemic (Webinar)',
                'author': '',
                'date': date.fromisoformat('2020-05-19'),
                'link': 'https://www.facebook.com/110190900641866/videos/2779922052293971',
                'image': 'media/mutualaid.jpg',
                'alt_text': 'Four faces in a video conference call.',
                'outlet': 'Toronto/Tkaronto Mutual Aid'
            },
            {
                'title': 'Organizing During a Pandemic: Lessons for the Left (Webinar)',
                'author': '',
                'date': date.fromisoformat('2020-06-23'),
                'link': 'https://www.youtube.com/watch?v=s2uw5GWrTKI',
                'image': 'media/sis.jpg',
                'alt_text': 'Several faces in a video conference call.',
                'outlet': 'SIS Salon'
            },
        ], key=lambda story: story['date'], reverse=True)
    }


class AboutView(TemplateView):
    template_name = "public/about.html"
    TESTIMONIAL_PHOTOS = [
        {
            "source": "testimonials/crystal.png",
            "alt_text": "Testimonial from Crystal: The work at TPP is centred on showing solidarity with our community and combatting food insecurity, a concern that has become even more pressing with the ongoing pandemic. Please consider donating, or volunteering with one of our teams to support the Pantry and join our mission!",
        },
        {
            "source": "testimonials/jan.png",
            "alt_text": "Testimonial from Jan: For the past several months, I was involved with coordinating grocery care packages and currently am assisting with developing a community cookbook filled with delicious and affordable recipes created by our volunteers. VOlunteering with the People's Pantry Toronto has been one of the most inspiring and fulfilling experiences, and I am grateful for having the opportunity to work with such an inclusive and diverse organization! If you are looking for ways to help our mission, please consider donating or volunteering with us, and spreading awareness on food security!",
        },
        {
            "source": "testimonials/liz.png",
            "alt_text": "Testimonial from Liz: I volunteer with the People's Pantry to use the resources that I have to support the people in my community. I know that if I needed it, the People's Pantry would be there for me too.",
        },
        {
            "source": "testimonials/wanyi.png",
            "alt_text": "Testimonial from Wanyi: THe pandemic has exacerbated food insecurity in our communities, and volunteering with TPP is the direct way to help people in need. We help because we care. Come join or donate today so we can secure our communities and deal with the crisis together.",
        },
    ]
    VOLUNTEER_PHOTOS = [
        "photos/chef_volunteers/img-20210402-wa0000.jpg",
        "photos/chef_volunteers/img_2398.jpg",
        "photos/chef_volunteers/image_from_ios-42.jpg",
        "photos/chef_volunteers/img_2399.jpg",
        "photos/chef_volunteers/img_2416.jpg",
        "photos/chef_volunteers/20210207_092201.jpg",
        "photos/chef_volunteers/img_2417.jpg",
        "photos/chef_volunteers/IMG_20210125_122959359.jpg",
        "photos/chef_volunteers/20210127_084539.jpg",
        "photos/chef_volunteers/img_2411.jpg",
        "photos/chef_volunteers/img_2405.jpg",
        "photos/chef_volunteers/img-20210402-wa0004.jpg",
        "photos/chef_volunteers/image_from_ios-4.jpg",
        "photos/chef_volunteers/IMG_2067.JPG",
        "photos/chef_volunteers/1275ba35-e885-4d59-9ec7-6e81d96431c6_1_105_c.jpeg",
        "photos/chef_volunteers/IMG_53871.jpg",
        "photos/chef_volunteers/IMG_2065.JPG",
        "photos/chef_volunteers/image_from_ios-36.jpg",
        "photos/chef_volunteers/image_from_ios-22.jpg",
        "photos/chef_volunteers/IMG_10791.jpg",
        "photos/chef_volunteers/img_2851.jpg",
        "photos/chef_volunteers/image7.jpeg",
        "photos/chef_volunteers/img_2263.jpg",
        "photos/chef_volunteers/image_from_ios-27.jpg",
        "photos/chef_volunteers/image_from_ios-3.jpg",
        "photos/chef_volunteers/img_2671.jpg",
        "photos/chef_volunteers/IMG_20210227_123814_400.jpg",
        "photos/chef_volunteers/image_from_ios-19.jpg",
        "photos/chef_volunteers/img_2260.jpg",
        "photos/chef_volunteers/img_2880.jpg",
        "photos/chef_volunteers/img_2325.jpg",
        "photos/chef_volunteers/IMG_20210324_090837_207.jpg",
        "photos/chef_volunteers/img_2332.jpg",
        "photos/chef_volunteers/img_2326.jpg",
        "photos/chef_volunteers/IMG_2247.JPG",
        "photos/chef_volunteers/img_2333.jpg",
        "photos/chef_volunteers/img_2455.jpg",
        "photos/chef_volunteers/img_2451.jpg",
        "photos/chef_volunteers/img_2337.jpg",
        "photos/chef_volunteers/img_2257.jpg",
        "photos/chef_volunteers/IMG_2068.jpg",
        "photos/chef_volunteers/img_2322.jpg",
        "photos/chef_volunteers/img_2320.jpg",
        "photos/chef_volunteers/img_2334.jpg",
        "photos/chef_volunteers/20200928_172633.jpg",
        "photos/chef_volunteers/img_2420.jpg",
        "photos/chef_volunteers/20210204_152223.jpg",
        "photos/chef_volunteers/image-1.png",
        "photos/chef_volunteers/img_2423.jpg",
        "photos/chef_volunteers/image_from_ios-59.jpg",
        "photos/chef_volunteers/image3.jpeg",
        "photos/delivery_volunteers/tppmaximg_3163.jpg",
        "photos/delivery_volunteers/tppimg_3167.jpg",
        "photos/delivery_volunteers/20210109_110836.jpg",
        "photos/delivery_volunteers/20201104_192418.jpg",
        "photos/delivery_volunteers/20210124_161154.jpg",
        "photos/delivery_volunteers/20210322_164028.jpg",
        "photos/delivery_volunteers/img_20210327_155559.jpg",
        "photos/delivery_volunteers/IMG_2516.JPG",
        "photos/delivery_volunteers/img_2851.jpg",
        "photos/delivery_volunteers/20210201_164929.jpg",
        "photos/delivery_volunteers/IMG_2492.JPG",
        "photos/delivery_volunteers/20210321_154951.jpg",
        "photos/delivery_volunteers/IMG_2490.JPG",
        "photos/delivery_volunteers/20210124_155001.jpg",
        "photos/delivery_volunteers/20210125_163325.jpg",
        "photos/delivery_volunteers/20210321_161025.jpg",
        "photos/delivery_volunteers/People_s Pantry delivery.jpg",
        "photos/delivery_volunteers/20210131_155054.jpg",
        "photos/delivery_volunteers/IMG_2340.JPG",
        "photos/delivery_volunteers/img_2341.jpg",
        "photos/organizers/yann-eli.jpg",
        "photos/organizers/jade.jpg",
        "photos/organizers/michelle.jpg",
        "photos/organizers/andrea.jpg",
    ]

    @property
    def extra_context(self):
        return {
            'testimonials': self.TESTIMONIAL_PHOTOS,
            'photos': random.sample(self.VOLUNTEER_PHOTOS, k=12),
        }


class RecipesView(TemplateView):
    template_name = "public/recipes.html"
