drop table taxi_paths_IV_attr;
drop table taxi_paths_IV;

create table taxi_paths_IV(
	tid int not null references taxi_tracks(id),
	way_ids text not null,
	path_geom geometry not null,
	primary key(tid));

create table taxi_paths_IV_attr(
	tid int not null references taxi_paths_IV(tid) on delete cascade,
	length double precision not null default -1,
	conf double precision not null default -1,
	valid int not null default -1,
	primary key(tid));
