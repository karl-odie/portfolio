import argparse
from pathlib import Path

from django.core.management.base import BaseCommand

from portfolio.fitness.models import Activity
from portfolio.users.models import User


class Command(BaseCommand):
    help = "Import a TCX file to a user account."

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("user")
        parser.add_argument("parent", type=Path)
        parser.add_argument("pattern", type=str)

    def handle(self, *args, **options):
        user: str = options["user"]
        parent: Path = options["parent"]
        pattern: Path = options["pattern"]
        user_object = User.objects.get(email=user)
        for tcx in parent.glob(pattern):
            self.stdout.write(f"{user_object}: Add {tcx}")
            self.load_tcx(user_object, tcx)

    def load_tcx(self, user_object: User, tcx_path: Path):
        activity = Activity.load_from_tcx_content(
            user_object,
            tcx_path.read_text(encoding="utf-8"),
        )
        self.stdout.write(f"Activity: {activity}")
