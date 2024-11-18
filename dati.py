import sqlite3


conn = sqlite3.connect("dati.db", check_same_thread=False)

def skolenu_tabulas_izveide():
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE skoleni(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vards TEXT NOT NULL,
        uzvards TEXT NOT NULL
        )
        """
    )
    conn.commit()


def skolotaju_tabulas_izveide():
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE skolotaji(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vards TEXT NOT NULL,
        uzvards TEXT NOT NULL
        )
        """
    )
    conn.commit()

def prieksmetu_tabulas_izveide():
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE prieksmeti(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nosaukums TEXT NOT NULL
        )
        """
    )
    conn.commit()

def atzimju_tabulas_izveide():
    cur = conn.cursor()
    cur.execute("""
CREATE TABLE atzimes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    atzime INTEGER NOT NULL,
    skolena_id INTEGER NOT NULL,
    prieksmeta_id INTEGER NOT NULL,
    FOREIGN KEY (skolena_id) REFERENCES skoleni(id),
    FOREIGN KEY (prieksmeta_id) REFERENCES prieksmeti(id)
                )
    """)
    conn.commit()

def skolotaju_prieksmetu_tabulas_izveide():
    cur = conn.cursor()
    cur.execute("""
CREATE TABLE skolotajuPrieksmeti(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skolotaja_id INTEGER NOT NULL,
    prieksmeta_id INTEGER NOT NULL,
    FOREIGN KEY (skolotaja_id) REFERENCES skolotaji(id),
    FOREIGN KEY (prieksmeta_id) REFERENCES prieksmeti(id)
                )
    """)
    conn.commit()

# skolotaju_prieksmetu_tabulas_izveide()

# atzimju_tabulas_izveide()

# skolotaju_tabulas_izveide()

# skolenu_tabulas_izveide()

# prieksmetu_tabulas_izveide()

def pievienot_skolenu(vards, uzvards):
    print(vards, uzvards)
    cur = conn.cursor()
    cur.execute(
        f"""
        INSERT INTO skoleni(vards, uzvards) VALUES("{vards}","{uzvards}")
        """
    )
    conn.commit()


def pievienot_skolotaju(vards, uzvards):
    cur = conn.cursor()
    cur.execute(
    f"""
    INSERT INTO skolotaji(vards, uzvards) VALUES("{vards}","{uzvards}")
    """
    )
    conn.commit()

    print(vards, uzvards)

def pievienot_prieksmetu(prieksmets):
    cur = conn.cursor()
    cur.execute(
    f"""
    INSERT INTO prieksmeti(nosaukums) VALUES("{prieksmets}")
    """
    )
    conn.commit()




def iegut_skolenus():
    cur = conn.cursor()
    cur.execute(
        """SELECT vards, uzvards, id FROM skoleni"""
    )
    conn.commit()
    dati = cur.fetchall()
    return dati


def iegut_skolotajus():
    cur = conn.cursor()
    cur.execute(
        """SELECT vards, uzvards, id FROM skolotaji"""
    )
    conn.commit()
    dati = cur.fetchall()
    return dati

def iegut_prieksmetus():
    cur = conn.cursor()
    cur.execute(
        """SELECT nosaukums, id FROM prieksmeti"""
    )
    conn.commit()
    dati = cur.fetchall()
    return dati

def pievienot_atzimi(atzime, skolens, prieksmets):
    cur = conn.cursor()
    cur.execute(
    f"""
    INSERT INTO atzimes(atzime, skolena_id, prieksmeta_id) VALUES("{atzime}","{skolens}","{prieksmets}")
    """
    )
    conn.commit()

def iegut_atzimes():
    db = sqlite3.connect("skola.db")
    cursor = db.cursor()
    cursor.execute("""
        SELECT skoleni.vards, skoleni.uzvards, prieksmeti.nosaukums, atzimes.atzime 
        FROM atzimes
        JOIN skoleni ON atzimes.skolens_id = skoleni.id
        JOIN prieksmeti ON atzimes.prieksmets_id = prieksmeti.id
    """)
    atzimes = cursor.fetchall()
    db.close()
    return atzimes

def pievienot_skolotaju_prieksmetam(skolotajs, prieksmets):
    cur = conn.cursor()
    cur.execute(
    f"""
    INSERT INTO skolotajuPrieksmeti(skolotaja_id, prieksmeta_id) VALUES("{skolotajs}","{prieksmets}")
    """
    )
    conn.commit()

def iegut_skolotaju_prieksmetus():
    cur = conn.cursor()
    cur.execute(
        """SELECT vards, uzvards, nosaukums 
        FROM 
        (skolotajuPrieksmeti JOIN skolotaji ON skolotaji.id = skolotajuPrieksmeti.skolotaja_id)
        JOIN prieksmeti ON prieksmeti.id = skolotajuPrieksmeti.prieksmeta_id
        """
    )
    conn.commit()
    dati = cur.fetchall()
    return dati

def iegut_videjas_atzimes():
    db = sqlite3.connect("skola.db")
    cursor = db.cursor()
    cursor.execute("""
        SELECT skoleni.vards, skoleni.uzvards, prieksmeti.nosaukums, AVG(atzimes.atzime) as videja_atzime
        FROM atzimes
        JOIN skoleni ON atzimes.skolens_id = skoleni.id
        JOIN prieksmeti ON atzimes.prieksmets_id = prieksmeti.id
        GROUP BY skoleni.id, prieksmeti.id
    """)
    videjas = cursor.fetchall()
    db.close()
    return videjas