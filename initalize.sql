CREATE TABLE Users (
    user_id serial PRIMARY KEY,
    user_name text UNIQUE NOT NULL,
    user_email text UNIQUE NOT NULL,
    user_password text NOT NULL,
	  email_sub_agreement boolean NOT NULL,
);

CREATE TABLE Groups (
	group_id serial PRIMARY KEY,
	alive_status boolean NOT NULL,
	group_name text UNIQUE NOT NULL
);

CREATE TABLE User_groups (
	group_id int NOT NULL REFERENCES Groups (group_id),
	user_id int NOT NULL REFERENCES Users (user_id)
);

CREATE TABLE Entitys (
  entity_id serial PRIMARY KEY,
  type boolean NOT NULL,
  entity_origin_id int UNIQUE NOT NULL
);

CREATE TABLE Sessions_log (
	session_id serial PRIMARY KEY,
  entity_id int NOT NULL REFERENCES Entitys (entity_id),
	type boolean NOT NULL,
	time_stamp timestamp NOT NULL
);