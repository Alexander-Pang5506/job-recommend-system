"""Import job_data from UTF-16LE SQL backup into MySQL"""
import pymysql
import re

# Connect
conn = pymysql.connect(
    host='localhost', user='root', password='12345678',
    database='recommend_job', charset='utf8mb4'
)
cur = conn.cursor()

# Read UTF-16LE file
with open(r"C:\Users\P.sir\WorkBuddy\2026-06-14-20-07-12\job_recommend_project\recommend_job_backup.sql", "rb") as f:
    raw = f.read()
content = raw.decode('utf-16-le')

def parse_values(text):
    """Parse MySQL VALUES list like (a,b,'c'),(d,e,'f') into list of tuples"""
    text = text.strip()
    results = []
    i = 0
    while i < len(text):
        if text[i] == '(':
            # Find matching close paren
            depth = 1
            j = i + 1
            in_str = False
            str_char = None
            while j < len(text) and depth > 0:
                ch = text[j]
                if in_str:
                    if ch == str_char and text[j-1] != '\\':
                        in_str = False
                else:
                    if ch in ("'", '"'):
                        in_str = True
                        str_char = ch
                    elif ch == '(':
                        depth += 1
                    elif ch == ')':
                        depth -= 1
                j += 1
            row_str = text[i+1:j-1]
            # Parse fields
            fields = []
            field = ''
            in_str = False
            str_char = None
            for ch in row_str:
                if in_str:
                    field += ch
                    if ch == str_char and (len(field) < 2 or field[-2] != '\\'):
                        in_str = False
                else:
                    if ch in ("'", '"'):
                        in_str = True
                        str_char = ch
                        field += ch
                    elif ch == ',':
                        fields.append(field.strip())
                        field = ''
                    else:
                        field += ch
            if field.strip():
                fields.append(field.strip())
            results.append(fields)
            i = j
        else:
            i += 1
    return results

# Process job_data INSERTs
count = 0
for m in re.finditer(r"INSERT INTO `job_data` VALUES (.+?);", content, re.DOTALL):
    values_text = m.group(1)
    rows = parse_values(values_text)
    for row in rows:
        if len(row) >= 10:
            vals = []
            for f in row[:11]:
                f = f.strip()
                if f.upper() == 'NULL':
                    vals.append(None)
                elif f.startswith("'") and f.endswith("'"):
                    vals.append(f[1:-1])
                elif f.startswith('"') and f.endswith('"'):
                    vals.append(f[1:-1])
                else:
                    vals.append(f)
            # Pad to 11 fields
            while len(vals) < 11:
                vals.append(None)
            try:
                cur.execute(
                    "INSERT IGNORE INTO job_data (job_id,name,salary,place,education,experience,company,label,scale,href,key_word) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    vals[:11]
                )
                count += 1
            except Exception as e:
                pass
    
    print(f"Processed {count} job_data rows...")

conn.commit()
print(f"Total job_data imported: {count}")

# Verify
cur.execute("SELECT COUNT(*) FROM job_data")
print(f"job_data in DB: {cur.fetchone()[0]}")

cur.execute("SELECT COUNT(*) FROM user_list")
print(f"user_list in DB: {cur.fetchone()[0]}")

cur.execute("SELECT COUNT(*) FROM user_expect")  
print(f"user_expect in DB: {cur.fetchone()[0]}")

cur.execute("SELECT COUNT(*) FROM send_list")
print(f"send_list in DB: {cur.fetchone()[0]}")

cur.close()
conn.close()
print("Done!")
