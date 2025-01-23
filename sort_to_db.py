import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

# Konfigurer tilkoblingsparametrene
server = os.getenv('DB_SERVER')  # Endre eventuelt til riktig server og instansnavn
database = os.getenv('DB_DATABASE')  # Navn på databasen
username = os.getenv('DB_USERNAME')  # Bruk rå streng for å unngå escape-sekvens problemer
password = ''  # Angi passordet ditt hvis nødvendig

# Koble til databasen
conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
cursor = conn.cursor()

# Opprett tabeller (om de ikke allerede finnes)
cursor.execute('''
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Teams')
BEGIN
    CREATE TABLE Teams (TeamID INT PRIMARY KEY IDENTITY(1,1), TeamNavn NVARCHAR(100) UNIQUE)
END
''')

cursor.execute('''
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Elever')
BEGIN
    CREATE TABLE Elever (ElevID INT PRIMARY KEY IDENTITY(1,1), Navn NVARCHAR(100), TeamID INT, FOREIGN KEY (TeamID) REFERENCES Teams (TeamID))
END
''')

# Les fra tekstfilen og strukturer dataene
current_team = None

with open('jeg er uorganisert.txt', 'r', encoding='utf-8') as f:
    for line in f:
        stripped_line = line.strip()

        if stripped_line.startswith("Team"):  # This indicates a new team
            current_team = stripped_line  # Store the team name
            cursor.execute('INSERT INTO Teams (TeamNavn) VALUES (?)', (current_team,))
            cursor.execute('SELECT TeamID FROM Teams WHERE TeamNavn = ?', (current_team,))
            team_id = cursor.fetchone()[0]

        elif stripped_line and line.startswith('\t'):  # This line starts with a tab and is a potential student name
            elev_navn = stripped_line.lstrip()  # Remove leading whitespace
            
            # Check if the student's name has more than one word
            if len(elev_navn.split()) > 1:  # At least two words for a valid name
                cursor.execute('INSERT INTO Elever (Navn, TeamID) VALUES (?, ?)', (elev_navn, team_id))

# Lagre endringer og lukk forbindelsen
conn.commit()
cursor.close()
conn.close()