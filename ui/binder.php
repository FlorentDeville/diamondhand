<script>
    $(document).ready(function()
	{
        const queryString = window.location.search;
	    const urlParams = new URLSearchParams(queryString);
	    const game_id = urlParams.get('game_id');

        var sql = `select sets_langs.name as set_name, sets_langs.id as set_lang_id, game.id as game_id, sets_langs.release_date
        from sets_langs
        inner join sets on sets_langs.set_id = sets.id
        inner join game on sets.game_id = game.id
        where game_id=` + game_id + ` order by sets_langs.release_date`;
        console.log(sql);
		$.get('php_scripts/execute_sql.php',{'sql':sql},function(return_data)
		{
			var sets = return_data.data;

            for(ii=0; ii < Object.keys(sets).length; ++ii)
            {
                var card = sets[ii];

                switch(game_id)
                {
                    case "1" : //mtg
                        break;

                    case "2" : //pokemon
                        card["side_link"] = "./pokemon_binder/side.php?set_lang_id=" + card["set_lang_id"];
                        card["front_link"] = "./pokemon_binder/front.php?set_lang_id=" + card["set_lang_id"];
                        break;

                    case "3" : //ff
                        card["side_link"] = "./ff_binder/side.php?set_lang_id=" + card["set_lang_id"];
                        card["front_link"] = "./ff_binder/front.php?set_lang_id=" + card["set_lang_id"];
                        card["checklist_p1"] = "./checklist/fftcg/checklist_fftcg.html?json=" + card["set_lang_id"] + "&pageIndex=0";
                        card["checklist_p2"] = "./checklist/fftcg/checklist_fftcg.html?json=" + card["set_lang_id"] + "&pageIndex=1";
                        break;

                    case "4" : //dbs
                        card["side_link"] = "./binder_dbs/side.php?set_lang_id=" + card["set_lang_id"];
                        card["front_link"] = "./binder_dbs/front.php?set_lang_id=" + card["set_lang_id"];
                        break;

                    case "5": //one piece
                        card["side_link"] = "./binder/one_piece/side.php?set_lang_id=" + card["set_lang_id"];
                        card["front_link"] = "./binder/one_piece/front.php?set_lang_id=" + card["set_lang_id"];
                        break;

                    default:
                        break;
                }
                
            }

			var column_array = new Array();
            column_array.push({header_name:"Id", field_name:"set_lang_id", type:"int"});
			column_array.push({header_name:"Set", field_name:"set_name", type:"string"});
			column_array.push({header_name:"Side", field_name:"side_link", type:"link"});
			column_array.push({header_name:"Front", field_name:"front_link", type:"link"});
            column_array.push({header_name:"P1", field_name:"checklist_p1", type:"link"});
            column_array.push({header_name:"P2", field_name:"checklist_p2", type:"link"});
            column_array.push({header_name:"Release", field_name:"release_date", type:"string"});
			display_table("content", column_array, sets, "release_date", 6, "asc");
		}, "json");
	});
</script>

<div id="menu" style="margin:10 0 20 0;">
    <div style="display:inline;"> Stocks : </div>
    <a class="stockMenuButton" href="./index.php?page=binder.php&game_id=2"><div class="stockMenuButton">Pokemon</div></a>
    <a class="stockMenuButton" href="./index.php?page=binder.php&game_id=1"><div class="stockMenuButton">MTG</div></a>
    <a class="stockMenuButton" href="./index.php?page=binder.php&game_id=3"><div class="stockMenuButton">Final Fantasy</div></a>
    <a class="stockMenuButton" href="./index.php?page=binder.php&game_id=4"><div class="stockMenuButton">DBS</div></a>
    <a class="stockMenuButton" href="./index.php?page=binder.php&game_id=5"><div class="stockMenuButton">One Piece</div></a>
</div>
<div id="content">
</div>