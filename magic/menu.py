from magic.config import BL, LB
from magic.console_utils import console

options = [
    {
        'num': 1,
        'text': 'Index Images',
        'func': 'index'
    },
    {
        'num': 2,
        'text': 'Find Images',
        'func': 'search'
    },
    {
        'num': 3,
        'text': 'Smart Search (Coming Soon)',
        'func': 'search'
    },
]

def call_option(opt, options=options):
    if not is_in_options(opt):
        console.print(f"\n[ [{BL}]! [/]] [{LB}]Option not found")
        return
    for option in options:
        if option['num'] == opt:
            if 'func' in option:
                if option['func'] == 'index':
                    from magic.index import index
                    index()
                elif option['func'] == 'search':
                    from magic.search.search import search
                    search()
            else:
                console.print('\n[/][ {BL}! [/]] {LB}No function detected')

def execute_option(opt, options=options):
    from revelio import main 
    try:
        call_option(opt, options=options)
        # console.input(f"\n[{BL}][ + ] [{LB}]Press enter to continue: [/]")
        main(False)
    except ValueError as e:
        print(e)
        execute_option(opt, options=options)
    except KeyboardInterrupt:
        console.print(f"\n[{BL}][ ! ] [{LB}]Mischief Managed! 🪄")
        exit()

def option_text(options=options):
    text = '\n'
    for opt in options:
        text += f'[ {opt["num"]} ] {opt["text"]}\n'
    return text

def is_in_options(num, options=options):
    for opt in options:
        if opt['num'] == num:
            return True
    return False