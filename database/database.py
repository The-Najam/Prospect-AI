import psycopg
from models.workflow_state import WorkflowState


def create_dbconnection():

    conn = psycopg.connect(
        """dbname=prospect-ai
        user=postgres
        password=ai_dev
        host=localhost
        port=5432"""
    )

    cur = conn.cursor()

    return conn, cur


def insert_data(conn,cur,url,id,started_at,status):
    cur.execute("""
    INSERT INTO runs (
        id,
        url,
        started_at,
        completed_at,
        status,
        error_type,
        retry_count,
        total_token_used,
        estimated_cost,
        latency_seconds
    )
    VALUES (%s, %s, %s, NULL, %s, NULL, 0, 0, NULL, NULL);
    """, (
        id,
        url,
        started_at,
        status
    ))

    conn.commit()
    cur.close()
    conn.close()


def update_data(conn,cur, run_id,completed_at,latency,estimated_cost):
    cur.execute("""
    UPDATE runs SET status='success', completed_at=%s, latency_seconds=%s, total_token_used=%s, estimated_cost=%s where id = %s;
    """, (completed_at,latency,state.total_token_used,estimated_cost,run_id))

    conn.commit()
    cur.close()
    conn.close()


def updata_data_fail(conn,cur, run_id,completed_at,latency,estimated_cost,error_type,retry_count):
    cur.execute("""
    UPDATE runs SET status='failed', completed_at=%s,latency_seconds=%s,total_tokens_used=%s,estimated_cost=%s,error_type=%s,retry_count=%s where id = %s;
    """,(completed_at,latency,state.total_token_used,estimated_cost,error_type,retry_count,run_id))
    
    conn.commit()
    cur.close()
    conn.close()

def view_data(con,cur):
    cur.execute("""SELECT * FROM runs""")

    rows = cur.fetchall()
    print(rows)




if __name__ == "__main__":
    con,cur = create_dbconnection()
    view_data(con,cur)

    