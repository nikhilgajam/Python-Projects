import urllib.request as req
import html

class SongLyrics:
    def __init__(self):
        self.title_url_values = []
        self.artist_names = []


    def get(self, song_name):
        # This method will get the first song and returns it
        artists = self.getArtists(song_name)

        if artists[0] == 'Entered song is unavailable':
            return "Entered song is unavailable"
        else:
            lyrics_string = self.getLyrics(artists[0])
            return lyrics_string

    
    def getArtists(self, song_name):
        # Converting spaces to html equivalent
        song_name = song_name.replace(" ", "+")

        # Retrieving the yahoo search page
        try:
            raw = str(req.urlopen("https://search.yahoo.com/search?p=" + song_name + "+site%3Aazlyrics.com").read(), "utf-8")
        except Exception as e:
            return ["Check Your Internet Connection", ]
        # raw = raw.replace("\n", "")

        # Unescaping the html entities
        raw = html.unescape(raw)

        # print(raw)
        

        # Declaring variables
        start = 0
        end = 0

        # Song data storing list
        data = []

        # Storing the actual url and artist in the list
        while True:
            start = raw.find('" href="https://www.azlyrics.com/lyrics/', end+1)
            end = raw.find('</a></h3>', start)

            if start == -1 or end == -1:  # If string is not found then break the loop
                break

            data.append(raw[start+8:end])  # Adding data to the data list

        # print(*data, sep="\n")
        # Title and url storing dictionary
        title_url_values = {}

        # Storing the title and url in dictionary
        for i in data:
            start = i.find('</span></span>')
            if " | AZLyrics.com" in i:
                end = i.find(" | AZLyrics.com")
            elif " | Lyrics at AZLyrics.com" in i:
                end = i.find(" | Lyrics at AZLyrics.com")
            else:
                end = len(i)
            title = i[start+14:end]

            start = 0
            end = i.find('"', start+1)
            url = i[start:end]

            title_url_values[title] = url
        
        # Making the local dictionary as global dictionary
        self.title_url_values = title_url_values

        # Handling unavailable songs
        if len(title_url_values) == 0:
            self.artist_names = ["Entered song is unavailable"]
            return self.artist_names

        # Returning artist or keys of the dictionary as a list
        self.artist_names = list(self.title_url_values.keys())
        return self.artist_names

    
    def getLyrics(self, artist_name):
        # Returns a message if this method is executed first
        if len(self.title_url_values) == 0:
            return "Use the getArtist method first and getLyrics method next"

        if artist_name not in self.title_url_values:
            return "Enter only the mentioned artist names"

        if self.artist_names[0] == "Entered song is unavailable":
            return "Enter any available song please"

        if self.artist_names[0] == "Check Your Internet Connection":
            return "Check Your Internet Connection"

        # Taking url by using artist
        artist_song_url = self.title_url_values[artist_name]

        # Retriving the lyricsfreak song page
        try:
            raw = str(req.urlopen(artist_song_url).read(), "utf-8")
        except Exception as e:
            return "Check Your Internet Connection"

        # Taking the song starting line by eliminating unwanted html script
        start = raw.find('that. -->')
        end = raw.find("</div>", start+1)

        lyrics = raw[start:end]

        # Removing the unwanted div, removing whitespaces from first and last
        lyrics = lyrics[lyrics.find(">")+2:].strip()
        # Unescaping the html entities
        lyrics = html.unescape(lyrics)
        # Replacing the break and italic tags with null string
        lyrics = lyrics.replace("<br>", "")
        lyrics = lyrics.replace("<i>", "")
        lyrics = lyrics.replace("</i>", "")


        # Returning the lyrics
        return lyrics
