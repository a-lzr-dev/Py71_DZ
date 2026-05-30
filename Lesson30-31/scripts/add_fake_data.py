import os
import random
import time

from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from django import setup

setup()

# --------------------------------------------------------------------------------

from notes.models import Note, Tag
from accounting.models import User


def add_user(faker: Faker) -> User:
    return User.objects.create_user(
        username=faker.user_name(),
        email=faker.email(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        password=faker.password(length=12),
    )


def add_tag(faker: Faker) -> Tag:
    return Tag.objects.create(name=faker.word())


def add_note(faker: Faker, user: User, tags: list[Tag]) -> Note:
    note = Note.objects.create(
        title=faker.word(),
        content=faker.paragraph(nb_sentences=600),
        user=user,
    )
    note.tags.set(tags)
    return note


def main():
    faker = Faker("ru_RU")

    users = User.objects.all()
    # for _ in range(10):
    #     users.append(add_user(faker))
    # print("Пользователи добавлены")

    tags: list[Tag] = list(Tag.objects.all())
    # for _ in range(100):
    #     tags.append(add_tag(faker))
    # print("Теги добавлены")

    posts = []
    for user in users:
        for _ in range(10_000):
            selected_tags = list(faker.random_choices(tags, length=random.randint(3, 5)))
            posts.append(add_note(faker, user, selected_tags))
        print(".", end="")
    print()


if __name__ == "__main__":
    time_start = time.perf_counter()
    main()
    end_start = time.perf_counter()
    print(f"Time taken: {end_start - time_start}")
