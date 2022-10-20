CREATE SCHEMA bot;

CREATE TABLE IF NOT EXISTS bot.subject (
	"id" serial NOT NULL,
	"name" varchar(255) NOT NULL,
	CONSTRAINT "subject_pk" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS bot.teacher (
	"id" serial NOT NULL,
	"full_name" varchar(255) NOT NULL,
	"subject" int NOT NULL REFERENCES bot.subject(id),
	CONSTRAINT "teacher_pk" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS bot.timetable (
	"id" serial NOT NULL,
	"day" smallint NOT NULL,
	"subject" int NOT NULL REFERENCES bot.subject(id),
	"room_number" int NOT NULL,
	"start_time" TIME NOT NULL,
	CONSTRAINT "timetable_pk" PRIMARY KEY ("id")
);

-- Тестовые данные

INSERT INTO
	bot.subject (id, name)
VALUES
	(1, 'Вычислительная техника'), (2, 'Высшая математика'),
	(3, 'Философия'), (4, 'Введение в информационные технологии'),
	(5, 'Компьютерная графика'), (6, 'Социология'),
	(7, 'Иностранный язык'), (8, 'Физическая культура и спорт'),
	(9, 'Алгебра и геометрия')
;

INSERT INTO
	bot.teacher (id, full_name, subject)
VALUES
	(1, 'Изотова А.А.', 1), (2, 'Изотова А.А.', 2),
	(3, 'Девайкин И.А.', 3), (4, 'Изотова А.А', 4),
	(5, 'Рывлина А.А.', 5), (6, 'Артамонова Я.С.', 6),
	(7, 'Мальцева С.Н.', 7), (8, 'Горячева Н.Н.', 8),
	(9, 'Изотова А.А.', 9)
;

INSERT INTO
	bot.timetable (day, subject, room_number, start_time)
VALUES
	(1, 1, 518, '11:20'), (1, 1, 520, '13:10'),
	(2, 2, 406, '9:30'), (2, 3, 131, '11:20'), (2, 4, 515, '13:10'), (2, 5, 223, '15:25'),
	(3, 6, 336, '9:30'), (3, 7, 412, '11:20'), (3, 8, 212, '13:10'),
	(4, 4, 344, '15:25'), (4, 4, 456, '17:15'),
	(5, 6, 344, '9:30'), (5, 8, 212, '11:20'), (5, 9, 406, '13:10'), (5, 1, 302, '15:25')
;