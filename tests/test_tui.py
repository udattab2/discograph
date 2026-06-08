import pytest
from tui.app import DiscographApp
from tui.widgets import ValueListItem
from textual.widgets import ListView, Input, Static

@pytest.mark.asyncio
async def test_tui_app_startup() -> None:
    app = DiscographApp()
    async with app.run_test() as pilot:
        # Verify basic attributes
        assert app.title == "DISCOGRAPH"
        assert app.left_mode == "artists"
        assert app.middle_view_mode == "albums"
        
        # Retrieve ListView widgets
        left_list = app.query_one("#left-list", ListView)
        middle_list = app.query_one("#middle-list", ListView)
        
        assert left_list is not None
        assert middle_list is not None
        
        # Set index explicitly to trigger highlight event
        left_list.index = 0
        # Let events settle so highlight triggers middle panel update
        await pilot.pause()
        
        # Our mock DB has 2 artists. Left pane should populate them.
        assert len(left_list.children) == 2
        
        first_item = left_list.children[0]
        assert isinstance(first_item, ValueListItem)
        # Coldplay should be the first due to alphabetical ordering
        assert "Coldplay" in str(first_item.children[0].render())
        
        # The middle list should also populate the albums for Coldplay (Parachutes)
        assert len(middle_list.children) == 1
        middle_item = middle_list.children[0]
        assert isinstance(middle_item, ValueListItem)
        assert "Parachutes" in str(middle_item.children[0].render())

@pytest.mark.asyncio
async def test_tui_search() -> None:
    app = DiscographApp()
    async with app.run_test() as pilot:
        # Toggle search input
        await pilot.press("f3")
        
        # Get search input widget
        search_input = app.query_one("#search-input", Input)
        assert search_input.display is True
        
        # Input search query
        search_input.value = "Yellow"
        # Submit the search
        await pilot.press("enter")
        
        # Let events settle
        await pilot.pause()
        
        # Assert left panel is now in search results mode
        assert app.left_mode == "search"
        
        left_list = app.query_one("#left-list", ListView)
        assert len(left_list.children) == 1
        
        # Explicitly select/highlight the search result
        left_list.index = 0
        await pilot.pause()
        
        # Assert middle pane contains metadata preview
        middle_list = app.query_one("#middle-list", ListView)
        assert len(middle_list.children) == 3
        
        # Check lyrics in the right pane
        right_content = app.query_one("#right-pane-content", Static)
        assert "Look at the stars" in str(right_content.render())

