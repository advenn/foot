import asyncio

import asyncpg

from config import constants


class Database:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool = asyncpg.pool = loop.run_until_complete(asyncpg.create_pool(
            user=constants.DBUSER,
            password=constants.DBPASS,
            database=constants.DBNAME,
            host=constants.DBHOST,
            port=constants.DBPORT)
        )

    async def create_tables(self):
        user_sql = """
        CREATE TABLE IF NOT EXISTS "User" (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );            
        """
        tour_sql = """
        CREATE TABLE IF NOT EXISTS Tour (
            id SERIAL PRIMARY KEY,
            number integer NOT NULL,
            is_active boolean NOT NULL DEFAULT false,
            start_time TIMESTAMP NOT NULL,
            deadline TIMESTAMP NOT NULL
            );            
            """
        upcoming_match_sql = """
        CREATE TABLE IF NOT EXISTS UpcomingMatch (
            id SERIAL PRIMARY KEY,
            tour_id integer,
            home_team VARCHAR(255) NOT NULL,
            away_team VARCHAR(255) NOT NULL,
            CONSTRAINT fk_tour
                FOREIGN KEY(tour_id) 
                    REFERENCES Tour(id) 
                        ON DELETE SET NULL );"""
        predict_sql = """
        CREATE TABLE IF NOT EXISTS Predict (
            id SERIAL PRIMARY KEY,
            match_id integer,
            user_id integer,
            home_score integer,
            away_score integer,
            date TIMESTAMP NOT NULL DEFAULT NOW(),
            CONSTRAINT fk_match
                FOREIGN KEY(match_id) 
                    REFERENCES UpcomingMatch(id)
                        ON DELETE SET NULL,
            CONSTRAINT fk_user
                FOREIGN KEY(user_id) 
                    REFERENCES "User"(id)
                        ON DELETE SET NULL 
            );
            """
        true_score_sql = """
        CREATE TABLE IF NOT EXISTS TrueScore (
            id SERIAL PRIMARY KEY,
            match_id integer UNIQUE NOT NULL,
            home_score integer,
            away_score integer,
            proportional integer,
            date TIMESTAMP NOT NULL DEFAULT NOW(),
            CONSTRAINT fk_match
                FOREIGN KEY(match_id) 
                    REFERENCES UpcomingMatch(id)
                        ON DELETE SET NULL 
            );"""

        rate_sql = """
        CREATE TABLE IF NOT EXISTS Rate (
            id SERIAL PRIMARY KEY,
            user_id integer UNIQUE NOT NULL,
            score integer default 0,
            date TIMESTAMP NOT NULL DEFAULT NOW(),
            CONSTRAINT fk_user
                FOREIGN KEY(user_id) 
                    REFERENCES "User"(id)
                        ON DELETE SET NULL
            );
            """
        await self.pool.execute(user_sql)
        await self.pool.execute(tour_sql)
        await self.pool.execute(upcoming_match_sql)
        await self.pool.execute(predict_sql)
        await self.pool.execute(true_score_sql)
        await self.pool.execute(rate_sql)

    # for sql in [user_sql, tour_sql, upcoming_match_sql, predict_sql, true_score_sql, rate_sql]:
    #     try:
    #         await self.pool.execute(sql)
    #     except Exception as e:
    #         print(e)

    async def create_user(self, username, password, email):
        try:
            await self.pool.execute(
                'INSERT INTO "User" (username, password, email) VALUES ($1, $2, $3)',
                username, password, email)
        except Exception as e:
            print(e)

    async def add_tour(self, number, is_active, start_time, deadline):
        try:
            await self.pool.execute(
                'INSERT INTO Tour (number, is_active, start_time, deadline) VALUES ($1, $2, $3, $4)',
                number, is_active, start_time, deadline)
        except Exception as e:
            print(e)

    async def add_match(self, tour_id, home_team, away_team):
        try:
            await self.pool.execute(
                'INSERT INTO UpcomingMatch (tour_id, home_team, away_team) VALUES ($1, $2, $3)',
                tour_id, home_team, away_team)
        except Exception as e:
            print(e)

    async def add_predict(self, match_id, user_id, home_score, away_score):
        try:
            await self.pool.execute(
                'INSERT INTO Predict (match_id, user_id, home_score, away_score) VALUES ($1, $2, $3, $4)',
                match_id, user_id, home_score, away_score)
        except Exception as e:
            print(e)

    async def add_true_score(self, match_id, home_score, away_score, proportional):
        try:
            await self.pool.execute(
                'INSERT INTO TrueScore (match_id, home_score, away_score, proportional) VALUES ($1, $2, $3, $4)',
                match_id, home_score, away_score, proportional)
        except Exception as e:
            print(e)

    async def add_rate(self, user_id, match_id, score):
        try:
            await self.pool.execute(
                'INSERT INTO Rate (user_id, match_id, score) VALUES ($1, $2, $3)',
                user_id, match_id, score)
        except Exception as e:
            print(e)

    async def update_rate(self, user_id, score):
        try:
            await self.pool.execute(
                'UPDATE Rate SET score = score + $1 WHERE user_id = $2',
                score, user_id)
        except Exception as e:
            print(e)

    async def change_tour_activity(self, tour_id, is_active):
        try:
            await self.pool.execute(
                'UPDATE Tour SET is_active = $1 WHERE id = $2',
                is_active, tour_id)
        except Exception as e:
            print(e)

    async def update_user_predict(self, user_id, match_id, home_score, away_score):
        try:
            await self.pool.execute(
                'UPDATE Predict SET home_score = $1, away_score = $2 WHERE user_id = $3 AND match_id = $4',
                home_score, away_score, user_id, match_id)
        except Exception as e:
            print(e)


# loop = asyncio.get_event_loop()
# db = Database(loop)
# loop.run_until_complete(db.create_tables())
