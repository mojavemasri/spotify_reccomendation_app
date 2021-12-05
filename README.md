# spotifyreccomendationapp
NOTES:
I added spotifySongID as well as songID. Up to your discretion if you want to use both or just one. I added it because the spotify ones are long and hard to read, and the only reason we would need it is to reference the spotify api

The junction table is used because artist-genre is a many many relationship.

Database Design:

ARTIST:
spotifyArtistID,
artistName,
artistPopularity,

JUNCTION:
junctionID,
artistID,
genreID


ALBUM:
albumID,
artistID,
albumName,
numTracks,
albumType,
releaseDate

SONG:
songID,
spotifySongID,
albumID,
artistID,
genreID,
songName,
songLength(ms),
songPopularity,
explicit


GENRE:
genreID,
genreName

USER:
userID,
userName

LISTENING_HISTORY:
userID,
songID,
listenLength


SONG_ATTRIBUTES:
songID,
spotifySongID,
danceability,
energy,
loudness,
speechiness,
acousticness,
instrumentalness,
liveness,
valence
