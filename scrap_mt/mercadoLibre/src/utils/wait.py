from termcolor import colored
from halo import Halo
from time import sleep




Spinners = {
    "dots": {
        "interval": 80,
        "frames": [
            "⠋",
            "⠙",
            "⠹",
            "⠸",
            "⠼",
            "⠴",
            "⠦",
            "⠧",
            "⠇",
            "⠏"
        ]
    },
    "dots2": {
        "interval": 80,
        "frames": [
            "⣾",
            "⣽",
            "⣻",
            "⢿",
            "⡿",
            "⣟",
            "⣯",
            "⣷"
        ]
    },
    "dots3": {
        "interval": 80,
        "frames": [
            "⠋",
            "⠙",
            "⠚",
            "⠞",
            "⠖",
            "⠦",
            "⠴",
            "⠲",
            "⠳",
            "⠓"
        ]
    },
    "dots4": {
        "interval": 80,
        "frames": [
            "⠄",
            "⠆",
            "⠇",
            "⠋",
            "⠙",
            "⠸",
            "⠰",
            "⠠",
            "⠰",
            "⠸",
            "⠙",
            "⠋",
            "⠇",
            "⠆"
        ]
    },
    "dots5": {
        "interval": 80,
        "frames": [
            "⠋",
            "⠙",
            "⠚",
            "⠒",
            "⠂",
            "⠂",
            "⠒",
            "⠲",
            "⠴",
            "⠦",
            "⠖",
            "⠒",
            "⠐",
            "⠐",
            "⠒",
            "⠓",
            "⠋"
        ]
    },
    "dots6": {
        "interval": 80,
        "frames": [
            "⠁",
            "⠉",
            "⠙",
            "⠚",
            "⠒",
            "⠂",
            "⠂",
            "⠒",
            "⠲",
            "⠴",
            "⠤",
            "⠄",
            "⠄",
            "⠤",
            "⠴",
            "⠲",
            "⠒",
            "⠂",
            "⠂",
            "⠒",
            "⠚",
            "⠙",
            "⠉",
            "⠁"
        ]
    },
    "dots7": {
        "interval": 80,
        "frames": [
            "⠈",
            "⠉",
            "⠋",
            "⠓",
            "⠒",
            "⠐",
            "⠐",
            "⠒",
            "⠖",
            "⠦",
            "⠤",
            "⠠",
            "⠠",
            "⠤",
            "⠦",
            "⠖",
            "⠒",
            "⠐",
            "⠐",
            "⠒",
            "⠓",
            "⠋",
            "⠉",
            "⠈"
        ]
    },
    "dots8": {
        "interval": 80,
        "frames": [
            "⠁",
            "⠁",
            "⠉",
            "⠙",
            "⠚",
            "⠒",
            "⠂",
            "⠂",
            "⠒",
            "⠲",
            "⠴",
            "⠤",
            "⠄",
            "⠄",
            "⠤",
            "⠠",
            "⠠",
            "⠤",
            "⠦",
            "⠖",
            "⠒",
            "⠐",
            "⠐",
            "⠒",
            "⠓",
            "⠋",
            "⠉",
            "⠈",
            "⠈"
        ]
    },
    "dots9": {
        "interval": 80,
        "frames": [
            "⢹",
            "⢺",
            "⢼",
            "⣸",
            "⣇",
            "⡧",
            "⡗",
            "⡏"
        ]
    },
    "dots10": {
        "interval": 80,
        "frames": [
            "⢄",
            "⢂",
            "⢁",
            "⡁",
            "⡈",
            "⡐",
            "⡠"
        ]
    },
    "dots11": {
        "interval": 100,
        "frames": [
            "⠁",
            "⠂",
            "⠄",
            "⡀",
            "⢀",
            "⠠",
            "⠐",
            "⠈"
        ]
    },
    "dots12": {
        "interval": 80,
        "frames": [
            "⢀⠀",
            "⡀⠀",
            "⠄⠀",
            "⢂⠀",
            "⡂⠀",
            "⠅⠀",
            "⢃⠀",
            "⡃⠀",
            "⠍⠀",
            "⢋⠀",
            "⡋⠀",
            "⠍⠁",
            "⢋⠁",
            "⡋⠁",
            "⠍⠉",
            "⠋⠉",
            "⠋⠉",
            "⠉⠙",
            "⠉⠙",
            "⠉⠩",
            "⠈⢙",
            "⠈⡙",
            "⢈⠩",
            "⡀⢙",
            "⠄⡙",
            "⢂⠩",
            "⡂⢘",
            "⠅⡘",
            "⢃⠨",
            "⡃⢐",
            "⠍⡐",
            "⢋⠠",
            "⡋⢀",
            "⠍⡁",
            "⢋⠁",
            "⡋⠁",
            "⠍⠉",
            "⠋⠉",
            "⠋⠉",
            "⠉⠙",
            "⠉⠙",
            "⠉⠩",
            "⠈⢙",
            "⠈⡙",
            "⠈⠩",
            "⠀⢙",
            "⠀⡙",
            "⠀⠩",
            "⠀⢘",
            "⠀⡘",
            "⠀⠨",
            "⠀⢐",
            "⠀⡐",
            "⠀⠠",
            "⠀⢀",
            "⠀⡀"
        ]
    },
    "line": {
        "interval": 130,
        "frames": [
            "-",
            "\\",
            "|",
            "/"
        ]
    },
    "line2": {
        "interval": 100,
        "frames": [
            "⠂",
            "-",
            "–",
            "—",
            "–",
            "-"
        ]
    },
    "pipe": {
        "interval": 100,
        "frames": [
            "┤",
            "┘",
            "┴",
            "└",
            "├",
            "┌",
            "┬",
            "┐"
        ]
    },
    "simpleDots": {
        "interval": 400,
        "frames": [
            ".  ",
            ".. ",
            "...",
            "   "
        ]
    },
    "simpleDotsScrolling": {
        "interval": 200,
        "frames": [
            ".  ",
            ".. ",
            "...",
            " ..",
            "  .",
            "   "
        ]
    },
    "star": {
        "interval": 70,
        "frames": [
            "✶",
            "✸",
            "✹",
            "✺",
            "✹",
            "✷"
        ]
    },
    "star2": {
        "interval": 80,
        "frames": [
            "+",
            "x",
            "*"
        ]
    },
    "flip": {
        "interval": 70,
        "frames": [
            "_",
            "_",
            "_",
            "-",
            "`",
            "`",
            "'",
            "´",
            "-",
            "_",
            "_",
            "_"
        ]
    },
    "hamburger": {
        "interval": 100,
        "frames": [
            "☱",
            "☲",
            "☴"
        ]
    },
    "growVertical": {
        "interval": 120,
        "frames": [
            "▁",
            "▃",
            "▄",
            "▅",
            "▆",
            "▇",
            "▆",
            "▅",
            "▄",
            "▃"
        ]
    },
    "growHorizontal": {
        "interval": 120,
        "frames": [
            "▏",
            "▎",
            "▍",
            "▌",
            "▋",
            "▊",
            "▉",
            "▊",
            "▋",
            "▌",
            "▍",
            "▎"
        ]
    },
    "balloon": {
        "interval": 140,
        "frames": [
            " ",
            ".",
            "o",
            "O",
            "@",
            "*",
            " "
        ]
    },
    "balloon2": {
        "interval": 120,
        "frames": [
            ".",
            "o",
            "O",
            "°",
            "O",
            "o",
            "."
        ]
    },
    "noise": {
        "interval": 100,
        "frames": [
            "▓",
            "▒",
            "░"
        ]
    },
    "bounce": {
        "interval": 120,
        "frames": [
            "⠁",
            "⠂",
            "⠄",
            "⠂"
        ]
    },
    "boxBounce": {
        "interval": 120,
        "frames": [
            "▖",
            "▘",
            "▝",
            "▗"
        ]
    },
    "boxBounce2": {
        "interval": 100,
        "frames": [
            "▌",
            "▀",
            "▐",
            "▄"
        ]
    },
    "triangle": {
        "interval": 50,
        "frames": [
            "◢",
            "◣",
            "◤",
            "◥"
        ]
    },
    "arc": {
        "interval": 100,
        "frames": [
            "◜",
            "◠",
            "◝",
            "◞",
            "◡",
            "◟"
        ]
    },
    "circle": {
        "interval": 120,
        "frames": [
            "◡",
            "⊙",
            "◠"
        ]
    },
    "squareCorners": {
        "interval": 180,
        "frames": [
            "◰",
            "◳",
            "◲",
            "◱"
        ]
    },
    "circleQuarters": {
        "interval": 120,
        "frames": [
            "◴",
            "◷",
            "◶",
            "◵"
        ]
    },
    "circleHalves": {
        "interval": 50,
        "frames": [
            "◐",
            "◓",
            "◑",
            "◒"
        ]
    },
    "squish": {
        "interval": 100,
        "frames": [
            "╫",
            "╪"
        ]
    },
    "toggle": {
        "interval": 250,
        "frames": [
            "⊶",
            "⊷"
        ]
    },
    "toggle2": {
        "interval": 80,
        "frames": [
            "▫",
            "▪"
        ]
    },
    "toggle3": {
        "interval": 120,
        "frames": [
            "□",
            "■"
        ]
    },
    "toggle4": {
        "interval": 100,
        "frames": [
            "■",
            "□",
            "▪",
            "▫"
        ]
    },
    "toggle5": {
        "interval": 100,
        "frames": [
            "▮",
            "▯"
        ]
    },
    "toggle6": {
        "interval": 300,
        "frames": [
            "ဝ",
            "၀"
        ]
    },
    "toggle7": {
        "interval": 80,
        "frames": [
            "⦾",
            "⦿"
        ]
    },
    "toggle8": {
        "interval": 100,
        "frames": [
            "◍",
            "◌"
        ]
    },
    "toggle9": {
        "interval": 100,
        "frames": [
            "◉",
            "◎"
        ]
    },
    "toggle10": {
        "interval": 100,
        "frames": [
            "㊂",
            "㊀",
            "㊁"
        ]
    },
    "toggle11": {
        "interval": 50,
        "frames": [
            "⧇",
            "⧆"
        ]
    },
    "toggle12": {
        "interval": 120,
        "frames": [
            "☗",
            "☖"
        ]
    },
    "toggle13": {
        "interval": 80,
        "frames": [
            "=",
            "*",
            "-"
        ]
    },
    "arrow": {
        "interval": 100,
        "frames": [
            "←",
            "↖",
            "↑",
            "↗",
            "→",
            "↘",
            "↓",
            "↙"
        ]
    },
    "arrow2": {
        "interval": 80,
        "frames": [
            "⬆️ ",
            "↗️ ",
            "➡️ ",
            "↘️ ",
            "⬇️ ",
            "↙️ ",
            "⬅️ ",
            "↖️ "
        ]
    },
    "arrow3": {
        "interval": 120,
        "frames": [
            "▹▹▹▹▹",
            "▸▹▹▹▹",
            "▹▸▹▹▹",
            "▹▹▸▹▹",
            "▹▹▹▸▹",
            "▹▹▹▹▸"
        ]
    },
    "bouncingBar": {
        "interval": 80,
        "frames": [
            "[    ]",
            "[=   ]",
            "[==  ]",
            "[=== ]",
            "[ ===]",
            "[  ==]",
            "[   =]",
            "[    ]",
            "[   =]",
            "[  ==]",
            "[ ===]",
            "[====]",
            "[=== ]",
            "[==  ]",
            "[=   ]"
        ]
    },
    "bouncingBall": {
        "interval": 80,
        "frames": [
            "( ●    )",
            "(  ●   )",
            "(   ●  )",
            "(    ● )",
            "(     ●)",
            "(    ● )",
            "(   ●  )",
            "(  ●   )",
            "( ●    )",
            "(●     )"
        ]
    },
    "smiley": {
        "interval": 200,
        "frames": [
            "😄 ",
            "😝 "
        ]
    },
    "monkey": {
        "interval": 300,
        "frames": [
            "🙈 ",
            "🙈 ",
            "🙉 ",
            "🙊 "
        ]
    },
    "hearts": {
        "interval": 100,
        "frames": [
            "💛 ",
            "💙 ",
            "💜 ",
            "💚 ",
            "❤️ "
        ]
    },
    "clock": {
        "interval": 100,
        "frames": [
            "🕛 ",
            "🕐 ",
            "🕑 ",
            "🕒 ",
            "🕓 ",
            "🕔 ",
            "🕕 ",
            "🕖 ",
            "🕗 ",
            "🕘 ",
            "🕙 ",
            "🕚 "
        ]
    },
    "earth": {
        "interval": 180,
        "frames": [
            "🌍 ",
            "🌎 ",
            "🌏 "
        ]
    },
    "moon": {
        "interval": 80,
        "frames": [
            "🌑 ",
            "🌒 ",
            "🌓 ",
            "🌔 ",
            "🌕 ",
            "🌖 ",
            "🌗 ",
            "🌘 "
        ]
    },
    "runner": {
        "interval": 140,
        "frames": [
            "🚶 ",
            "🏃 "
        ]
    },
    "pong": {
        "interval": 80,
        "frames": [
            "▐⠂       ▌",
            "▐⠈       ▌",
            "▐ ⠂      ▌",
            "▐ ⠠      ▌",
            "▐  ⡀     ▌",
            "▐  ⠠     ▌",
            "▐   ⠂    ▌",
            "▐   ⠈    ▌",
            "▐    ⠂   ▌",
            "▐    ⠠   ▌",
            "▐     ⡀  ▌",
            "▐     ⠠  ▌",
            "▐      ⠂ ▌",
            "▐      ⠈ ▌",
            "▐       ⠂▌",
            "▐       ⠠▌",
            "▐       ⡀▌",
            "▐      ⠠ ▌",
            "▐      ⠂ ▌",
            "▐     ⠈  ▌",
            "▐     ⠂  ▌",
            "▐    ⠠   ▌",
            "▐    ⡀   ▌",
            "▐   ⠠    ▌",
            "▐   ⠂    ▌",
            "▐  ⠈     ▌",
            "▐  ⠂     ▌",
            "▐ ⠠      ▌",
            "▐ ⡀      ▌",
            "▐⠠       ▌"
        ]
    },
    "shark": {
        "interval": 120,
        "frames": [
            "▐|\\____________▌",
            "▐_|\\___________▌",
            "▐__|\\__________▌",
            "▐___|\\_________▌",
            "▐____|\\________▌",
            "▐_____|\\_______▌",
            "▐______|\\______▌",
            "▐_______|\\_____▌",
            "▐________|\\____▌",
            "▐_________|\\___▌",
            "▐__________|\\__▌",
            "▐___________|\\_▌",
            "▐____________|\\▌",
            "▐____________/|▌",
            "▐___________/|_▌",
            "▐__________/|__▌",
            "▐_________/|___▌",
            "▐________/|____▌",
            "▐_______/|_____▌",
            "▐______/|______▌",
            "▐_____/|_______▌",
            "▐____/|________▌",
            "▐___/|_________▌",
            "▐__/|__________▌",
            "▐_/|___________▌",
            "▐/|____________▌"
        ]
    },
    "dqpb": {
        "interval": 100,
        "frames": [
            "d",
            "q",
            "p",
            "b"
        ]
    },
    "weather": {
        "interval": 100,
        "frames": [
            "☀️ ",
            "☀️ ",
            "☀️ ",
            "🌤 ",
            "⛅️ ",
            "🌥 ",
            "☁️ ",
            "🌧 ",
            "🌨 ",
            "🌧 ",
            "🌨 ",
            "🌧 ",
            "🌨 ",
            "⛈ ",
            "🌨 ",
            "🌧 ",
            "🌨 ",
            "☁️ ",
            "🌥 ",
            "⛅️ ",
            "🌤 ",
            "☀️ ",
            "☀️ "
        ]
    },
    "christmas": {
        "interval": 400,
        "frames": [
            "🌲",
            "🎄"
        ]
    },
    "grenade": {
        "interval": 80,
        "frames": [
            "،   ",
            "′   ",
            " ´ ",
            " ‾ ",
            "  ⸌",
            "  ⸊",
            "  |",
            "  ⁎",
            "  ⁕",
            " ෴ ",
            "  ⁓",
            "   ",
            "   ",
            "   "
        ]
    },
    "point": {
        "interval": 125,
        "frames": [
            "∙∙∙",
            "●∙∙",
            "∙●∙",
            "∙∙●",
            "∙∙∙"
        ]
    },
    "layer": {
        "interval": 150,
        "frames": [
            "-",
            "=",
            "≡"
        ]
    }
}

def wait(n, spinner_name='dots', mensaje_espera="", bar=True, percentage=True, seconds=True, clear=False):
    """
        Muestra un spinner con barra de progreso, porcentaje y tiempo restante durante una espera.

        Parámetros:
        n (int): Número de segundos a esperar.
        spinner_name (str): Nombre del spinner a utilizar.
        mensaje_espera (str): Mensaje que se mostrará durante la espera.
        bar (bool): Si True, muestra una barra de progreso.
        percentage (bool): Si True, muestra el porcentaje completado.
        seconds (bool): Si True, muestra el tiempo restante.
        clear_on_finish (bool): Si True, borra la pantalla al finalizar la espera.
    """
    if spinner_name not in Spinners:
        raise ValueError(f"Spinner '{spinner_name}' no está definido.")
    
    spinner_info = Spinners[spinner_name]
    halo_spinner = Halo(text=f'\n{mensaje_espera}', spinner=spinner_info, color='cyan')
    barra_ancho = 50
    
    halo_spinner.start()
    try:
        for i in range(n):
            porcentaje = (i / n if n != 0 else 0) * 100
            num_barras = int(barra_ancho * (i / n)) if bar else 0
            barra = '[' + '█' * num_barras + '-' * (barra_ancho - num_barras) + ']' if bar else ''
            tiempo_texto = f"{i}/{n}" if seconds else ''
            porcentaje_texto = f"{porcentaje:.2f}%" if percentage else ''
            elementos = ['[<-'+mensaje_espera+'->]', tiempo_texto, barra, porcentaje_texto]
            texto = colored(' '.join([el for el in elementos if el]), 'magenta')
            halo_spinner.text = colored(f"{texto}", 'cyan')
            sleep(4)
    finally:
        if clear:
            halo_spinner.stop()
        else:   
            barra = '[██████████████████████████████████████████████████]' if bar else ''
            porcentaje = '100.00%' if percentage else ''
            seconds = f'{n}/{n}' if seconds else ''
            final_text = colored(f"{'[<-'+mensaje_espera+'->]'} {seconds} {barra} {porcentaje}", 'green')
            halo_spinner.stop_and_persist(symbol='🚀', text=final_text)
            


def build_progress_bar_string(mensaje: str, current: int, total: int, width: int = 50,
                               show_percentage: bool = True, show_count: bool = True) -> str:
    """
    Construye una cadena con una barra de progreso, porcentaje y contador opcionales.

    Args:
        mensaje (str): Mensaje personalizado.
        current (int): Progreso actual.
        total (int): Progreso total.
        width (int): Ancho de la barra de progreso (en caracteres).
        show_percentage (bool): Mostrar porcentaje.
        show_count (bool): Mostrar contador (current/total).

    Returns:
        str: Cadena con barra de progreso formateada.
    """
    porcentaje = current / total if total != 0 else 0
    num_barras = int(width * porcentaje)

    barra = '[' + '█' * num_barras + '-' * (width - num_barras) + ']'
    porcentaje_texto = f"{porcentaje * 100:6.2f}%" if show_percentage else ""
    contador_texto = f"{current}/{total}" if show_count else ""

    elementos = [
        f"[<–{mensaje}–>]",
        contador_texto,
        barra,
        porcentaje_texto
    ]
    
    return colored(' '.join([e for e in elementos if e]), 'magenta')



def wait_scrap(n,message):
    wait(n, 'dots', message, bar=False, percentage=False, seconds=True, clear=True)
