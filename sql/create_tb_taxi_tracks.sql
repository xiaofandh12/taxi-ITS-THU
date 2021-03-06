drop table taxi_tracks_attr;
drop table taxi_tracks;

create table taxi_tracks(
	id SERIAL,
	cuid int not null,
	track_geom geometry not null,
	track_desc text not null,
	primary key(id));

create table taxi_tracks_attr(
	tid int not null references taxi_tracks(id) on delete cascade,
	length double precision not null default 0,
	rds_num int not null default 0,
	primary key(tid));

	
