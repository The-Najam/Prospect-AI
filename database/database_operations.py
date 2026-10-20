import datetime
from database.database_connection import create_dbconnection
from psycopg.types.json import Jsonb


def add_record(con, cur, run_id, prospect_url):
    started_at = datetime.datetime.now(datetime.timezone.utc)

    cur.execute(
        """
        INSERT INTO prospect_tracking_run (
            run_id,
            prospect_url,
            status,
            started_at,
            completed_at,
            final_report,
            error_type,
            error_message,
            failed_phase,
            gemini_tokens,
            groq_tokens
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            run_id,
            prospect_url,
            "running",
            started_at,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
    )

    con.commit()


def update_complete_record(
    con,
    cur,
    final_report,
    gemini_tokens,
    groq_tokens,
    run_id,
):
    completed_at = datetime.datetime.now(datetime.timezone.utc)

    cur.execute(
        """
        UPDATE prospect_tracking_run
        SET
            status = %s,
            completed_at = %s,
            final_report = %s,
            gemini_tokens = %s,
            groq_tokens = %s
        WHERE run_id = %s
        """,
        (
            "completed",
            completed_at,
            Jsonb(final_report),
            gemini_tokens,
            groq_tokens,
            run_id,
        ),
    )

    con.commit()


def update_failed_record(
        con,
        cur,
        final_report,
        gemini_tokens,
        groq_tokens,
        failed_phase,
        error_type,
        error_message,
        run_id
):
    completed_at = datetime.datetime.now(datetime.timezone.utc)
    cur.execute(
            """
            UPDATE prospect_tracking_run
            SET
                status = %s,
                completed_at = %s,
                final_report = %s,
                gemini_tokens = %s,
                groq_tokens = %s,
                failed_phase = %s,
                error_type = %s,
                error_message = %s
            WHERE run_id = %s
            """,
            (
                "failed",
                completed_at,
                Jsonb(final_report),
                gemini_tokens,
                groq_tokens,
                failed_phase,
                error_type,
                error_message,
                run_id
            ),
    )
    con.commit()

def get_report(run_id):
    conn, cur = create_dbconnection()

    try:
        cur.execute(
            """
            SELECT final_report
            FROM prospect_tracking_run
            WHERE run_id = %s
            """,
            (run_id,),
        )

        row = cur.fetchone()
        return row[0] if row else None

    finally:
        cur.close()
        conn.close()

