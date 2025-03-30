# 🎵 Spotify Playlist Shuffler 🔀

A Python tool that truly randomizes your Spotify playlists by removing and re-adding all tracks in a random order. Unlike Spotify's built-in shuffle which uses algorithms that may repeat songs, this provides a completely fresh order every time.

## 📚 Libraries Used

This project utilizes the following Python libraries:

1. spotipy (v2.23.0+)
   - Official Spotify API wrapper for Python
   - Handles all Spotify API communications
   - Manages OAuth2 authentication
   - Provides playlist modification capabilities

2. colorama (v0.4.6+)
   - Cross-platform colored terminal text
   - Enables the visually appealing console interface
   - Works on Windows, macOS, and Linux

3. random (Python built-in)
   - Provides cryptographically secure randomization
   - Used for the core shuffling algorithm

4. os (Python built-in)
   - Handles system operations
   - Manages screen clearing functionality

5. sys (Python built-in)
   - Provides system-specific functionality
   - Used for proper error handling

6. time (Python built-in)
   - Manages delays between operations
   - Provides retry timing mechanism

## 🌟 Features

- ✅ True random shuffling - Not just Spotify's algorithm
- 🔐 Secure authentication - Uses Spotify's official API
- 🚀 Handles large playlists - Processes in batches of 100 tracks
- ♻️ Retry mechanism - Automatically retries failed operations
- 🎨 Beautiful console interface - Colorful output with emojis
- ⏳ Progress tracking - See each step as it happens

## 📋 Prerequisites

Before you begin, ensure you have:

1. Python 3.8 or higher installed
2. A Spotify Premium account (required for API access)
3. A Spotify Developer account (free)

## 🛠️ Setup

### 1. Install Dependencies

pip install spotipy colorama

### 2. Create a Spotify Developer Application

1. Go to the Spotify Developer Dashboard (https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Click "Create an App"
4. Fill in:
   - App Name: Playlist Shuffler (or any name you prefer)
   - Description: Tool for truly randomizing playlists
   - Redirect URI: http://127.0.0.1:8080
5. Click "Save"

### 3. Get Your Credentials

After creating the app:
1. Note your Client ID (visible on the app page)
2. Click "Show Client Secret" to reveal your Client Secret
3. Keep these credentials secure - they're like passwords!

## 🚀 Usage

Run the script:

python spotify_shuffler.py

You'll be prompted to:
1. Enter your Client ID
2. Enter your Client Secret
3. Enter the playlist URL or ID you want to shuffle
4. Confirm the operation

### Finding Playlist URLs

To shuffle a playlist, you can use either:
- The playlist URL (from the "Share" menu in Spotify)
- The playlist ID (the last part of the URL)

Example:
https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
                          ↑ This is the ID: 37i9dQZF1DXcBWIGoYBM5M

## 🔧 How It Works

1. Authentication: Uses OAuth2 to securely connect to your Spotify account
2. Track Retrieval: Fetches all tracks from your playlist
3. Shuffling: Randomizes the track order using Python's secure randomizer
4. Playlist Update:
   - Removes all tracks (in batches of 100)
   - Adds them back in the new random order (in batches of 100)
5. Completion: Provides a link to your newly shuffled playlist

## ⚠️ Important Notes

- This modifies your playlist directly - use with caution!
- For large playlists (500+ songs), the process may take a few minutes
- Always back up important playlists before shuffling
- Requires Spotify Premium for API access

## 🤔 FAQ

Q: Why doesn't Spotify's shuffle work properly?
A: Spotify uses "smart" shuffle algorithms that consider your listening history, which can lead to repeated patterns.

Q: Is this against Spotify's Terms of Service?
A: No, this uses Spotify's official API within normal usage limits.

Q: Can I shuffle collaborative playlists?
A: Yes, if you have edit permissions for the playlist.

Q: What if I get an authentication error?
A: Double-check your Client ID and Secret, and ensure your Redirect URI is set to http://127.0.0.1:8080.

## 🙏 Credits

Special thanks to:

1. kxllswxtchXD (https://github.com/kxllswxtchXD)
   - For initial project inspiration and concept
   - Valuable contributions to the shuffling algorithm

2. DeepSeek | 深度求索 (https://www.deepseek.com/)
   - AI assistance in code optimization
   - Documentation and README improvements

3. Spotipy (https://github.com/plamere/spotipy)
   - Python library for Spotify Web API

4. Colorama (https://github.com/tartley/colorama)
   - Cross-platform colored terminal text

5. Spotify Developer Team
   - For maintaining the excellent Spotify Web API
   - Their comprehensive API documentation

6. Python Software Foundation
   - For creating such a versatile programming language
   - Maintaining the core libraries we depend on

## 📜 License

MIT License - Free for personal and commercial use

💡 Tip: For best results, shuffle your playlists occasionally to rediscover forgotten gems in your music collection!
