-- add invoice
INSERT INTO invoices(date, customer_id)
VALUES (CAST('2019-06-15' AS date), 136)

-- add customer
INSERT INTO customers(first_name, last_name)
VALUES ('Cookie','Monster')

-- inspect primary key sequence in table 'customers' with primary key 'id'
select * from customers_id_seq

-- get highest id
SELECT MAX(id) FROM customers

-- get next primary key sequence
-- NOTE: this advances the primary key sequence!
SELECT nextval('customers_id_seq')

-- set primary key sequence to next highest available
SELECT setval('customers_id_seq', (SELECT MAX(id) FROM customers)+1);


select * from customers
select * from invoices
