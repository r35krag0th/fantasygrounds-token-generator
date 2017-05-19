from fantasygrounds_tokens.token import Token
import click

@click.command()
@click.option('--directory', default='./', help='Where to output the files?')
def handle(directory):
    # (self, letter_prefix, max_tokens, color):
    tokens = [
        Token('A', 9, (241, 63, 63)).circular(),
        Token('B', 9, (26, 129, 255)).circular(),
        Token('C', 9, (184, 0, 138)).circular(),
        Token('D', 9, (0, 111, 61)).circular(),
        Token('E', 9, (41, 26, 255)).circular(),
        Token('F', 9, (255, 42, 27)).circular(),

        Token('T', 3, (72, 61, 139)).square(),
        Token('U', 2, (153, 50, 204)).square(),
        Token('V', 2, (127, 255, 212)).square(),
        Token('W', 2, (173, 216, 230)).square(),
        Token('X', 2, (169, 169, 169)).square(),
        Token('Y', 2, (186, 85, 211)).square(),
        Token('Z', 2, (0, 206, 209)).square(),
    ]

    for token in tokens:
        token.render(output_dir=directory)

if __name__ == '__main__':
    handle()
