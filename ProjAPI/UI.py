import tkinter as tk
import requests
import pygame

#initialize the pygame mixer
pygame.mixer.init()
is_paused = False

#works at least
def play_song():
    global is_paused
    is_paused = False #reset it to play the song
    track_id = track_id_entry.get()
    #pygame.mixer.music.load({})  # Change to your music file path
    try:
        response = requests.get(f"http://127.0.0.1:5000/get-track/{track_id}")  # Get the info from API
        if response.status_code == 200:
            track_data = response.json()
            # result_label.config(text=f"Title: {track_data['title']}, Artist: {track_data['artist']}")
            result_label.config(text=f"Now playing - Title: {track_data['title']}, Artist: {track_data['artist']}")
            pygame.mixer.music.load("ProjAPI\music\Vhs.mp3") #cannot be named \vhs.mp3 cuz \v means something diff!!!
            pygame.mixer.music.play(loops=0)
            pygame.time.delay(2000)
            pygame.mixer.music.load(track_data['path'])
            pygame.mixer.music.play(loops=0)
        else:
            result_label.config(text="Song not found")
    except Exception as e:
        result_label.config(text=f"Error: {e}")
    #pygame.mixer.music.play(loops=0) #so it wont loop

def toggle_pause():
    global is_paused
    if is_paused:
        pygame.mixer.music.unpause()
        pause_button.config(text="Pause")  # Update button text to "Pause"
    else:
        pygame.mixer.music.pause()
        pause_button.config(text="Resume")  # Update button text to "Resume"
    is_paused = not is_paused  # Toggle the paused state
    
def fetch_track():
    track_id = track_id_entry.get()  # Get the song ID from the text field
    try:
        response = requests.get(f"http://127.0.0.1:5000/get-track/{track_id}")  # Adjust the URL as necessary
        if response.status_code == 200:
            track_data = response.json()
            result_label.config(text=f"Title: {track_data['title']}, Artist: {track_data['artist']}")
        else:
            result_label.config(text="Song not found")
    except Exception as e:
        result_label.config(text=f"Error: {e}")

# Play a specific song
def play_spec_song(track_path, track_title, track_artist):
    try:
        result_label.config(text=f"Now playing - Title: {track_title}, Artist: {track_artist}")
        pygame.mixer.music.load("ProjAPI/music/Vhs.mp3") #cannot be named \vhs.mp3 cuz \v means something diff!!!
        pygame.mixer.music.play(loops=0)
        pygame.time.delay(2000)
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play(loops=0)
    except Exception as e:
        result_label.config(text=f"Error: {e}")

def search():
    #two approaches, make one single text entry (HARD) i find this to be quite impossible and i have a time limit but maybe?
    # make multuiple entries(EASY) i have a vision but omg
    #query = search_entry.get() # Get the text and try the hard way
    #destroy the results every time i press search in order to refresh it
    for widget in result_search_frame.winfo_children(): 
        widget.destroy()

    track_title = search_title_entry.get()      
    track_artist = search_artist_entry.get()
    track_album = search_ablum_entry.get()
    params = {} #initialize dictionary
    #These will either be false or true depending if anything was provided in the entry
    if track_title:
        params["title"] = track_title #adding the input within the params
    if track_artist:
        params["artist"] = track_artist
    if track_album:
        params["album"] = track_album
    try:
        response = requests.get("http://127.0.0.1:5000/search-track", params=params)  #how to implement it.... no clue
        print(response.text)
        track_data = response.json()

        if response.status_code == 200:
            for i,track in enumerate(track_data):
                
                # Make a frame for the border
                track_frame = tk.Frame(result_search_frame, bd=2, relief="groove", padx=10, pady=5)
                track_frame.grid(row=i, column=0, sticky="w", padx=10, pady=5, columnspan=4) 
                # Display each track info
                track_info = f"Title: {track['title']} | Artist: {track['artist']} | Album: {track['album']} | BPM: {track['bpm']} | Key: {track['key']}"
                track_label = tk.Label(track_frame, text=track_info)
                track_label.grid(row = 0, column =0, padx =10, pady = 5)

                # Create a play button for each track
                play_button = tk.Button(
                    track_frame,
                    text="Play",
                    command=lambda path=track["path"], title=track["title"], artist=track["artist"]: # LAMBDA  creates an anonymous (inline) function that takes no parameters but allows me to pass in the values from the track dictionary (such as path, title, and artist)
                        play_spec_song(path, title, artist)
                )
                play_button.grid(row=0, column=1, padx=5)# Update label with results

                #Create a vocal and beat button for each track
                vocal_button = tk.Button(
                    track_frame,
                    text="Vocals",
                    command=lambda path=track["path"], title=track["title"], artist=track["artist"], bpm=track["bpm"],vocal=track["vocal"], beats=track["beats"]: 
                        set_vocal_info(path, title, artist, bpm, vocal, beats) #make some logic here! im almost done!!!!!!
                )
                vocal_button.grid(row=0, column=2, padx=5)# Update label with results

                beats_button = tk.Button(
                    track_frame,
                    text="Beats",
                    command=lambda path=track["path"], title=track["title"], artist=track["artist"], bpm=track["bpm"],vocal=track["vocal"], beats=track["beats"]: 
                        set_beat_info(path, title, artist, bpm, vocal, beats)
                )
                beats_button.grid(row=0, column=3, padx=5)# Update label with results
        else:
            result_search_label.config(text="Song not found")
    except Exception as e:
        result_search_label.config(text=f"Error: {e}")

# Logic for the Vocal and Beat Button

selected_vocal_track = None
selected_beat_track = None
def set_vocal_info(path,title,artist,bpm,vocal,beats):
    global selected_vocal_track
    selected_vocal_track = {"path": path, "title": title, "artist": artist, "bpm": bpm, "vocal":vocal, "beats":beats}

    try: 
        VocalConfirm_label.config(text=f"Vocals Chosen for: {title} by {artist} with a bpm of {bpm}")
    except Exception as e:
        VocalConfirm_label.config(text=f"Error: {e}")
    print(f"Vocal track selected: {selected_vocal_track}")

def set_beat_info(path,title,artist,bpm,vocal,beats):
    global selected_beat_track
    selected_beat_track = {"path": path, "title": title, "artist": artist, "bpm": bpm,"vocal":vocal, "beats":beats} 
    try: 
        BeatConfirm_label.config(text=f"Beats Chosen for: {title} by {artist} with a bpm of {bpm}")
    except Exception as e:
        BeatConfirm_label.config(text=f"Error: {e}")
    print(f"Beat track selected: {selected_beat_track}")


vocal_muted = False
beat_muted = False
def play_mashup_tracks(vocal_path, beat_path):
    global vocal_sound, beat_sound

    
    try:
        # Load the vocal track
        vocal_sound = pygame.mixer.Sound(vocal_path)
        vocal_sound.play(loops=0)

        # Load the beat track
        beat_sound = pygame.mixer.Sound(beat_path)
        beat_sound.play(loops=0)
        
    except Exception as e:
        print(f"Error: {e}")

def toggle_vocal():
    global vocal_muted, vocal_sound

    if not vocal_muted:
        vocal_sound.set_volume(0)  # Mute vocal track
        vocal_muted = True
        mute_vocal.config(text="Unmute Vocal")
    else:
        vocal_sound.set_volume(1)  # Unmute vocal track
        vocal_muted = False
        mute_vocal.config(text="Mute Vocal")

def toggle_beat():
    global beat_muted, beat_sound
    
    if not beat_muted:
        beat_sound.set_volume(0)  # Mute beat track
        beat_muted = True
        mute_beats.config(text="Unmute Beats")
    else:
        beat_sound.set_volume(1)  # Unmute beat track
        beat_muted = False
        mute_beats.config(text="Mute Beats")

is_playing = True
def toggle_mashup():
    global is_playing
    
    if is_playing:
        # Pause (stop both tracks)
        vocal_sound.stop()
        beat_sound.stop()
        toggle_mashup_button.config(text="Restart") 
        is_playing = False
    else:
        # Resume (play both tracks)
        vocal_sound.stop()  # why is it overlapping?
        beat_sound.stop()
        vocal_sound.play()
        beat_sound.play()
        toggle_mashup_button.config(text="Stop")  # Change button text to Stop
        is_playing = True

def mashup():
    if selected_vocal_track and selected_beat_track:
        vocal_title = selected_vocal_track["title"]
        vocal_artist = selected_vocal_track["artist"]
        vocal_path = selected_vocal_track["vocal"]
        beat_title = selected_beat_track["title"]
        beat_artist = selected_beat_track["artist"]
        beat_path = selected_beat_track["beats"]
        MashupConfirm_label.config(text=f"Mashing Up: Audio from {vocal_title} by {vocal_artist} WITH Beats from {beat_title} by {beat_artist}!")
        print("Using Selected Tracks:")
        print(f"Vocals: {selected_vocal_track}")
        print(f"Beats: {selected_beat_track}")
        play_mashup_tracks(vocal_path, beat_path)

    else:
        print("Error: Both vocal and beat tracks must be selected.")
        MashupConfirm_label.config(text=f"Error: Both vocal and beat tracks must be selected!")




# find a website that can split a song into vocals and beats
#use channels to play two audios at the same time
link1 = ("https://stackoverflow.com/questions/38028970/how-to-assign-sounds-to-channels-in-pygame")
# make a stop button, forgot aobut that


def fetch_songs(): #making sure API works as intended
    try:
        response = requests.get("http://127.0.0.1:5000/get-ALL-tracks")  # Flask API endpoint
        songs = response.json()  # Parse the response JSON
        
        # Clear the text area before inserting new data
        text_area.delete(1.0, tk.END)
        
        # Display the songs in the text area
        for song in songs:
            song_info = f"Song ID: {song['id']}\n Title: {song['title']}\n Artist: {song['artist']}\n Album: {song['album']}\n\n"
            text_area.insert(tk.END, song_info)
    except Exception as e:
        text_area.insert(tk.END, f"Error fetching songs: {e}\n")

# Set up the Tkinter window
# tkinter/python package dont got fit contents for text field ;(
#RIP shouldve put it in a scrollable canvas first
window = tk.Tk()
window.title("Project API")
window.geometry("1920x1080")




# button to fetch ALL songs
fetch_button = tk.Button(window, text="Fetch All Songs", command=fetch_songs)
fetch_button.pack(pady=10)

# text area to display the song list
text_area = tk.Text(window, wrap=tk.WORD, height=7, width=60)
text_area.pack(pady=5)




# # entry field for the song ID
# track_id_entry = tk.Entry(window, width=10)
# track_id_entry.pack(pady=10)

# # button to fetch ONE song
# fetch_button = tk.Button(window, text="Fetch Track", command=fetch_track)
# fetch_button.pack(pady=5)

# # button to play the song
# play_button = tk.Button(window, text="Play Song", command=play_song)
# play_button.pack(pady=5)


# Label to display the result
# text area stinks
result_label = tk.Label(window, text="")
result_label.pack(pady=10)


#container window for title entry and label
input_frame = tk.Frame(window, bd=5, relief=tk.SUNKEN)
input_frame.pack(pady=10)

#the  elements within the window
title_label = tk.Label(input_frame, text="Title:")
title_label.grid(row=0, column=0, padx=10, pady=10)
search_title_entry = tk.Entry(input_frame, width=10)
search_title_entry.grid(row=0, column=1, padx=10, pady=10)
#---------------
artist_label = tk.Label(input_frame, text="Artist:")
artist_label.grid(row=1, column=0, padx=10, pady=10)
search_artist_entry = tk.Entry(input_frame, width=10)
search_artist_entry.grid(row=1, column=1, padx=10, pady=10)
#---------------
album_label = tk.Label(input_frame, text="Album:")
album_label.grid(row=2, column=0, padx=10, pady=10)
search_ablum_entry = tk.Entry(input_frame, width=10)
search_ablum_entry.grid(row=2, column=1, padx=10, pady=10)

#Search/Pause Frame
searchAndpauseframe = tk.Frame(window)
searchAndpauseframe.pack(pady=5)
#search button
search_button = tk.Button(searchAndpauseframe, text="Get Songs", command=search)
search_button.grid(row=0, column=0, padx=5, pady=5)
#Pause Button
pause_button = tk.Button(searchAndpauseframe, text="Pause", command=toggle_pause)
pause_button.grid(row=0, column=1, padx=5, pady=5)
#---------------
#results for search
result_search_frame = tk.Frame(window)
result_search_frame.pack(pady=5)

result_search_label = tk.Label(window, text="")
result_search_label.pack(pady=20)

confirm_frame = tk.Frame(window, bd=5, relief="ridge")
confirm_frame.pack(pady=0)
#Confirmation Label
VocalConfirm_label = tk.Label(confirm_frame, text="Wating For Vocals!")  
VocalConfirm_label.grid(row=0, column=0, padx=10, pady=10)
BeatConfirm_label = tk.Label(confirm_frame, text="Waiting For Beats!")  
BeatConfirm_label.grid(row=1, column=0, padx=10, pady=10)

#mashup frame
masuhp_frame = tk.Frame(window, bd=5, relief="flat")
masuhp_frame.pack(pady=0)
#mashup button
mashup_button = tk.Button(masuhp_frame, text="Mashup!", command=mashup)
mashup_button.grid(row=0, column=0, padx=5, pady=5)
mute_vocal = tk.Button(masuhp_frame, text="Mute Vocal", command=toggle_vocal)
mute_vocal.grid(row=0, column=1, padx=5, pady=5)
mute_beats = tk.Button(masuhp_frame, text="Mute Beats", command=toggle_beat)
mute_beats.grid(row=0, column=2, padx=5, pady=5)
toggle_mashup_button = tk.Button(masuhp_frame, text="Stop", command=toggle_mashup)
toggle_mashup_button.grid(row=0, column=3, padx=5, pady=5)

#mashup confirmation
MashupConfirm_label = tk.Label(window, text="")  
MashupConfirm_label.pack(pady=5)

# Run the Tkinter main loop
window.mainloop()
