import SongLyricsAPI

api = SongLyricsAPI.SongLyrics()

# print("Song Lyrics API Command Line Interface(CLI)")
# song = input("Enter song name: ")
# artists = api.getArtists(song)

# print(*artists, sep="\n")

# if artists[0] != "Entered song is unavailable":
#     artist = input("\nEnter any artist name from above mentioned list: ")
#     lyrics = api.getLyrics(artist)
#     print(lyrics)
print(api.get("baby"))