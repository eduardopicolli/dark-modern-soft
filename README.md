# Dark Modern Soft

Tema escuro para o VS Code: o Dark+ de sempre, só que mais suave.

- **Sintaxe:** as mesmas regras do Dark+ (via [Slack Theme Dark Mode](https://marketplace.visualstudio.com/items?itemName=felipe-mendes.slack-theme)). O que tem cor, o que fica branco e o contraste entre os papéis não mudam. Cada cor é puxada 50% em direção à equivalente da paleta [Catppuccin Frappé](https://github.com/catppuccin/catppuccin).
- **Interface:** baseada no [Calmppuccin Frappé](https://marketplace.visualstudio.com/items?itemName=kenan-salar.calmppuccin-vscode), com os cinzas azulados neutralizados e escurecidos, o painel inteiro na cor do editor e destaques azuis mais discretos.

| Papel | Dark+ | Dark Modern Soft |
|---|---|---|
| Palavras-chave, `null`, `false` | `#569cd6` | `#71a3e2` |
| `return`, `try`, `import` | `#c586c0` | `#c892d3` |
| Funções | `#dcdcaa` | `#e0d29d` |
| Tipos e classes | `#4ec9b0` | `#68c8b7` |
| Variáveis | `#9cdcfe` | `#9ad6ec` |
| Strings | `#ce9178` | `#d89a7a` |
| Comentários | `#6a9955` | `#76927e` |

## Instalação

Baixe o `.vsix` da [última release](https://github.com/eduardopicolli/dark-modern-soft/releases/latest) e rode:

```sh
code --install-extension dark-modern-soft.vsix
```

Depois escolha **Dark Modern Soft** em `Ctrl+K Ctrl+T`.

## Terminais

Os arquivos em `extras/` usam as mesmas cores do tema:

- `extras/windows-terminal.json`: esquema de cores e tema da janela do Windows Terminal. Copie os itens de `schemes` e `themes` para o `settings.json` do Windows Terminal e escolha **Dark Modern Soft**.
- `extras/zsh/dark-modern-soft-powerline.zsh-theme`: prompt Powerline para Oh My Zsh (precisa de uma Nerd Font). Copie para `~/.oh-my-zsh/custom/themes/` e use `ZSH_THEME="dark-modern-soft-powerline"`.
- `extras/palette.json`: cores de destaque, para usar em outras ferramentas.

O terminal integrado do VS Code já vem com as mesmas cores ANSI do esquema do Windows Terminal.

## Ajustes e build

O tema é gerado por script, a partir dos dois temas de origem em `base-*.json`. Os ajustes ficam no topo do `build.py`:

- `BLEND`: quanto cada cor do Dark+ vai em direção ao Frappé (0 = Dark+ puro, 1 = Frappé puro).
- `SLACK_TO_FRAPPE`: qual cor do Frappé corresponde a cada cor do Dark+.
- `HIGHLIGHT_SOFTEN`: quanto o azul dos destaques da interface se mistura ao texto.

```sh
python3 build.py   # gera themes/dark-modern-soft.json e extras/*.json
python3 pack.py    # gera dark-modern-soft.vsix
```

## Créditos

- [Calmppuccin](https://github.com/KenanSalar/calmppuccin-vscode), de KenanSalar (MIT)
- [Slack Theme](https://github.com/felipemendes/slack-theme), de Felipe Mendes (MIT)
- [Catppuccin](https://github.com/catppuccin/catppuccin) (MIT)
