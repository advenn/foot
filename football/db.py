import psycopg2

class Database:
    def __init__(self,path='football.db'):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

    def connection(self):
        return self.conn

    def cursor(self):
        return self.cursor

    def create_table_game(self):
        sql = """CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            home_team TEXT,
            away_team TEXT,
            home_score INTEGER,
            away_score INTEGER,
            date TEXT,
            time TEXT,
        """
        self.cursor.execute(sql)



class Game:
    def __init__(self, home_team, away_team, home_score, away_score):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score

    def write(self):
        conn = sqlite3.connect('football.db')
        c = conn.cursor()
        c.execute("INSERT INTO games VALUES (?, ?, ?, ?)", (self.home_team, self.away_team, self.home_score, self.away_score))
        conn.commit()
        conn.close()