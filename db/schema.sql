create table if not exists customers (
  customer_id serial primary key,
  country text not null,
  created_at timestamp not null
);

create table if not exists orders (
  order_id serial primary key,
  customer_id int references customers(customer_id),
  order_date timestamp not null,
  channel text check (channel in ('web','app')),
  amount numeric(12,2) not null
);

create index if not exists idx_orders_date on orders(order_date);

