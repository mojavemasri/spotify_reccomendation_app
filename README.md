# spotifyreccomendationapp
NOTES:
I added spotifytrackID as well as trackID. Up to your discretion if you want to use both or just one. I added it because the spotify ones are long and hard to read, and the only reason we would need it is to reference the spotify api. The trackid can be implemented in SQL with autoincrement pk

The artist-genre junction table is used because artist-genre is a many many relationship.
The playlist-track junction table is used because playlist-track is a many many relationship.

genre and both the junction tables should also be implemented with autoincrement pk



Database Design:

ARTIST:
spotifyArtistID
artistName
artistPopularity

artistGenreJUNCTION:
junctionID
artistID
genreID


ALBUM:
albumID
artistID
albumName
numTracks
albumType
releaseDate

track:
trackID
spotifytrackID
albumID
artistID
genreID
trackName
trackLength(ms)
trackPopularity
explicit


GENRE:
genreID
genreName

USER:
userID
userName

LISTENING_HISTORY:
userID
trackID
listenLength

PLAYLIST:
playlistID
playlistName
numTracks

PLAYLIST_TRACK_JUNCTION:
juncID
playlistID
trackID
trackPlace


track_ATTRIBUTES:
spotifytrackID
danceability
energy
loudness
speechiness
acousticness
instrumentalness
liveness
valence

FILES LEFT TO IMPLEMENT:\
Reccomendation algo(Youssef)\
Database commands \
app



FUNCTIONS TO IMPLEMENT:\
Print functions for all attributes in printRecords.py


NOTES FOR THE FUTURE:\
Add a user table?\
Remove loudness from the attributes column(currently any new records inserted will have a 0 in that category)
