schema_description = """### Схема базы данных

#### Таблица: `users` (Пользователи)
- **id**: INTEGER PRIMARY KEY  
  Уникальный идентификатор пользователя.
- **name**: TEXT  
  Полное имя пользователя.
- **email**: TEXT  
  Электронная почта пользователя. Уникальная для каждого пользователя.
- **phone**: TEXT  
  Телефонный номер пользователя.
- **address**: TEXT  
  Адрес пользователя.

---

#### Таблица: `employees` (Работники)
- **id**: INTEGER PRIMARY KEY  
  Уникальный идентификатор работника.
- **name**: TEXT  
  Полное имя работника.
- **position**: TEXT  
  Должность работника.
- **salary**: REAL  
  Зарплата работника.
- **hire_date**: TEXT  
  Дата приема на работу.

---

#### Таблица: `products` (Товары)
- **id**: INTEGER PRIMARY KEY  
  Уникальный идентификатор товара.
- **name**: TEXT  
  Название товара.
- **price**: REAL  
  Цена товара.
- **stock**: INTEGER  
  Количество товара на складе.

---

#### Таблица: `orders` (Заказы)
- **id**: INTEGER PRIMARY KEY  
  Уникальный идентификатор заказа.
- **user_id**: INTEGER  
  Идентификатор пользователя, сделавшего заказ (ссылается на `users.id`).
- **product_id**: INTEGER  
  Идентификатор товара в заказе (ссылается на `products.id`).
- **quantity**: INTEGER  
  Количество единиц товара в заказе.
- **order_date**: TEXT  
  Дата оформления заказа.

---

### Взаимосвязи между таблицами
1. **Таблица `orders`**:
   - Поле `user_id` связано с таблицей `users` через `users.id`.
   - Поле `product_id` связано с таблицей `products` через `products.id`.

### Примерные запросы для аналитиков
1. **Список всех заказов с данными о пользователях и товарах:**
   ```sql
   SELECT orders.id, users.name AS user_name, products.name AS product_name, orders.quantity, orders.order_date
   FROM orders
   JOIN users ON orders.user_id = users.id
   JOIN products ON orders.product_id = products.id;
   ```

2. **Сумма продаж по каждому товару:**
   ```sql
   SELECT products.name, SUM(orders.quantity * products.price) AS total_revenue
   FROM orders
   JOIN products ON orders.product_id = products.id
   GROUP BY products.id;
   ```

3. **Список работников с зарплатой выше 50,000:**
   ```sql
   SELECT * FROM employees WHERE salary > 50000;
   ```

4. **Складские остатки товаров:**
   ```sql
   SELECT name, stock FROM products WHERE stock > 0;
   ```"""
