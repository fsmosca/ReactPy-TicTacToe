"""A Tic-Tac-Toe Web Application

Uses bootstrap 5 to style the elements.

requirements:
    reactpy
"""


from reactpy import component, html, hooks
from reactpy.backend.fastapi import configure
from fastapi import FastAPI


BOOTSTRAP_CSS = html.link(
    {
        'rel': 'stylesheet',
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/'
                'dist/css/bootstrap.min.css',
        'integrity': 'sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Y'
                     'z1ztcQTwFspd3yD65VohhpuuCOmLASjC',
        'crossorigin': 'anonymous',
    }
)

SQ_SIZE = '60px'
PC_CHAR = {'p1': 'W', 'p2': 'B'}

WIN_RESULT_PATTERN = [
    [0, 1, 2],  # hor
    [3, 4, 5],  # hor
    [6, 7, 8],  # hor
    [0, 4, 8],  # diag
    [2, 4, 6],  # anti-diag
    [0, 3, 6],  # ver
    [1, 4, 7],  # ver
    [2, 5, 8],  # ver
]


@component
def Tictactoe():
    stm, set_stm = hooks.use_state(True)  # side to move

    board_status = [None] * 9  # a list from 9 squares
    set_board_status = [None] * 9  # an array of 9 functions
    for i in range(len(board_status)):
        board_status[i], set_board_status[i] = hooks.use_state('')

    def make_move(event):
        btn_value = event['currentTarget']['value']
        set_board_status[int(btn_value)](
            PC_CHAR['p1'] if stm else PC_CHAR['p2']
        )
        set_stm(not stm)

    def disable_buttons():
        """Disables button if game is over.

        We call this function once we know that a game is over.
        Board square button is disabled if its value is not an empty char.
        The initial value of a square is '' and we just replace it with ' '
        to disable the button.
        """
        for i, v in enumerate(board_status):
            if v == '':
                set_board_status[i](' ')

    @component
    def CreateSquare(index):
        """Creates a button to represent a square."""
        return html.button(
            {
                'style': {'width': SQ_SIZE, 'height': SQ_SIZE},
                'class': 'btn shadow-none rounded-1 btn-warning \
                          border-secondary m-0 fw-bold fs-3 \
                          align-items-center justify-content-center',
                'value': index,
                'on_click': make_move,
                'disabled': board_status[index],
            },
            board_status[index]
        )

    @component
    def MakeBoardSquares(values: list):
        """Creates a row of board squares as buttons."""
        return html.div(
            {'class': 'd-flex flex-row'},
            [CreateSquare(i) for i in values]
        )

    @component
    def determine_winner():
        result = None
        for res in WIN_RESULT_PATTERN:
            if all([board_status[v] == PC_CHAR['p1'] for v in res]):
                result = PC_CHAR['p1']
                break
            if all([board_status[v] == PC_CHAR['p2'] for v in res]):
                result = PC_CHAR['p2']
                break
        if result is not None:
            disable_buttons()
            return html.h5({'class': 'text-success'}, f'The winner is {result}.')
        done = all([bs == PC_CHAR['p2'] or bs == PC_CHAR['p1']
                    for bs in board_status])
        if done:
            disable_buttons()
            return html.h5({'class': 'text-secondary'}, 'The result is a draw.')
        return html.h5({'class': 'text-muted'}, 'No winner yet.')

    return html.div(
        BOOTSTRAP_CSS,
        html.div(
            html.div({'class': 'container justify-content-center mt-3 text-center'},
                html.div(
                    html.h1({'class': 'text-dark'}, 'TicTacToe'),
                    html.h6({'class': 'text-primary'}, 'Built by ReactPy'),
                    html.p(),

                    html.div(
                        {'class': 'container d-flex justify-content-center'},
                        html.div(
                            {'class': 'd-flex flex-column justify-content-center'},
                            html.div(MakeBoardSquares([0, 1, 2])),
                            html.div(MakeBoardSquares([3, 4, 5])),
                            html.div(MakeBoardSquares([6, 7, 8])),
                        ),
                    ),
                    html.br(),
                    html.div({'class': 'container d-flex justify-content-center'},
                        determine_winner(),
                    ),
                ),
            ),
        ),
    )


app = FastAPI()
configure(app, Tictactoe)
