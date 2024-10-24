import tkinter as tk
import requests
import pygame

#initialize the pygame mixer
pygame.mixer.init()

#works at least
def play_song():
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


def search():
    #two approaches, make one single text entry (HARD) i find this to be quite impossible and i have a time limit but maybe?
    # make multuiple entries(EASY) i have a vision but omg
    #query = search_entry.get() # Get the text
    track_title = search_title_entry.get()      
    track_artist = search_artist_entry.get()
    track_album = search_ablum_entry.get()
    params = {} #initialize dictionary
    #These will either be false or true depending if anything was provided
    if track_title:
        params["title"] = track_title #adding the input within the params
    if track_artist:
        params["artist"] = track_artist
    if track_album:
        params["album"] = track_album
    try:
        response = requests.get("http://127.0.0.1:5000/search-track", params=params)  #how to implement it.... no clue
        print(response.text)
        
        if response.status_code == 200:
            track_data = response.json()
            result_text = "\n".join(f"Title: {track['title']}, Artist: {track['artist']}, Album: {track['album']}" for track in track_data)
            result_search_label.config(text=result_text)  # Update label with results
        else:
            result_search_label.config(text="Song not found")
    except Exception as e:
        result_search_label.config(text=f"Error: {e}")

def fetch_songs(): #making sure API works as intended
    try:
        response = requests.get("http://127.0.0.1:5000/get-ALL-tracks")  # Your Flask API endpoint
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
window = tk.Tk()
window.title("Music Library")
window.geometry("1920x1080")

# button to fetch ALL songs
fetch_button = tk.Button(window, text="Fetch Songs", command=fetch_songs)
fetch_button.pack(pady=10)

# text area to display the song list
text_area = tk.Text(window, wrap=tk.WORD, height=15, width=60)
text_area.pack(pady=20)

# entry field for the song ID
track_id_entry = tk.Entry(window, width=10)
track_id_entry.pack(pady=20)

# button to fetch ONE song
fetch_button = tk.Button(window, text="Fetch Track", command=fetch_track)
fetch_button.pack(pady=10)

# button to play the song
play_button = tk.Button(window, text="Play Song", command=play_song)
play_button.pack(pady=10)

# Label to display the result
# text area stinks
result_label = tk.Label(window, text="")
result_label.pack(pady=20)


#container window for title entry and label
input_frame = tk.Frame(window, bd=5, relief=tk.SUNKEN)
input_frame.pack(pady=10)

#the  elements within the window
title_label = tk.Label(input_frame, text="Title:")
title_label.grid(row=0, column=0, padx=10, pady=10)
search_title_entry = tk.Entry(input_frame, width=10)
search_title_entry.grid(row=0, column=1, padx=10, pady=10)

artist_label = tk.Label(input_frame, text="Artist:")
artist_label.grid(row=1, column=0, padx=10, pady=10)
search_artist_entry = tk.Entry(input_frame, width=10)
search_artist_entry.grid(row=1, column=1, padx=10, pady=10)

album_label = tk.Label(input_frame, text="Album:")
album_label.grid(row=2, column=0, padx=10, pady=10)
search_ablum_entry = tk.Entry(input_frame, width=10)
search_ablum_entry.grid(row=2, column=1, padx=10, pady=10)

#search button
search_button = tk.Button(window, text="Get the song", command=search)
search_button.pack(pady=0)

#results for search
result_search_label = tk.Label(window, text="")
result_search_label.pack(pady=20)


# Run the Tkinter main loop
window.mainloop()
