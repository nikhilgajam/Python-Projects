import tkinter
import random


# Window settings
window = tkinter.Tk()
window.title("PyTyping")
window.geometry("1050x510")


# Text
text = '''Do you ever send or receive e-mails? Are you on the Internet a lot? Do you go to chat rooms? Did you know there are rules of behavior for all of these? The rules are called Netiquette. They can be applied to almost every situation -- real life, as well as cyberspace. These rules might seem kind of obvious to you, but they're important. They will help you and your friends' Internet experience be productive, as well as fun.

Don't break any laws. Cyberspace is an extension of the real world. Just because you're dealing with computers and not people (at least not directly), it doesn't mean the law no longer applies. If it's illegal in the real world, it's probably illegal in cyberspace.

Be polite. You've certainly heard the saying "Do unto others as you would have them do unto you." It's true not only when you're talking to someone face-to-face, but also when you're talking to them on the Web. Being polite doesn't just include what you say. It also covers how you say it, and to whom. If you use humor or sarcasm in your writing, be sure the recipient is going to like your sense of humor. Otherwise, you might offend the person. And never send an e-mail when you're angry or upset! It will probably show in your message, and you may hurt someone else's feelings.

Be careful of flames and flame wars. A "flame" refers to any insulting message. Nearly everyone receives a flame sooner or later. The question becomes what to do with them. The best move is to just ignore them. If, however, you feel the flame is worth a response, your reply may start a flame war, where the insults continue back and forth. In these situations, everybody loses.

Be patient. Everybody was new to the Internet at one time or another! Be patient with those who are new. If someone shows poor Netiquette, don't get angry. Politely respond and tell them of their error. Usually, the other person will be thankful for the advice. You may even find that you have made a new friend. Sometimes you'll bump into someone that you just don't see eye to eye with. In those cases, all you can do is agree to disagree.

Be concise and accurate. E-mail wasn't intended for carrying on long talks. E-mail is about convenience. Keep your messages brief and to the point. If you write long messages that drift from one subject to the next, your reader's attention will drift as well. Also, take the time to delete long header text when you're forwarding or replying to an e-mail. This shows the recipient that you know their time is valuable, too. And above all, proofread your message for spelling and grammar before you send it. In cyberspace, people only know you from what you type. If you're sloppy with the basics, how can anyone trust you when it's really important?

Always fill-in the subject line! When you start receiving dozens of e-mails a day, you'll come to appreciate people who use subject lines. The subject line is the only label you have to identify each of the messages in your mailbox. Use something appropriate, such as the topic sentence or the main idea. Be sure to keep it brief, though, since most e-mail clients only show the first 20-30 characters of the subject line anyway.

Be careful with formatting. Remember that not everyone uses the same software to read their e-mail. Just because you can center your text and make it green and boldface doesn't mean your recipient can too! Some e-mail clients make all messages left-justified plain text, no matter how they were sent. If it's important to use formatting, make sure the recipient can read it first.

Think about signature files. These files are text files that you can include with each message. They provide information about you, the sender. Keep them short, less than 10 lines. Long ones make threads hard to read because of the extra text separating each message. Signature files usually include the following information: Name, E-mail Address, Homepage Address, Character Quote. A character quote is that cute little phrase or saying you often see at the end of a signature file. It can be funny or serious. It can be a favorite saying of yours. Perhaps you have a line from a movie that you really like. It is meant to let your reader know a little something extra about you.

Use care when attaching files. Attachments are an easy way to share programs, graphics, sounds, or any other kind of file you find on your computer. If you intend to send someone a large file (say, greater than 20K) you should contact them and ask their permission first. There are three reasons for this. First, you don't even know if they have e-mail software that can handle attached files. Second, large files (we're talking megabytes here) can completely fill someone's e-mail box.  Then they can't receive any more e-mail. Third, some e-mail programs limit the size of file attachments. Your e-mail message may not get sent if the file is too large, or it may bounce back to you. Graphics and sound files tend to be quite large, so send these with care.

Think about distribution lists. You may want to send an e-mail to several people at once. The best way to do this is to use a list. Start a blank text file. Start listing all the e-mail addresses you want included in the list, separated by a comma and a blank space. Cut and paste the distribution list into the "To," the "CC," or the "BCC" field in your e-mail client. Be sure to use your own e-mail address in the "To" field. That way you will receive an e-mail to verify that it was sent! The advantage to the BCC field is that everyone on your list will receive a copy of your message without the entire list appearing in the header.

Distribution lists are not intended for spamming purposes. It's often the practice to include instructions on how to be removed from a distribution list for those who don't wish to receive future mailings. Do not spam! Spam is the e-mail equivalent of junk mail, and spamming is the practice of sending out unsolicited bulk e-mail. Some e-mail systems let you filter out unwanted mail, but they're not perfect. And nothing gets people angrier than seeing their inbox fill up with junk every day. Do your part to help by not spamming others. And report any spam you get to your Internet Service Provider -- ISP.

Group communication is no different from sending out a single e-mail. But sometimes it's hard to tell what good Netiquette is when joining a new online group. As always, it's important to follow the basic rules above, but each group has its own quirks and customs. Here's some general advice for dealing with new group Netiquette situations.

When you're new to the area, it's best to observe for a moment before diving into the mix. When you enter a new chat room, or when you want to post something to a bulletin board for the first time, stop and look around. The best way to get a feel for the correct group Netiquette is to see what the people around you are doing. Another good way to find out what's going on is to look for a FAQ, About, or Help page.

Privacy is another issue on the Internet. The truth is, there is no such thing as complete privacy. If you send out an e-mail, there's always a chance someone else could intercept it. And with most e-mail systems, the E-mail Administrator has access to your messages. Some companies even monitor their employee e-mail. As a result, you need to think about security. The following are a few tips to get you started.

Don't e-mail any information you want to keep secure! And never give out your password, not even to friends. If someone else has it, there's a chance that more people will find out. Don't use easy-to-guess words or numbers, like your name or your birthday. It's easy for people to guess those. Use both numbers and symbols. It is much harder guessing a password like "z67Aa98bC". And make sure you change your password a lot, in case someone does find out.

Don't leave your machine running when you're not there. This is especially true if you're logged on to someplace secure. If you must leave your computer unattended use a screen saver with password protection for greater security.

Beware of viruses and hoaxes. A virus can't be transmitted through the body (text) of an e-mail. You need to have an executable program that you download from somewhere else to introduce a virus into your computer. A virus could be carried in any attached files you receive with your e-mail. Make sure you use a current anti-virus scanning program before running any attached files. And never open a file if you don't know the sender.

Also be wary of any messages you receive that warn you of an e-mail virus and tell you to immediately forward the message to everyone you know. These are usually hoaxes. To protect yourself from viruses, first invest in some SOLID virus protection software. The two virus protection giants are Norton Antivirus (also known as Symantec) & McAfee VirusScan (Network Associates).

Second, create a rescue disk set! The virus protection software will include one. Third, don't keep chain letters and hoaxes going. Do not forward them to anyone and everyone you know. A responsible Netizen will be mindful of others and delete them immediately.

The quick brown fox jumps over the lazy dog. Waltz, bad nymph, for quick jigs vex. Quick zephyrs blow, vexing daft Jim. Sphinx of black quartz, judge my vow. Two driven jocks help fax my big quiz. Five quacking zephyrs jolt my wax bed. The five boxing wizards jump quickly. Pack my box with five dozen liquor jugs. Crazy Fredrick bought many very exquisite opal jewels. We promptly judged antique ivory buckles for the next prize. A mad boxer shot a quick, gloved jab to the jaw of his dizzy opponent.

Jaded zombies acted quaintly but kept driving their oxen forward. The job requires extra pluck and zeal from every young wage earner. Go, lazy fat vixen; be shrewd, jump quick. When zombies arrive, quickly fax Judge Pat. Amazingly few discotheques provide jukeboxes. Puzzled women bequeath jerks very exotic gifts. The quick onyx goblin jumps over the lazy dwarf.

Watch "Jeopardy!", Alex Trebek's fun TV quiz game. Five or six big jet planes zoomed quickly by the tower. Six big devils from Japan quickly forgot how to waltz. Jack amazed a few girls by dropping the antique onyx vase. A quick movement of the enemy will jeopardize six gunboats No kidding-Lorenzo called off his trip to Mexico City just because they told him the conquistadors were extinct. Quixotic jugglers repent; wave away fake methods and brazen mishaps. Woven silk pyjamas exchanged for blue quartz. Grumpy wizards make a toxic brew for the jovial queen. Jim quickly realized that the beautiful gowns are expensive.

Charles Babbage (1791-1871) was an English politician, philosopher, mathematician, and scientist, perhaps best known today as the "Father of Computing" for his contributions to the basic design of the computer. His observations in 1830 regarding the decline of science in the England of the time are timeless; resonating even in our "Age of Technology," they can provide us with useful insight into the way we approach this critical subject: That the state of knowledge in any country will exert a directive influence on the general system of instruction adopted in it, is a principle too obvious to require investigation. And it is equally certain that the tastes and pursuits of our manhood will bear on them the traces of the earlier impressions of our education. It is therefore not unreasonable to suppose that some portion of the neglect of science in England, may be attributed to the system of education we pursue. A young man passes from our public schools to the universities, ignorant almost of the elements of every branch of useful knowledge; and at these latter establishments, formed originally for instructing those who are intended for the clerical profession, classical and mathematical pursuits are nearly the sole objects proposed to the student's ambition.

Much has been done at one of our universities during the last fifteen years, to improve the system of study; and I am confident that there is no one connected with that body, who will not do me the justice to believe that, whatever suggestions I may venture to offer, are prompted by the warmest feelings for the honor and the increasing prosperity of its institutions. The ties which connect me with Cambridge are indeed of no ordinary kind.

Taking it then for granted that our system of academical education ought to be adapted to nearly the whole of the aristocracy of the country, I am inclined to believe that whilst the modifications I should propose would not be great innovations on the spirit of our institutions, they would contribute materially to that important object.

It will be readily admitted, that a degree conferred by a university, ought to be a pledge to the public that he who holds it possesses a certain quantity of knowledge. The progress of society has rendered knowledge far more various in its kinds than it used to be; and to meet this variety in the tastes and inclinations of those who come to us for instruction, we have, besides the regular lectures to which all must attend, other sources of information from whence the students may acquire sound and varied knowledge in the numerous lectures on chemistry, geology, botany, history, etc. It is at present a matter of option with the student, which, and how many of these courses he shall attend, and such it should still remain. All that it would be necessary to add would be, that previously to taking his degree, each person should be examined by those Professors, whose lectures he had attended. The pupils should then be arranged in two classes, according to their merits, and the names included in these classes should be printed. I would then propose that no young man, except his name was found amongst the "List of Honors," should be allowed to take his degree, unless he had been placed in the first class of some one at least of the courses given by the professors. But it should still be imperative upon the student to possess such mathematical knowledge as we usually require. If he had attained the first rank in several of these examinations, it is obvious that we should run no hazard in a little relaxing the strictness of his mathematical trial.

If it should be thought preferable, the sciences might be grouped, and the following subjects be taken together: Modern History, Laws of England, and Civil Law; Political Economy, and Applications of Science to Arts and Manufactures; Chemistry, Mineralogy, and Geology; Zoology, including Physiology and Comparative Anatomy; and Botany, including Vegetable Physiology and Anatomy.

One of the great advantages of such a system would be, that no young person would have an excuse for not studying, by stating, as is most frequently done, that the only pursuits followed at Cambridge, classics and mathematics, are not adapted either to his taste, or to the wants of his after life. His friends and relatives would then reasonably expect every student to have acquired distinction in some pursuit. If it should be feared that this plan would lead to too great a diversity of pursuits in the same individual, a limitation might be placed upon the number of examinations into which the same person might be permitted to enter. It might also be desirable not to restrict the whole of these examinations to the third year, but to allow the student to enter on some portion of them in the first or second year, if he should prefer it.

By such an arrangement, which would scarcely interfere seriously with our other examinations, we should, I think, be enabled effectually to keep pace with the wants of society, and retaining fully our power and our right to direct the studies of those who are intended for the church, as well as of those who aspire to the various offices connected with our academical institutions; we should, at the same time, open a field of honorable ambition to multitudes, who, from the exclusive nature of our present studies, leave us with but a very limited addition to their stock of knowledge.

Much more might be said on a subject so important to the interests of the country, as well as of our university, but my wish is merely to open it for our own consideration and discussion. We have already done so much for the improvement of our system of instruction, that public opinion will not reproach us for any unwillingness to alter. It is our first duty to be well satisfied that we can improve: such alterations ought only to be the result of a most mature consideration, and of a free interchange of sentiments on the subject, in order that we may condense upon the question the accumulated judgment of many minds.

It is in some measure to be attributed to the defects of our system of education, that scientific knowledge scarcely exists amongst the higher classes of society. The discussions in the Houses of Lords or of Commons, which arise on the occurrence of any subjects connected with science, sufficiently prove this fact, which, if I had consulted the extremely limited nature of my  personal experience, I should, perhaps, have doubted.

Interest or inclination form the primary and ruling motives in this matter, and both these exert greater or less proportionate influence in each of the respective cases to be examined.

A large portion of those who are impelled by ambition or necessity to advance themselves in the world, make choice of some profession in which they imagine their talents likely to be rewarded with success; and there are peculiar advantages resulting to each from this classification of society into professions. The esprit de corps frequently overpowers the jealousy which exists between individuals, and pushes on to advantageous situations some of the more fortunate of the profession; whilst, on the other hand, any injury or insult offered to the weakest, is redressed or resented by the whole body. There are other advantages which are perhaps of more importance to the public. The numbers which compose the learned professions in England are so considerable, that a kind of public opinion is generated amongst them, which powerfully tends to repress conduct that is injurious either to the profession or to the public. Again, the mutual jealousy and rivalry excited amongst the whole body is so considerable, that although the rank and estimation which an individual holds in the profession may be most unfairly appreciated, by taking the opinion of his rival; yet few estimations will be found generally more correct than the opinion of a whole profession on the merits of any one of its body. This test is of great value to the public, and becomes the more so, in proportion to the difficulty of the study to which the profession is devoted. It is by availing themselves of it that men of sense and judgment, who have occasion for the services of professional persons, are, in a great measure, guided in their choice.

The pursuit of science does not, in England, constitute a distinct profession, as it does in many other countries. It is therefore, on that ground alone, deprived of many of the advantages which attach to professions. One of its greatest misfortunes arises from this circumstance; for the subjects on which it is conversant are so difficult, and require such un-remitted devotion of time, that few who have not spent years in their study can judge of the relative knowledge of those who pursue them. It follows, therefore, that the public, and even that men of sound sense and discernment, can scarcely find means to distinguish between the possessors of knowledge, in the present day, merely elementary, and those whose acquirements are of the highest order. This remark applies with peculiar force to all the more difficult applications of mathematics; and the fact is calculated to check the energies of those who only look to reputation in England.'''

text = text.split("\n\n")  # Splitting the text into small lines to display on screen


# Variables
word_pointer = 0
chars_typed = 0
data = ""
data_list = []
time_var = 60
time_count = time_var
started = False


# Methods

def init():
    # This method initializes the variables to their default values
    global word_pointer, chars_typed, data, data_list, time_var, time_count, started

    displayAnalysis()  # Showing analysis before making the values to default

    word_pointer = 0
    chars_typed = 0
    data = ""
    time_count = time_var
    started = False

    random_number = random.randint(0, len(text)-1)  # Randomly selecting a line
    data = text[random_number]
    data = data.split(" ")

    time_box['state'] = tkinter.NORMAL  # Making the time_box changeable
    updateInputBox('Press "Enter" Key To Start  ')
    updateTimeBox(time_count)

    word_pointer = 0

    displayStringUpdation()


def timer():
    # Updates the timer count and this method runs as long as this program runs
    global time_count, started

    if started:
        time_count -= 1  # Decreasing the time count
        
        # Making the time_box inactive after the updation
        time_box['state'] = tkinter.NORMAL
        updateTimeBox(time_count)
        time_box['state'] = tkinter.DISABLED
        displayAnalysis()

        # Checking whether the time_count is zero. If it zero then stop reducing and display analysis
        if time_count <= 0:
            started = False
            init()  # Setting the state to default

    window.after(1000, timer)  # Calling this method after every 1 second


def displayAnalysis():
    # This method calculates the wpm and other analysis and displays it
    global chars_typed

    # WPM Information: https://www.speedtypingonline.com/typing-equations
    time_taken = abs(time_var - time_count)  # Duration = Time Selected - Time Spent In Typing
    time_taken_in_minutes = time_taken / 60.0  # Divide by 60 to convert seconds to minutes
    chars_typed_divided_by_5 = chars_typed / 5.0

    # Gross WPM(Words Per Minute) = (No. of chars typed/5)/Time taken (in minutes)
    gross_wpm = 0
    # CPM (Characters Per Minute) = WPM * 5
    cpm = 0
    if time_taken_in_minutes > 0:
        gross_wpm = int((chars_typed_divided_by_5) / (time_taken_in_minutes))
        cpm = round(gross_wpm * 5)
    # Gross strokes = All Characters Typed
    gross_strokes = chars_typed

    # Displaying the analysis
    text_data = "Analysis:\n\n"
    text_data += "Duration: " + str(time_taken) + " Seconds Of Total " + str(time_var) + " Seconds\n"
    if gross_wpm < 0:
        text_data += "Speed: Cannot Be Calculated [Try To Type For More Time With Less Mistakes]\n"
        text_data += "CPM: Cannot Be Calculated\n"
    else:
        text_data += "Speed: " + str(gross_wpm) + " Words Per Minute (WPM)      [Typing Level :  " + getTypingLevel(gross_wpm) + "]\n"
        text_data += "CPM: " + str(cpm) + " Characters Per Minute (CPM)\n"
    text_data += "Key Strokes: " + str(gross_strokes) + "\n"
    text_data += "Typing Speed Levels (In WPM):\n"
    text_data += "(0-25 = Slow)      (26-45 = Average)      (46-65 = Fluent)      (66-80 = Fast)      (81-âˆž = Insane)"

    analysis_display['text'] = text_data


def spacePressed(e=""):
    # This method will be triggered when space key on the keyboard is pressed in the input_box
    global word_pointer, started, chars_typed

    inp = input_box.get()

    # Should not allow the blank input
    if inp == "":
        return "break"

    # To avoid any extra key presses when 'Press "Enter" Key To Start is displayed
    if inp == 'Press "Enter" Key To Start  ':
        return "break"

    if word_pointer < len(data) and inp == data[word_pointer]:
        updateInputBox("")
        chars_typed += len(data[word_pointer]) + 1  # +1 is for the space
        word_pointer += 1
        displayStringUpdation()

    # Checking whether the words are over
    if word_pointer >= len(data):
        started = False
        init()  # Setting the state to default
    
    # When this method is triggered then space will not be added to the input
    return "break"


def getTypingLevel(speed):
    # This methods returns the typing level
        if speed >= 0 and speed <= 25:
            return "Slow"
        elif speed >= 26 and speed <= 45:
            return "Average"
        elif speed >= 46 and speed <= 65:
            return "Fluent"
        elif speed >= 66 and speed <= 80:
            return "Fast"
        else:
            return "Insane"


def enterPressedToStartTyping(e=""):
    # This method is invoked when enter key is pressed in input_box
    global started

    if not started:
        started = True
        updateInputBox("")
        updateTimeValue()


def displayStringUpdation():
    # This methods displays 10 new words on screen each and every time you enter a word correctly
    temp_data = ""
    for i in data[word_pointer : word_pointer + 10]:  
        temp_data += i + " "

    display['text'] = temp_data


def updateTimeValue():
    # This methods will take the value from time_box and stores it
    global time_var, time_count

    time_var = int(time_box.get().replace("Time (In Seconds): ", "").strip())
    time_count = time_var


def inputEscapePressed(e=""):
    # This method is triggered when you press escape key in input_box
    global started

    started = False
    init()  # Setting the state to default


def timeBoxBackspace(e=""):
    # This method is triggered when you press backspace key in input_box and it allows you to delete only numbers
    if time_box.get() == "Time (In Seconds): ":
        return "break"
    

def updateInputBox(data: str):
    # This methods updates the input_box display data
    input_box.delete(0, tkinter.END)
    input_box.insert(0, data)


def updateTimeBox(time: int):
    # This methods updates the time_box display data
    time_box.delete(0, tkinter.END)
    time_box.insert(0, "Time (In Seconds): " + str(time))


# Widgets


# Heading label 
heading = tkinter.Label(window, text="PyTyping", font=("Times New Roman", 28))
heading.pack(padx=40, pady=40)

# Display label
display = tkinter.Label(window, text="Hello", font=("Times New Roman", 22))
display.pack()

# Input entry
input_box = tkinter.Entry(window, font=("Times New Roman", 22), width=60)
input_box.bind("<space>", spacePressed)
input_box.bind("<Escape>", inputEscapePressed)
input_box.bind("<Return>", enterPressedToStartTyping)
input_box.bind("<Tab>", lambda e: "break")
input_box.pack(padx=20)
input_box.focus()

# Time entry
time_box = tkinter.Entry(window, width=26, font=("Times New Roman", 20))
time_box.bind("<Key>", lambda e: "break")  # Unbinding all keys
for i in range(0, 10):  # Binding the number keys 0-9
    key = "<Key-" + str(i) + ">"
    time_box.bind(key, lambda e: None)
time_box.bind("<BackSpace>", timeBoxBackspace)  # Binding backspace with method
time_box.bind("<Return>", lambda e: input_box.focus())  # Binding backspace with time_box
time_box.pack(padx=10, pady=40)

# Analysis display label
analysis_display = tkinter.Label(window, font=("Times New Roman", 15))
analysis_display.pack(pady=4)


# Initalization
init()
# Start timer
timer()

window.mainloop()
