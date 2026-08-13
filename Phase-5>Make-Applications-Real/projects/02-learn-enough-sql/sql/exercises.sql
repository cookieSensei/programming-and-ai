-- Run these against the inventory_project database.
-- Inspect the table first:
SELECT * FROM inventory_product;

-- 1. Show only product names and prices.
SELECT name, price FROM inventory_product;

-- 2. Find products costing more than 1000.
SELECT name, price
FROM inventory_product
WHERE price > 1000;

-- 3. Sort products from cheapest to most expensive.
SELECT name, price
FROM inventory_product
ORDER BY price ASC;

-- 4. Add a practice product.
-- INSERT INTO inventory_product
-- (name, description, price, quantity, created_at)
-- VALUES ('Notebook', 'Practice product', 250, 10, datetime('now'));

-- 5. Update a product.
-- UPDATE inventory_product
-- SET quantity = 15
-- WHERE name = 'Notebook';

-- 6. Delete the practice product.
-- DELETE FROM inventory_product
-- WHERE name = 'Notebook';
