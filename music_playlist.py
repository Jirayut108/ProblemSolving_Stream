import streamlit as st
import os

# --- Song Class ---
class Song:
    def __init__(self, title, artist, audio_data=None):
        self.title = title
        self.artist = artist
        self.audio_data = audio_data # Store actual audio data (bytes)
        self.next_song = None

    def __str__(self):
        return f"{self.title} by {self.artist}"

# --- MusicPlaylist Class ---
class MusicPlaylist:
    def __init__(self):
        self.head = None
        self.current_song = None
        self.length = 0

    def add_song(self, title, artist, audio_file=None):
        audio_data = None
        if audio_file:
            audio_data = audio_file.read()

        new_song = Song(title, artist, audio_data)
        if self.head is None:
            self.head = new_song
            self.current_song = new_song
        else:
            current = self.head
            while current.next_song:
                current = current.next_song
            current.next_song = new_song
        self.length += 1
        st.success(f"Added: {new_song}")
        return True # Indicate successful addition

    def display_playlist(self):
        if self.head is None:
            return []

        playlist_songs = []
        current = self.head
        count = 1
        while current:
            playlist_songs.append(f"{count}. {current.title} by {current.artist}")
            current = current.next_song
            count += 1
        return playlist_songs

    def play_current_song(self):
        if self.current_song:
            st.info(f"Now playing: {self.current_song}")
            if self.current_song.audio_data:
                # Streamlit's st.audio handles playing from bytes
                st.audio(self.current_song.audio_data, format='audio/mp3', start_time=0)
            else:
                st.warning("No audio data available for this song.")
        else:
            st.warning("Playlist is empty or no song is selected to play.")

    def next_song(self):
        if self.current_song and self.current_song.next_song:
            self.current_song = self.current_song.next_song
            st.session_state.play_after_navigation = True # Flag to play after navigation
            return True # Indicate successful navigation
        elif self.current_song and not self.current_song.next_song:
            st.warning("End of playlist. No next song.")
            return False
        else:
            st.warning("Playlist is empty.")
            return False

    def prev_song(self):
        if self.head is None or self.current_song is None:
            st.warning("Playlist is empty or no song is selected.")
            return False
        if self.current_song == self.head:
            st.warning("Already at the beginning of the playlist.")
            return False

        current = self.head
        while current.next_song != self.current_song:
            current = current.next_song
        self.current_song = current
        st.session_state.play_after_navigation = True # Flag to play after navigation
        return True # Indicate successful navigation

    def get_length(self):
        return self.length

    def delete_song(self, title):
        if self.head is None:
            st.error(f"Cannot delete '{title}'. Playlist is empty.")
            return False

        # If the song to be deleted is the head
        if self.head.title == title:
            if self.current_song == self.head:
                self.current_song = self.head.next_song # Move current_song if deleted
            self.head = self.head.next_song
            self.length -= 1
            st.success(f"Deleted: {title}")
            if self.length == 0:
                self.current_song = None
            return True

        current = self.head
        prev = None
        while current and current.title != title:
            prev = current
            current = current.next_song

        if current: # Song found
            if self.current_song == current: # If the deleted song was the current one
                if current.next_song:
                    self.current_song = current.next_song
                elif prev:
                    self.current_song = prev
                else: # Only one song, and it's deleted
                    self.current_song = None

            if prev:
                prev.next_song = current.next_song
            self.length -= 1
            st.success(f"Deleted: {title}")
            return True
        else:
            st.error(f"Song '{title}' not found in the playlist.")
            return False
# ฟังก์ชันสำหรับจัดการการเพิ่มเพลง
def handle_add_song():
    title = st.session_state.add_title
    artist = st.session_state.add_artist
    file = st.session_state.add_file

    if title and artist and file:
        if st.session_state.playlist.add_song(title, artist, file):
            st.session_state.add_title = ""
            st.session_state.add_artist = ""
# ฟังก์ชันสำหรับจัดการการลบเพลง
def handle_delete_song():
    title = st.session_state.delete_title
    if title:
        if st.session_state.playlist.delete_song(title):
            st.session_state.delete_title = ""
# --- Streamlit App Layout ---
st.set_page_config(layout="wide") # Use wide layout for better UI

st.title("🎶 Music Playlist App")
st.markdown("Upload your favorite songs and manage your playlist!")

# Initialize playlist in session state
if 'playlist' not in st.session_state:
    st.session_state.playlist = MusicPlaylist()
    st.session_state.play_after_navigation = False # Flag to control auto-play after next/prev

# Layout with columns for better organization
col_add, col_delete = st.columns(2)

with col_add:
    st.header("Add New Song")
    st.text_input("Title", key="add_title")
    st.text_input("Artist", key="add_artist")
    st.file_uploader("Upload Song (MP3/WAV)", type=["mp3", "wav"], key="add_file")
    st.button("Add Song to Playlist", on_click=handle_add_song)

with col_delete:
    st.header("Delete Song")
    st.text_input("Song Title to Delete", key="delete_title")
    st.button("Delete Song", on_click=handle_delete_song)

st.markdown("---")
st.header("Your Current Playlist")
playlist_content = st.session_state.playlist.display_playlist()
if playlist_content:
    for song_str in playlist_content:
        st.write(song_str)
else:
    st.info("Playlist is empty. Add some songs from the 'Add New Song' section!")

st.markdown("---")
st.header("Playback Controls")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⏪ Previous Song"):
        st.session_state.playlist.prev_song()
        st.session_state.play_after_navigation = True # Set flag to play after navigation
        st.rerun()

with col2:
    if st.button("▶️ Play Current Song"):
        st.session_state.playlist.play_current_song()

with col3:
    if st.button("⏩ Next Song"):
        st.session_state.playlist.next_song()
        st.session_state.play_after_navigation = True # Set flag to play after navigation
        st.rerun()

st.markdown("---")
st.write(f"Total songs in playlist: {st.session_state.playlist.get_length()} song(s)")

# Display current playing song info and audio player below controls
st.markdown("### Currently Playing")
if st.session_state.playlist.current_song:
    st.write(f"**Title:** {st.session_state.playlist.current_song.title}")
    st.write(f"**Artist:** {st.session_state.playlist.current_song.artist}")
    # Auto-play after next/prev or if it's the very first song added
    if st.session_state.play_after_navigation and st.session_state.playlist.current_song.audio_data:
        st.audio(st.session_state.playlist.current_song.audio_data, format='audio/mp3', start_time=0, autoplay=True)
        st.session_state.play_after_navigation = False # Reset flag
    elif st.session_state.playlist.current_song.audio_data:
        # If not auto-playing, still show the player for manual control
        st.audio(st.session_state.playlist.current_song.audio_data, format='audio/mp3', start_time=0)
    else:
        st.warning("No audio data available for this song.")
else:
    st.write("No song selected.")
