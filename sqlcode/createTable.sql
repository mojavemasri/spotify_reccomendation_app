CREATE DATABASE IF NOT EXISTS spotifyDB;
USE spotifyDB;
CREATE TABLE artist(
artistID VARCHAR(22) NOT NULL PRIMARY KEY,
artistName VARCHAR(100),
artistPopularity Integer
);
CREATE TABLE album(
albumID VARCHAR(22) NOT NULL PRIMARY KEY,
artistID VARCHAR(22) NOT NULL UNIQUE,
albumName VARCHAR(140) NOT NULL,
numTracks Integer,
albumType VARCHAR(30),
releaseDate Date,
CONSTRAINT FK_albumID_artistID FOREIGN KEY (artistID) REFERENCES artist(artistID)
);
CREATE TABLE track(
trackID VARCHAR(22) NOT NULL UNIQUE PRIMARY KEY,
albumID VARCHAR(22) NOT NULL UNIQUE,
artistID VARCHAR(22) NOT NULL UNIQUE,
trackName VARCHAR(140) NOT NULL,
trackLength Float,
trackPopularity Integer,
explicit Boolean,
CONSTRAINT FK_trackID_albumID FOREIGN KEY (albumID) REFERENCES album(albumID),
CONSTRAINT FK_trackID_artistID FOREIGN KEY (artistID) REFERENCES artist(artistID)
);
CREATE TABLE genre(
genreID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
genreName VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE playlist(
playlistID VARCHAR(22) NOT NULL PRIMARY KEY,
playlistName VARCHAR(100),
numTracks Integer
);

CREATE TABLE ptjunction(
ptID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
playlistID VARCHAR(22) NOT NULL,
trackID VARCHAR(22) NOT NULL,
CONSTRAINT FK_ptID_trackID FOREIGN KEY (trackID) REFERENCES track(trackID),
CONSTRAINT FK_ptID_playlistID FOREIGN KEY (playlistID) REFERENCES playlist(playlistID)
);

CREATE TABLE gajunction(
gaID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
genreID Integer NOT NULL,
artistID VARCHAR(22) NOT NULL,
CONSTRAINT FK_gaID_artistID FOREIGN KEY (artistID) REFERENCES artist(artistID),
CONSTRAINT FK_ptID_genreID FOREIGN KEY (genreID) REFERENCES genre(genreID)
);

CREATE TABLE track_ATTRIBUTES
(
  trackID CHAR(22) PRIMARY KEY UNIQUE NOT NULL,
  danceability FLOAT,
  energy FLOAT,
  loudness FLOAT,
  speechiness FLOAT,
  acousticness FLOAT,
  instrumentalness FLOAT,
  liveness FLOAT,
  valence FLOAT

);
