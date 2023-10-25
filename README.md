﻿# venushacks2023
The graphical user interface of the program was designed using HTML code, carefully designed to catch the user's attention. It used Spotify's green color scheme as well as a cow print background, inspired from the title of the product. On their screen, the user would first see a page to log into their Spotify account, where they can grant the program access to their library of top streamed artists. After this, the user would see on their screen the various buttons representing possible moods. These moods were determined from researching about Spotify's dictionary of genres, ranging from "singer-songwriter" to "house" to "reggae." These genres were categorized in MooDY 4 MooSIC as different moods, such as "happy" and "main character," to provide a variety of interesting options for the user. These categories would be keywords to eventually use for determining the final playlist, as well as become an initial filter for the user's top artists. The only top artists used to make the music recommendations would be the top artists with genres that the user's mood matched with.

After the user would click on one of these buttons, they would immediately see a list of their top ten artists. The term "top artists" refer to the user's most listened to artists. MooDY 4 MooSIC then uses the user's top ten artists to find related artists. The Spotify API determines "related artists" based on an artist ID, as provided by the backend. The user's chosen mood will then be sent from the frontend to the backend, and is used to query related artists to only include genres matching their mood's keyword. With these filtered artists, MooDY 4 MooSIC randomly selects one song from each artist, and these songs are added to a new playlist. This completed playlist is immediately synchronized into the user's Spotify account.
