from tkinter import *
import threading
import cv2
import os.path

# use for deep learning
import mvnc.mvncapi as mvnc
import numpy


# PokeDex V3.0
class Pokedex:
    def __init__(self):
        # initialize variables
        self.analyze = False
        self.running = False
        self.thread_killed = True

        self.play = False
        self.pause_vid = False

        # pictures initialization
        self.assets_path = "/home/pi/keep/project Pokedex v3.0/assets/"
        self.photo1_file = self.assets_path + "unknown.png"
        self.photo2_file = self.assets_path + "pokedex.png"
        self.photo = PhotoImage
        self.label1 = Label

        # info label initialization
        self.label2 = Label
        self.label3 = Label
        self.label4 = Label
        self.label5 = Label
        self.text = Text

        # buttons initialization
        self.button1 = Button
        self.button2 = Button
        self.button3 = Button
        self.button4 = Button
        self.button5 = Button
        self.button6 = Button

        # current frame from the video camera
        self.frame = None
        self.dictionary = None

        # input text
        self.text_entry = Entry

        # used to keep an object of the neural class
        self.recognition = NeuralCompute(self.assets_path)

        # start/run the actual program
        self.initialize_dictionary()
        self.start_window()

    # initialize every pokemon that is known by the POKEDEX
    def initialize_dictionary(self):
        self.dictionary = {
            "Pikachu": [" Pokémon Characteristics:"
                        "\n\n   - Whenever Pikachu comes across something new, it blasts it with a jolt of electricity."
                        "If you come across a blackened berry, it's evidence that this Pokémon mistook the intensity "
                        "of its charge."
                        "\n\n   - This Pokémon has electricity-storing pouches on its cheeks. These "
                        "appear to become electrically charged during the night while Pikachu sleeps. It occasionally "
                        "discharges electricity when it is dozy after waking up."
                        "\n\n Pokémon Evolution chart:\n   - Pichu   >  Pikachu  >  Raichu"
                        "\n\n Pokémon Skills:\n   * Tail Whip\n   * Thunder Shock\n   * Quick Attack\n   * Double Team"
                        "\n   * Thunderbolt",
                        self.assets_path + "pikachu.png"],

            "Piplup": [" Pokémon Characteristics:"
                       "\n\n   - It doesn't like to be taken care of. It's difficult to bond with since it won't "
                       "listen to its Trainer."
                       "\n\n   - Because it is very proud, it hates accepting food from people. "
                       "Its thick down guards it from cold."
                       "\n\n Pokémon Evolution chart:\n   - Piplup  >  Prinplup  >  Empoleon"
                       "\n\n Pokémon Skills:\n   * Water Sport\n   * Whirlpool\n   * Hydro Pump\n   * Fury Attack"
                       "\n   * Pound\n   * Waterfall",
                       self.assets_path + "piplup.png"],

            "Bulbasaur": [" Pokémon Characteristics:"
                          "\n\n   - Bulbasaur can be seen napping in bright sunlight. There is a seed on its back. "
                          "By soaking up the sun's rays, the seed grows progressively larger."
                          "\n\n   - For some time after its birth, it grows by gaining nourishment from the seed on "
                          "its back."
                          "\n\n Pokémon Evolution chart:\n   - Bulbasaur  >  Ivysaur  >  Venusaur"
                          "\n\n Pokémon Skills:\n   * Tackle\n   * Leech Seed\n   * Vine Whip\n   * Sweet Scent"
                          "\n   * Synthesis\n   * Seed Bomb",
                          self.assets_path + "bulbasaur.png"],

            "Charmander": [" Pokémon Characteristics:"
                           "\n\n   - The flame that burns at the tip of its tail is an indication of its emotions. "
                           "The flame wavers when Charmander is enjoying itself. If the Pokémon becomes enraged, the "
                           "flame burns fiercely."
                           "\n\n   - It has a preference for hot things. When it rains, steam is said to spout from "
                           "the tip of its tail."
                           "\n\n Pokémon Evolution chart:\n   - Charmander  >  Charmeleon  >  Charizard"
                           "\n\n Pokémon Skills:\n   * Scratch\n   * Ember\n   * Dragon Rage\n   * Smokescreen"
                           "\n   * Flame Burst\n   * Fire Spin",
                           self.assets_path + "charmander.png"],

            "Gastly": [" Pokémon Characteristics:"
                       "\n\n   - Gastly is largely composed of gaseous matter. When exposed to a strong wind, the "
                       "gaseous body quickly dwindles away. Groups of this Pokémon cluster under the eaves of houses "
                       "to escape the ravages of wind."
                       "\n\n   - Almost invisible, this gaseous Pokémon cloaks the target and puts it to sleep without "
                       "notice."
                       "\n\n Pokémon Evolution chart:\n   - Gastly  >  Haunter  >  Gengar"
                       "\n\n Pokémon Skills:\n   * Mean Look\n   * Curse\n   * Night Shade\n   * Payback"
                       "\n   * Hex\n   * Nightmare",
                       self.assets_path + "gastly.png"],

            "Hitmonchan": [" Pokémon Characteristics:"
                           "\n\n   - Hitmonchan is said to possess the spirit of a boxer who had been working toward a "
                           "world championship. This Pokémon has an indomitable spirit and will never give up in the "
                           "face of adversity."
                           "\n\n   - While apparently doing nothing, it fires punches in lightning fast volleys that "
                           "are impossible to see."
                           "\n\n Pokémon Evolution chart:\n   - Tyrogue  >  Hitmonchan"
                           "\n\n Pokémon Skills:\n   * Quick Guard\n   * Close Combat\n   * Comet Punch"
                           "\n   * Focus Punch\n   * Bullet Punch\n   * Agility",
                           self.assets_path + "hitmonchan.png"],

            "Jigglypuff": [" Pokémon Characteristics:"
                           "\n\n   - Jigglypuff's vocal cords can freely adjust the wavelength of its voice. This "
                           "Pokémon uses this ability to sing at precisely the right wavelength to make its foes most "
                           "drowsy."
                           "\n\n   - When this Pokémon sings, it never pauses to breathe. If it is in a battle against "
                           "an opponent that does not easily fall asleep, Jigglypuff cannot breathe, endangering its "
                           "life."
                           "\n\n Pokémon Evolution chart:\n   - Igglybuff  >  Jigglypuff  >  Wigglytuff"
                           "\n\n Pokémon Skills:\n   * Defense Curl\n   * Sing\n   * Disarming Voice\n   * Play Nice"
                           "\n   * Hyper Voice",
                           self.assets_path + "jigglypuff.png"],

            "Pidgeotto": [" Pokémon Characteristics:"
                          "\n\n   - Pidgeotto claims a large area as its own territory. This Pokémon flies around, "
                          "patrolling its living space. If its territory is violated, it shows no mercy in thoroughly "
                          "punishing the foe with its sharp claws."
                          "\n\n   - It has outstanding vision. However high it flies, it is able to distinguish the "
                          "movements of its prey."
                          "\n\n Pokémon Evolution chart:\n   - Pidgey  >  Pidgeotto  >  Pidgeot"
                          "\n\n Pokémon Skills:\n   * Tackle\n   * Sand Attack\n   * Quick Attack\n   * Whirlwind"
                          "\n   * Agility\n   * Wing Attack",
                          self.assets_path + "pidgeotto.png"],

            "Squirtle": [" Pokémon Characteristics:"
                         "\n\n   - Squirtle's shell is not merely used for protection. The shell's rounded shape and "
                         "the grooves on its surface help minimize resistance in water, enabling this Pokémon to swim "
                         "at high speeds."
                         "\n\n   - The shell, which hardens soon after it is born, is resilient. If you poke it, it "
                         "will bounce back out."
                         "\n\n Pokémon Evolution chart:\n   - Squirtle  >  Wartortle  >  Blastoise"
                         "\n\n Pokémon Skills:\n   * Tackle\n   * Tail Whip\n   * Water Gun\n   * Rapid Spin"
                         "\n   * Bubble\n   * Aqua Tail",
                         self.assets_path + "squirtle.png"],

            "Togepi": [" Pokémon Characteristics:"
                       "\n\n   - As its energy, Togepi uses the positive emotions of compassion and pleasure exuded by "
                       "people and Pokémon. This Pokémon stores up feelings of happiness inside its shell, then shares "
                       "them with others."
                       "\n\n   - The shell seems to be filled with joy. It is said that it will share good luck when "
                       "treated kindly."
                       "\n\n Pokémon Evolution chart:\n   - Togepi  >  Togetic  >  Togekiss"
                       "\n\n Pokémon Skills:\n   * Charm\n   * Follow Me\n   * Encore\n   * Ancient Power"
                       "\n   * Safeguard\n   * Baton Pass",
                       self.assets_path + "togepi.png"],

            "Unknown": [" Pokémon Characteristics:"
                        "\n\n   - This pokemon is not in our database,\n  caution is advised"
                        "\n\n   - Unknown"
                        "\n\n Pokémon Evolution chart:\n   - Unknown"
                        "\n\n Pokémon Skills:\n   * Unknown",
                        self.assets_path + "unknown2.png"]
        }

    # start actual program window
    def start_window(self):
        # set up blank program
        window = Tk()

        # set up parameters
        window.title("Personal Pokedex v3.0")
        window.configure(background="gray10")
        window.geometry("1000x800")
        window.resizable(0, 0)

        # add photo to the program
        self.photo = PhotoImage(file=self.photo1_file)
        self.label1 = Label(window, image=self.photo, bg="gray10")
        self.label1.place(x=20, y=20)

        # add console writings / output the status info
        self.label2 = Label(window, text="info: ---", bg="gray10", fg="white", font="none 13 italic")
        self.label2.place(x=520, y=720)

        self.label3 = Label(window, text="Pokémon Description:", bg="gray10", fg="white", font="Helvetica 20 italic")
        self.label3.place(x=610, y=30)

        self.label4 = Label(window, text="", bg="gray10", fg="white", font="Helvetica 18 italic")
        self.label4.place(x=520, y=100)

        self.label5 = Label(window, text="File:", bg="gray10", fg="white", font="Helvetica 18 italic")
        self.label5.place(x=30, y=497)

        self.text = Text(window, width=40, height=23, wrap=WORD, fg="white", bg="gray10", font="Helvetica 15 italic")
        self.text.place(x=520, y=140)

        # add buttons
        self.button1 = Button(window, text="WEBCAM", font="Helvetica 30 bold", width=9, command=self.click_start)
        self.button1.place(x=30, y=400)

        self.button2 = Button(window, text="ANALYZE", font="Helvetica 30 bold", width=9, command=self.click_analyze)
        self.button2.place(x=271, y=400)
        # self.button2.config(height=1, width=8)

        self.button3 = Button(window, text="EXIT", font="Helvetica 30 bold", width=9, command=self.click_exit)
        self.button3.place(x=271, y=642)

        self.button4 = Button(window, text="IMAGE", font="Helvetica 30 bold", width=9, command=self.click_path)
        self.button4.place(x=30, y=642)

        self.button5 = Button(window, text="delete", font="Helvetica 15 bold", width=5, command=self.click_reset)
        self.button5.place(x=414, y=496)

        self.button6 = Button(window, text="PLAY VIDEO", font="Helvetica 30 bold", width=20, command=self.click_play_video)
        self.button6.place(x=30, y=555)

        # add input method
        self.text_entry = Entry(window, width=28, font="Helvetica 15 bold", bg="white")
        self.text_entry.place(x=90, y=500)

        # loop through main
        window.mainloop()

    # resets the input box
    def click_reset(self):
        # if it is already empty, print a specific output
        if self.text_entry.get() == "":
            self.print_info("empty filepath...")
            return
        # delete the containment of the input box
        self.text_entry.delete(0, END)
        self.print_info("filepath deleted...")

    # check the current frame
    def check_video_frame(self):
        # this is how we pause the video and set the thread to verify the current frame
        self.pause_vid = True
        self.print_info("video analyzing...")

        # reset every status
        self.text.delete(0.0, END)
        self.label4.configure(text="")
        self.photo = PhotoImage(file=self.photo1_file)
        self.label1.configure(image=self.photo)

    # start playing the video thread
    def run_video_thread(self):
        # start the video
        self.play = True
        self.pause_vid = False
        text_location = self.text_entry.get()
        # open testing purposes only: "C:\\Users\\PREDATOREL\\Desktop\\pokemon.mkv"
        cap = cv2.VideoCapture(text_location)

        # if the format is not supported, then close
        if cap.isOpened() is False:
            self.print_info("not a video format, closing...")
            self.play = False
            cap.release()
            cv2.destroyAllWindows()
            return

        while cap.isOpened():
            # if the machine learning should check the current frame
            if self.pause_vid is True:
                # directly analyze the current frame & don't start a new thread so we can pause this process
                self.analyze_frame(frame)
                # set the video to continue playing
                self.pause_vid = False
                self.print_info("video analysis ended...")
                continue

            # show the current frame (play the video seamless)
            ret, frame = cap.read()

            # if the video is ended or it was another type of video, then it will stop
            if ret is False:
                self.print_info("video ended...")
                self.play = False
                cap.release()
                cv2.destroyAllWindows()
                self.button6.config(text="PLAY VIDEO")
                return

            cv2.imshow('frame', frame)
            cv2.waitKey(10)

            # stop the video when it is over
            if self.play is False:
                break

        # set everything to turn off
        self.play = False
        cap.release()
        cv2.destroyAllWindows()

    # play the video from the specified location
    def click_play_video(self):
        # check if the video is playing, if yes then commute it and close the video thread
        if self.play is True:
            self.play = False
            self.print_info("video closed...")
            self.button6.config(text="PLAY VIDEO")
            return

        # check if the web cam is opened, so the video can't be played
        if self.thread_killed is False:
            self.print_info("webcam opened, cannot open video...")
            return

        # checks if an instance of the thread that is doing the prediction already started
        for i in threading.enumerate():
            if i.getName() == "Thread-Predict":
                self.print_info("analyzing... image already processing...")
                return

        # get the text from the input
        text_location = self.text_entry.get()

        # check if string is empty
        if text_location == "":
            self.print_info("no input location...")
            return

        # checks if the input file video exists
        file_exist = os.path.isfile(text_location)
        if file_exist is False:
            self.print_info("no such file...")
            return

        # prepare the thread to start
        self.play = True
        self.print_info("video started...")
        self.button6.config(text="STOP")

        # start new thread, running the main program
        new_thread = threading.Thread(target=self.run_video_thread, name="Thread-Video-Run")
        # set the thread to be daemon so if you close the main thread, then this will close too
        new_thread.setDaemon(True)
        new_thread.start()

    # used for path input pictures
    def click_path(self):
        # checks if an instance of the thread that is doing the prediction already started
        for i in threading.enumerate():
            if i.getName() == "Thread-Predict":
                self.print_info("analyzing... image already processing...")
                return

        # get the text from the input
        text_location = self.text_entry.get()

        # check if string is empty
        if text_location == "":
            self.print_info("no input location...")
            return

        # read the input image
        pokemon_image = cv2.imread(text_location)

        # check if the file / image exists
        if pokemon_image is None:
            # delete the file path if it does not exist
            self.text_entry.delete(0, END)
            self.print_info("no such file...")
            return
        
        # reset every status
        self.text.delete(0.0, END)
        self.label4.configure(text="")
        self.photo = PhotoImage(file=self.photo1_file)
        self.label1.configure(image=self.photo)
            
        # call the AI
        self.print_info("image analyzing...")
        self.analyze_thread(pokemon_image)
        # self.print_info("analysis ended...")

    # clean exit
    def click_exit(self):
        if self.running:
            self.print_info("make sure you stop the program...")
            return
        if self.play:
            self.print_info("make sure you stop the video...")
            return
        self.recognition.close()
        exit(0)

    # analyze the input pokemon
    def click_analyze(self):
        # checks if an instance of the thread that is doing the prediction already started
        for i in threading.enumerate():
            if i.getName() == "Thread-Predict":
                self.print_info("analyzing... image already processing...")
                return

        # check if the video is opened
        if self.play is True:
            self.check_video_frame()
            return

        # checks if there is a frame to analyze
        if self.frame is None:
            self.print_info("no existing frame to analyze...")
        else:
            self.print_info("webcam analyzing...")
            self.analyze = True
            print("reset")
            
            # reset every status
            self.text.delete(0.0, END)
            self.label4.configure(text="")
            self.photo = PhotoImage(file=self.photo1_file)
            self.label1.configure(image=self.photo)
        
    # start button starts the program and changes to stop button
    def click_start(self):
        # check if the thread is already killed before creating a new one
        if self.thread_killed is False:
            self.print_info("wait for current thread to kill itself...")
            return

        if self.play is True:
            self.print_info("video opened, cannot open webcam...")
            return

        # change the button functionality
        self.running = True
        self.button1.config(text="STOP", command=self.click_stop)

        # start new thread, running the main program
        new_thread = threading.Thread(target=self.run_thread, name="Thread-Program-Poop")
        # set the thread to be daemon so if you close the main thread, then this will close too
        new_thread.setDaemon(True)
        new_thread.start()

    # stop and change to start
    def click_stop(self):
        # change the button functionality and stop the main program
        self.running = False
        self.button1.config(text="WEBCAM", command=self.click_start)

    # run the separate thread
    def run_thread(self):
        self.thread_killed = False
        # set everything for the beginning of the main program
        self.photo = PhotoImage(file=self.photo2_file)
        self.label1.configure(image=self.photo)

        # print the status info
        self.print_info("working...")

        # capture from the web cam
        self.cap = cv2.VideoCapture(0)

        # check if the camera exists / is connected to this PC
        if self.cap.isOpened() is False:
            # print the status info
            self.print_info("no camera detected, thread closing...")
            # stop and change to start
            self.click_stop()
            # when ends change back to the main picture and before the start program
            self.photo = PhotoImage(file=self.photo1_file)
            self.label1.configure(image=self.photo)
            # delete pokemon description status
            self.text.delete(0.0, END)
            # delete pokemon name
            self.label4.configure(text="")

            # mark this thread as killed
            self.thread_killed = True
            return

        while self.running:
            # if we should analyze the frame, then we treat that case here in the thread
            if self.analyze:
                self.analyze = False
                # analyze the current frame
                self.analyze_thread(self.frame)

            # Capture frame-by-frame
            ret, self.frame = self.cap.read()

            # check if the camera gives an output
            if ret is False:
                # print the status info
                self.print_info("error: no frames taken from the camera, closing...")
                # stop and change to start if the camera frame has no value
                self.click_stop()
                # when ends change back to the main picture and before the start program
                self.photo = PhotoImage(file=self.photo1_file)
                self.label1.configure(image=self.photo)
                # delete pokemon description status
                self.text.delete(0.0, END)
                # delete pokemon name
                self.label4.configure(text="")
                # When everything is done, release the capture
                self.frame = None
                self.cap.release()
                cv2.destroyAllWindows()
                # mark this thread as killed
                self.thread_killed = True
                return

            # this freezes the frame when a prediction is running
            for i in threading.enumerate():
                if i.getName() == "Thread-Predict":
                    break
            else:
                # Display the resulting frame
                cv2.imshow('Pokemon Capture', self.frame)
            cv2.waitKey(1)

        # when ends change back to the main picture and before the start program
        self.photo = PhotoImage(file=self.photo1_file)
        self.label1.configure(image=self.photo)
        self.label2.configure(text="info: ---")
        # delete pokemon description status
        self.text.delete(0.0, END)
        # delete pokemon name
        self.label4.configure(text="")

        # When everything is done, release the capture
        self.frame = None
        self.cap.release()
        cv2.destroyAllWindows()

        self.thread_killed = True
        return

    # print the status info
    def print_info(self, info_text):
        self.label2.configure(text=info_text)

    # this method starts a separate thread thad tries to predict the pokemon
    def analyze_thread(self, frame):
        # start new thread, running the main program, also providing the frame parameter as a tuple
        predict_thread = threading.Thread(target=self.analyze_frame, args=[frame], name="Thread-Predict")
        # set the thread to be daemon so if you close the main thread, then this will close too
        predict_thread.setDaemon(True)
        predict_thread.start()
        print("started thread")

    # analyze the frame that is given as a parameter
    def analyze_frame(self, frame):
        # get the prediction name of the deep neural graph
        pokemon_name = self.prediction_ai(frame)
        
        try:
            pokemon_data = self.dictionary[pokemon_name]
        except:
            pokemon_name = "Exception"
            pokemon_data = ["  - Big Exception, this case was not treated in the dictionary and this never should have "
                            "happened\n\n- Easter egg discovered i guess .......\n\n .....\n\n- Congrats !!! Yay....",
                            self.photo1_file]

        # update pokemon description status
        self.text.delete(0.0, END)
        self.text.insert(END, pokemon_data[0])
        # update pokemon name
        self.label4.configure(text="Pokémon Name: " + str(pokemon_name))
        # update pokemon picture
        self.photo = PhotoImage(file=pokemon_data[1])
        self.label1.configure(image=self.photo)
        self.print_info("analysis ended...")

    # use deep learning to determine the pokemon
    def prediction_ai(self, frame):
        pokemon_predict = self.recognition.runAI(frame)
        # for testing purposes only for now
        # return "Pikachu"
        return pokemon_predict


# class used for AI neural recognition
class NeuralCompute(object):

    def __init__(self, assets_path):
        # DEFINED variables
        self.assets_path = assets_path
        self.GRAPH_PATH = self.assets_path + "graph"
        self.LABELS_FILE_PATH = self.assets_path + "retrained_labels.txt"
        self.IMAGE_DIM = (299, 299)
        self.MEAN = 128
        self.STANDARD_DEVIATION = 1.0 / 128.0
        self.NUM_OF_GUESSES = 1

        # initialize everything that's not related to DEFINED type variables
        self.initialize()

    # initialize the essentials
    def initialize(self):
        # Look for enumerated Intel Movidius NCS device(s); quit program if none found.
        self.devices = mvnc.EnumerateDevices()

        if len(self.devices) == 0:
            print("There are no plugged in devices ... exiting ...")
            # something went wrong
            return -1

        # Get a handle to the first enumerated device and open it
        self.device = mvnc.Device(self.devices[0])
        self.device.OpenDevice()

        # Read the graph file into a buffer
        with open(self.GRAPH_PATH, mode='rb') as f:
            self.blob = f.read()

        # Load the graph buffer into the NCS
        self.graph = self.device.AllocateGraph(self.blob)

        # everything went good
        return 1

    # runs the image detection AI
    def runAI(self, picture):
        # convert format
        picture = picture.astype(numpy.float32)
        # Read & resize image (make useful operations on it)
        dx, dy, dz = picture.shape
        delta = float(abs(dy - dx))
        if dx > dy:  # crop the x dimension
            picture = picture[int(0.5 * delta):dx - int(0.5 * delta), 0:dy]
        else:
            picture = picture[0:dx, int(0.5 * delta):dy - int(0.5 * delta)]
        picture = cv2.resize(picture, self.IMAGE_DIM)

        picture = cv2.cvtColor(picture, cv2.COLOR_BGR2RGB)

        for i in range(3):
            picture[:, :, i] = (picture[:, :, i] - self.MEAN) * self.STANDARD_DEVIATION

        # Load the image as a half-precision floating point array
        self.graph.LoadTensor(picture.astype(numpy.float16), 'user object')

        # Get the results from NCS
        output, userobj = self.graph.GetResult()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PRINT RESULT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Print the results
        #print('~ FINAL RESULT:')

        labels = numpy.loadtxt(self.LABELS_FILE_PATH, str, delimiter='\t')

        order = output.argsort()[::-1][:self.NUM_OF_GUESSES + 1]
        """
        for i in range(0, self.NUM_OF_GUESSES):
            print('~ Prediction ' + str(i + 1) + ' is ' + labels[order[i]] + " with " + str(
                round(output[order[i]] * 100, 3)) + "%")
        """
        for i in range(0, self.NUM_OF_GUESSES):
            print('~ Prediction: ' + labels[order[i]])
            
        print("~ DONE...\n")
        return labels[order[i]]

    # close the graph and the device
    def close(self):
        # closing
        self.graph.DeallocateGraph()
        self.device.CloseDevice()


# run the program by creating an object of that class
x = Pokedex()
print("---Program Ended Gracefully---")
