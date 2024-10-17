import tkinter as tk
import requests
import pygame

#initialize the pygame mixer
pygame.mixer.init()


def play_song():
    track_id = track_id_entry.get()
    #pygame.mixer.music.load({})  # Change to your music file path
    try:
        response = requests.get(f"http://127.0.0.1:5000/get-track/{track_id}")  # Get the info from API
        if response.status_code == 200:
            track_data = response.json()
            # result_label.config(text=f"Title: {track_data['title']}, Artist: {track_data['artist']}")
            result_label.config(text=f"Its working!")
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
    track_str = search_entry.get()  # Get the text
    try:
        response = requests.get(f"http://127.0.0.1:5000/search-track/{track_str}")  
        if response.status_code == 200:
            track_data = response.json()
            result_search_label.config(text=f"Title: {track_data['title']}, Artist: {track_data['artist']}")
        else:
            result_search_label.config(text="Song not found")
    except Exception as e:
        result_search_label.config(text=f"Error 2: {e}")

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




#text entry for search
search_entry = tk.Entry(window, width=10)
search_entry.pack(pady=20)

#search button
search_button = tk.Button(window, text="Get the song", command=search)
search_button.pack(pady=10)

#results for search
result_search_label = tk.Label(window, text="")
result_search_label.pack(pady=20)


# Run the Tkinter main loop
window.mainloop()
