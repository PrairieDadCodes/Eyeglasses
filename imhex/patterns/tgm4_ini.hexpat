#pragma description 

import std.mem;
import std.io;
import hex.core;

fn decrypt_section(u8 key, std::mem::Section section)
{
    for (u32 i = 0, i < std::mem::get_section_size(section), i = i+1)
    {
        sectionData[i] = $[i] ^ key;
    }
};

struct DataFile
{
    u8 key;
    std::mem::Section DecryptedSection = std::mem::create_section("Decrypted Section");
    
    auto remaining_size = std::mem::size()-1;
    std::mem::set_section_size(DecryptedSection, remaining_size);
    u8 sectionData[remaining_size] @ 0x00 in DecryptedSection;
    decrypt_section(key, DecryptedSection);   
    hex::core::add_virtual_file("Decoded", sectionData);

};

DataFile data @ 0x00;