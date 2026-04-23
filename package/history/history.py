import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


class History:
    _warned = False

    @classmethod
    def database_path(cls):
        return Path(os.getenv("SQLITE_PATH", "data/simpleequalizer.sqlite3"))

    @classmethod
    def is_configured(cls):
        conn = cls._connect()
        if conn is None:
            return False
        conn.close()
        return True

    @classmethod
    def _warn(cls, message):
        if not cls._warned:
            print(f"History warning: {message}", file=sys.stderr)
            cls._warned = True

    @classmethod
    def _connect(cls):
        try:
            db_path = cls.database_path()
            db_path.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cls._ensure_schema(conn)
            return conn
        except Exception as exc:
            cls._warn(f"SQLite history disabled; {exc}")
            return None

    @staticmethod
    def _ensure_schema(conn):
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at TEXT NOT NULL,
                finished_at TEXT NULL,
                run_type TEXT NOT NULL,
                params_json TEXT NULL,
                status TEXT NOT NULL,
                image_paths TEXT NULL,
                note TEXT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_measurements_started_at ON measurements(started_at)"
        )
        conn.commit()

    @staticmethod
    def _now():
        return datetime.now().isoformat(sep=" ", timespec="seconds")

    @classmethod
    def record_start(cls, run_type, params):
        conn = cls._connect()
        if conn is None:
            return None
        try:
            with conn:
                cursor = conn.execute(
                    """
                    INSERT INTO measurements
                        (started_at, run_type, params_json, status)
                    VALUES (?, ?, ?, 'running')
                    """,
                    (cls._now(), run_type, json.dumps(params, ensure_ascii=False)),
                )
                return cursor.lastrowid
        except Exception as exc:
            cls._warn(f"record_start failed; {exc}")
            return None
        finally:
            conn.close()

    @classmethod
    def record_finish(cls, run_id, status, image_paths, note=None):
        if run_id is None:
            return None
        conn = cls._connect()
        if conn is None:
            return None
        try:
            with conn:
                conn.execute(
                    """
                    UPDATE measurements
                    SET finished_at = ?,
                        status = ?,
                        image_paths = ?,
                        note = ?
                    WHERE id = ?
                    """,
                    (
                        cls._now(),
                        status,
                        json.dumps(image_paths, ensure_ascii=False),
                        note,
                        run_id,
                    ),
                )
        except Exception as exc:
            cls._warn(f"record_finish failed; {exc}")
        finally:
            conn.close()
        return None

    @classmethod
    def list_recent(cls, limit=20):
        conn = cls._connect()
        if conn is None:
            return []
        try:
            rows = conn.execute(
                """
                SELECT id, started_at, finished_at, run_type, params_json,
                       status, image_paths, note
                FROM measurements
                ORDER BY started_at DESC, id DESC
                LIMIT ?
                """,
                (int(limit),),
            ).fetchall()
            return [dict(row) for row in rows]
        except Exception as exc:
            cls._warn(f"list_recent failed; {exc}")
            return []
        finally:
            conn.close()
