#pragma description TGM4 file
#pragma magic [54 47 52 50] @ 0x00

import type.time;
import type.magic;
import std.mem;
import std.string;
import type.byte;


bitfield Modifiers
{
    bool TwentyG: 1;
    bool Big: 1;
    Unknown1: 1 [[color("FFFFFF"), comment("Unknown")]];
    Unknown2: 1 [[color("FFFFFF"), comment("Unknown")]];
    bool Easy: 1;
    bool Hard: 1;
    bool Daily: 1;
    Unknown3: 1 [[color("FFFFFF"), comment("Unknown")]];
    
    bool Vanish: 1;
    bool Vanish_1: 1;
    bool Vanish_2: 1;
    bool Vanish_3: 1;
    Unknown: 4 [[color("FFFFFF"), comment("Unknown")]];
 
} [[single_color]];

enum GameMode : u32
{
    Marathon,
    Master,
    Normal,
    Konoha,
    Shiranui,
    Asuka,
    Versus
};

bitfield Input {
    bool HardDrop: 1;
    bool SoftDrop: 1;
    bool MoveRight: 1;
    bool MoveLeft: 1;
    bool LeftRot1: 1;
    bool RightRot1: 1;
    bool Hold: 1;
    bool Extra: 1;
    bool LeftRot2: 1;
    bool RightRot2: 1;
    bool Backstep: 1;
    Unused: 5 [[color("FFFFFF"), comment("Unused")]];
} [[single_color]];

bitfield AltByte {
    bool versus : 1;
    bool unlisted_record: 1; 
    bool event_mode: 1;
    Unknown: 5 [[color("FFFFFF"), comment("Unknown")]];
};

struct Results
{
    u8 Unknown1 [[color("FFFFFF"), comment("Unknown")]];
    u8 Unused1;
    u8 Unused2;
    u8 Unknown2 [[color("FFFFFF"), comment("Unknown")]];
    
    // Other results for Unknown1, Unknown2
    // Normal Mode, Level 12 , Zero of Zero : 0x00, 0x00
    // Normal Mode, Level 199, Zero of One  : 0x00, 0x00
    // Normal Mode, Level 389, Zero of Three: 0x03, 0x00
    // Normal Mode, Level 137, Zero of One  : 0x00, 0x00
    // Normal Mode, ---------, Four of Ten  : 0x03, 0x02
    // Master Mode, Level 660, -----------  : 0x03, ----
    // Normal Mode, ---------, One of Ten   : ----, 0x02
    // Normal Mode, ---------, Two of Ten   : ----, 0x01 (normal_20250405_113128.bin)
    // Normal Mode, ---------, Two of Ten   : ----, 0x02 (normal_20250404_204014.bin)
    // Normal Mode, ---------, Zero of Five : 0x03, ----
};

fn format_frame_time(s32 time_frames) {
    u32 total_sec = time_frames / 60;
    u32 time_min = total_sec / 60;
    u32 time_sec = total_sec % 60;
    time_frames = time_frames % 60 * 100 / 60;
    return std::format("{:02d}'{:02d}\"{:02d}", time_min, time_sec, time_frames);
};

struct SingleGameReplay
{
    s32 num_frames;
    s32 playtime_frames @ 0x38 [[hidden]];
    // 112 frames for "Ready Go"
    // ReplayData.playtime_frames of gameplay
    // The rest is used during credits
    s32 ready_go_time = 112 [[export, format("format_frame_time")]];
    // game_time and post_game_time is nonsense in versus modes since playtime_frames is the sum over all rounds :)
    s32 game_time = playtime_frames [[export, format("format_frame_time")]];
    s32 post_game_time = num_frames - playtime_frames - 112 [[export, format("format_frame_time")]];
    s32 total_time = num_frames [[export, format("format_frame_time")]];
    // SEED = (1103515245*SEED + 12345) 
    u32 seed;
 
    Input inputs[num_frames];
};

struct VersusGameReplay
{
    SingleGameReplay player1_replay;
    SingleGameReplay player2_replay;
};

struct ReplayData {
    type::Magic<"TGRP">;
    u32 file_version;
    // possibly major version, minor version?
    // april 4: 0x00000104 (260) (possibly 1.0.2)
    // april 9: 0x00000104 (260) (possibly 1.0.7)
    // may 2: 0x00000107 (263) (possibly 1.2.2)
    // may 11: 0x00000107 (263) (possibly 1.3.0)
    // june 23: 0x00000107 (263) (1.5.1)
    // 1.6.0 beta: 0x00000107 (263) (1.6.0b)
    // june 23: Master mode has 0x00000107 (264)
    
    $ = 0x10;
    u64 steamid;
    type::time64_t timestamp;
    $ = 0x20;
    AltByte alt_byte;
    std::mem::AlignTo<4>;
    GameMode game_mode;
    bool is_versus = alt_byte.versus || game_mode == GameMode::Shiranui;
    bool player1_is_tgm_controls;
    std::mem::AlignTo<4>;
    bool player2_is_tgm_controls;
    std::mem::AlignTo<4>;
    Modifiers modifiers;
    std::mem::AlignTo<4>;
    
    $ = 0x34;
    u32 last_round_seed; // it seems to be the seed of the last played round?
    
    s32 playtime_frames;
    // play time excluding "ready go" and credits play
    s32 playtime = playtime_frames [[export, format("format_frame_time")]];
    s32 level;
    s32 score;
    s32 bravo;
    s32 shiranui_tier;
    s32 shiranui_points;
    Results normal_results [[color("FFFFFF"), comment("Unknown")]];

    $ = 0x54;
    s32 skin[[comment("Valid values: 0 to 39")]];
    $ = 0x60;
    u8 set_in_shiranui [[color("FFFFFF"), comment("Unknown")]]; // Is 0x09 in shiranui
   
    // Various settings
    $ = 0x6c;
    s32 number_of_next_previews [[comment("Valid values: 0 to 6")]];
    bool hold;
    std::mem::AlignTo<4>;
    bool ghost;
    std::mem::AlignTo<4>;
    bool konoha_all_clear_assist;
    std::mem::AlignTo<4>;
    bool show_tetromino_directional_guide;
    std::mem::AlignTo<4>;
    bool background_animation;
    std::mem::AlignTo<4>;
    bool diagonal_upperward_input;
    std::mem::AlignTo<4>;
    bool diagonal_downward_input;
    std::mem::AlignTo<4>;

    // Input data
    $ = 0x100;

    if (is_versus)
    {
        VersusGameReplay matches[while(!std::mem::eof())];
    } else {
        SingleGameReplay replay;
    }
};

ReplayData header @ 0x00;