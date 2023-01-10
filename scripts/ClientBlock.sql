-- 59 23 * * * psql postgresql://gpadmin:gpadmin@greenplum:5432/bank -c ""

do
$credit_process$
begin
	update clients
	set cash = case 
			when cash - amount >= '0.00' then cash - amount
			else cash
		end,
		block = case
			when cash - amount < '0.00' then true
			else false
		end
	from (
		select id_client, sum(amount) as amount
		from clients inner join clients_credits 
		on id_client = client_init
		where maturity_date < now() and
			  status_return = false
		group by id_client
	) pay;
	
	update credits
	set status_return = true
	where id in (
		select distinct id
		from clients_credits inner join clients
		on id = id_client
		where block = false and
			  maturity_date < now()
	);
end
$credit_process$;

do
$morgage_process$
begin
	update clients
	set cash = case 
			when cash - amount >= '0.00' then cash - amount
			else cash
		end,
		block = case
			when cash - amount < '0.00' then true
			else false
		end
	from (
		select id_client, sum(amount) as amount
		from clients inner join clients_mortgages 
		on id_client = client_init
		where maturity_date < now() and
			  status_return = false
		group by id_client
	) pay;
	
	update mortgages
	set status_return = true
	where id in (
		select distinct id
		from clients_mortgages inner join clients
		on id = id_client
		where block = false and
			  maturity_date < now()
	);
end
$morgage_process$;