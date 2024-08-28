import datetime

import factory
import factory.fuzzy

from portfolio.fitness.models import Activity
from portfolio.fitness.models import Biometrics
from portfolio.fitness.models import Point
from portfolio.fitness.models import Profile
from portfolio.users.models import User


class OwnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.fuzzy.FuzzyText(suffix="@example.com")


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(OwnerFactory)


class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Activity

    owner = factory.SubFactory(OwnerFactory)
    name = factory.fuzzy.FuzzyText(length=64)
    time = factory.fuzzy.FuzzyDateTime(
        start_dt=datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC),
    )


class PointFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Point

    activity = factory.SubFactory(ActivityFactory)
    time = factory.fuzzy.FuzzyDateTime(
        start_dt=datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC),
    )
    latitude = factory.fuzzy.FuzzyFloat(-90.0, 90.0)
    longitude = factory.fuzzy.FuzzyFloat(-180.0, 180.0)


class BiometricsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Biometrics

    point = factory.SubFactory(PointFactory)
