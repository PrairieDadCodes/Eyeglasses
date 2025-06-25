import enum
import pathlib

from construct import *

from format_utils import CheckedFlag, Unused, CheckedEnum, CheckedFlagsEnum

TGM4Header = Struct(
    "signature" / Const(b"TGRP"),
    "version" / Int32ul,
    Unused(8)
)

GameMode = CheckedEnum(Enum(
    Int32ul,
    Normal=0,
    Marathon=0,
    Master=1,
    Konoha=3,
    Shiranui=4,
    Asuka=5,
    Versus=6
))


class InputEnum(enum.IntFlag):
    HardDrop = 1 << 0
    SoftDrop = 1 << 1
    MoveRight = 1 << 2
    MoveLeft = 1 << 3
    LeftRot1 = 1 << 4
    RightRot1 = 1 << 5
    Hold = 1 << 6
    Extra = 1 << 7
    LeftRot2 = 1 << 8
    RightRot2 = 1 << 9
    Backstep = 1 << 10
    UNUSED_11 = 1 << 11
    UNUSED_12 = 1 << 12
    UNUSED_13 = 1 << 13
    UNUSED_14 = 1 << 14
    UNUSED_15 = 1 << 15


InputFlags = CheckedFlagsEnum(FlagsEnum(Int16ul, InputEnum))


class ResultsEnum(enum.IntFlag):
    UNUSED_0 = 1 << 0
    UNUSED_1 = 1 << 1
    UNUSED_2 = 1 << 2
    UNUSED_3 = 1 << 3
    UNUSED_4 = 1 << 4
    UNUSED_5 = 1 << 5
    UNUSED_6 = 1 << 6
    UNUSED_7 = 1 << 7
    UNUSED_8 = 1 << 8
    UNUSED_9 = 1 << 9
    UNUSED_10 = 1 << 10
    UNUSED_11 = 1 << 11
    UNUSED_12 = 1 << 12
    UNUSED_13 = 1 << 13
    UNUSED_14 = 1 << 14
    UNUSED_15 = 1 << 15
    UNUSED_16 = 1 << 16
    UNUSED_17 = 1 << 17
    UNUSED_18 = 1 << 18
    UNUSED_19 = 1 << 19
    UNUSED_20 = 1 << 20
    UNUSED_21 = 1 << 21
    UNUSED_22 = 1 << 22
    UNUSED_23 = 1 << 23
    UNUSED_24 = 1 << 24
    UNUSED_25 = 1 << 25
    UNUSED_26 = 1 << 26
    UNUSED_27 = 1 << 27
    UNUSED_28 = 1 << 28
    UNUSED_29 = 1 << 29
    UNUSED_30 = 1 << 30
    UNUSED_31 = 1 << 31


ResultsFlags = CheckedFlagsEnum(FlagsEnum(Int32ul, ResultsEnum))

PlayerInputs = Struct(
    "num_frames" / Int32sl,
    "seed" / Int32ul,
    "inputs" / InputFlags[this.num_frames]
)

VersusInputs = Struct(
    "player1_inputs" / PlayerInputs,
    "player2_inputs" / PlayerInputs,
)

Data = Struct(
    "steam_id" / Int64ul,
    "timestamp" / Bytes(8),
    "replay_metadata" / Bytes(1),
    Unused(3),
    # Mode settings
    "game_mode" / GameMode,
    "player1_tgm_controls" / CheckedFlag,
    Unused(3),
    "player2_tgm_controls" / CheckedFlag,
    Unused(3),
    "modifiers" / Bytes(2),
    Unused(2),
    "last_round_seed" / Int32ul,

    # Results
    "playtime_frames" / Int32sl,
    "level" / Int32sl,
    "score" / Int32sl,
    "bravo_count" / Int32sl,
    "shiranui_tier" / Int32sl,
    "shiranui_points" / Int32sl,
    "UNKNOWN_results_flags" / ResultsFlags,
    "Skin" / Int32sl,  # 0-39 valid
    Unused(8),
    "UNKNOWN_set_in_shiranui" / Bytes(1),
    Unused(11),

    # Game settings
    "number_of_next_previews" / Int32sl,  # "0-6 valid"
    "hold_enabled" / CheckedFlag,
    Unused(3),
    "ghost_enabled" / CheckedFlag,
    Unused(3),
    "konoha_all_clear_assist" / CheckedFlag,
    Unused(3),
    "show_tetromino_directional_guide" / CheckedFlag,
    Unused(3),
    "background_animation" / CheckedFlag,
    Unused(3),
    "diagonal_upperward_input" / CheckedFlag,
    Unused(3),
    "diagonal_downward_input" / CheckedFlag,
    Unused(3),
    Unused(116),

    # Replay data
    "inputs" / Switch(
        lambda ctx: ctx.game_mode == "Versus" or ctx.game_mode == "Shiranui",
        {
            False: PlayerInputs,
            True: VersusInputs
        }
    ),
    Terminated
)

GameSettings = Pass
Inputs = Pass

"""
Version 0x107 replay
"""
ReplayVer107 = Struct(
    "header" / TGM4Header,
    "data" / Data,
)

"""
Loader for any version TGM4 replay
"""
Replay = Switch(
    lambda ctx: ctx.header.version,
    {
        0x00000107: ReplayVer107
    },
    Pass
)


def load_replay(path: pathlib.Path) -> Replay:
    with open(path, 'rb') as f:
        contents = f.read()

    header = TGM4Header.parse(contents)
    return Replay.parse(contents, header=header)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python format_reply.py replay_file")
        sys.exit(1)

    file_path = pathlib.Path(sys.argv[1])
    if not file_path.is_file():
        print(f"Error: {file_path} is not a file")
        sys.exit(1)

    print(load_replay(file_path))
