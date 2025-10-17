CREATE TABLE testdb.위탁병원현황 (
	연번 INT auto_increment NOT NULL,
	시군구 varchar(8) NOT NULL,
	요양기관명 varchar(32) NOT NULL,
	병상수 INT NOT NULL,
	진료과수 INT NOT NULL,
	전화번호 varchar(16) NOT NULL,
	주소 varchar(64) NOT NULL,
	종별 varchar(4) NOT NULL,
	상세주소 varchar(64) NOT NULL,
	경도 DOUBLE NOT NULL,
	위도 DOUBLE NOT null,
	PRIMARY KEY (연번)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

select * from testdb.위탁병원현황;

CREATE TABLE testdb.위탁병원현황_연도별현황 (
	광역지자체    varchar(4)  NOT NULL,
	2022년12월  int        ,
	2023년12월  int    ,
	2024년12월  int     ,
	
	PRIMARY KEY (광역지자체)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE testdb.위탁병원현황_이용현황 (
    연번 INT auto_increment NOT NULL, 
	yyyymm   varchar(6)    not null  ,
	시군구     varchar(8)    not null ,
	인원       int          not null   ,
	PRIMARY KEY (연번),
    UNIQUE  KEY (시군구)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE testdb.보훈병원_이용현황 (
	연번 INT auto_increment NOT NULL,
    yyyymm   varchar(6)    not null  ,
    보훈병원   varchar(32)  NOT NULL,
	인원      int        ,
	PRIMARY KEY (연번),
    UNIQUE KEY (보훈병원)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;
