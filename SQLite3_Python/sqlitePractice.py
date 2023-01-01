# SQL NOTES
import sqlite3

connection = sqlite3.connect("aquarium.db")

# Cursor is an object which allows us to send and manipulate SQL commands as strings.
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS fish")
cursor.execute("CREATE TABLE IF NOT EXISTS fish (id INTEGER PRIMARY KEY, name TEXT, species TEXT, tank_number INTEGER)")

for each in [('Sammy', 'shark', 1), ('Jamie', 'cuttlefish', 7), ('Jax', 'Octopus', 7)]:
    cursor.execute("INSERT INTO fish (name, species, tank_number) VALUES (?, ?, ?)", each)
                                            # Cannot use ? and (tuple,) instead of (?, ?, ?)

cursor.execute("DELETE FROM fish WHERE name = ?", ("Sammy",)) #Ensure that values are always passed in as a tuple!
cursor.execute("UPDATE fish SET tank_number = ? WHERE name = ?" (3, "Jax"))
cursor.execute("UPDATE fish SET species = 'Micheal Jackson' WHERE name LIKE 'J%'")
connection.commit() # Update database with changes
rows = cursor.execute("SELECT * FROM fish").fetchall() # Select all from fish


# SQL Practice Question
''' QUESTION WRITTEN BY RICHARD MOTORGEANU (https://github.com/Multipixels)
    ANSWER WRITTEN BY MYSELF
Implement the function `getSongDict(database)` that will return a dictionary with the relevant data from the database.
The dictionary will have the following format.

The key for each entry should be its trackid (as a string). Value is a dictionary of relevant data.

{
    trackid (string): {
        'trackname': string,
        'genre': string,
        'genreid': int,
        'composer': string,
        'album': {
            'albumtitle': string,
            'artistname': string
         }
    },
    trackid (string): {
        'trackname': string,
        'genre': string,
        'genreid': int,
        'composer': string,
        'album': {
            'albumtitle': string,
            'artistname': string
         }
    }
}
'''
import sqlite3

def getSongDict(database):
    
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    trackParse = cursor.execute(
        "SELECT TrackId, tracks.Name, genres.Name, tracks.GenreId, Composer, albums.Title, artists.Name \
        FROM tracks, genres, albums, artists \
        WHERE tracks.GenreId = genres.GenreId \
        AND tracks.AlbumId = albums.AlbumId \
        AND albums.ArtistId = artists.ArtistId"
        ).fetchall()

    connection.close()

    return { str(each[0]): {
             'trackname': each[1],
             'genre': each[2],
             'genreid': each[3],
             'composer': each[4],
             'album': {'albumtitle': each[5], 'artistname': each[6]},
            } for each in trackParse }

print(getSongDict("chinook.db"))