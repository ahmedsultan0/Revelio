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

def call_option(opt):
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
                    from magic.search import search
                    search()
            else:
                console.print('\n[/][ {BL}! [/]] {LB}No function detected')

def execute_option(opt):
    from revilio import main 
    try:
        call_option(opt)
        console.input(f"\n[{BL}][ + ] [{LB}]Press enter to continue: [/]")
        main()
    except ValueError as e:
        print(e)
        execute_option(opt)
    except KeyboardInterrupt:
        console.print(f'\n[/][ {BL}! [/]] {LB}Exit')
        exit()

def option_text():
    text = ''
    for opt in options:
        text += f'[ {opt["num"]} ] {opt["text"]}\n'
    return text

def is_in_options(num):
    for opt in options:
        if opt['num'] == num:
            return True
    return False