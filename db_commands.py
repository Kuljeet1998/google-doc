create_table_command = '''CREATE TABLE IF NOT EXISTS information (
                            id INT,
                            REVISION_ID INT,
                            URL VARCHAR(100),
                            CREATED TIMESTAMP,
                            START_TIME TIMESTAMP,
                            END_TIME TIMESTAMP,
                            AUTHOR VARCHAR(100),
                            DURATION INT,
                            NEW_CONTENT VARCHAR(1000),
                            COPY_PASTED INT,
                            PRIMARY KEY (id)
                            );'''

insert_command = '''INSERT INTO information (id,revision_id,url,created,start_time,end_time,author,duration,new_content,copy_pasted)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ;'''

get_latest_row_command = 'SELECT * FROM information ORDER BY created desc limit 1;'