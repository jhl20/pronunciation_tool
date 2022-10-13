
import os
import sounddevice as sd
from pydub import AudioSegment as AS
from pydub.playback import play
from scipy.io.wavfile import write
import speech_recognition as sr
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import auditok
import contextlib
import wave
import sqlite3
from tkinter import*
from tkinter.ttk import*
from tkinter import filedialog
from PIL import Image, ImageTk
import pyphen
import shutil


# converting m4a to wav
def m4atowav():
    """
    Title: Python script to convert m4a files to wav files
    Author: Arjun Sharma
    Date: 2019
    Availability: https://gist.github.com/arjunsharma97/0ecac61da2937ec52baf61af1aa1b759"""
    convertFrom = ['.m4a']
    for (dirpath, dirnames, filenames) in os.walk("m4a/"):
        for filename in filenames:
            if filename.endswith(tuple(convertFrom)):
                filepath = dirpath + '/' + filename
                (path, file_extension) = os.path.splitext(filepath)
                file_extension_final = file_extension.replace('.', '')
                try:
                    audio = AS.from_file(filepath, file_extension_final)
                    wav_filename = filename.replace(file_extension_final, 'wav')
                    wav_path = dirpath + '/' + wav_filename
                    print('Converting: ' + str(filepath))
                    audio.export(wav_path, format='wav')
                    os.remove(filepath)
                except:
                    print("Conversion Error " + str(filepath))


# Play WAV
def play_wav(filename):
    for (dirpath, dirnames, filenames) in os.walk("m4a/"):
        if filename in filenames:
            filepath = dirpath + '/' + filename
            sound = AS.from_wav(filepath)
            print("Wave Playing")
            play(sound)

# Play from output, always wav file so won't need to convert using m4atowav
def play_wavout(filename):
    for (dirpath, dirnames, filenames) in os.walk("out/"):
        if filename in filenames:
            filepath = dirpath + '/' + filename
            sound = AS.from_wav(filepath)
            print("Wave Playing")
            play(sound)


# Recording WAV
def record(name):
    # int 16 reduces samplewidth to 2, in line with provided audio
    # bit depth being 16 along with a sample frequency of 48000 allows for
    # the recording to be of bit rate 768
    sd.default.dtype = 'int16', 'int16'  # Saving file as an integer format
    fs = 48000  # Sample frequency
    seconds = 5  # Duration of recording in seconds

    print("Recording")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write("out/" + name, fs, myrecording)  # Save as WAV file
    print("Recording Stopped")


# Speech To Text, filename = 'name.wav'
def speech2text(filename):
    for (dirpath, dirnames, filenames) in os.walk("m4a/"):
        if filename in filenames:
            filepath = dirpath + '/' + filename
            # filename = filename
            # initialize the recognizer
            r = sr.Recognizer()
             # open the file
            with sr.AudioFile(filepath) as source:
                # listen for the data (load audio to memory)
                audio_data = r.record(source)
                # recognize (convert from speech to text)
                text = r.recognize_google(audio_data)
                print(text)
                return text


def speech2textout(filename):
    for (dirpath, dirnames, filenames) in os.walk("out/"):
        if filename in filenames:
            filepath = dirpath + '/' + filename
            # filename = filename
            # initialize the recognizer
            r = sr.Recognizer()
             # open the file
            with sr.AudioFile(filepath) as source:
                # listen for the data (load audio to memory)
                audio_data = r.record(source)
                # recognize (convert from speech to text)
                text = r.recognize_google(audio_data)
                print(text)
                return text


# def plotwave(filename):
#     for (dirpath, dirnames, filenames) in os.walk("m4a/"):
#         if filename in filenames:
#             filepath = dirpath + '/' + filename
#             input_data = wave.open(filepath, 'r')
#             sample_rate = 16000
#             sig = np.frombuffer(input_data.readframes(sample_rate), dtype=np.int16)
#             sig = sig[:]
#
#             plot_a = plt.subplot(211)
#             plot_a.plot(sig)
#             plot_a.set_xlabel('sample rate * time')
#             plot_a.set_ylabel('energy')
#
#             plt.show()


def plotwave(filename):
    # read audio samples
    for (dirpath, dirnames, filenames) in os.walk("out/"):
        if filename in filenames:
            filepath = dirpath + '/' + filename
            data = read(filepath)
            # Audio data
            audio = data[1]

            # # Calculating onset and offset times
            # call_onsets = np.asarray(call_detector(audio, 200, 2, 44100, 30))
            # call_offsets = np.asarray(call_detector(audio[::-1], 200, 2, 44100, 30))
            # for i in range(len(call_offsets)):
            #     call_offsets[i] = len(audio) - call_offsets[i] - 1
            # call_offsets = np.asarray(call_offsets[::-1])
            #
            # [[call_onsets[i], call_offsets[i]] for i in range(min(len(call_onsets), len(call_offsets)))]

            # plot samples equal to the length of audio file
            plt.plot(audio[0:len(audio)])

            # for onset in call_onsets:
            #     plot.axvline(x=onset / 44100, color='g')
            # for offset in call_offsets:
            #     plot.axvline(x=offset / 44100, color='r')

            # label the axes
            plt.ylabel("Amplitude")
            plt.xlabel("Time")
            # set the title
            if filename == "prof_spliced.wav":
                plt.title("Professional Audio")
                plt.savefig('prof_graph.png')
            elif filename == "user_spliced.wav":
                plt.title("Your Attempt")
                plt.savefig('your_graph.png')
            elif filename == "profNorm.wav":
                plt.title("Professional Normalised")
                plt.savefig('profnorm.png')
            elif filename == "userNorm.wav":
                plt.title("User Normalised")
                plt.savefig('usernorm.png')
            # display the plot
            # plt.show()
            plt.clf()


def normalize(filename, filename2):
    for (dirpath, dirnames, filenames) in os.walk("out/"):
        if filename in filenames and filename2 in filenames:
            filepath = dirpath + '/' + filename
            filepath2 = dirpath + '/' + filename2
            command = f"ffmpeg-normalize {filepath} {filepath2} -o out/profNorm.wav out/userNorm.wav -f -tp 0.0"
            os.system(command)


def spectrogram(filename):
    for (dirpath, dirnames, filenames) in os.walk("out/"):
        if filename in filenames:
            filepath = dirpath + '/' + filename
            samplingFrequency, signalData = read(filepath)

            plt.title('Spectrogram')
            plt.specgram(signalData, Fs=samplingFrequency, NFFT=512)
            plt.xlabel('Time')
            plt.ylabel('Frequency')
            plt.show()


# def spectrogram(filename):
#     for (dirpath, dirnames, filenames) in os.walk("m4a/"):
#         if filename in filenames:
#             filepath = dirpath + '/' + filename
#             # Read the .wav file
#             samplingFrequency, signalData = read(filepath)
#
#             # Spectrogram of .wav file
#             sampleFreq, segmentTime, specData = signal.spectrogram(signalData, samplingFrequency)
#
#             plt.pcolormesh(segmentTime, sampleFreq, specData)
#             plt.ylabel('Frequency [Hz]')
#             plt.xlabel('Time [sec]')
#             plt.show()

# def call_detector(signal, threshold, dispersion, rate, window):
#     separation = dispersion * rate
#     noise = separation + 1
#     output = []
#     for i in range(len(signal) - window - 1):
#         if np.mean(signal[i : i + window]) < threshold:
#             noise += 1
#         elif np.mean(signal[i : i + window]) > threshold:
#             if noise > separation:
#                 output.append(i)
#             noise = 0
#         return output


# def butter_lowpass(cutoff, nyq_freq, order=4):
#     normal_cutoff = float(cutoff) / nyq_freq
#     b, a = signal.butter(order, normal_cutoff, btype='lowpass')
#     return b, a
#
#
# def butter_lowpass_filter(data, cutoff_freq, nyq_freq, order=4):
#     b, a = butter_lowpass(cutoff_freq, nyq_freq, order=order)
#     y = signal.filtfilt(b, a, data)
#     return y
#
# sample_rate = 1000  # 50 Hz resolution
# cutoff_frequency = 400.0
# y = butter_lowpass_filter("adalimumab_1_a.wav", cutoff_frequency, sample_rate/2)


# Used when testing wave files to check pcm and sample rate
def wave_info(path):
    """Reads a .wav file.
    Takes the path, and returns (PCM audio data, sample rate).
    """
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        # assert num_channels == 2
        sample_width = wf.getsampwidth()
        # assert sample_width == 2
        sample_rate = wf.getframerate()
        # assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        print(pcm_data)
        print(sample_rate)
        return pcm_data, sample_rate


def splice(filename, splicedname):
    """
        Title: Auditok
        Author: Amine Sehili
        Date: 2015
        Availability: https://auditok.readthedocs.io/en/latest/index.html"""
    # split returns a generator of AudioRegion objects
    audio_regions = auditok.split(
        "m4a/"+filename,
        min_dur=0.2,  # minimum duration of a valid audio event in seconds
        max_dur=5,  # maximum duration of an event
        max_silence=0.1,  # maximum duration of tolerated continuous silence before splitting
        energy_threshold=55  # threshold of energy detection for audible audio
    )
    for i, r in enumerate(audio_regions):
        # Regions returned by `split` have 'start' and 'end' metadata fields
        print("Region {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i, r=r))

        # play detection
        # r.play(progress_bar=True)

        # region's metadata can also be used with the `save` method
        # (no need to explicitly specify region's object and `format` arguments)
        # "region_{meta.start:.3f}-{meta.end:.3f}.wav"
        filename = r.save("out/" + splicedname)
        print("region saved as: {}".format(filename))


def spliceout(filename, splicedname):
    """
           Title: Auditok
           Author: Amine Sehili
           Date: 2015
           Availability: https://auditok.readthedocs.io/en/latest/index.html"""
    # split returns a generator of AudioRegion objects
    audio_regions = auditok.split(
        "out/"+filename,
        min_dur=0.2,  # minimum duration of a valid audio event in seconds
        max_dur=5,  # maximum duration of an event
        max_silence=0.1,  # maximum duration of tolerated continuous silence within an event
        energy_threshold=55  # threshold of detection
    )
    for i, r in enumerate(audio_regions):
        # Regions returned by `split` have 'start' and 'end' metadata fields
        print("Region {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i, r=r))

        # play detection
        # r.play(progress_bar=True)

        # region's metadata can also be used with the `save` method
        # (no need to explicitly specify region's object and `format` arguments)
        # "region_{meta.start:.3f}-{meta.end:.3f}.wav"
        filename = r.save("out/" + splicedname)
        print("region saved as: {}".format(filename))


def main():
    m4atowav()
    conn = sqlite3.connect('recordings.db')
    c = conn.cursor()
    comm1 = """CREATE TABLE IF NOT EXISTS terms(filename TEXT PRIMARY KEY, name TEXT, category TEXT)"""
    c.execute(comm1)
    # c.execute("""DROP TABLE IF EXISTS terms""")
    conn.commit()

    # add rows
    for (dirpath, dirnames, filenames) in os.walk("m4a/"):
        c.executemany("INSERT OR IGNORE INTO terms VALUES (?,?,?)", [(filename, '', '') for filename in filenames])

    # c.execute("INSERT INTO terms VALUES('test', 't', 't')")
    c.execute("DELETE FROM terms WHERE filename = 'user_word.wav'")
    c.execute("DELETE FROM terms WHERE filename = 'user_spliced.wav'")
    c.execute("DELETE FROM terms WHERE filename = 'prof_spliced.wav'")

    conn.commit()
    # results = c.fetchall()
    # print(results)

    m = Tk()
    m.title('Pronunciation Tool')
    frame_list = Frame(m)
    frame_list.grid(row=0, column=0)

    # upload file either m4a or wav
    def UploadAction(event=None):
        uploadedfile = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("wav files","*.wav"), ("m4a files", "*.m4a")))
        uploadTo = filedialog.askdirectory(initialdir = "/m4a")
        shutil.copy(uploadedfile, uploadTo)
        print('Selected:')

    uploadButton = Button(frame_list, text='Add file', command=UploadAction)
    uploadButton.grid(row=0, column=5)

    # def copyFile():
    #     print(uploadedfile)
    #     # shutil.copy(uploadedfile, "/m4a")
    #
    # copyButton = Button(frame_list, text='Copy file', command=copyFile)
    # copyButton.grid(row=0, column=6)

    # update database
    def UpdateDatabase():
        m4atowav()
        # add rows
        for (dirpath, dirnames, filenames) in os.walk("m4a/"):
            c.executemany("INSERT OR IGNORE INTO terms VALUES (?,?,?)", [(filename, '', '') for filename in filenames])
        for (dirpath, dirnames, filenames) in os.walk("m4a/"):
            c.executemany("UPDATE terms SET name = ? WHERE filename = ?",[(speech2text(filename), filename) for filename in filenames])
        c.execute("DELETE FROM terms WHERE filename = 'user_word.wav'")
        c.execute("DELETE FROM terms WHERE filename = 'user_spliced.wav'")
        c.execute("DELETE FROM terms WHERE filename = 'prof_spliced.wav'")
        conn.commit()

    updateDatabase = Button(frame_list, text='Update Database', command=UpdateDatabase)
    updateDatabase.grid(row=0, column=4)

    lbl_list = Label(frame_list, text='List of words:', font=('bold', 12), padding=20)
    lbl_list.grid(row=0, column=0, sticky=W)
    word_list = Combobox(frame_list, width=40)

    # Populate Listbox
    query = c.execute("SELECT DISTINCT name FROM terms")
    # print(query.fetchall())
    # Query.fetchall() returned ('name1',), ('name2',), ('name3',)
    # So take only the strings
    query2 = [i[0] for i in query.fetchall()]
    word_list['values'] = query2

    def allCategories():
        query = c.execute("SELECT DISTINCT name FROM terms")
        query2 = [i[0] for i in query.fetchall()]
        word_list['values'] = query2

    # gives the combobox a search functionality
    def check_input(event):
        value = event.widget.get()
        if value == '':
            word_list['values'] = query2
        else:
            data = []
            for item in query2:
                if value.lower() in item.lower():
                    data.append(item)
            word_list['values'] = data

    word_list.bind('<KeyRelease>', check_input)
    # print(word_list)
    word_list.grid(row=0, column=1)

    lbl_category = Label(frame_list, text='Categories:', font=('bold', 12), padding=20)
    lbl_category.grid(row=1, column=0, sticky=W)
    category_list = Combobox(frame_list, width=40)

    def reloadCategory():
        # Populate Listbox
        query3 = c.execute("SELECT DISTINCT category FROM terms")
        query4 = [i[0] for i in query3.fetchall()]
        # print(query4)
        category_list['values'] = query4

    # print(category_list['values'])
    category_list.grid(row=1, column=1)

    def updateCategory():
        # print(category_list.get())
        if category_list.get():
            query5 = c.execute("SELECT DISTINCT name FROM terms WHERE category LIKE ?", ('%' + category_list.get() + '%',))
            query6 = [i[0] for i in query5.fetchall()]
            # print(query6)
            word_list['values'] = query6

    # print(category_list.get())
    btn_category = Button(frame_list, text = 'Select category', padding=20, command=updateCategory)
    btn_category.grid(row=1, column=2)

    btn_allCategory = Button(frame_list, text='All categories', padding=20, command=allCategories)
    btn_allCategory.grid(row=1, column=3)

    btn_reloadCategory = Button(frame_list, text='Reload categories', padding=20, command=reloadCategory)
    btn_reloadCategory.grid(row=1, column=4)

    lbl_rename_category = Text(frame_list, font=('bold', 12), height=1, width=40)
    lbl_rename_category.grid(row=2, column=0)

    def updateTermCat():
        # making sure text box is not empty
        if not lbl_rename_category.compare("end-1c", "==", "1.0"):
            res = str(lbl_rename_category.get("1.0", "end-1c"))
            print(res)
             # query the primary key for each name based on the word_list
            q = c.execute("SELECT filename FROM terms WHERE name LIKE ?", ('%' + word_list.get() + '%',))
            id = str(q.fetchone()[0])
            if not res.isspace():
                c.execute("UPDATE terms SET category = ? WHERE filename = ?", (res, id))
                conn.commit()
            lbl_rename_category.delete("1.0", "end")

    btn_renameCat = Button(frame_list, text='Rename category', padding=20, command=updateTermCat)
    btn_renameCat.grid(row=2, column=1)

    def deleteWord():
        q = c.execute("SELECT filename FROM terms WHERE name LIKE ?", ('%' + word_list.get() + '%',))
        id = str(q.fetchone()[0])
        print(id)
        c.execute("DELETE FROM terms WHERE filename = ?", (id,))
        conn.commit()

    dltWord = Button(frame_list, text='Delete word from database', padding=20, command=deleteWord)
    dltWord.grid(row=1, column=5)

    # h = Hyphenator('en_US')
    dic = pyphen.Pyphen(lang='nl_NL')
    wordVar = StringVar()
    syllVar = StringVar()

    # select button
    def select():
        # play_wav(word_list.get())
        # print(word_list.get())
        # query the primary key for each name based on the word_list
        q = c.execute("SELECT filename FROM terms WHERE name LIKE ?", ('%' + word_list.get() + '%',))
        id = str(q.fetchone()[0])

        # print(dic.inserted(word_list.get()))
        # print(h.syllables(word_list.get()))
        # wordVar = StringVar()
        # syllVar = StringVar()
        wordVar.set("Word: " + speech2text(id))
        syllVar.set("Syllables: " + dic.inserted(word_list.get()))
        play_wav(id)
        # return speech2text(word_list.get())

    word = Label(frame_list, textvariable =wordVar, padding=20)
    wordToSyll = Label(frame_list, textvariable=syllVar, padding=20)
    word.grid(row=3, column=0)
    wordToSyll.grid(row=3, column=1)

    playbtn = Button(frame_list, text='Play word', padding=20, command=select)
    playbtn.grid(row=0, column=2)

    def btnrec():
        record("user_word.wav")
        # Toplevel object which will
        # be treated as a new window
        newWindow = Toplevel(m)

        # sets the title of the
        # Toplevel widget
        newWindow.title("Results")

        q = c.execute("SELECT filename FROM terms WHERE name LIKE ?", ('%' + word_list.get() + '%',))
        id = str(q.fetchone()[0])

        if speech2text(id) == speech2textout("user_word.wav"):
            resultCheck = "Correct"
            result = Label(newWindow, text=resultCheck, padding=20)
            result.grid(row=0, column=0)
        else:
            resultCheck = "Wrong. What we think you said: " + speech2textout("user_word.wav")
            result = Label(newWindow, text=resultCheck, padding=20)
            result.grid(row=0, column=0)

        spliceout("user_word.wav", "user_spliced.wav")
        splice(id, "prof_spliced.wav")
        plotwave("user_spliced.wav")
        plotwave("prof_spliced.wav")
        load = Image.open("your_graph.png")
        render = ImageTk.PhotoImage(load)
        panel = Label(newWindow, image=render)
        panel.image = render
        panel.grid(row=1, column=0)
        load3 = Image.open("prof_graph.png")
        render3 = ImageTk.PhotoImage(load3)
        panel3 = Label(newWindow, image=render3)
        panel3.image = render3
        panel3.grid(row=1, column=1)
        normalize("prof_spliced.wav", "user_spliced.wav")
        plotwave("profNorm.wav")
        plotwave("userNorm.wav")
        load4 = Image.open("profnorm.png")
        render4 = ImageTk.PhotoImage(load4)
        panel4 = Label(newWindow, image=render4)
        panel4.image = render4
        panel4.grid(row=2, column=1)
        load2 = Image.open("usernorm.png")
        render2 = ImageTk.PhotoImage(load2)
        panel2 = Label(newWindow, image=render2)
        panel2.image = render2
        panel2.grid(row=2, column=0)

        def playUser():
            play_wavout("user_spliced.wav")

        def playProf():
            play_wavout("prof_spliced.wav")

        userBut = Button(newWindow, text="Play your recording", command=playUser)
        userBut.grid(row=0, column=1)
        profBut = Button(newWindow, text="Play professional recording", command=playProf)
        profBut.grid(row=0, column=2)

    recbtn = Button(frame_list, text ='Rec word', padding=20, command=btnrec)
    recbtn.grid(row=0, column=3)
    m.mainloop()
    c.close()
    conn.close()


if __name__ == "__main__":
    main()