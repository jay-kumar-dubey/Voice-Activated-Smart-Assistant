import pytest
from unittest.mock import patch, MagicMock

# Import the functions from your module
from main import (
    processCommand,
    play_on_youtube,
    play_on_spotify,
    choose_music_service,
    newsapikey,
)


# Test the processCommand function
@pytest.mark.parametrize("input_command, expected_domain", [
    ("open google", "google.com"),
    ("open youtube", "youtube.com"),
])
@patch('webbrowser.open')
def test_processCommand_open(mock_web_open, input_command, expected_domain):
    processCommand(input_command)
    mock_web_open.assert_called_once_with(f"https://{expected_domain}")


# Test play_on_youtube function
"""This test require the require the involvement of temp.mp3 file , but it is being removed in main programm to avoid complication."""
# @patch('webbrowser.open')
# def test_play_on_youtube(mock_web_open):
#     song_name = "test song"
#     play_on_youtube(song_name)
#     mock_web_open.assert_called_once_with("https://www.youtube.com/results?search_query=test+song")


# Test play_on_spotify function
@patch('webbrowser.open')
def test_play_on_spotify(mock_web_open):
    song_name = "test song"
    play_on_spotify(song_name)
    mock_web_open.assert_called_once_with("https://open.spotify.com/search/test+song")


# Test choose_music_service function
@patch('main.play_on_youtube')
@patch('main.play_on_spotify')
@patch('speech_recognition.Recognizer.listen')
@patch('speech_recognition.Recognizer.recognize_google', return_value="youtube")
@patch('main.speak')
def test_choose_music_service(mock_speak, mock_recognize_google, mock_listen, mock_play_on_spotify, mock_play_on_youtube):
    song_name = "test song"
    choose_music_service(song_name)
    mock_play_on_youtube.assert_called_once_with(song_name)
    mock_play_on_spotify.assert_not_called()


# Test newsapikey function (success case)
@patch('requests.get')
def test_newsapikey_success(mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_requests_get.return_value = mock_response

    response = newsapikey()
    assert response.status_code == 200


# Test newsapikey function (error case)
@patch('requests.get', side_effect=Exception('API Error'))
def test_newsapikey_error(mock_requests_get):
    response = newsapikey()
    assert "Error" in response
    assert "API Error" in response


# Test the speak function by mocking the gTTS, pygame, and os.remove
@patch('pygame.mixer.music.load')
@patch('pygame.mixer.music.play')
@patch('pygame.mixer.music.get_busy', side_effect=[True, False])
@patch('pygame.mixer.init')
@patch('os.remove')
@patch('gtts.gTTS.save')
def test_speak(mock_gtts_save, mock_os_remove, mock_pygame_init, mock_get_busy, mock_pygame_play, mock_pygame_load):
    from main import speak
    speak("Testing speech output")

    mock_gtts_save.assert_called_once_with('temp.mp3')
    mock_pygame_load.assert_called_once_with('temp.mp3')
    mock_pygame_play.assert_called_once()
    mock_os_remove.assert_called_once_with("temp.mp3")

