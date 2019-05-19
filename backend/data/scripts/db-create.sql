CREATE TABLE `WAGONS`
(
  `wagon_id`       TEXT NOT NULL PRIMARY KEY UNIQUE,
  `last_camera_id` INTEGER,
  `last_timestamp` TEXT,
  `latitude`       FLOAT,
  `longitude`      FLOAT
);

CREATE TABLE `HISTORY`
(
  `wagon_id`  INTEGER NOT NULL,
  `camera_id` INTEGER   NOT NULL,
  `timestamp` TEXT   NOT NULL
);

CREATE TABLE `CAMERAS`
(
  `camera_id`   INTEGER NOT NULL PRIMARY KEY UNIQUE,
  `description` TEXT    NOT NULL,
  `connected`   TEXT    DEFAULT 'false'
);