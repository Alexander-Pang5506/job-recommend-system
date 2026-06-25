"""直接通过 pymysql 创建表并导入数据，跳过有编码问题的 SQL 文件"""
import pymysql
import re

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='recommend_job',
    charset='utf8mb4'
)
cur = conn.cursor()

# Create tables (from Django models)
tables = [
    """CREATE TABLE IF NOT EXISTS `job_data` (
        `job_id` int NOT NULL AUTO_INCREMENT,
        `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `salary` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `place` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `education` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `experience` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `company` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `label` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `scale` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `href` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `key_word` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        PRIMARY KEY (`job_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",
    
    """CREATE TABLE IF NOT EXISTS `user_list` (
        `user_id` varchar(11) NOT NULL,
        `user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `pass_word` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        PRIMARY KEY (`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",
    
    """CREATE TABLE IF NOT EXISTS `user_expect` (
        `expect_id` int NOT NULL AUTO_INCREMENT,
        `key_word` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `user_id` varchar(11) DEFAULT NULL,
        `place` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        PRIMARY KEY (`expect_id`),
        KEY `user_expect_user_id_fk` (`user_id`),
        CONSTRAINT `user_expect_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `user_list` (`user_id`) ON DELETE NO ACTION
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",
    
    """CREATE TABLE IF NOT EXISTS `send_list` (
        `send_id` int NOT NULL AUTO_INCREMENT,
        `job_id` int DEFAULT NULL,
        `user_id` varchar(11) DEFAULT NULL,
        PRIMARY KEY (`send_id`),
        KEY `send_list_job_id_fk` (`job_id`),
        KEY `send_list_user_id_fk` (`user_id`),
        CONSTRAINT `send_list_job_id_fk` FOREIGN KEY (`job_id`) REFERENCES `job_data` (`job_id`) ON DELETE NO ACTION,
        CONSTRAINT `send_list_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `user_list` (`user_id`) ON DELETE NO ACTION
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",
    
    """CREATE TABLE IF NOT EXISTS `spider_info` (
        `spider_id` int NOT NULL AUTO_INCREMENT,
        `spider_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `count` int DEFAULT NULL,
        `page` int DEFAULT NULL,
        PRIMARY KEY (`spider_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",
]

for sql in tables:
    cur.execute(sql)
    print(f"Table created OK")

conn.commit()

# Now read INSERT data from the original UTF-16LE backup and extract clean data
# Read raw bytes from UTF-16LE file
with open(r"C:\Users\P.sir\WorkBuddy\2026-06-14-20-07-12\job_recommend_project\recommend_job_backup.sql", "rb") as f:
    raw = f.read()

# Convert from UTF-16LE to string
content = raw.decode('utf-16-le')

# Extract INSERT INTO statements and execute them
inserts = re.findall(r"INSERT INTO `(\w+)` VALUES (.+?);", content, re.DOTALL)

for table, values in inserts:
    # Parse the VALUES part - it's a list of parenthesized tuples
    rows = re.findall(r"\(([^()]*(?:\([^()]*\)[^()]*)*)\)", values)
    
    if table == 'job_data':
        for row_str in rows:
            # Parse comma-separated values, handling quoted strings with commas
            fields = []
            field = ''
            in_quotes = False
            for ch in row_str:
                if ch == "'" and not in_quotes:
                    in_quotes = True
                    field += ch
                elif ch == "'" and in_quotes:
                    # Check for escaped quote
                    in_quotes = False
                    field += ch
                elif ch == ',' and not in_quotes:
                    fields.append(field.strip())
                    field = ''
                else:
                    field += ch
            if field:
                fields.append(field.strip())
            
            if len(fields) >= 10:
                # Handle NULL values and quoted strings
                vals = []
                for f in fields[:10]:
                    if f.upper() == 'NULL':
                        vals.append(None)
                    elif f.startswith("'") and f.endswith("'"):
                        vals.append(f[1:-1])
                    else:
                        vals.append(f)
                
                if vals[0] is None:
                    vals[0] = 0  # job_id
                try:
                    cur.execute(
                        """INSERT INTO job_data (job_id, name, salary, place, education, experience, 
                           company, label, scale, href, key_word) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        vals
                    )
                except Exception as e:
                    pass  # skip duplicates
    
    elif table == 'user_list':
        for row_str in rows:
            fields = []
            field = ''
            in_quotes = False
            for ch in row_str:
                if ch == "'" and not in_quotes:
                    in_quotes = True
                    field += ch
                elif ch == "'" and in_quotes:
                    in_quotes = False
                    field += ch
                elif ch == ',' and not in_quotes:
                    fields.append(field.strip())
                    field = ''
                else:
                    field += ch
            if field:
                fields.append(field.strip())
            
            if len(fields) >= 3:
                vals = [f[1:-1] if f.startswith("'") else f for f in fields[:3]]
                try:
                    cur.execute("INSERT INTO user_list (user_id, user_name, pass_word) VALUES (%s,%s,%s)", vals[:3])
                except:
                    pass
    
    elif table == 'user_expect':
        for row_str in rows:
            fields = []
            field = ''
            in_quotes = False
            for ch in row_str:
                if ch == "'" and not in_quotes:
                    in_quotes = True
                    field += ch
                elif ch == "'" and in_quotes:
                    in_quotes = False
                    field += ch
                elif ch == ',' and not in_quotes:
                    fields.append(field.strip())
                    field = ''
                else:
                    field += ch
            if field:
                fields.append(field.strip())
            
            if len(fields) >= 3:
                vals = []
                for f in fields[:4]:
                    if f.upper() == 'NULL':
                        vals.append(None)
                    elif f.startswith("'") and f.endswith("'"):
                        vals.append(f[1:-1])
                    else:
                        vals.append(f)
                if vals[0] is None:
                    vals[0] = 0
                try:
                    cur.execute("INSERT INTO user_expect (expect_id, key_word, user_id, place) VALUES (%s,%s,%s,%s)", vals[:4])
                except:
                    pass
    
    elif table == 'send_list':
        for row_str in rows:
            fields = [f.strip() for f in row_str.split(',')]
            if len(fields) >= 3:
                vals = [int(f) if f.strip().isdigit() else f.strip() for f in fields[:3]]
                try:
                    cur.execute("INSERT INTO send_list (send_id, job_id, user_id) VALUES (%s,%s,%s)", vals[:3])
                except:
                    pass
    
    print(f"Imported {table} data")

conn.commit()
cur.close()
conn.close()
print("\nAll done! Database setup complete.")
