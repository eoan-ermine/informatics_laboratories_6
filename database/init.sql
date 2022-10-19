CREATE TABLE "public.subject" (
	"id" serial NOT NULL,
	"name" varchar(255) NOT NULL,
	CONSTRAINT "subject_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "public.teacher" (
	"id" serial NOT NULL,
	"full_name" varchar(255) NOT NULL,
	"subject" int NOT NULL,
	CONSTRAINT "teacher_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "public.timetable" (
	"id" serial NOT NULL,
	"day" smallint NOT NULL,
	"subject" int NOT NULL,
	"room_number" int NOT NULL,
	"start_time" TIME NOT NULL,
	CONSTRAINT "timetable_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

ALTER TABLE "teacher" ADD CONSTRAINT "teacher_fk0" FOREIGN KEY ("subject") REFERENCES "subject"("id");
ALTER TABLE "timetable" ADD CONSTRAINT "timetable_fk0" FOREIGN KEY ("subject") REFERENCES "subject"("id");
