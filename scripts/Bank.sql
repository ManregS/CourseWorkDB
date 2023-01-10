create table if not exists Clients (
	id_client serial not null primary key,
  	name varchar(100) not null,
  	birth_date date not null,
  	series int not null,
  	number int not null,
  	cash money not null default '0.00',
	password text not null,
  	block bool default false,
  	check(cash >= '0.00'),
  	check(id_client > 0),
  	check(extract(year from age(now(), birth_date))::int >= 18)
);

create table if not exists Operations (
	id serial not null primary key,
  	type varchar(100) not null,
  	time_start timestamp not null default now(),
  	client_init int not null,
  	constraint fk_clientoperation
  		foreign key(client_init)
  			references Clients(id_client)
);

create table if not exists Money_transfers (
	id serial not null primary key,
  	client_recip int not null,
  	amount money not null default '0.00',
  	check(amount >= '0.00'),
  	constraint fk_operationtransfer
  		foreign key(id)
  			references Operations(id),
  	constraint fk_clienttransfer
  		foreign key(client_recip)
  			references Clients(id_client)
);

create table if not exists Credits (
	id serial not null primary key,
  	amount money not null default '0.00',
  	maturity_date date not null,
  	status_return bool not null default false,
  	check(amount >= '0.00'),
  	check(maturity_date > now()),
  	constraint fk_operationcredit
  		foreign key(id)
  			references Operations(id)
);

create table if not exists Mortgages (
	id serial not null,
  	amount money not null default '0.00',
  	maturity_date date not null,
  	status_return bool not null default false,
  	address_prop varchar(100) not null primary key,
  	check(amount >= '0.00'),
  	check(maturity_date > now()),
  	constraint fk_operationcredit
  		foreign key(id)
  			references Operations(id)
);

create view clients_transfers as
select money_transfers.id, client_init, client_recip, amount, time_start
from money_transfers left join operations
on operations.id = money_transfers.id;

create view clients_credits as
select credits.id, client_init, amount, time_start, maturity_date, status_return
from credits left join operations
on operations.id = credits.id;

create view clients_mortgages as
select mortgages.id, client_init, amount, time_start, maturity_date, address_prop, status_return
from mortgages left join operations
on operations.id = mortgages.id;