import psycopg2

# Database connection
conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_OnC1e4KspNdk@ep-purple-hat-ahw4nk3o-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
)
cursor = conn.cursor()

# Add priority and due_date columns
try:
    cursor.execute("ALTER TABLE tasks ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium';")
    cursor.execute("ALTER TABLE tasks ADD COLUMN IF NOT EXISTS due_date TIMESTAMP;")
    conn.commit()
    print("✅ Columns added successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    cursor.close()
    conn.close()