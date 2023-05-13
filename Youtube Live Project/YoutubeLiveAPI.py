import urllib.request as req

class YoutubeLive:
    def getList(self, keyword: str):
        try:
            # Converting the space to + symbol
            keyword = keyword.replace(' ', '+')
            link = 'https://www.youtube.com/results?search_query=' + keyword + '&sp=CAMSAkAB'

            # Getting the data from the internet
            raw = str(req.urlopen(link).read(), "utf-8")

            # Declaring variables
            start = 0
            end = 0

            # Song data storing list
            data = {}

            # Storing the actual url and artist in the list
            while True:
                start = raw.find('}]},"title":{"runs":[{"text":"', end+1)
                end = raw.find('"}],', start)

                title = raw[start+30:end]

                start = raw.find('}},"watchEndpoint":{"videoId":"', end+1)
                end = raw.find('","params":', start+1)

                video_id = 'https://www.youtube.com/embed/' + raw[start+31:end]  # https://www.youtube.com/embed/VIDEOID

                if video_id in data.values():
                    break

                if start == -1 or end == -1:  # If string is not found then break the loop
                    break

                data[title] =video_id  # Adding data to the data dictionary

            return data
        
        except Exception as e:
            return "Check Your Internet Connection"


if __name__ == '__main__':
    yt = YoutubeLive()
    print(yt.getList("telugu news"))