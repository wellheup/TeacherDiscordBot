ALTER TABLE syllabus ADD COLUMN newUniqueId SERIAL;
ALTER TABLE syllabus DROP COLUMN 'uniqueId';
ALTER TABLE syllabus RENAME COLUMN newUniqueId TO 'uniqueId';

ALTER TABLE syllabus RENAME COLUMN "uniqueId" TO "unique_id";
ALTER TABLE syllabus RENAME COLUMN "isCompleted" TO "is_ompleted";
ALTER TABLE syllabus RENAME COLUMN "addedBy" TO "added_by";
ALTER TABLE syllabus RENAME COLUMN "numInSeries" TO "num_in_series";
ALTER TABLE syllabus RENAME COLUMN "isExtraCredit" TO "is_extra_credit";
ALTER TABLE syllabus RENAME COLUMN "dateCompleted" TO "date_completed";
ALTER TABLE syllabus RENAME COLUMN "dateAdded" TO "date_added";

SELECT
	column_name,
	data_type,
	character_maximum_length,
	is_nullable,
	column_default
FROM
	information_schema.columns
WHERE
	table_name = 'syllabus'