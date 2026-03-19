import json
from collections import defaultdict
from datetime import datetime

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "green-trips",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=5000,
)

hourly_tips = defaultdict(float)

for message in consumer:
    try:
        data = json.loads(message.value.decode("utf-8"))
        pickup_time = datetime.fromisoformat(data["lpep_pickup_datetime"])
        hour_key = pickup_time.replace(minute=0, second=0, microsecond=0)
        tip_amount = float(data.get("tip_amount", 0))
        hourly_tips[hour_key] += tip_amount
    except Exception as e:
        print(f"Error processing message: {e}")

consumer.close()

print("\nHourly tips summary:")
print("-" * 50)
for hour, total_tip in sorted(hourly_tips.items()):
    print(f"{hour}: ${total_tip:.2f}")

if hourly_tips:
    max_hour = max(hourly_tips.items(), key=lambda x: x[1])
    print("-" * 50)
    print(f"\nHour with highest total tips: {max_hour[0]} with ${max_hour[1]:.2f}")
