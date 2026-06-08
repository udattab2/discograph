# Discograph

**Created by:**  
Udatta Bhattacharya (udattab2@gmail.com)

---

This software/tool provides an interface to the user for browsing through different audio artists and discovering their work. Hence the name: **Disco-Graph**.

> The application now runs as a modern Textual TUI with a three-column layout, live album/track previews, keyboard-driven navigation, and background artist import support.

---

## Introduction

A discography tool allows users to browse and explore details of recorded audio media, but it does not function as a media player. The current interface is a three-panel terminal experience that shows artists or genres on the left, albums or tracks in the middle, and rich metadata or lyrics on the right.

Users can switch between artist and genre browsing with hotkeys, search for tracks on the fly, and open an add-artist dialog to import new catalog data without freezing the interface. As selections change, the adjacent panes update instantly to show album lists, track details, and lyrics.

Additional information is provided for albums and tracks. For albums, the tool displays the year of release and track count. For individual tracks, it shows the length or duration, and the preview pane can reveal lyrics when available.

## Package Documentation

[Go to Discograph Package Documentation](/docs/html/index.html)

## Concept

Discography is the study and cataloging of published sound recordings, often by specific artists or within particular musical genres. The exact information included varies depending on the type and scope of the discography, but a typical entry will often list details such as the names of the artists involved, the time and place of the recording, the title of the piece performed, and release dates. Using this tool, users can extract such information, which is stored in the database as various relations containing artists, genres, albums, and tracks.

## Implementation and Schema

The discography tool uses a structured SQLite database to store catalog information. SQL is used for querying, and the user interface is now a keyboard-driven Textual TUI developed in Python.

Key entities are stored in separate tables and linked via entity relationships:

- **Artist**: Stores artist information, including name and a unique ID.
- **Genre**: Stores genre information, including name and a unique ID.
- **Album**: Stores albums with details such as name, unique ID, artist ID, year of release, track count, and album sequence number.
- **Track**: Stores tracks with details such as name, unique ID, album ID, genre ID, length, and track sequence number.

## How To Use

1. Start the application from the project root:
   ```bash
   python src/discograph.py
   ```
2. Use the three-panel TUI to browse your discography:
   - Left panel: artists, genres, or search results
   - Middle panel: albums or tracks for the current selection
   - Right panel: metadata, track lists, and lyrics preview
3. Keyboard controls:
   - `F1`: switch to artist browsing
   - `F2`: switch to genre browsing
   - `F3`: open the inline search box for track names
   - `F4`: open the Add Artist dialog to import new artists
   - `↑ / ↓` or `j / k`: move through lists
   - `→ / Enter` or `l`: move into the next panel / expand an album
   - `← / Backspace` or `h`: move back / collapse back to albums
   - `q`: quit the application
4. Search is now partial and keyboard-friendly, and the preview pane updates live as you move through the lists.

Enjoy exploring your discography in the new terminal interface.

