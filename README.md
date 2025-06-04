# Discograph

**Created by:**  
Udatta Bhattacharya (udattab2@gmail.com)

---

This software/tool provides an interface to the user for browsing through different audio artists and discovering their work. Hence the name: **Disco-Graph**.

> While a graphical user interface is not included in this version, the application offers a straightforward and user-friendly experience.

---

## Introduction

A discography tool allows users to browse and explore details of recorded audio media, but it does not function as a media player. It displays information about specific recordings or tracks, including the album they belong to, the artist who composed and recorded them, and their genre. Users can navigate through artists, genres, albums, and songs using a choice-based interface.

Users can choose to browse by artist or genre, after which the tool presents relevant catalogues of information. The tool also provides details about artists, such as the number of albums they have composed, album names, and album contents. For example, if a user remembers an artist but not a song name, they can search for the artist and browse their works.

Additional information is provided for albums and tracks. For albums, the tool displays the year of release and track count. For individual tracks, it shows the length or duration.

## Package Documentation

 [Go to Discograph Package Documentation](/docs/build/html/index.html)

## Concept

Discography is the study and cataloging of published sound recordings, often by specific artists or within particular musical genres. The exact information included varies depending on the type and scope of the discography, but a typical entry will often list details such as the names of the artists involved, the time and place of the recording, the title of the piece performed, and release dates. Using this tool, users can extract such information, which is stored in the database as various relations containing artists, genres, albums, and tracks.

## Implementation and Schema

The discography tool uses a structured database to store data, implemented with a DBMS. SQL is used for querying, and the user interface is command-based, developed in Python.

Key entities are stored in separate tables and linked via entity relationships:

- **Artist**: Stores artist information, including name and a unique ID.
- **Genre**: Stores genre information, including name and a unique ID.
- **Album**: Stores albums with details such as name, unique ID, artist ID, year of release, track count, and album sequence number.
- **Track**: Stores tracks with details such as name, unique ID, album ID, genre ID, length, and track sequence number.

## How To Use

- To run the application, open `discograph.exe`.
- A console window opens up displaying a few options.
- The first display console (**DISCOGRAPH**) prompts you to select the browsing mode/basis.
- To select an option on the screen, simply type in the character/number associated with the option and hit **RETURN**.
- On each console display, a similar methodology is used for browsing purposes.
- However, the searching is **case sensitive**, so make sure to maintain proper case as you enter your search query.

Enjoy using the application.

