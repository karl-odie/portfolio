import datetime
import math
import uuid
from collections.abc import Iterable

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from pytcx import parse_to_activities


def average(*args) -> float:
    return sum(args) / len(args)


def date_array(start, end) -> list[datetime.datetime]:
    return [(start + datetime.timedelta(days=i)) for i in range((end - start).days + 1)]


def delta_minutes(new: datetime.datetime, old: datetime.datetime) -> float:
    return (new - old).total_seconds() / 60.0


def heart_rate_reserve(
    average_heart_rate: int,
    minimum_heart_rate: int,
    heart_reserve: int,
) -> float:
    return min(max((average_heart_rate - minimum_heart_rate) / heart_reserve, 0), 1)


def height_coordinate(value, average_value, max_range, height) -> float:
    return (height * (1 - (value - average_value) / max_range)) - (height / 2)


def range_and_average(iterable) -> tuple[float, float]:
    max_value = max(iterable)
    min_value = min(iterable)
    range_value = max_value - min_value
    return range_value, average(max_value, min_value)


def width_coordinate(value, average_value, max_range, width) -> float:
    return (width * (value - average_value) / max_range) + (width / 2)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    minimum_heart_rate = models.IntegerField(default=60)
    maximum_heart_rate = models.IntegerField(default=190)

    MALE = "M"
    FEMALE = "F"
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=MALE,
    )

    def __str__(self):
        return f"Profile for {self.user}"

    def heart_rate_reserve(self):
        return self.maximum_heart_rate - self.minimum_heart_rate

    def percent_of_heart_rate_reserve(self, heart_rate):
        return max(
            (heart_rate - self.minimum_heart_rate) / self.heart_rate_reserve(),
            0,
        )

    def save(self, *args, **kwargs):
        self.minimum_heart_rate = max(1, self.minimum_heart_rate)
        self.maximum_heart_rate = max(
            self.maximum_heart_rate,
            self.minimum_heart_rate + 1,
        )
        super().save(*args, **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(
    sender,
    instance,
    created,
    **kwargs,
):  # pragma: no cover
    if created:
        Profile.objects.create(user=instance)


class Point(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    activity = models.ForeignKey("Activity", on_delete=models.CASCADE)
    time = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField(default=0.0)

    def __str__(self):
        return f"Point({self.uuid})"


def haversine(a: Point, b: Point) -> float:
    earth_radius = 6371000  # m.
    a_lat = math.radians(a.latitude)
    b_lat = math.radians(b.latitude)
    a_lon = math.radians(a.longitude)
    b_lon = math.radians(b.longitude)

    delta_lat = b_lat - a_lat
    delta_lon = b_lon - a_lon

    half_chord = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(a_lat) * math.cos(b_lat) * math.sin(delta_lon / 2) ** 2
    )
    angular_distance = 2 * math.atan2(math.sqrt(half_chord), math.sqrt(1 - half_chord))
    return earth_radius * angular_distance


class Biometrics(models.Model):
    point = models.OneToOneField(Point, on_delete=models.CASCADE, primary_key=True)
    heart_rate = models.PositiveSmallIntegerField(null=True, blank=True, default=None)
    cadence = models.PositiveSmallIntegerField(null=True, blank=True, default=None)

    def __str__(self):
        return f"Biometrics({self.point})"


class Activity(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    time = models.DateTimeField()
    distance = models.FloatField(null=True, blank=True, default=None)
    duration = models.FloatField(null=True, blank=True, default=None)
    elevation = models.PositiveIntegerField(null=True, blank=True, default=None)
    trimp = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        ordering = ["-time"]

    def __str__(self):
        return f"{self.name} - {self.time}"

    def points_with_heart_rate(self) -> Iterable[Point]:
        return (
            self.point_set.select_related("biometrics")
            .filter(biometrics__heart_rate__isnull=False)
            .order_by("time")
        )

    def delta_trimp(
        self,
        current_time: datetime.datetime,
        last_time: datetime.datetime,
        current_heart_rate: int,
        last_heart_rate: int,
    ) -> float:
        exponent = 1.92 if self.owner.profile.gender == "M" else 1.67
        minutes = delta_minutes(current_time, last_time)
        average_heart_rate = average(current_heart_rate, last_heart_rate)
        reserve = self.owner.profile.percent_of_heart_rate_reserve(average_heart_rate)
        return minutes * reserve * 0.64 * math.exp(exponent * reserve)

    def calculate_trimp(self) -> float | None:
        trimp = 0.0
        last_point: Point | None = None
        for point in self.points_with_heart_rate():
            if last_point is not None:
                trimp += self.delta_trimp(
                    point.time,
                    last_point.time,
                    point.biometrics.heart_rate,
                    last_point.biometrics.heart_rate,
                )
            last_point = point
        return trimp or None

    def point_stream(self) -> Iterable[Point]:
        return self.point_set.order_by("time")

    def point_stream_with_biometrics(self) -> Iterable[Point]:
        return self.point_set.select_related("biometrics").order_by("time")

    def adjusted_track(self) -> list[tuple[float, float]]:
        track = self.point_stream()
        max_latitude = max(a.latitude for a in track)
        longitude_factor = math.cos(math.radians(max_latitude))
        return [(a.latitude, a.longitude * longitude_factor) for a in track]

    def svg_points(self, width=30, height=30) -> list[tuple[float, float]]:
        track = self.adjusted_track()
        latitude_range, average_latitude = range_and_average([a[0] for a in track])
        longitude_range, average_longitude = range_and_average([a[1] for a in track])
        max_range = max([longitude_range, latitude_range])
        return [
            (
                width_coordinate(a[1], average_longitude, max_range, width),
                height_coordinate(a[0], average_latitude, max_range, height),
            )
            for a in track
        ]

    def svg_points_xy(self, width=30, height=30) -> list[dict[str, float]]:
        return [
            {"x": a[0], "y": a[1]} for a in self.svg_points(width=width, height=height)
        ]

    def display_distance(self, unit="km") -> float:
        distance = self.distance or 0.0
        if unit == "km":
            return distance / 1000.0
        return distance

    def duration_as_string(self) -> str:
        duration = self.duration or 0
        total_seconds = int(duration)
        total_minutes = int(total_seconds // 60)
        hours = int(total_minutes // 60)
        minutes = total_minutes - (60 * hours)
        seconds = total_seconds - (60 * total_minutes)
        if hours:
            return f"{hours}:{minutes:0>2}:{seconds:0>2}"
        return f"{minutes}:{seconds:0>2}"

    def average_pace(self) -> float:
        distance = self.display_distance()
        if distance == 0:
            pace = 0
        else:
            pace = (self.duration / 60.0) / distance
        return pace

    def average_pace_as_string(self) -> str:
        pace = self.average_pace()
        minutes = int(pace)
        seconds = int((pace - minutes) * 60)
        return f"{minutes}:{seconds:0>2}"

    def has_heart_rate(self) -> bool:
        return self.point_set.filter(biometrics__heart_rate__isnull=False).count() > 0

    @staticmethod
    def geo_line(index: int, new: Point, old: Point, rolling_distance: float):
        delta_distance = haversine(new, old)
        rolling_distance += delta_distance
        elapsed = abs((new.time - old.time).total_seconds())
        speed = delta_distance / elapsed
        line = {
            "type": "Feature",
            "properties": {
                "id": index,
                "elevation": new.altitude,
                "speed": speed,
                "distance": rolling_distance,
                "cadence": new.biometrics.cadence,
                "heart_rate": new.biometrics.heart_rate,
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        old.longitude,
                        old.latitude,
                    ],
                    [
                        new.longitude,
                        new.latitude,
                    ],
                ],
            },
        }
        return line, rolling_distance

    @staticmethod
    def geo_point(name, point):
        return {
            "type": "Feature",
            "properties": {
                "id": name,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    point.longitude,
                    point.latitude,
                ],
            },
        }

    def geo_json(self) -> list[dict]:
        data = []
        points = list(self.point_stream_with_biometrics())
        distance = 0
        for index, point in enumerate(points):
            if index > 0:
                previous_point = points[index - 1]
                line_data, distance = self.geo_line(
                    index - 1,
                    point,
                    previous_point,
                    distance,
                )
                data.append(line_data)
        first = points[0]
        last = points[-1]
        data.append(self.geo_point("progress", first))
        data.append(self.geo_point("start", first))
        data.append(self.geo_point("stop", last))
        return data

    @classmethod
    def trimp_activities(cls, user, start=None, end=None):
        activities = cls.objects.filter(owner=user).filter(trimp__isnull=False)
        if start is None:
            start = activities.order_by("time").first().time.date()
        else:
            activities = activities.filter(time__gte=start)
        if end is None:
            end = activities.order_by("time").last().time.date()
        else:
            activities = activities.filter(time__lte=end)
        return activities, start, end

    @classmethod
    def load_from_tcx_content(cls, user: AbstractUser, text: str) -> None:
        activities = parse_to_activities(text)
        created = []
        for tcx_activity in activities:
            duration = (tcx_activity.stop() - tcx_activity.start()).total_seconds()
            start = tcx_activity.start().isoformat()
            default_name = f"{tcx_activity.sport} - {start}"
            tcx_name = tcx_activity.name.strip() or default_name
            activity = Activity(
                owner=user,
                name=tcx_name,
                time=tcx_activity.start(),
                duration=duration,
            )
            activity.save()
            rolling_distance = 0.0
            rolling_elevation = 0.0
            point_number = 0
            last_point: Point | None = None
            for lap in tcx_activity.laps:
                for tcx_point in lap.points:
                    point_number += 1
                    point = Point(
                        activity=activity,
                        time=tcx_point.time,
                        latitude=tcx_point.latitude,
                        longitude=tcx_point.longitude,
                        altitude=tcx_point.altitude,
                    )
                    point.save()
                    if last_point is not None:
                        rolling_distance += haversine(point, last_point)
                        rolling_elevation += max(
                            0,
                            (point.altitude - last_point.altitude),
                        )
                    last_point = point
                    biometrics = Biometrics(
                        point=point,
                        heart_rate=tcx_point.heart_rate,
                        cadence=tcx_point.cadence,
                    )
                    biometrics.save()
            activity.distance = rolling_distance
            activity.elevation = rolling_elevation
            activity.trimp = activity.calculate_trimp()
            activity.save()
            created.append(activity)
        return created


class TrainingStressBalance:
    def __init__(self, start, end):
        self.data = {k: TrainingStressBalancePoint(k) for k in date_array(start, end)}

    def insert(self, activity):
        self.data[activity.time.date()].trimp += activity.trimp or 0

    def inflate(self):
        last_point = None
        for index, point in enumerate(self.points()):
            if index != 0:
                point.increment_fitness(last_point)
            last_point = point

    def points(self):
        return sorted(self.data.values(), key=lambda h: h.date)

    @classmethod
    def history_for_user(cls, user, start=None, end=None):
        activities, start, end = Activity.trimp_activities(user, start, end)
        balance = cls(start, end)
        for activity in activities:
            balance.insert(activity)
        balance.inflate()
        return balance.points()


class TrainingStressBalancePoint:
    def __init__(self, date):
        self.date = date
        self.trimp = 0
        self.fitness = 0
        self.fatigue = 0
        self.form = 0

    def increment_fitness(self, last_point):
        self.fitness = last_point.fitness + (self.trimp - last_point.fitness) * (
            1.0 - math.exp(-1.0 / 42.0)
        )
        self.fatigue = last_point.fatigue + (self.trimp - last_point.fatigue) * (
            1.0 - math.exp(-1.0 / 7.0)
        )
        self.form = self.fitness - self.fatigue
