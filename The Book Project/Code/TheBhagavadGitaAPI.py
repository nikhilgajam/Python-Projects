from urllib.request import Request, urlopen
import re

class TheBhagavadGita:
    # Chapter and verse ranges
    chp_ver_nos = {0:0, 1:47, 2:72, 3:43, 4:42, 5:29, 6:47, 7:30, 8:28, 9:34, 10:42, 11:55, 12:20, 13:35, 14:27, 15:20, 16:24, 17:28, 18:78}

    def getData(self, chapter_no: int, verse_no: int, language="en"):
        if chapter_no >= 0 and chapter_no <= 18:
            if verse_no >= 0 and verse_no <= self.chp_ver_nos[chapter_no]:
                if language in ("hi", "te", "en"):
                    self.chapter_no = str(chapter_no)
                    self.verse_no = str(verse_no)
                    self.language = str(language)
                    return self.__work()
                else:
                    return 'You can only give "hi" = Hindi or "te" = Telugu to the language parameter'
            else:
                return 'You can only enter 0-' + str(self.chp_ver_nos[chapter_no]) + " verse numbers for chapter " + str(chapter_no)
        else:
            return 'Check chapter number it should be in the range (1-18)'

    def __work(self):
        raw_data = self.__getPage()
        raw_data = raw_data.replace("\n", "")
        # Writing raw data
        # with open("a.html", "w", encoding="utf-8") as p:
        #     p.write(raw_data)
        data = ""
        start = 0
        end = 0

        if self.chapter_no == '0':
            temp = "Data/Introduction/"
            if self.language == "":
                temp += "Chapter_0_English.txt"
            elif self.language == "hi":
                temp += "Chapter_0_Hindi.txt"
            elif self.language == "te":
                temp += "Chapter_0_Telugu.txt"
            
            with open(temp, "r", encoding="utf-8") as p:
                data += p.read()
            
            return data

        elif self.chapter_no != '0' and self.verse_no == '0':
            # Extracting the title
            start = raw_data.find("<h1")
            end = raw_data.find("</h1>", start)
            data += "=== " + raw_data[start:end] + " ===\n"

            # Extracting the description
            start = raw_data.find("<p", end)
            end = raw_data.find("</p>", start)
            data += "== " + raw_data[start:end] + " ==\n\n"

            # Extracting the introduction
            start = raw_data.find('<div class="chapterIntro">', end)
            end = raw_data.find('</div>', start)
            data += raw_data[start:end].replace("</p>", "\n")
        
        else:
            # Extracting the heading
            start = raw_data.find("<h1")
            start = raw_data.find(">", start)+1
            end = raw_data.find("</h1>")

            heading = "=== " + raw_data[start:end].strip() + " ===\n\n\n"  # Heading
            data += heading

            next = raw_data.find("<h2", end+1)

            # Extracting the shloka
            c = 0
            while start < next and end < next and c < 2:
                start = raw_data.find("<p>", end)+3
                end = raw_data.find("</p>", start+1)+4
                data += raw_data[start:end] + "\n"

                if self.language != "":  # "" Represents english and in english sholka presented in english and sanksrit
                    if c == 0:
                        break
                
                c += 1

            data = data.replace("<br/>", "<br>").replace("।", "|")

            # Correcting a small space in the shloka
            if self.language == "":
                data = data.replace("||<br>", " ||\n").replace("||</p>", " ||\n")
            
            if self.chapter_no == '1' and self.verse_no == '1' and self.language == "":
                data = data.replace("||1", "|| 1")

            data = data.replace("<br>", "\n")

            # Extracting the word meaning
            data += "\n\n== Word Meanings ==\n\n"
            start = raw_data.find('<div id="wordMeanings">')
            end = raw_data.find('</div>', start)
            data += raw_data[start:end].replace("—", " — ").replace(";", "\n") + "\n"

            start = end = 0

            # Extracting the translation
            start = raw_data.find('<div id="translation">', end)
            end = raw_data.find('</div>', start)
            if start != -1 and end != -1:
                data += "\n\n== Translation ==\n\n"
                data += raw_data[start:end]

            data += "\n"

            # Extracting the commentary
            start = raw_data.find('<div id="commentary">', end)
            end = raw_data.find('</div>', start)
            if start != -1 and end != -1:
                data += "\n\n== Commentary ==\n\n"
                data += raw_data[start:end].replace("</p>", "\n")

        data = self.__removeHTMLTags(data)
        return data


    def __getPage(self):
        if self.language == 'en':
            self.language = ''
        
        try:
            if self.chapter_no == '0':
                url = "http://www.holy-bhagavad-gita.org/introduction/" + self.language
            elif self.chapter_no != '0' and self.verse_no == '0':
                url = "http://www.holy-bhagavad-gita.org/chapter/" + self.chapter_no + "/" + self.language
            else:
                url = "http://www.holy-bhagavad-gita.org/chapter/" + self.chapter_no + "/verse/" + self.verse_no + "/" + self.language
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})  # To access the websites which show errors
            data = str(urlopen(req).read(), 'utf-8')
            return data
        except Exception as e:
            return str(e)

    def __removeHTMLTags(self, data):
        regex = re.compile('<span class="verseShort">.*</span>|<.*?>') 
        text = re.sub(regex, '', data)

        all_lines = text.split("\n")
        text = ""

        for i in all_lines:
            text += i.strip() + "\n"
        
        return text

# Using the API
# api = TheBhagavadGita()
# data = api.getData(1, 1, 'te')
# with open("a.txt", "w", encoding="utf-8") as p:
#     p.write(data)
