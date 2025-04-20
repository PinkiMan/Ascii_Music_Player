from pynput import keyboard

def on_press(key):
    if key == keyboard.Key.media_play_pause or key == keyboard.Key.space:
        print('pause/play')
    elif key == keyboard.Key.media_next:
        print('skip')
    elif key == keyboard.Key.media_previous:
        print('previous')
    else:
        if hasattr(key, 'char'):
            if key.char == 'p' or key.char == 'k':
                print('pause/play')
            elif key.char == 'l':
                print('skip')
            elif key.char == 'j':
                print('previous')
            elif key.char == '+':
                print('volume +')
            elif key.char == '-':
                print('volume -')


    """try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))"""

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()