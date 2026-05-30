-- note = Note.objects.get(id=1)
-- note.tags.all()

SELECT "notes_tag"."id", "notes_tag"."name"
FROM "notes_tag"
         INNER JOIN "notes_note_tags" ON ("notes_tag"."id" = "notes_note_tags"."tag_id")
WHERE "notes_note_tags"."note_id" = 1;

-- Tag.objects.filter(note=1)

SELECT "notes_tag"."id", "notes_tag"."name"
FROM "notes_tag"
         INNER JOIN "notes_note_tags" ON ("notes_tag"."id" = "notes_note_tags"."tag_id")
WHERE "notes_note_tags"."note_id" = 1;


-- note = Note.objects.get(id=1)
-- note.tags.filter(name__icontains="python")

SELECT "notes_tag"."id", "notes_tag"."name"
FROM "notes_tag"
         INNER JOIN "notes_note_tags" ON ("notes_tag"."id" = "notes_note_tags"."tag_id")
WHERE ("notes_note_tags"."note_id" = 1 AND "notes_tag"."name" = 'python');

-- Tag.objects.filter(note=1, name='python')
SELECT "notes_tag"."id", "notes_tag"."name"
FROM "notes_tag"
         INNER JOIN "notes_note_tags" ON ("notes_tag"."id" = "notes_note_tags"."tag_id")
WHERE ("notes_note_tags"."note_id" = 1 AND "notes_tag"."name" = 'python');


-- Note.objects.filter(tags__name="python")
SELECT "notes_note"."id",
       "notes_note"."user_id",
       "notes_note"."title",
       "notes_note"."content",
       "notes_note"."created_at",
       "notes_note"."updated_at",
       "notes_note"."image"
FROM "notes_note"
         INNER JOIN "notes_note_tags" ON ("notes_note"."id" = "notes_note_tags"."note_id")
         INNER JOIN "notes_tag" ON ("notes_note_tags"."tag_id" = "notes_tag"."id")
WHERE "notes_tag"."name" = 'python'
ORDER BY "notes_note"."created_at" DESC
