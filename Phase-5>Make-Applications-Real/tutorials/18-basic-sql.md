# Tutorial 18 — Basic SQL

## Why This Matters

Students need enough SQL to understand and inspect relational data.

## SELECT

```sql
SELECT * FROM products;

SELECT name, price
FROM products;
```

## WHERE and ORDER BY

```sql
SELECT *
FROM products
WHERE price > 1000;

SELECT *
FROM products
ORDER BY price DESC;
```

## INSERT

```sql
INSERT INTO products (name, price)
VALUES ('Mouse', 1000);
```

## UPDATE

```sql
UPDATE products
SET price = 1200
WHERE id = 3;
```

The `WHERE` condition matters; without it, every row could be changed.

## DELETE

```sql
DELETE FROM products
WHERE id = 3;
```

Again, inspect the affected rows before destructive operations.

## CRUD Connection

```text
SELECT → Read
INSERT → Create
UPDATE → Update
DELETE → Delete
```

## Try It

Use a small database to find records, filter them, sort them, add one, modify it, and remove it.
