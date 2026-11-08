import psycopg
from models.workflow_state import WorkflowState
from config.settings import setting

# creating database connection
def create_dbconnection():

    conn = psycopg.connect(
        f"""dbname=prospect-ai
        user={setting.DB_USER}
        password={setting.DB_PASSWORD}
        host={setting.DB_HOST}
        port={setting.DB_PORT}"""
    )
    cur = conn.cursor()
    return conn, cur



if __name__ == "__main__":
    con,cur = create_dbconnection()


    