"""Gera themes/dark-modern-soft.json.

Interface: Calmppuccin Frappé com os cinzas azulados neutralizados e escurecidos,
para ficar perto do #222222 do Slack Dark Mode.
Sintaxe: as regras do Slack Dark Mode (Dark+) tal como são, só com cada cor
puxada BLEND (50%) em direção à cor equivalente do Frappé. Assim os papéis, o contraste
entre eles e o que fica sem cor continuam iguais ao Slack.
"""
import colorsys
import json
from pathlib import Path

ROOT = Path(__file__).parent

# Quanto cada cor do Slack é puxada em direção ao Frappé (0 = Slack puro, 1 = Frappé puro)
BLEND = 0.5

# Cor do Slack (Dark+) -> cor equivalente do Frappé
SLACK_TO_FRAPPE = {
    "#d4d4d4": "#d5d9e6",  # texto
    "#6a9955": "#838ba7",  # comentário
    "#569cd6": "#8caaee",  # keyword, storage, null/true/false
    "#c586c0": "#ca9ee6",  # controle de fluxo, import/export
    "#dcdcaa": "#e5c890",  # funções
    "#4ec9b0": "#81c8be",  # tipos e classes
    "#9cdcfe": "#99d1db",  # variáveis e propriedades
    "#ce9178": "#e2a47d",  # strings
    "#b5cea8": "#a6d189",  # números
    "#d7ba7d": "#e5c890",  # escapes, seletores CSS
    "#d16969": "#e78284",  # regex
    "#646695": "#babbf1",  # constante de regex
    "#808080": "#838ba7",  # < > das tags
    "#6796e6": "#8caaee",  # lista markdown, log info
    "#f44747": "#e78284",  # inválido, log error
    "#cd9731": "#e5c890",  # log warn
    "#b267e6": "#ca9ee6",  # log debug
    "#000080": "#8caaee",  # header
}

# Cores de terminal (ANSI) do esquema "Slack Dark Mode" do Windows Terminal -> Frappé.
# Vão para o terminal do VS Code e para o Windows Terminal (extras/).
TERMINAL_ANSI = {
    "black": ("#3a3d41", "#51576d"),
    "red": ("#d16969", "#e78284"),
    "green": ("#6a9955", "#a6d189"),
    "yellow": ("#d7ba7d", "#e5c890"),
    "blue": ("#569cd6", "#8caaee"),
    "purple": ("#b267e6", "#ca9ee6"),
    "cyan": ("#4ec9b0", "#81c8be"),
    "white": ("#d4d4d4", "#b5bfe2"),
    "brightBlack": ("#7a7a7a", "#838ba7"),
    "brightRed": ("#f44747", "#e78284"),
    "brightGreen": ("#b5cea8", "#a6d189"),
    "brightYellow": ("#dcdcaa", "#e5c890"),
    "brightBlue": ("#9cdcfe", "#99d1db"),
    "brightPurple": ("#c586c0", "#f4b8e4"),
    "brightCyan": ("#7fe0cc", "#81c8be"),
    "brightWhite": ("#e6e6e6", "#c6d0f5"),
}

# Cores de marca do Slack usadas no prompt do zsh e no mod Clean View -> Frappé
ACCENTS = {
    "teal": ("#1d978d", "#81c8be"),
    "blue": ("#0077b5", "#8caaee"),
    "link": ("#1d9bd1", "#85c1dc"),
    "cyan": ("#36c5f0", "#99d1db"),
    "yellow": ("#ecb22e", "#e5c890"),
    "green": ("#2eb67d", "#a6d189"),
    "red": ("#e01e5a", "#e78284"),
    "subtext": ("#ababab", "#a5adce"),
    "overlay": ("#7a7a7a", "#838ba7"),
    "surface": ("#404040", "#51576d"),
}

# Textos destacados da interface (arquivo selecionado, aba ativa, item de menu...):
# o azul do Frappé misturado meio a meio com o texto, para chamar menos atenção
HIGHLIGHT_KEYS = [
    "list.activeSelectionForeground", "list.inactiveSelectionForeground", "list.hoverForeground",
    "list.highlightForeground", "tab.activeForeground", "tab.hoverForeground", "menu.selectionForeground",
    "breadcrumb.focusForeground", "breadcrumb.activeSelectionForeground", "sideBarTitle.foreground",
    "commandCenter.activeForeground", "pickerGroup.foreground", "settings.settingsHeaderHoverForeground",
    "statusBarItem.hoverForeground", "editorSuggestWidget.highlightForeground",
    "editorHoverWidget.highlightForeground", "editorLineNumber.activeForeground",
]
HIGHLIGHT_SOFTEN = 0.5

# Cores padrão do VS Code para pares de chaves (o Slack não define) -> Frappé
BRACKETS = {"#ffd700": "#e5c890", "#da70d6": "#ca9ee6", "#179fff": "#8caaee"}


def blend(slack, frappe, amount=BLEND):
    a = [int(slack[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(frappe[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * amount):02x}" for x, y in zip(a, b))


TEXT = blend("#d4d4d4", SLACK_TO_FRAPPE["#d4d4d4"])


def neutralize(value):
    """Tira o azul dos cinzas do Frappé e escurece os fundos."""
    hexpart, alpha = value[1:7], value[7:]
    if len(hexpart) < 6:
        return value
    r, g, b = (int(hexpart[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    is_grey = 205 <= h * 360 <= 255 and (s < 0.5 or hexpart.lower() == "c6d0f5")
    if not is_grey:
        return value
    s *= 0.35
    if l < 0.45:
        l *= 0.75 + max(0.0, l - 0.3) / 0.15 * 0.25
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#" + "".join(f"{round(c * 255):02x}" for c in (r, g, b)) + alpha


def remap_tokens(token_colors):
    out = []
    for token in token_colors:
        settings = dict(token["settings"])
        if "foreground" in settings:
            color = settings["foreground"].lower()
            settings["foreground"] = blend(color, SLACK_TO_FRAPPE[color])
        out.append({**token, "settings": settings})
    return out


def terminal_palette(colors):
    ansi = {name: neutralize(blend(slack, frappe)) for name, (slack, frappe) in TERMINAL_ANSI.items()}
    selection = colors["editor.selectionBackground"]
    return {
        "background": colors["editor.background"],
        "foreground": TEXT,
        "cursorColor": colors["editorCursor.foreground"],
        "selectionBackground": blend(colors["editor.background"], selection[:7], int(selection[7:9], 16) / 255),
        **ansi,
    }


def accent_palette(colors):
    accents = {name: neutralize(blend(slack, frappe)) for name, (slack, frappe) in ACCENTS.items()}
    return {
        **accents,
        "text": TEXT,
        "track": blend(colors["editor.background"], accents["surface"], 0.3),
        "background": colors["editor.background"],
        "crust": colors["activityBar.background"],
    }


def write_json(path, data):
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"ok: {path}")


def main():
    base = json.loads((ROOT / "base-calmppuccin-frappe.json").read_text(encoding="utf-8"))
    slack = json.loads((ROOT / "base-slack-dark-mode.json").read_text(encoding="utf-8"))
    colors = {k: neutralize(v) for k, v in base["colors"].items()}
    colors["editor.foreground"] = TEXT
    # Painel inteiro (cabeçalho, terminal, lista de terminais) na cor do editor
    colors["panel.background"] = colors["editor.background"]
    for key in HIGHLIGHT_KEYS:
        colors[key] = blend(colors[key][:7], TEXT, HIGHLIGHT_SOFTEN)
    brackets = [blend(slack_color, frappe_color) for slack_color, frappe_color in BRACKETS.items()]
    for i in range(6):
        colors[f"editorBracketHighlight.foreground{i + 1}"] = brackets[i % 3]
    terminal = terminal_palette(colors)
    vscode_ansi = {"purple": "Magenta", "brightPurple": "BrightMagenta"}
    for name, value in terminal.items():
        if name in TERMINAL_ANSI:
            key = vscode_ansi.get(name, name[0].upper() + name[1:])
            colors[f"terminal.ansi{key}"] = value
    colors["terminal.foreground"] = TEXT
    theme = {
        "name": "Dark Modern Soft",
        "type": "dark",
        "colors": colors,
        "tokenColors": remap_tokens(slack["tokenColors"]),
    }
    write_json(ROOT / "themes" / "dark-modern-soft.json", theme)
    write_json(ROOT / "extras" / "windows-terminal.json", {
        "schemes": [{"name": "Dark Modern Soft", **terminal}],
        "themes": [{
            "name": "Dark Modern Soft",
            "tab": {"background": colors["editor.background"] + "FF", "iconStyle": "default",
                    "showCloseButton": "always", "unfocusedBackground": None},
            "tabRow": {"background": colors["activityBar.background"] + "FF",
                       "unfocusedBackground": colors["activityBar.background"] + "FF"},
            "window": {"applicationTheme": "dark", "experimental.rainbowFrame": False,
                       "frame": None, "unfocusedFrame": None, "useMica": False},
        }],
    })
    write_json(ROOT / "extras" / "palette.json", accent_palette(colors))


if __name__ == "__main__":
    main()
