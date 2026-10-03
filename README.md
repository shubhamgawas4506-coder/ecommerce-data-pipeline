\# 🛒 E-Commerce Data Pipeline \& Analytics Warehouse



An end-to-end data pipeline that simulates transactional e-commerce order streams, performs schema cleaning and ETL transformations, stores optimized columnar Parquet data, and executes analytical SQL queries.



\---



\## 🏗️ Architecture Overview



```text

\[ Raw Producer ] ──> \[ JSON Staging ] ──> \[ ETL Engine ] ──> \[ Parquet Storage ] ──> \[ Analytics Warehouse ]

(Python + Faker)    (raw\_orders.json)    (Pandas + Arrow)   (Partitioned Data)      (DuckDB + SQL)

