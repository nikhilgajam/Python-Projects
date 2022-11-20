import SongLyricsAPI

api = SongLyricsAPI.SongLyrics()

print("Song Lyrics API Command Line Interface(CLI)")
song = input("\nEnter song name: ")
artists = api.getArtists(song)

for i, j in enumerate(artists):
    print(str(i+1) + " " + j)

if artists[0] != "Entered song is unavailable":
    artist_number = int(input("\nEnter song or artist number: "))
    if artist_number < 1 or artist_number > len(artists):
        print("Enter the correct number shown on the screen")
    else:
        lyrics = api.getLyrics(artists[artist_number])
        print(lyrics)

print(api.get("baby"))   # Gets the first song in the list
