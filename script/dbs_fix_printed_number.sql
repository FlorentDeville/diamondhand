set @set_to_change = 103; make sure the set id is correct

update card set printed_number = concat(printed_number, " C") where set_lang_id = @set_to_change and rarity = "Common";
update card set printed_number = concat(printed_number, " R") where set_lang_id = @set_to_change and rarity = "Rare";
update card set printed_number = concat(printed_number, " SR") where set_lang_id = @set_to_change and rarity = "Super Rare";
update card set printed_number = concat(printed_number, " SPR") where set_lang_id = @set_to_change and rarity = "Special Rare";
update card set printed_number = concat(printed_number, " SCR") where set_lang_id = @set_to_change and rarity = "Secret Rare";
update card set printed_number = concat(printed_number, " UC") where set_lang_id = @set_to_change and rarity = "Uncommon";
