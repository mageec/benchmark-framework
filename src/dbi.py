import os
import sqlite3

class DBi:
    def __init__(self, db_loc, username=None, password=None, socket=None):
        self.db_dir, self.db_file = os.path.split(db_loc)
        self.db_loc = db_loc

        if not self.__db_dir_exists():
            os.makedirs(os.path.abspath(self.db_dir))

        if not self.__db_is_setup():
            self.__setup_db()

    def fetch(self, run_id):
        with self:
            self.cursor.execute("SELECT time, energy FROM results WHERE run_id = ?;", (run_id,))
            return self.cursor.fetchall()

    def record(self, run_id, results):
        with self:
            for result in results:
                self.cursor.execute("INSERT INTO results(run_id, time, energy) VALUES(?, ?, ?);", (run_id,) + result)
            self.connection.commit()

    def add_run(self, benchmark, compiler, platform, flags):
        return self.__create_run(benchmark, compiler, platform, flags)

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_loc)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, type, value, traceback):
# It's not our responsibility to commit. This should be done where changes are
# made
        self.connection.close()

    def __setup_db(self):
        connection = sqlite3.connect(self.db_loc)
        cursor = connection.cursor()
        to_exec  = "CREATE TABLE runs("
        to_exec += "run_id INTEGER PRIMARY KEY,"
        to_exec += "benchmark VARCHAR(50),"
        to_exec += "compiler VARCHAR(50),"
        to_exec += "platform VARCHAR(50)"
        to_exec += ");"
        cursor.execute(to_exec)

        to_exec  = "CREATE TABLE flags ("
        to_exec += "flag_id INTEGER PRIMARY KEY,"
        to_exec += "flag VARCHAR(50)"
        to_exec += ");"
        cursor.execute(to_exec)

        to_exec  = "CREATE TABLE run_flags ("
        to_exec += "run_id INTEGER,"
        to_exec += "flag_id INTEGER,"
        to_exec += "PRIMARY KEY (run_id, flag_id),"
        to_exec += "FOREIGN KEY (run_id) REFERENCES runs,"
        to_exec += "FOREIGN KEY (flag_id) REFERENCES flags"
        to_exec += ");"
        cursor.execute(to_exec)

        to_exec  = "CREATE TABLE results ("
        to_exec += "id INTEGER PRIMARY KEY,"
        to_exec += "run_id INTEGER,"
        to_exec += "time INT,"
        to_exec += "energy REAL,"
        to_exec += "FOREIGN KEY (run_id) REFERENCES runs"
        to_exec += ");"
        cursor.execute(to_exec)

        connection.commit()
        cursor.close()
        connection.close()

    def __db_dir_exists(self):
        return (self.db_dir == '') or os.path.isdir(self.db_dir)

    def __db_is_setup(self):
        try:
            connection = sqlite3.connect(self.db_loc)
        except sqlite3.OperationalError:
            connection.close()
            return False

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM runs LIMIT 1;")
        except sqlite3.OperationalError:
            return False
        finally:
            cursor.close()
            connection.close()
        return True

    def __gen_run_id(self):
        pass

    def __existing_run(self, benchmark, compiler, platform, flags):
        with self:
            to_exec  = "SELECT run_id FROM runs WHERE "
            to_exec += "benchmark = ?"
            to_exec += " AND compiler = ?"
            to_exec += " AND platform = ?;"
            self.cursor.execute(to_exec, (benchmark, compiler, platform))
            potential_runs = [x[0] for x in self.cursor.fetchall()]

#TODO: Speed up
            flag_set = set(flags)
            len_flags = len(flags)
            for run_id in potential_runs:
                self.cursor.execute("SELECT flag FROM (SELECT * FROM run_flags WHERE run_id = ?) NATURAL JOIN flags;", (str(run_id),))
                out_flags = [x[0] for x in self.cursor.fetchall()]
                if flag_set == set(out_flags) and len_flags == len(out_flags):
                    return run_id
        return None

    def __create_run(self, benchmark, compiler, platform, flags):
        with self:
            self.cursor.execute("INSERT INTO runs(benchmark, compiler, platform) VALUES (?, ?, ?);", (benchmark, compiler, platform))
            run_id = self.cursor.lastrowid
            for flag in flags:
                self.cursor.execute("INSERT INTO flags(flag) VALUES (?);", (flag,))
                flag_id = self.cursor.lastrowid
                self.cursor.execute("INSERT INTO run_flags VALUES (?, ?);", (run_id, flag_id))
            self.connection.commit()
            return run_id
