EXPLAIN ANALYSE
(SELECT "notes_note"."id",
       "notes_note"."user_id",
       "notes_note"."title",
       "notes_note"."updated_at",
       SUBSTRING("notes_note"."content", 1, 200) AS "short_content",
       "accounting_user"."id",
       "accounting_user"."username"
FROM "notes_note"
         INNER JOIN "accounting_user" ON ("notes_note"."user_id" = "accounting_user"."id")
WHERE "notes_note"."search_vector" @@ websearch_to_tsquery('search text')
ORDER BY 6 DESC, "notes_note"."created_at" DESC)