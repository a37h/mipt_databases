CREATE TABLE Users (
    user_id serial PRIMARY KEY,
    user_name text UNIQUE NOT NULL,
    user_email text UNIQUE NOT NULL,
    user_password varchar(100) NOT NULL
);

CREATE TABLE Sessions_log (
	session_id serial PRIMARY KEY,
    user_id int NOT NULL REFERENCES Users (user_id),
	type boolean NOT NULL,
	time_stamp timestamp NOT NULL
);

CREATE TABLE User_expirience (
    user_id int PRIMARY KEY REFERENCES Users (user_id),
	total_time_spent real NOT NULL,
	amount_of_finished_sessions real NOT NULL
);

CREATE TABLE Mailing_list (
    user_id int PRIMARY KEY REFERENCES Users (user_id),
	email_sub_agreement boolean NOT NULL,
	last_notification timestamp,
	notfication_clickthrough_rate real
);

CREATE TABLE Groups (
	group_id serial PRIMARY KEY,
	type boolean NOT NULL, 
	group_name text UNIQUE NOT NULL
);

CREATE TABLE User_groups (
	group_id int NOT NULL REFERENCES Groups (group_id),
	user_id int NOT NULL REFERENCES Users (user_id)
);