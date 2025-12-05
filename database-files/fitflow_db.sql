DROP DATABASE IF EXISTS fitflow;
CREATE DATABASE IF NOT EXISTS fitflow;
USE fitflow;


DROP TABLE IF EXISTS System_Admin;
CREATE TABLE System_Admin
(
  system_admin_id INT PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name  VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL
);


DROP TABLE IF EXISTS User;
CREATE TABLE User(
  user_id       INT PRIMARY KEY AUTO_INCREMENT,
  email         VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255)        NOT NULL,
  role          ENUM ('admin','trainer','client','analyst') NOT NULL,
  permissions   VARCHAR(255),
  created_by    INT NULL,
  created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_user_created_by
      FOREIGN KEY (created_by)
      REFERENCES System_Admin(system_admin_id)
      ON DELETE SET NULL
      ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Health_Analyst;
CREATE TABLE Health_Analyst(
  analyst_id INT PRIMARY KEY AUTO_INCREMENT,
  user_id    INT NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  last_name  VARCHAR(50) NOT NULL,
  CONSTRAINT fk_analyst_user
     FOREIGN KEY (user_id) REFERENCES User(user_id)
     ON DELETE CASCADE ON UPDATE CASCADE,


  UNIQUE (user_id)
);


DROP TABLE IF EXISTS Trainer;
CREATE TABLE Trainer(
  trainer_id    INT PRIMARY KEY AUTO_INCREMENT,
  user_id       INT NOT NULL,
  first_name    VARCHAR(50) NOT NULL,
  last_name     VARCHAR(50) NOT NULL,
  specialization VARCHAR(100),
  certification VARCHAR(100),


  CONSTRAINT fk_trainer_user
     FOREIGN KEY (user_id) REFERENCES User(user_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  UNIQUE (user_id)
);


DROP TABLE IF EXISTS Client;
CREATE TABLE Client(
  client_id     INT PRIMARY KEY AUTO_INCREMENT,
  user_id       INT NOT NULL,
  first_name    VARCHAR(50) NOT NULL,
  last_name     VARCHAR(50) NOT NULL,
  date_of_birth DATE,
  age           INT, -- derived attribute from date_of_birth
  fitness_level VARCHAR(50),
  goals         VARCHAR(255),
  join_date     DATE,
  CONSTRAINT fk_client_user
     FOREIGN KEY (user_id) REFERENCES User(user_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  UNIQUE (user_id)
);


DROP TABLE IF EXISTS System_Log;
CREATE TABLE System_Log(
  log_id      INT PRIMARY KEY AUTO_INCREMENT,
  user_id     INT NOT NULL,
  action_type VARCHAR(100) NOT NULL,
  description TEXT,
  timestamp   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,


  CONSTRAINT fk_systemlog_user
     FOREIGN KEY (user_id) REFERENCES User(user_id)
     ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Backup_Log;
CREATE TABLE Backup_Log(
  backup_id        INT PRIMARY KEY AUTO_INCREMENT,
  performed_by     INT NOT NULL,   -- system_admin_id
  backup_start     DATETIME NOT NULL,
  backup_end       DATETIME NOT NULL,
  backup_time_mins INT,
  status           ENUM('success','failed','partial') NOT NULL,
  CONSTRAINT fk_backuplog_admin
     FOREIGN KEY (performed_by) REFERENCES System_Admin(system_admin_id)
     ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Health_Metrics;
CREATE TABLE Health_Metrics(
  metric_id           INT PRIMARY KEY AUTO_INCREMENT,
  client_id           INT NOT NULL,
  analyst_id          INT,
  record_date         DATE NOT NULL,
  weight_kg           DECIMAL(5,2),
  height_inches       DECIMAL(4,1),
  bmi                 DECIMAL(4,1),
  body_fat_percentage DECIMAL(4,1),
  heart_rate          INT,
  notes               VARCHAR(500),
  CONSTRAINT fk_metrics_client
     FOREIGN KEY (client_id) REFERENCES Client(client_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_metrics_analyst
     FOREIGN KEY (analyst_id) REFERENCES Health_Analyst(analyst_id)
     ON DELETE SET NULL ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Trainer_Client;
CREATE TABLE Trainer_Client(
  trainer_id INT NOT NULL,
  client_id  INT NOT NULL,
  start_date DATE NOT NULL,
  PRIMARY KEY (trainer_id, client_id, start_date),
  CONSTRAINT fk_tc_trainer
     FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_tc_client
     FOREIGN KEY (client_id) REFERENCES Client(client_id)
     ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Exercise;
CREATE TABLE Exercise(
  exercise_id INT PRIMARY KEY AUTO_INCREMENT,
  name        VARCHAR(100) NOT NULL,
  description TEXT,
  category    VARCHAR(50) NOT NULL
);


DROP TABLE IF EXISTS Workout_Session_Template;
CREATE TABLE Workout_Session_Template(
  workout_id        INT PRIMARY KEY AUTO_INCREMENT,
  trainer_id        INT NOT NULL,
  analyst_id        INT,
  name              VARCHAR(100) NOT NULL,
  description       TEXT,
  duration_minutes  INT,
  difficulty        ENUM('easy','moderate','hard') NOT NULL,
  date_created      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_wst_trainer
     FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_wst_analyst
     FOREIGN KEY (analyst_id) REFERENCES Health_Analyst(analyst_id)
     ON DELETE SET NULL ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Workout_Specific_Exercise;
CREATE TABLE Workout_Specific_Exercise(
  workout_exercise_id INT PRIMARY KEY AUTO_INCREMENT,
  workout_id          INT NOT NULL,
  exercise_id         INT NOT NULL,
  sets                INT NOT NULL,
  reps                INT NOT NULL,
  rest_period         INT,
  CONSTRAINT fk_wse_workout
     FOREIGN KEY (workout_id) REFERENCES Workout_Session_Template(workout_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_wse_exercise
     FOREIGN KEY (exercise_id) REFERENCES Exercise(exercise_id)
     ON DELETE RESTRICT ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Client_Specific_Workout_Program;
CREATE TABLE Client_Specific_Workout_Program(
  program_id  INT PRIMARY KEY AUTO_INCREMENT,
  workout_id  INT NOT NULL,
  created_by  INT NOT NULL,   -- trainer_id
  client_id   INT NOT NULL,
  name        VARCHAR(100) NOT NULL,
  description TEXT,
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_cswp_workout
     FOREIGN KEY (workout_id) REFERENCES Workout_Session_Template(workout_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_cswp_trainer
     FOREIGN KEY (created_by) REFERENCES Trainer(trainer_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_cswp_client
     FOREIGN KEY (client_id) REFERENCES Client(client_id)
     ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Client_Workout_Log;
CREATE TABLE Client_Workout_Log (
  log_id            INT PRIMARY KEY AUTO_INCREMENT,
  client_id         INT NOT NULL,
  workout_id        INT NOT NULL,  -- from Workout_Session_Template
  analyst_id        INT,
  workout_date      DATE NOT NULL,
  completion_status ENUM('not_started','partial','completed') NOT NULL DEFAULT 'not_started',
  duration_minutes  INT,
  notes             TEXT,
  PR                TEXT,     -- multivalued attribute
  CONSTRAINT fk_cwl_client
     FOREIGN KEY (client_id) REFERENCES Client(client_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_cwl_workout
     FOREIGN KEY (workout_id) REFERENCES Workout_Session_Template(workout_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_cwl_analyst
     FOREIGN KEY (analyst_id) REFERENCES Health_Analyst(analyst_id)
     ON DELETE SET NULL ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Trainer_Feedback;
CREATE TABLE Trainer_Feedback(
  feedback_id INT PRIMARY KEY AUTO_INCREMENT,
  trainer_id  INT NOT NULL,
  log_id      INT NOT NULL,
  comment     TEXT NOT NULL,
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_tf_trainer
     FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_tf_log
     FOREIGN KEY (log_id) REFERENCES Client_Workout_Log(log_id)
     ON DELETE CASCADE ON UPDATE CASCADE
);


-- INSERT STATEMENTS FOR SAMPLE DATA


-- SYSTEM ADMIN
INSERT INTO System_Admin (system_admin_id, first_name, last_name, email)
VALUES (001, 'Ava', 'Martinez', 'avamartinez@fitflow.com');


-- Note: All user_ids and role_ids are auto-incremented
-- TRAINER USER #1
INSERT INTO User (email, password_hash, role, permissions, created_by)
VALUES (
   'marcus.rod@fitflow.com',
   'marcdagoat2025',
   'trainer',
   'create_exercise, edit_exercise, create_template, edit_template, create_program, edit_program',
   1
);


INSERT INTO Trainer (user_id, first_name, last_name, certification, specialization)
VALUES (LAST_INSERT_ID(), 'Marcus', 'Rodriguez', 'NASM-CPT', 'Strength Training');


-- TRAINER USER #2
INSERT INTO User (email, password_hash, role, permissions, created_by)
VALUES (
   'chad.zibz@gmail.com',
   'chaddddd387',
   'trainer',
   'create_exercise, edit_exercise, create_template, edit_template, create_program, edit_program',
   1
);


INSERT INTO Trainer (user_id, first_name, last_name, certification, specialization)
VALUES (LAST_INSERT_ID(), 'Chad', 'Zibermann', 'ACE-CPT', 'Cardio & HIIT');


-- CLIENT USER #1
INSERT INTO User (email, password_hash, role, permissions, created_by)
VALUES (
   'Chester.stone@gmail.com',
   'gmfd25!',
   'client',
   'add_log, edit_log, view_exercises',
   1
);


INSERT INTO Client (user_id, first_name, last_name, date_of_birth, fitness_level, join_date, goals)
VALUES (LAST_INSERT_ID(), 'Chester', 'Stone', '2001-11-02', 'Beginner', CURRENT_DATE, 'Build Muscle');


-- CLIENT USER #2
INSERT INTO User (email, password_hash, role, permissions, created_by)
VALUES (
   'CooperFlagg23@gmail.com',
   'bullCity',
   'client',
   'add_log, edit_log, view_exercises',
   1
);


INSERT INTO Client (user_id, first_name, last_name, date_of_birth, fitness_level, join_date, goals)
VALUES (LAST_INSERT_ID(), 'Cooper', 'Flagg', '1998-01-15', 'Intermediate', CURRENT_DATE, 'General Fitness');


-- HEALTH ANALYST USER (user_id = 6)
INSERT INTO User (email, password_hash, role, permissions, created_by)
VALUES (
   'k.smith@fitflow.com',
   'pw6',
   'analyst',
   'analyze_logs, analyze_templates',
   1
);


INSERT INTO Health_Analyst (user_id, first_name, last_name)
VALUES (LAST_INSERT_ID(), 'Kennedy', 'Smith');


INSERT INTO Exercise (name, description, category)
VALUES ('Push-Up', 'Bodyweight chest and triceps exercise', 'Upper Body');


INSERT INTO Exercise (name, description, category)
VALUES ('Squat', 'Lower-body strength exercise', 'Legs');


INSERT INTO Exercise (name, description, category)
VALUES ('Plank', 'Core stabilization exercise', 'Core');


INSERT INTO Workout_Session_Template (trainer_id, analyst_id, name, description, duration_minutes, difficulty)
VALUES (1, 1, 'Upper Body Blast', 'Push-oriented strength routine', 45, 'moderate');


INSERT INTO Workout_Session_Template (trainer_id, analyst_id, name, description, duration_minutes, difficulty)
VALUES (2, 1, 'Leg Day Starter', 'Lower-body compound movements', 40, 'easy');


INSERT INTO Workout_Specific_Exercise (workout_id, exercise_id, sets, reps, rest_period)
VALUES (1, 1, 3, 12, 60);


INSERT INTO Workout_Specific_Exercise (workout_id, exercise_id, sets, reps, rest_period)
VALUES (2, 2, 4, 10, 90);


INSERT INTO Client_Specific_Workout_Program (workout_id, created_by, client_id, name, description)
VALUES (1, 1, 1, 'Emily Strength Program', '4-week upper-body strength plan');


INSERT INTO Client_Specific_Workout_Program (workout_id, created_by, client_id, name, description)
VALUES (2, 2, 2, 'Max Leg Program', 'Leg-focused starter program');


INSERT INTO Client_Workout_Log (client_id, workout_id, analyst_id, workout_date, completion_status, duration_minutes, notes, PR)
VALUES (1, 1, 1, '2025-02-24', 'completed', 45, 'Felt great', 'Push-up:20');


INSERT INTO Client_Workout_Log (client_id, workout_id, analyst_id, workout_date, completion_status, duration_minutes, notes, PR)
VALUES (2, 2, 1, '2025-02-24', 'partial', 30, 'Legs were tired', 'Squat:120lbs');


INSERT INTO Trainer_Feedback (trainer_id, log_id, comment)
VALUES (1, 1, 'Great job on form!');


INSERT INTO Trainer_Feedback (trainer_id, log_id, comment)
VALUES (2, 2, 'Increase warm-up next time.');


INSERT INTO System_Log (user_id, action_type, description)
VALUES (1, 'CREATE_USER', 'Admin created trainer profile for Marcus.');


INSERT INTO System_Log (user_id, action_type, description)
VALUES (2, 'CREATE_EXERCISE', 'Trainer Marcus added Squat exercise.');


INSERT INTO Backup_Log (performed_by, backup_start, backup_end, backup_time_mins, status)
VALUES (1, '2025-02-20 03:00:00', '2025-02-20 03:05:00', 5, 'success');


INSERT INTO Backup_Log (performed_by, backup_start, backup_end, backup_time_mins, status)
VALUES (1, '2025-02-22 03:00:00', '2025-02-22 03:08:00', 8, 'success');