import psycopg2
import config
def connect():
    try:
        conn = psycopg2.connect(config.PSQL_URL)
        print(True, 433434)
        return conn
    except:
        print('Can`t establish connection to database')


class Data_base:
    
    def add_user_breef(self, username: str, user_id: int, name: str, email: str, phone: int, message: str):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users_breef (username, id_user, full_name, email, phone_number, message_text) VALUES (%s, %s, %s, %s, %s, %s)", (username, user_id, name, email, phone, message))
        conn.commit()
        cursor.close()
        conn.close()
    
    def add_user_communi(self, username: str, user_id: int, phone: str, message: str):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users_communi (username, id_user, phone_number, message_text) VALUES (%s, %s, %s, %s)", (username, user_id, phone, message))    
        conn.commit()
        cursor.close()
        conn.close()

    def add_users_tap_bot(self, username: str, user_id: int, message: str) -> None:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users_tap_bot (username, id_user, message_text) VALUES (%s, %s, %s)", (username, user_id, message))
        conn.commit()
        cursor.close()
        conn.close()
