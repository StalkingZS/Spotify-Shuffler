import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import List
import time
import sys
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

class SpotifyPlaylistShuffler:
    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize the Spotify playlist shuffler.
        
        Args:
            client_id (str): Spotify app Client ID
            client_secret (str): Spotify app Client Secret
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.sp = self._authenticate_spotify()
        self.retry_delay = 5  # seconds between retries
        self.max_retries = 3  # maximum retry attempts

    def _authenticate_spotify(self) -> spotipy.Spotify:
        """Authenticate with Spotify API."""
        scope = "playlist-read-private playlist-modify-private playlist-modify-public"
        
        auth_manager = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri="http://127.0.0.1:8080",
            scope=scope
        )
        
        return spotipy.Spotify(auth_manager=auth_manager)

    def _extract_playlist_id(self, playlist_uri: str) -> str:
        """Extract playlist ID from URI or URL."""
        if "spotify:playlist:" in playlist_uri:
            return playlist_uri.split(":")[2]
        elif "open.spotify.com/playlist/" in playlist_uri:
            return playlist_uri.split("/")[-1].split("?")[0]
        return playlist_uri

    def _batch_processor(self, items: List, batch_size: int = 100) -> List[List]:
        """Split a list into smaller batches."""
        return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]

    def get_playlist_tracks(self, playlist_uri: str) -> List[str]:
        """
        Get all track URIs from a playlist with error handling.
        
        Args:
            playlist_uri (str): Playlist URI, URL or ID
            
        Returns:
            List[str]: List of track URIs
        """
        playlist_id = self._extract_playlist_id(playlist_uri)
        tracks = []
        offset = 0
        batch_size = 100  # API maximum
        
        while True:
            for attempt in range(self.max_retries):
                try:
                    results = self.sp.playlist_items(
                        playlist_id,
                        limit=batch_size,
                        offset=offset,
                        additional_types=('track',)
                    )
                    
                    if not results['items']:
                        return tracks
                        
                    tracks.extend([
                        item['track']['uri'] 
                        for item in results['items'] 
                        if item['track']
                    ])
                    
                    offset += batch_size
                    if len(results['items']) < batch_size:
                        return tracks
                    
                    break  # exit retry loop if successful
                    
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise
                    print(f"{Fore.YELLOW}Error getting tracks (attempt {attempt + 1}): {e}")
                    time.sleep(self.retry_delay)

    def shuffle_playlist(self, playlist_uri: str) -> None:
        """
        Shuffle an existing playlist directly on Spotify.
        
        Args:
            playlist_uri (str): Playlist URI, URL or ID
        """
        playlist_id = self._extract_playlist_id(playlist_uri)
        
        try:
            # 1. Get playlist info
            playlist = self.sp.playlist(playlist_id)
            os.system('cls' if os.name == 'nt' else 'clear')
            self._print_header()
            print(f"\n{Fore.CYAN}🎵 Playlist: {Fore.GREEN}{playlist['name']}")
            print(f"{Fore.CYAN}🔗 URL: {Fore.BLUE}{playlist['external_urls']['spotify']}")
            print(f"{Fore.CYAN}📊 Total tracks: {Fore.GREEN}{playlist['tracks']['total']}")
            time.sleep(3)
            
            # 2. Get all track URIs
            os.system('cls' if os.name == 'nt' else 'clear')
            self._print_header()
            print(f"\n{Fore.YELLOW}🔄 Retrieving playlist tracks...")
            track_uris = self.get_playlist_tracks(playlist_uri)
            
            if not track_uris:
                print(f"{Fore.RED}Empty playlist - nothing to shuffle.")
                return
                
            print(f"{Fore.GREEN}✅ Successfully retrieved {len(track_uris)} tracks!")
            
            # 3. Shuffle the tracks
            os.system('cls' if os.name == 'nt' else 'clear')
            self._print_header()
            print(f"\n{Fore.MAGENTA}🎲 Shuffling track order...")
            random.shuffle(track_uris)
            
            # 4. Process update in batches
            os.system('cls' if os.name == 'nt' else 'clear')
            self._print_header()
            print(f"\n{Fore.YELLOW}🔄 Updating playlist on Spotify...")
            
            # Split into batches of 100 tracks (API limit)
            batches = self._batch_processor(track_uris)
            
            # 4.1 Remove all current tracks (in batches)
            os.system('cls' if os.name == 'nt' else 'clear')
            self._print_header()
            print(f"\n{Fore.RED}🧹 Removing current tracks...")
            for i, batch in enumerate(batches, 1):
                for attempt in range(self.max_retries):
                    try:
                        self.sp.playlist_remove_all_occurrences_of_items(playlist_id, batch)
                        print(f"{Fore.GREEN}✅ Batch {i}/{len(batches)} removed")
                        break
                    except Exception as e:
                        if attempt == self.max_retries - 1:
                            raise
                        print(f"{Fore.YELLOW}Error removing batch {i} (attempt {attempt + 1}): {e}")
                        time.sleep(self.retry_delay)
            
            # 4.2 Add tracks in new order (in batches)
            os.system('cls' if os.name == 'nt' else 'clear')
            self._print_header()
            print(f"\n{Fore.GREEN}✨ Adding tracks in new order...")
            for i, batch in enumerate(batches, 1):
                for attempt in range(self.max_retries):
                    try:
                        self.sp.playlist_add_items(playlist_id, batch)
                        print(f"{Fore.GREEN}✅ Batch {i}/{len(batches)} added")
                        break
                    except Exception as e:
                        if attempt == self.max_retries - 1:
                            raise
                        print(f"{Fore.YELLOW}Error adding batch {i} (attempt {attempt + 1}): {e}")
                        time.sleep(self.retry_delay)
            
            # 5. Final result
            os.system('cls' if os.name == 'nt' else 'clear')
            self._print_header()
            print(f"\n{Fore.GREEN}🎉 Playlist '{playlist['name']}' successfully shuffled!")
            print(f"{Fore.CYAN}🔗 Access it at: {Fore.BLUE}{playlist['external_urls']['spotify']}")
            
        except Exception as e:
            print(f"\n{Fore.RED}⛔ Critical error: {e}")
            sys.exit(1)

    def _print_header(self):
        """Print the colorful header."""
        print(f"{Fore.BLUE}{Style.BRIGHT}=============================== {Fore.MAGENTA}Spotify Shuffler {Fore.BLUE}===============================")
        print(f"{Fore.CYAN}Format and shuffle your playlist, leave your songs in a completely random order!\n")


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    shuffler = None
    
    try:
        # Print header
        print(f"{Fore.BLUE}{Style.BRIGHT}=============================== {Fore.MAGENTA}Spotify Shuffler {Fore.BLUE}===============================")
        print(f"{Fore.CYAN}Format and shuffle your playlist, leave your songs in a completely random order!\n")
        
        # 1. Get credentials
        client_id = input(f"{Fore.YELLOW}Enter your Spotify App Client ID: {Style.RESET_ALL}").strip()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.BLUE}{Style.BRIGHT}=============================== {Fore.MAGENTA}Spotify Shuffler {Fore.BLUE}===============================")
        print(f"{Fore.CYAN}Format and shuffle your playlist, leave your songs in a completely random order!\n")
        client_secret = input(f"{Fore.YELLOW}Enter your Spotify App Client Secret: {Style.RESET_ALL}").strip()
        
        if not client_id or not client_secret:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Fore.BLUE}{Style.BRIGHT}=============================== {Fore.MAGENTA}Spotify Shuffler {Fore.BLUE}===============================")
            print(f"{Fore.CYAN}Format and shuffle your playlist, leave your songs in a completely random order!\n")
            raise ValueError(f"{Fore.RED}Client ID and Client Secret are required")
        
        # 2. Initialize shuffler
        shuffler = SpotifyPlaylistShuffler(client_id, client_secret)
        
        # 3. Get playlist to shuffle
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.BLUE}{Style.BRIGHT}=============================== {Fore.MAGENTA}Spotify Shuffler {Fore.BLUE}===============================")
        print(f"{Fore.CYAN}Format and shuffle your playlist, leave your songs in a completely random order!\n")
        playlist_uri = input(f"{Fore.YELLOW}Enter playlist URL or ID: {Style.RESET_ALL}").strip()
        if not playlist_uri:
            raise ValueError(f"{Fore.RED}Playlist URI is required")
        
        # 4. Confirm action
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.BLUE}{Style.BRIGHT}=============================== {Fore.MAGENTA}Spotify Shuffler {Fore.BLUE}===============================")
        print(f"{Fore.CYAN}Format and shuffle your playlist, leave your songs in a completely random order!\n")
        confirm = input(f"{Fore.RED}⚠️ WARNING: This will modify the playlist directly. Continue? (y/n): {Style.RESET_ALL}").strip().lower()
        if confirm != 'y':
            print(f"{Fore.YELLOW}Operation cancelled by user.")
            return
        
        # 5. Shuffle playlist
        shuffler.shuffle_playlist(playlist_uri)
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user.")
    except Exception as e:
        print(f"\n{Fore.RED}⛔ Error: {e}")        

if __name__ == "__main__":
    main()
