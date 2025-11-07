insert into customers (country, created_at)
values 
('NL','2024-01-05'),
('DE','2024-02-10'),
('NL','2024-03-20');

insert into orders (customer_id, order_date, channel, amount)
values
(1,'2025-01-10','web',59.90),
(1,'2025-02-12','app',19.99),
(2,'2025-02-18','web',120.00),
(3,'2025-03-02','app',9.99);

