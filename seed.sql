-- Employees
INSERT INTO employees (name, email, position, salary, hire_date) VALUES
('Alice Johnson', 'alice@example.com', 'Store Manager', 65000.00, '2023-01-15'),
('Bob Smith', 'bob@example.com', 'Sales Associate', 42000.00, '2023-03-10'),
('Carol Davis', 'carol@example.com', 'Sales Associate', 42000.00, '2023-06-01'),
('David Lee', 'david@example.com', 'Inventory Specialist', 48000.00, '2024-02-20');

-- Suppliers
INSERT INTO suppliers (name, contact_email, city) VALUES
('TechCorp', 'info@techcorp.com', 'San Francisco'),
('ShoeMakers', 'contact@shoemakers.com', 'Portland'),
('FitGear', 'hello@fitgear.com', 'Denver');

-- Products
INSERT INTO products (name, category, price, stock, supplier_id) VALUES
('Wireless Headphones', 'Electronics', 79.99, 50, 1),
('Phone Case', 'Accessories', 19.99, 200, 1),
('Running Shoes', 'Footwear', 129.99, 30, 2),
('Yoga Mat', 'Fitness', 34.99, 80, 3),
('Water Bottle', 'Accessories', 14.99, 150, 3),
('Hiking Sandals', 'Footwear', 89.99, 25, 2);

-- Customers
INSERT INTO customers (name, email, city) VALUES
('Jane Doe', 'jane@email.com', 'Austin'),
('Mike Brown', 'mike@email.com', 'Seattle'),
('Sarah Wilson', 'sarah@email.com', 'Austin'),
('Tom Garcia', 'tom@email.com', 'Denver');

-- Sales
INSERT INTO sales (product_id, customer_id, employee_id, quantity, sale_date) VALUES
(1, 1, 2, 2, '2025-03-01'),
(3, 2, 2, 1, '2025-03-02'),
(4, 3, 3, 3, '2025-03-03'),
(2, 1, 3, 1, '2025-03-05'),
(5, 4, 2, 2, '2025-03-06'),
(1, 3, 2, 1, '2025-03-07'),
(6, 2, 3, 1, '2025-03-08'),
(3, 4, 2, 2, '2025-03-10'),
(4, 1, 3, 1, '2025-03-12'),
(5, 2, 2, 3, '2025-03-14');

-- Reviews
INSERT INTO reviews (product_id, customer_id, rating, comment, review_date) VALUES
(1, 1, 5, 'Great sound quality!', '2025-03-04'),
(3, 2, 4, 'Very comfortable for running', '2025-03-05'),
(4, 3, 5, 'Perfect for my yoga sessions', '2025-03-06'),
(2, 1, 3, 'Does the job but nothing special', '2025-03-08'),
(5, 4, 4, 'Keeps water cold all day', '2025-03-09'),
(1, 3, 4, 'Good value for the price', '2025-03-10'),
(6, 2, 2, 'Not durable, sole came apart', '2025-03-12');