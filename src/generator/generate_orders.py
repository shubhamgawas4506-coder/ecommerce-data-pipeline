import json
import random
import uuid
from datetime import datetime, timezone
from faker import Faker

fake = Faker()

def generate_order():
    unit_price = round(random.uniform(5.0, 500.0), 2)
    quantity = random.randint(1, 5)
    return {
        "order_id": str(uuid.uuid4()),
        "customer_id": random.randint(1000, 9999),
        "product_id": random.randint(100, 500),
        "quantity": quantity,
        "unit_price": unit_price,
        "total_amount": round(quantity * unit_price, 2),
        "order_status": random.choices(["completed", "cancelled", "refunded", "pending"], weights=[0.80, 0.10, 0.05, 0.05])[0],
        "payment_method": random.choice(["credit_card", "paypal", "upi", "net_banking"]),
        "order_timestamp": fake.date_time_between(start_date="-30d", end_date="now", tzinfo=timezone.utc).isoformat()
    }

def generate_batch(num_records=100, output_path="raw_orders_sample.json"):
    orders = [generate_order() for _ in range(num_records)]
    with open(output_path, "w") as f:
        for order in orders:
            f.write(json.dumps(order) + "\n")
    print(f"Successfully generated {num_records} orders -> {output_path}")

if __name__ == "__main__":
    generate_batch(num_records=100, output_path="raw_orders_sample.json")