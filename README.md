# Medical Shop Management System

A command-line Python application designed to manage the inventory, sales, and purchases of a medical shop. This project uses a MySQL database to securely store and track medicine details, transactions, and generate helpful reports like low-stock and expiring medicine alerts.

---

## Features

### Role-Based Access
* **Admin Mode:** Full access to inventory management, transaction recording, and reporting.
* **Guest Mode:** Limited access to browse and search the available medicine inventory.

### Inventory Management
* Add, view, update, and search for medicines.
* Automatic stock quantity updates when purchases or sales are recorded.
* Low stock alerts based on a custom threshold.
* Expiring medicines report to track inventory shelf-life.

### Transaction Tracking
* **Purchases:** Record new medicine batches and calculate total purchase amounts.
* **Sales:** Sell medicines (with stock validation) and calculate total sale amounts.
* **Daily Reports:** Generate daily sales and purchase summaries to track revenue and expenses.

---

## Prerequisites

Before you run this project, ensure you have the following installed on your system:
* **Python 3.x**
* **MySQL Server** * **MySQL Connector for Python**

You can install the required Python library using pip:
```bash
pip install mysql-connector-python
