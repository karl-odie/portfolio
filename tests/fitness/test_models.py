import datetime
import json

import pytest

from portfolio.fitness.models import Activity
from portfolio.fitness.models import Point
from portfolio.fitness.models import Profile
from portfolio.fitness.models import haversine

from .factories import ActivityFactory
from .factories import BiometricsFactory
from .factories import OwnerFactory
from .factories import PointFactory
from .factories import ProfileFactory


def test_profile():
    profile = ProfileFactory.build()
    reserve = profile.heart_rate_reserve()
    assert reserve == 130, reserve
    percent = profile.percent_of_heart_rate_reserve(125)
    assert percent == 0.5, percent
    percent = profile.percent_of_heart_rate_reserve(30)
    assert percent == 0.0, percent


@pytest.mark.django_db
def test_profile_default():
    user = OwnerFactory()
    assert user.profile.minimum_heart_rate == 60
    assert user.profile.maximum_heart_rate == 190


@pytest.mark.django_db
def test_profile_low_max():
    user = OwnerFactory()
    user.profile.minimum_heart_rate = 60
    user.profile.maximum_heart_rate = 55
    user.profile.save()
    profile = Profile.objects.get(user=user)
    assert profile.minimum_heart_rate == 60
    assert profile.maximum_heart_rate == 61


@pytest.mark.django_db
def test_profile_zero():
    user = OwnerFactory()
    user.profile.minimum_heart_rate = 0
    user.profile.maximum_heart_rate = 0
    user.profile.save()
    profile = Profile.objects.get(user=user)
    assert profile.minimum_heart_rate == 1
    assert profile.maximum_heart_rate == 2


def test_activity_string():
    activity = ActivityFactory.build(
        name="Test Name",
        time=datetime.datetime(2023, 5, 3, 14, 52, 31, tzinfo=datetime.UTC),
    )
    assert str(activity) == "Test Name - 2023-05-03 14:52:31+00:00", str(activity)


@pytest.mark.django_db
def test_points_with_heart_rate():
    activity = ActivityFactory()
    point_1 = PointFactory(
        activity=activity,
        time=datetime.datetime(2023, 5, 3, 14, 52, 31, tzinfo=datetime.UTC),
    )
    point_2 = PointFactory(
        activity=activity,
        time=datetime.datetime(2023, 5, 3, 14, 53, 31, tzinfo=datetime.UTC),
    )
    PointFactory(
        activity=activity,
        time=datetime.datetime(2023, 5, 3, 14, 54, 31, tzinfo=datetime.UTC),
    )
    point_4 = PointFactory(
        activity=activity,
        time=datetime.datetime(2023, 5, 3, 14, 54, 31, tzinfo=datetime.UTC),
    )

    BiometricsFactory(point=point_1, heart_rate=150)
    BiometricsFactory(point=point_2, heart_rate=None)
    BiometricsFactory(point=point_4, heart_rate=160)

    heart_rate_points = list(activity.points_with_heart_rate())
    assert heart_rate_points == [point_1, point_4], heart_rate_points


@pytest.mark.django_db
def test_delta_trimp():
    activity: Activity = ActivityFactory()
    start = datetime.datetime(2023, 5, 3, 14, 53, 00, tzinfo=datetime.UTC)
    end = datetime.datetime(2023, 5, 3, 14, 57, 00, tzinfo=datetime.UTC)
    trimp = round(activity.delta_trimp(start, end, 170, 150), 5)
    expected = -8.62415
    assert trimp == expected, trimp
    activity.owner.profile.gender = "F"
    trimp = round(activity.delta_trimp(start, end, 170, 150), 5)
    expected = -7.11538
    assert trimp == expected, trimp


@pytest.mark.django_db
def test_calculate_trimp():
    activity: Activity = ActivityFactory()
    BiometricsFactory(point__activity=activity)
    BiometricsFactory(point__activity=activity)
    BiometricsFactory(point__activity=activity)
    # No heartbeat.
    assert activity.calculate_trimp() is None
    assert activity.has_heart_rate() is False
    BiometricsFactory(
        point__activity=activity,
        heart_rate=150,
        point__time=datetime.datetime(2023, 5, 3, 14, 57, 0, tzinfo=datetime.UTC),
    )
    BiometricsFactory(
        point__activity=activity,
        heart_rate=160,
        point__time=datetime.datetime(2023, 5, 3, 14, 57, 5, tzinfo=datetime.UTC),
    )
    BiometricsFactory(
        point__activity=activity,
        heart_rate=170,
        point__time=datetime.datetime(2023, 5, 3, 14, 57, 10, tzinfo=datetime.UTC),
    )
    assert activity.has_heart_rate() is True
    trimp = round(activity.calculate_trimp(), 5)
    expected = 0.36165
    assert trimp == expected, trimp


@pytest.mark.django_db
def test_track():
    activity: Activity = ActivityFactory()
    point_3 = PointFactory(
        activity=activity,
        latitude=42,
        longitude=-22,
        time=datetime.datetime(2023, 5, 3, 14, 59, 00, tzinfo=datetime.UTC),
    )
    point_1 = PointFactory(
        activity=activity,
        latitude=40,
        longitude=-20,
        time=datetime.datetime(2023, 5, 3, 14, 57, 00, tzinfo=datetime.UTC),
    )
    point_2 = PointFactory(
        activity=activity,
        latitude=41,
        longitude=-21,
        time=datetime.datetime(2023, 5, 3, 14, 58, 00, tzinfo=datetime.UTC),
    )
    track = list(activity.point_stream())
    assert track == [point_1, point_2, point_3], "3 points"
    adjusted_track = activity.adjusted_track()
    assert adjusted_track == [
        (40, -14.862896509547884),
        (41, -15.60604133502528),
        (42, -16.349186160502672),
    ], adjusted_track
    svg = activity.svg_points()
    assert svg == [
        (26.14717238216091, 30.0),
        (14.999999999999973, 15.0),
        (3.8528276178390897, 0.0),
    ], svg


def test_display_distance():
    activity: Activity = ActivityFactory.build(distance=2500)
    km = 2.5
    assert activity.display_distance() == km
    metres = 2500
    assert activity.display_distance(unit="m") == metres


def test_duration_as_string():
    activity: Activity = ActivityFactory.build(duration=4000)
    duration = activity.duration_as_string()
    assert duration == "1:06:40", duration


def test_average_pace():
    activity: Activity = ActivityFactory.build(duration=1800, distance=5000)
    average_pace = activity.average_pace()
    expected = 6.0
    assert average_pace == expected, average_pace
    average_pace_as_string = activity.average_pace_as_string()
    assert average_pace_as_string == "6:00", average_pace_as_string


def test_haversine():
    point_1 = Point(latitude=54.65210884809494, longitude=-3.5566462855786085)
    point_2 = Point(latitude=54.65220347978175, longitude=-3.556569339707494)
    distance = round(haversine(point_1, point_2), 2)
    expected = 11.63
    assert distance == expected, distance


@pytest.mark.django_db
def test_geo_json():
    activity: Activity = ActivityFactory()
    BiometricsFactory(
        point__activity=activity,
        point__time=datetime.datetime(2023, 5, 3, 11, 45, 0, tzinfo=datetime.UTC),
        point__latitude=54.65210884809494,
        point__longitude=-3.5566462855786085,
    )
    BiometricsFactory(
        point__activity=activity,
        point__time=datetime.datetime(2023, 5, 3, 11, 45, 5, tzinfo=datetime.UTC),
        point__latitude=54.65220347978175,
        point__longitude=-3.556569339707494,
    )
    BiometricsFactory(
        point__activity=activity,
        point__time=datetime.datetime(2023, 5, 3, 11, 45, 6, tzinfo=datetime.UTC),
        point__latitude=54.65227992273867,
        point__longitude=-3.5565729439258575,
    )
    BiometricsFactory(
        point__activity=activity,
        heart_rate=150,
        cadence=180,
        point__time=datetime.datetime(2023, 5, 3, 11, 45, 8, tzinfo=datetime.UTC),
        point__latitude=54.65233909897506,
        point__longitude=-3.5566111654043198,
    )
    BiometricsFactory(
        point__activity=activity,
        heart_rate=160,
        cadence=181,
        point__time=datetime.datetime(2023, 5, 3, 11, 45, 9, tzinfo=datetime.UTC),
        point__latitude=54.652375811710954,
        point__longitude=-3.556636730208993,
    )
    BiometricsFactory(
        point__activity=activity,
        heart_rate=170,
        cadence=182,
        point__time=datetime.datetime(2023, 5, 3, 11, 45, 10, tzinfo=datetime.UTC),
        point__latitude=54.6524200681597,
        point__longitude=-3.556660283356905,
    )
    data = activity.geo_json()
    expected = [
        {
            "type": "Feature",
            "properties": {
                "id": 0,
                "elevation": 0.0,
                "speed": 2.32573928071072,
                "distance": 11.6286964035536,
                "cadence": None,
                "heart_rate": None,
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -3.5566462855786085,
                        54.65210884809494,
                    ],
                    [
                        -3.556569339707494,
                        54.65220347978175,
                    ],
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {
                "id": 1,
                "elevation": 0.0,
                "speed": 8.503230698981664,
                "distance": 20.131927102535265,
                "cadence": None,
                "heart_rate": None,
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -3.556569339707494,
                        54.65220347978175,
                    ],
                    [
                        -3.5565729439258575,
                        54.65227992273867,
                    ],
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {
                "id": 2,
                "elevation": 0.0,
                "speed": 3.512242264196969,
                "distance": 27.156411630929203,
                "cadence": 180,
                "heart_rate": 150,
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -3.5565729439258575,
                        54.65227992273867,
                    ],
                    [
                        -3.5566111654043198,
                        54.65233909897506,
                    ],
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {
                "id": 3,
                "elevation": 0.0,
                "speed": 4.401091613595513,
                "distance": 31.557503244524717,
                "cadence": 181,
                "heart_rate": 160,
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -3.5566111654043198,
                        54.65233909897506,
                    ],
                    [
                        -3.556636730208993,
                        54.652375811710954,
                    ],
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {
                "id": 4,
                "elevation": 0.0,
                "speed": 5.149069759621499,
                "distance": 36.706573004146215,
                "cadence": 182,
                "heart_rate": 170,
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -3.556636730208993,
                        54.652375811710954,
                    ],
                    [
                        -3.556660283356905,
                        54.6524200681597,
                    ],
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {
                "id": "progress",
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -3.5566462855786085,
                    54.65210884809494,
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {
                "id": "start",
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -3.5566462855786085,
                    54.65210884809494,
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {
                "id": "stop",
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -3.556660283356905,
                    54.6524200681597,
                ],
            },
        },
    ]
    assert data == expected, json.dumps(data, indent=4)
