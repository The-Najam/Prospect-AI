import redis
import uuid


client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)


def save_reports(session_id,report):
    key = f"session:{session_id}:reports"
    if client.ttl(key) == -1:
        client.expire(key, 86400)
    client.lpush(key, report)
    client.ltrim(key, 0, 4)


def get_reports(session_id):
    key = f"session:{session_id}:reports"

    reports = client.lrange(key, 0, -1)

    return reports

    

if __name__ == "__main__":
    session_id = uuid.uuid4() # generating the temp id
    for i in range(1, 7):
        save_reports(session_id, f"Report {i}")

    print(get_reports(session_id))