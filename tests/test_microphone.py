
from unittest.mock import MagicMock, patch
from src.audio.MicrophoneStream import MicrophoneStream

def test_MicrophoneStream_context_manager():
    with patch('pyaudio.PyAudio') as mock_pyaudio:
        mock_audio_interface = MagicMock()
        mock_audio_stream = MagicMock()
        mock_pyaudio.return_value = mock_audio_interface
        mock_audio_interface.open.return_value = mock_audio_stream

        stream = MicrophoneStream()
        with stream:
            mock_audio_interface.open.assert_called_once()
            assert stream.closed == False

        mock_audio_stream.stop_stream.assert_called_once()
        mock_audio_stream.close.assert_called_once()
        assert stream.closed == True
