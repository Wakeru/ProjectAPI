import tkinter as tk
import requests
import pygame

#initialize the pygame mixer
pygame.mixer.init()


def play_song():
    pygame.mixer.music.load("ProjAPI\music\Karma Police - Pierce The Veil.mp3")  # Change to your music file path
    response = requests.get("http://127.0.0.1:5000/get-track/{track_ID}")
    songs = response.json()
    pygame.mixer.music.play(loops=0) #so it wont loop

    
def fetch_track():
    track_id = track_id_entry.get()  # Get the song ID from the text field
    try:
        response = requests.get(f"http://127.0.0.1:5000/get-song/{track_id}")  # Adjust the URL as necessary
        if response.status_code == 200:
            track_data = response.json()
            result_label.config(text=f"Title: {track_data['title']}, Artist: {track_data['artist']}")
        else:
            result_label.config(text="Song not found")
    except Exception as e:
        result_label.config(text=f"Error: {e}")

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

# button to fetch ALL songs
fetch_button = tk.Button(window, text="Fetch Track", command=fetch_track)
fetch_button.pack(pady=10)

# button to play the song
play_button = tk.Button(window, text="Play Song", command=play_song)
play_button.pack(pady=10)

# Label to display the result
# text area stinks
result_label = tk.Label(window, text="")
result_label.pack(pady=20)


# Run the Tkinter main loop
window.mainloop()
