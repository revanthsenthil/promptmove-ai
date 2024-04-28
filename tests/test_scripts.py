from src.functions import perform_action_on_object, run_script
import os
import shutil

os.chdir("src")

def test_perform_action_on_object():
    """Test the perform_action_on_object function"""
    assert perform_action_on_object("walk", "door") == '{"action": "walk", "object": "door", "status": "success"}'
    assert perform_action_on_object("grab", "bananas") == '{"action": "grab", "object": "bananas", "status": "success"}'

    assert perform_action_on_object("open", "nothing") == '{"action": "open", "object": "nothing", "status": "failed to find nothing"}'
    assert perform_action_on_object("find", "window") == '{"action": "find", "object": "window", "status": "failed to find window"}'

    assert perform_action_on_object("jump", "kitchentable") == '{"action": "jump", "object": "kitchentable", "status": "failed to perform jump on kitchentable"}'
    assert perform_action_on_object("sprint", "coffeepot") == '{"action": "sprint", "object": "coffeepot", "status": "failed to perform sprint on coffeepot"}'

def test_run_script_success():
    """Test the run_script function"""
    acts = ['walk', 'grab']
    objs = ['door', 'bananas']

    if os.path.isfile("logs/log.txt"):
        os.remove("logs/log.txt")

    run_script("2021-07-01_12-00-00", frame_rate=10, image_width=320, image_height=240, actions=acts, objects=objs, no_graphics=True)

    assert os.path.isfile("logs/log.txt")
    assert os.path.isdir("Output/2021-07-01_12-00-00")
    assert os.path.isfile("video_output/2021-07-01_12-00-00/video_normal.mp4")
    with open("logs/log.txt") as f:
        lines = f.readlines()
        assert len(lines) == 7
        assert lines[0].endswith("] Running run_script(['walk', 'grab'], ['door', 'bananas'])\n")
        assert lines[1].endswith("] Connected to Unity\n")
        assert lines[2].endswith("] Creating the scene\n")
        assert 'Initial character position:' in lines[3]
        assert lines[4].endswith("] script: ['<char1> [sit] <sofa> (27)', '<char0> [walk] <door> (130)', '<char0> [grab] <bananas> (203)']\n")
        assert 'Final Character position:' in lines[5]
        assert lines[6].endswith("] {\"success_actions\": [\"walk\", \"grab\"], \"success_objects\": [\"door\", \"bananas\"], \"failed_actions\": [], \"failed_objects\": []}\n")

    os.remove("logs/log.txt")
    shutil.rmtree("video_output/2021-07-01_12-00-00/")
    shutil.rmtree("Output/2021-07-01_12-00-00/")

def test_run_script_failure():
    """Test the run_script function"""
    acts = ['walk', 'walk']
    objs = ['ball', 'door']
    
    if os.path.isfile("logs/log.txt"):
        os.remove("logs/log.txt")

    run_script("2021-07-01_12-00-01", frame_rate=10, image_width=320, image_height=240, actions=acts, objects=objs, no_graphics=True)

    assert os.path.isfile("logs/log.txt")
    assert os.path.isdir("Output/2021-07-01_12-00-01")
    assert os.path.isfile("video_output/2021-07-01_12-00-01/video_normal.mp4")

    with open("logs/log.txt") as f:
        lines = f.readlines()
        assert len(lines) == 8
        assert lines[0].endswith("] Running run_script(['walk', 'walk'], ['ball', 'door'])\n"), print('1')
        assert lines[1].endswith("] Connected to Unity\n"), print('2')
        assert lines[2].endswith("] Expanding the scene\n"), print('3')
        assert 'Initial character position:' in lines[3], print('4')
        assert lines[4].endswith("] Object ball not found in the environment\n"), print('5')
        assert lines[5].endswith("] script: ['<char1> [sit] <sofa> (27)', '<char0> [walk] <door> (130)']\n"), print('6')
        assert 'Final Character position:' in lines[6], print('7')
        assert lines[7].endswith("] {\"success_actions\": [\"walk\"], \"success_objects\": [\"door\"], \"failed_actions\": [], \"failed_objects\": [\"ball\"]}\n"), print('8')

    os.remove("logs/log.txt")
    shutil.rmtree("video_output/2021-07-01_12-00-01/")
    shutil.rmtree("Output/2021-07-01_12-00-01/")