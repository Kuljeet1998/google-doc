create_table_command = '''CREATE TABLE IF NOT EXISTS information (
                            id INT,
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

insert_command = '''INSERT INTO information (url,created,start_time,end_time,author,duration,new_content,copy_pasted)
                    VALUES ({url},{created},{start_time},{end_time},{author},{duration},{new_content},{copy_pasted})
                    ;'''