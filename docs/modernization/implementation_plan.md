# Implementation Plan - Yazi-style Panelled Textual TUI

This plan outlines the refactoring of **Discograph** into a high-fidelity, yazi-like three-column panelled TUI (Text User Interface) utilizing the **Textual** framework. It features keyboard-driven column navigation, instant metadata previewing, and asynchronous database updates.

---

## The Yazi Column Layout Architecture

The new terminal UI replicates the classic 3-column file-manager pane style:

```
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Left Column         ┃ Middle Column       ┃ Right Column                       ┃
┃ (Artists or Genres) ┃ (Albums list)       ┃ (Lyrics / Details Preview Panel)   ┃
┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ ❯ Artists           ┃ Album 1             ┃ Track: Song Title                  ┃
┃   Genres            ┃ Album 2             ┃ Length: 3:45                       ┃
┃   [Add Artist]      ┃ Album 3             ┃ Album: Album Name                  ┃
┃                     ┃                     ┃ Lyrics:                            ┃
┃                     ┃                     ┃ Line 1 of the song...              ┃
┃                     ┃                     ┃ Line 2 of the song...              ┃
┗━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

*   **Left Column:** Top-level navigation (Browse by Artists, Browse by Genres) and item lists (e.g. list of Artists or list of Genres).
*   **Middle Column:** Active context sub-items (Albums of the selected Artist, or Tracks of the selected Album).
*   **Right Column:** Rich preview card (Album release metadata, artist details, or full scrollable song lyrics).

---

## Modern Keyboard Navigation

Mimicking modern CLI tools (like `yazi` and `ranger`), users navigate using standard directional arrows or Vim keys:
*   `Up` / `Down` (or `k` / `j`): Scroll lists vertically within the active panel.
*   `Right` / `Enter` (or `l`): Expand selected item, slide focus to the next column.
*   `Left` (or `h`): Collapse back, sliding focus to the previous column.
*   `a`: Prompt to Add a New Artist.
*   `s`: Toggle a search field overlay.
*   `q`: Quit the application.

---

## Proposed Changes

### 1. Main TUI Entry Point

#### [MODIFY] [discograph.py](file:///home/udatta/github/discograph/src/discograph.py)
We will completely rewrite `src/discograph.py` as a subclass of `textual.app.App`. It will coordinate the custom layouts, query the SQLite database dynamically when focus shifts, and manage keys.

Key components of the app class:
- **`compose()`**: Lays out three vertical columns in a horizontal row (`Horizontal(LeftPane, MiddlePane, RightPane)`).
- **`on_mount()`**: Sets up connection with `test2.db` and loads the initial Left list.
- **`on_list_view_selected()` / `on_list_view_highlighted()`**: Automatically refreshes adjacent columns when selecting or highlighting items, enabling **instant previewing** as the user scrolls!
- **`run_worker()`**: Spawns database fetches (like adding a new artist via `addart.py`) in a background thread to prevent UI freezing, showing a beautiful loading modal spinner.

---

### 2. Add Artist Integration

#### [MODIFY] [addart.py](file:///home/udatta/github/discograph/src/utils/addart.py)
- Refactor network hooks in `addart.py` so they do not print directly to standard terminal outputs.
- Pass progress callback triggers back to the Textual interface so the main TUI app can update a progress loader widget.

---

### 3. Cleanup of Unused Utilities
Since the entire UI is now integrated into a unified three-column reactive app in `src/discograph.py`, we will keep the old modular CLI files as backups or remove them to maintain a clean project source tree.

---

## Verification Plan

### Automated Verification
- Verify syntactic compatibility by running Python compilation tests:
  ```bash
  .venv/bin/python3 -m py_compile src/discograph.py
  ```

### Manual TUI Walkthrough
1. **Interactive Column Sliding:** Verify arrow keys `Right` / `Left` shift focus cleanly between Column 1 (Artists), Column 2 (Albums), and Column 3 (Tracks/Lyrics).
2. **Scrolling Previews:** Scroll through tracks and verify lyrics instantly update in the Right Pane.
3. **Background Updates:** Press `a` key to open the "Add Artist" dialog, enter an artist, and ensure the loading indicator is displayed and the list updates dynamically without freezing.
