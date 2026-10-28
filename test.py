
import curses
import requests

URL = "http://127.0.0.1:5000"

KEY_MAP = {
    curses.KEY_UP: "up",
    curses.KEY_DOWN: "down",
    curses.KEY_LEFT: "left",
    curses.KEY_RIGHT: "right",
    ord(" "): "select",
}


def main(stdscr):
    stdscr.keypad(True)
    stdscr.addstr("Keyboard remote active\n")
    stdscr.addstr("Arrows = navigate | Space = select\n")
    stdscr.addstr("Esc = exit\n")
    stdscr.refresh()

    while True:
        key = stdscr.getch()

        if key == 27:
            break

        input_value = KEY_MAP.get(key)
        if input_value is None:
            continue

        try:
            response = requests.post(
                URL,
                json={"input": input_value},
                timeout=2,
            )
            message = f"Sent {input_value}: HTTP {response.status_code}"
        except requests.RequestException as e:
            message = f"Request failed: {e}"

        stdscr.move(4, 0)
        stdscr.clrtoeol()
        stdscr.addstr(message[:curses.COLS - 1])
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
