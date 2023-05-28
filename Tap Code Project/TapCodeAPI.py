TAP_CODE_TABLE = [['A', 'B', 'C', 'D', 'E'],
                  ['F', 'G', 'H', 'I', 'J'],
                  ['L', 'M', 'N', 'O', 'P'], 
                  ['Q', 'R', 'S', 'T', 'U'],
                  ['V', 'W', 'X', 'Y', 'Z']]   # Row first and column next. There is no K because C sounds like K

TAP_CODE_LETTERS = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 
                    'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' '}


# TapCode Class
class TapCode:
    def englishToTapCode(self, english_data : str) -> str:

        english_data = english_data.upper()
        english_data = english_data.replace("K", "C")  # Replacing all K letters with C because K is not used in tap code
        english_data = english_data.replace('\n', '').replace('\t', '')
        english_data = list(english_data)

        data = ""

        for i in english_data:
            if i in TAP_CODE_LETTERS:
                if i == ' ':
                    data += '/'  # Space in english is replaced with / in tap code
                else:
                    for j in range(5):
                        if i in TAP_CODE_TABLE[j]:
                            # Adding 1 to list index to show correct numbers
                            row = j + 1
                            col = TAP_CODE_TABLE[j].index(i) + 1
                            # A space is added between row and column taps
                            data += ("." * row) + " " + ("." * col) + "/"
        
        # Last character is a slash. So, returning till last second character
        return data[0:-1]
    

    def tapCodeToEnglish(self, tap_code_data : str) -> str:

        tap_code_data = tap_code_data.replace('\n', '').replace('\t', '')
        tap_code_data = tap_code_data.split("/")

        data = ""

        for line in tap_code_data:
            if line != "":
                x = line.split(" ")
                # Subtracting one because the list index values start with 0
                i = len(x[0]) - 1
                j = len(x[1]) - 1
                # Getting the letter based on number of taps using tap code table
                letter = TAP_CODE_TABLE[i][j]
                data += letter
            if line == "":
                data += " "
        
        # Returning the english form of tap code
        return data

    

    