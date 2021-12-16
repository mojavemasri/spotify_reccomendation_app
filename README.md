# spotifyreccomendationapp
README

REPO LINK: 
https://github.com/yhegab/mgsc532finalproject

SUMMARY:  
My project seeks to use a Genetic Algorithm to generate music reccomendations. In this project, I use the Spotify API as well as my own database in order to implement this as an app. My app gives several menu options to the user, specifically the option to get reccomendations. Once selected, the app prompts the user to enter a playlist url, and once taken in will ask the user about specifications for their playlist(minimum and maximum artist popularity, playlist style, etc) and will then generate a sample population based on these preferences. At this stage the app runs the GA, and will print a playlist from the samples it got.  

The fitness of the algorithm is based on the track attributes, which is something Spotify created for each track. Each track attribute describes a sonic aspect of a track(energy, danceability, etc) by assignint it a value from 0 to 1 indicating how much of said quality a track has. The actual fitness is determined based on the variance of each attribute in a playlist, and the avg value of an attribute in a playlist, each of these values are weighted.  

The selection is done using a tournament select.  

All of the GA functionality is done in the reccomendation.py file inside the pythoncode folder. Within this, the runGA() function is where the main driver of the GA is.


REQUIRED INSTALLS:  
pip3 install spotipy --upgrade  
pip3 install mysql-connector-python  

RUN THE CODE:
After cloning the repo(or unzipping the folder), cd into the folder and run the command "python3 pythoncode/app.py"  
Once you run that, select the "reccomendations" menu option and follow the prompts.  
The app will prompt you to enter your own spotify playlists to get a reccomendation. In case you don't use spotify, I will include some of my own playlists below for you to run(don't judge my music taste haha)  
I have included some sample text chunk inputs you can run instead of having to select all the different options, just so you can see the genetic algorithm run without having to do all the commands.  

EXAMPLE COMMAND 1:  
python3 pythoncode/app.py  
3  
1  
https://open.spotify.com/playlist/4LnQEJS9WuX5rhBa3JMnWm?si=cf220acb902b4f89  
60  
10  
65  
10  
1  

EXAMPLE COMMAND 2:  
python3 pythoncode/app.py  
3  
1  
https://open.spotify.com/playlist/7bXzIXuxZtVTwd28IeJQdd?si=a1a2da5a7a064cbc  
60  
10  
65  
10  
2  


SPOTIFY PLAYLISTS:  
https://open.spotify.com/playlist/5Z6UzaQDxgC9xrChuAA6DM?si=76f1630c5e0b4588
https://open.spotify.com/playlist/40FRYg4xxA7co7lAeCdrh8?si=1d5e97e4a9044bdf
https://open.spotify.com/playlist/7gFEStua1YiLRQWTBOXYtU?si=c583dc28cec749a1
https://open.spotify.com/playlist/6EAhari7eVE7UWy0GiuJ16?si=d80f98d516a14092



