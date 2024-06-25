import pygame
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from mutagen.mp3 import MP3

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.playlist = []
        self.current_index = 0
        self.volume = 0.5
        self.is_paused = False
        self.is_muted = False

    def add_song(self, song_path):
        self.playlist.append(song_path)

    def play_song(self):
        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            self.is_paused = False
            self.is_muted = False

    def pause_song(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.is_paused = not self.is_paused

    def mute_song(self):
        if self.is_muted:
            pygame.mixer.music.set_volume(self.volume)
        else:
            pygame.mixer.music.set_volume(0)
        self.is_muted = not self.is_muted

    def next_song(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_song()

    def previous_song(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_song()

    def shuffle_playlist(self):
        random.shuffle(self.playlist)

    def repeat_song(self):
        if self.playlist:
            pygame.mixer.music.play()

    def count_songs(self):
        return len(self.playlist)

    def set_volume(self, volume):
        self.volume = volume
        if not self.is_muted:
            pygame.mixer.music.set_volume(self.volume)

    def get_song_duration(self):
        if self.playlist:
            audio = MP3(self.playlist[self.current_index])
            return audio.info.length
        return 0

    def live_song_duration(self):
        return pygame.mixer.music.get_pos() / 1000

    def get_current_song(self):
        return self.playlist[self.current_index] if self.playlist else None

class MusicPlayerGUI:
    def __init__(self, root, player):
        self.player = player
        self.root = root
        self.root.title("Music Player")
        self.root.configure(bg="#222222")

        # Frame for buttons
        button_frame = tk.Frame(root, bg="#222222")
        button_frame.pack(pady=20)

        # Upload button
        self.upload_button = tk.Button(button_frame, text="Upload", command=self.upload_song, bg="#444444", fg="#FFFFFF", bd=2, relief="raised", font=("Arial", 12), width=15)
        self.upload_button.grid(row=0, column=0, pady=5)

        # Play button
        self.play_button = tk.Button(button_frame, text="Play", command=self.play_song, bg="#444444", fg="#FFFFFF", bd=2, relief="raised", font=("Arial", 12), width=15)
        self.play_button.grid(row=1, column=0, pady=5)

        # Pause button
        self.pause_button = tk.Button(button_frame, text="Pause", command=self.player.pause_song, bg="#444444", fg="#FFFFFF", bd=2, relief="raised", font=("Arial", 12), width=15)
        self.pause_button.grid(row=2, column=0, pady=5)

        # Mute button
        self.mute_button = tk.Button(button_frame, text="Mute", command=self.player.mute_song, bg="#444444", fg="#FFFFFF", bd=2, relief="raised", font=("Arial", 12), width=15)
        self.mute_button.grid(row=3, column=0, pady=5)

        # Next button
        self.next_button = tk.Button(button_frame, text="Next", command=self.player.next_song, bg="#444444", fg="#FFFFFF", bd=2, relief="raised", font=("Arial", 12), width=15)
        self.next_button.grid(row=4, column=0, pady=5)

        # Previous button
        self.prev_button = tk.Button(button_frame, text="Previous", command=self.player.previous_song, bg="#444444", fg="#FFFFFF", bd=2, relief="raised", font=("Arial", 12), width=15)
        self.prev_button.grid(row=5, column=0, pady=5)

        # Shuffle button
        self.shuffle_button = tk.Button(button_frame, text="Shuffle", command=self.player.shuffle_playlist, bg="#444444", fg="#FFFFFF", bd=2, relief="raised", font=("Arial", 12), width=15)
        self.shuffle_button.grid(row=6, column=0, pady=5)

        # Repeat button
        self.repeat_button = tk.Button(button_frame, text="Repeat", command=self.player.repeat_song, bg="#444444", fg="#FFFFFF", bd=2, relief="raised", font=("Arial", 12), width=15)
        self.repeat_button.grid(row=7, column=0, pady=5)

        # Volume slider
        volume_frame = tk.Frame(root, bg="#222222")
        volume_frame.pack(pady=20)
        volume_label = tk.Label(volume_frame, text="Volume", bg="#222222", fg="#FFFFFF", font=("Arial", 12))
        volume_label.pack(side="left")
        self.volume_slider = tk.Scale(volume_frame, from_=0, to=1, orient="horizontal", resolution=0.01, command=self.change_volume, bg="#222222", fg="#FFFFFF", font=("Arial", 12), highlightbackground="#222222", highlightcolor="#FFFFFF", troughcolor="#444444", sliderrelief="raised")
        self.volume_slider.set(self.player.volume)
        self.volume_slider.pack(side="right")

        # Song name label
        self.song_name_label = tk.Label(root, text="", bg="#222222", fg="#FFFFFF", font=("Arial", 12))
        self.song_name_label.pack(pady=10)

        # Progress bar frame
        progress_frame = tk.Frame(root, bg="#222222")
        progress_frame.pack(pady=10)
        
        # Start time label
        self.start_time_label = tk.Label(progress_frame, text="00:00", bg="#222222", fg="#FFFFFF", font=("Arial", 10))
        self.start_time_label.pack(side="left")

        # Progress bar
        self.progress = Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(side="left", padx=10)

        # End time label
        self.end_time_label = tk.Label(progress_frame, text="00:00", bg="#222222", fg="#FFFFFF", font=("Arial", 10))
        self.end_time_label.pack(side="left")

        self.update_progress()

    def upload_song(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        if file_path:
            self.player.add_song(file_path)
            self.update_song_name()
            messagebox.showinfo("Success", "Song uploaded successfully!")

    def change_volume(self, volume):
        self.player.set_volume(float(volume))

    def play_song(self):
        self.player.play_song()
        self.update_song_name()
        self.update_end_time()

    def update_song_name(self):
        current_song = self.player.get_current_song()
        if current_song:
            song_name = current_song.split("/")[-1]
            self.song_name_label.config(text=song_name)
        else:
            self.song_name_label.config(text="")

    def update_end_time(self):
        song_length = self.player.get_song_duration()
        minutes = int(song_length // 60)
        seconds = int(song_length % 60)
        self.end_time_label.config(text=f"{minutes:02}:{seconds:02}")

    def update_progress(self):
        if pygame.mixer.music.get_busy():
            song_length = self.player.get_song_duration()
            current_pos = self.player.live_song_duration()
            self.progress['value'] = (current_pos / song_length) * 100
            
            current_minutes = int(current_pos // 60)
            current_seconds = int(current_pos % 60)
            self.start_time_label.config(text=f"{current_minutes:02}:{current_seconds:02}")
        else:
            self.progress['value'] = 0
            self.start_time_label.config(text="00:00")
        self.root.after(1000, self.update_progress)

if __name__ == "__main__":
    root = tk.Tk()
    player = MusicPlayer()
    gui = MusicPlayerGUI(root, player)
    root.mainloop()
