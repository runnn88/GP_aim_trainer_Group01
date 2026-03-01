import sqlite3
import datetime
import os

class Database:
    def __init__(self, db_name="aim_trainer.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        
    def create_table(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        schema_dir = os.path.join(current_dir, 'aim_trainer.sql')
        
        with open(schema_dir, 'r') as f:
            sql_script = f.read()
            
        self.cursor.executescript(sql_script)
        self.conn.commit()
    
    def insert_result(self, score, accuracy, avg_reaction, hits, misses, max_combo):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.cursor.execute('''
                            INSERT INTO GAME_STATS (PLAY_DATE, SCORE, ACCURACY, AVG_REACTION, HITS, MISSES, MAX_COMBO)
                            VALUES (?, ?, ?, ?, ?, ?, ?)''',
                            (now, score, accuracy, avg_reaction, hits, misses, max_combo))
        self.conn.commit()
        
    def get_best_record(self, limit=3):
        self.cursor.execute('''
                            SELECT PLAY_DATE, SCORE, ACCURACY, AVG_REACTION, MAX_COMBO
                            FROM GAME_STATS
                            ORDER BY SCORE DESC
                            LIMIT ?''', (limit,))
        return self.cursor.fetchall()
    
    def get_absolute_best_score(self):
        self.cursor.execute('''
                            SELECT MAX(SCORE), MAX(MAX_COMBO)
                            FROM GAME_STATS''')
        
        result = self.cursor.fetchone()
        best_score = result[0] if result[0] is not None else 0
        best_combo = result[1] if result[1] is not None else 0
        return best_score, best_combo