-- Note.objects.all()
SELECT "notes_note"."id",
       "notes_note"."user_id",
       "notes_note"."title",
       "notes_note"."content",
       "notes_note"."created_at",
       "notes_note"."updated_at"
FROM "notes_note";


-- Note.objects.filter(user_id=1)
SELECT "notes_note"."id",
       "notes_note"."user_id",
       "notes_note"."title",
       "notes_note"."content",
       "notes_note"."created_at",
       "notes_note"."updated_at"
FROM "notes_note"
WHERE "notes_note"."user_id" = 1;


-- Note.objects.filter(title="test")
SELECT "notes_note"."id",
       "notes_note"."user_id",
       "notes_note"."title",
       "notes_note"."content",
       "notes_note"."created_at",
       "notes_note"."updated_at"
FROM "notes_note"
WHERE "notes_note"."title" = 'test';


-- Note.objects.filter(title__contains="test")
SELECT "notes_note"."id",
       "notes_note"."user_id",
       "notes_note"."title",
       "notes_note"."content",
       "notes_note"."created_at",
       "notes_note"."updated_at"
FROM "notes_note"
WHERE "notes_note"."title"::text LIKE '%test%';


-- Note.objects.filter(title__icontains="tEst")
SELECT "notes_note"."id",
       "notes_note"."user_id",
       "notes_note"."title",
       "notes_note"."content",
       "notes_note"."created_at",
       "notes_note"."updated_at"
FROM "notes_note"
WHERE UPPER("notes_note"."title"::text) LIKE UPPER('%tEst%');


-- Note.objects.filter(user=1).select_related("user")[:10]
SELECT "notes_note"."id",
       "notes_note"."user_id",
       "notes_note"."title",
       "notes_note"."content",
       "notes_note"."created_at",
       "notes_note"."updated_at",
       "accounting_user"."id",
       "accounting_user"."password",
       "accounting_user"."last_login",
       "accounting_user"."is_superuser",
       "accounting_user"."username",
       "accounting_user"."first_name",
       "accounting_user"."last_name",
       "accounting_user"."email",
       "accounting_user"."is_staff",
       "accounting_user"."is_active",
       "accounting_user"."date_joined"
FROM "notes_note"
         INNER JOIN "accounting_user" ON ("notes_note"."user_id" = "accounting_user"."id")
WHERE "notes_note"."user_id" = 1 LIMIT 10


-- Note.objects.filter(user=1).select_related("user")[:10].only("id", "title", "content", "updated_at", "user__username")
SELECT "notes_note"."id",
       "notes_note"."user_id",
       "notes_note"."title",
       "notes_note"."content",
       "notes_note"."updated_at",
       "accounting_user"."id",
       "accounting_user"."username",
FROM "notes_note"
         INNER JOIN "accounting_user" ON ("notes_note"."user_id" = "accounting_user"."id")
WHERE "notes_note"."user_id" = 1 LIMIT 10


-- Note.objects.all().annotate(short_content=Substr("content", 1, 10))
SELECT "notes_note"."id",
       "notes_note"."user_id",
       "notes_note"."title",
       "notes_note"."content",
       "notes_note"."created_at",
       "notes_note"."updated_at",
       "notes_note"."image",
       SUBSTRING("notes_note"."content", 1, 10) AS "short_content"
FROM "notes_note"
ORDER BY "notes_note"."created_at" DESC


-- Note.objects.filter(user=request.user)                           # Фильтр пользователя
--     .select_related("user")                                     # JOIN с users
--     .annotate(short_content=Substr("content", 1, 200))          # Уменьшаем длину контента.
--     .order_by("-created_at")[:10]                               # Сортировка и первые 10 заметок
--     .only("id", "title", "updated_at", "user__username")        # Только нужные поля из модели.
SELECT "notes_note"."id",
       "notes_note"."user_id",
       "notes_note"."title",
       "notes_note"."updated_at",
       SUBSTRING("notes_note"."content", 1, 200) AS "short_content",
       "accounting_user"."id",
       "accounting_user"."username"
FROM "notes_note"
         INNER JOIN "accounting_user" ON ("notes_note"."user_id" = "accounting_user"."id")
WHERE "notes_note"."user_id" = 1
ORDER BY "notes_note"."created_at" DESC LIMIT 10


-- from django.db.models.query import Q
-- Note.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))
SELECT "notes_note"."id",
       "notes_note"."user_id",
       "notes_note"."title",
       "notes_note"."content",
       "notes_note"."created_at",
       "notes_note"."updated_at",
       "notes_note"."image"
FROM "notes_note"
WHERE (UPPER("notes_note"."title"::text) LIKE UPPER(%queries.sql%) OR
       UPPER("notes_note"."content"::text) LIKE UPPER(%queries.sql%))
ORDER BY "notes_note"."created_at" DESC
