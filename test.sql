drop table if exists donor;
create table donor(PAN varchar(20), ContactNo bigint, userid int, address text, foreign key (userid) references auth_user(id) on delete set null on update cascade);



drop table if exists teacher;
create table teacher(t_id int primary key auto_increment, name varchar(50), salary int, start_year int, contact_no bigint, image longblob);

/*insert into teacher(name,salary,start_year,contact_no) values("Vandit Jain",205000,2012,1234567890);
insert into teacher(name,salary,start_year,contact_no) values("Anil Jain",205000,2010,976543210);*/



drop table if exists subject;
create table subject(su_id int primary key auto_increment, title varchar(30), tr_id int, foreign key (tr_id) references teacher(t_id) on delete set null on update cascade);

/*insert into subject(title,tr_id) values("mathematics",1);
insert into subject(title,tr_id) values("english core",2);*/



drop table if exists nurse;
create table nurse(n_id int primary key auto_increment, name varchar(50), salary int, start_year int, contact_no bigint, image longblob, s_a int default 0);



drop table if exists doctor;
create table doctor(d_id int primary key auto_increment, name varchar(50), specialisation varchar(50), salary int, start_year int, contact_no bigint, image longblob, s_a int default 0);



drop table if exists nontechnicalstaff;
create table nontechnicalstaff(ns_id int primary key auto_increment, name varchar(50), designation varchar(50), salary int, start_year int, contact_no bigint, isadmin bool, image longblob);



drop table if exists donation;
create table donation(dn_id int primary key auto_increment, amount bigint, timestamp datetime, dr_id int, foreign key (dr_id) references auth_user(id) on delete set null on update cascade);



drop table if exists student;
create table student(s_id int primary key auto_increment, name varchar(30), address varchar(200), major_disability varchar(20), father_name varchar(30), mother_name varchar(30), contact_no bigint, nu_id int, dc_id int, foreign key (nu_id) references nurse(n_id) on delete set null on update cascade, foreign key (dc_id) references doctor(d_id) on delete set null on update cascade);



drop table if exists news;
create table news(ne_id int primary key auto_increment,heading varchar(200), link varchar(200), timestamp datetime, nsf_id int, foreign key (nsf_id) references nontechnicalstaff(ns_id) on delete set null on update cascade);



drop table if exists ecommittee;
create table ecommittee(e_id int primary key auto_increment, post varchar(30), ntf_id int, dt_id int, th_id int, foreign key (ntf_id) references nontechnicalstaff(ns_id) on delete set null on update cascade, foreign key (dt_id) references doctor(d_id) on delete set null on update cascade, foreign key (th_id) references teacher(t_id) on delete set null on update cascade);



drop table if exists student_subject;
create table student_subject(st_id int, sb_id int, foreign key (st_id) references student(s_id) on delete set null on update cascade, foreign key (sb_id) references subject(su_id) on delete set null on update cascade);



drop table if exists student_teacher;
create table student_teacher(sd_id int, te_id int, foreign key (sd_id) references student(s_id) on delete set null on update cascade, foreign key (te_id) references teacher(t_id) on delete set null on update cascade);