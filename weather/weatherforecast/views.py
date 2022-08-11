import json
import datetime

import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, TemplateView

from .models import *
from .utils import WeatherMixin


class RegionListView(ListView):
    allow_empty = False
    model = RegionsModel
    template_name = 'weatherforecast/regions.html'
    context_object_name = 'regions'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['abc'] = list('АБВДЕЗИКЛМНОПРСТУХЧЯ')
        return context

    def get_queryset(self):
        return RegionsModel.objects.all()


class SingleRegionView(ListView):
    model = CitiesModel
    slug_url_kwarg = 'reg_slug'
    template_name = 'weatherforecast/region_cities.html'
    context_object_name = 'cities'

    def get_queryset(self):
        return CitiesModel.objects.filter(reg__slug=self.kwargs['reg_slug']).all()


class WeatherNowView(WeatherMixin, TemplateView):
    template_name = 'weatherforecast/weather_now.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = get_object_or_404(CitiesModel, slug=self.kwargs['city_slug'])
        context['weather'] = self.current_weather(context['city'])
        context['weather_list'] = self.five_by_day_weather(context['city'])
        context['region'] = context['city'].reg
        return context


class WeatherDayView(WeatherMixin, TemplateView):
    template_name = 'weatherforecast/weather_day.html'

    def chose_days(self, weather_list):
        num = self.kwargs['day_num']
        if num == 0:
            response_list = [weather_list[i] for i in range(3)]
        elif num == 4:
            response_list = [weather_list[i] for i in range(2, 5)]
        else:
            response_list = [weather_list[i] for i in range(num - 1, num + 2)]

        return response_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = get_object_or_404(CitiesModel, slug=self.kwargs['city_day_slug'])
        context['weather'] = self.five_by_hour_weather(context['city'])[self.kwargs['day_num']]
        context['three_day_weather'] = self.chose_days(self.five_by_day_weather(context['city']))

        return context


class FiveDayView(WeatherMixin, TemplateView):
    template_name = 'weatherforecast/five_days.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = get_object_or_404(CitiesModel, slug=self.kwargs['city_five_slug'])
        context['weather'] = self.five_by_hour_weather(context['city'])

        return context
