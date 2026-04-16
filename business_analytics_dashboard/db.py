import duckdb
import os

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "volis_analytics",
    "dev.duckdb"
)

def get_connection():
    return duckdb.connect(DB_PATH, read_only=True)