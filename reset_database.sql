DROP DATABASE mipt_db_project;
DROP ROLE mipt_db_project_user;

CREATE DATABASE mipt_db_project;

\c mipt_db_project;

CREATE TABLE Users (
    user_id serial NOT NULL PRIMARY KEY,
    user_name text UNIQUE NOT NULL,
    user_email text UNIQUE NOT NULL,
    user_password text NOT NULL,
	  email_sub_agreement boolean NOT NULL
);

CREATE TABLE Groups (
	group_id serial NOT NULL PRIMARY KEY,
	group_name text UNIQUE NOT NULL
);

CREATE TABLE User_groups (
	group_id int NOT NULL REFERENCES Groups (group_id),
	user_id int NOT NULL REFERENCES Users (user_id),
	user_status varchar(1) NOT NULL
);

CREATE TABLE Entitys (
  entity_id serial PRIMARY KEY,
  type boolean NOT NULL,
  group_id integer ,
  user_id integer,
  FOREIGN KEY (user_id) REFERENCES Users (user_id),
  FOREIGN KEY (group_id) REFERENCES Groups (group_id)
);

CREATE TABLE Sessions_log (
	session_id serial PRIMARY KEY,
  entity_id int NOT NULL REFERENCES Entitys (entity_id),
	type boolean NOT NULL,
	time_stamp varchar(100) NOT NULL
);

CREATE ROLE mipt_db_project_user with login;

GRANT ALL ON Users TO mipt_db_project_user;
GRANT ALL ON Groups TO mipt_db_project_user;
GRANT ALL ON Groups_group_id_seq TO mipt_db_project_user;
GRANT ALL ON User_groups TO mipt_db_project_user;
GRANT ALL ON Entitys TO mipt_db_project_user;
GRANT ALL ON Sessions_log TO mipt_db_project_user;
GRANT ALL ON entitys_entity_id_seq TO mipt_db_project_user;
GRANT ALL ON sessions_log_session_id_seq TO mipt_db_project_user;
GRANT ALL ON users_user_id_seq TO mipt_db_project_user;

\password mipt_db_project_user
ggHkfIJ9aAFxzjmrkIMfWrvC03wZkgpK