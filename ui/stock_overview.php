<script>
    function toggleShowMissingCard(set_lang_id, clicked_element_id)
    {
        var SELECTED_CLASS_NAME = "progressionSelectedSet";
        var DEFAULT_CLASS_NAME = "progressionSet";

        var currentClassName = document.getElementById(clicked_element_id).className;
        if (currentClassName == SELECTED_CLASS_NAME)
        {
            document.getElementById(clicked_element_id).className = DEFAULT_CLASS_NAME;
            $("#countMissingCards").empty();
            $("#missingCards").empty();
            return;
        }

        var sql = "select * from owned_card right join card on owned_card.card_id = card.id where owned_card.id is NULL and set_lang_id=" + set_lang_id;
        $.get('php_scripts/execute_sql.php',{'sql':sql},function(return_data)
        {
            //show missing cards
            if(return_data.data.length>0)
            {
                $("#countMissingCards").empty();
                $("#countMissingCards").append("<div style=\"margin:0 0 5 0;\">" + return_data.data.length + " missing card(s) in this set.</div>");
                var cards = return_data.data;
                var column_array = new Array();
                column_array.push({header_name:"N", field_name:"printed_number", type:"int"});
                column_array.push({header_name:"Name", field_name:"name", type:"string"});
                column_array.push({header_name:"Variation", field_name:"variation", type:"string"});
			    display_table("missingCards", column_array, cards, "id", 0, "asc");
            }
            else
            {
                $('#msg').html('No records Found');
            }
            
            var oldSelectedSets = document.getElementsByClassName("progressionSelectedSet");
            Array.prototype.forEach.call(oldSelectedSets, function(element) 
            {
                element.className = "progressionSet";
            });
            document.getElementById(clicked_element_id).className = "progressionSelectedSet";
        }, "json");
    }

    function addGamesButton(current_game_id)
    {
        gameList = [];
        gameList.push({name:"All", link:"./index.php?page=stock_index.php&stock_page=stock_overview.php", id:null});
        gameList.push({name:"MTG", link:"./index.php?page=stock_index.php&stock_page=stock_overview.php&gameid=1", id:1});
        gameList.push({name:"Pokemon", link:"./index.php?page=stock_index.php&stock_page=stock_overview.php&gameid=2", id:2});
        gameList.push({name:"FF", link:"./index.php?page=stock_index.php&stock_page=stock_overview.php&gameid=3", id:3});
        gameList.push({name:"DBS", link:"./index.php?page=stock_index.php&stock_page=stock_overview.php&gameid=4", id:4});

        var menu = document.getElementById("game_menu");
        for(var ii = 0; ii < gameList.length; ++ii)
        {
            game = gameList[ii];
            var gameButton = document.createElement("a");
            gameButton.href = game.link;
            if(game.id == current_game_id)
                gameButton.classList.add("selectedStockMenuButton");
            else
                gameButton.classList.add("stockMenuButton");

            gameButton.style.padding="0px 2px 0px 2px";

            var buttonContent = document.createElement("div");
            buttonContent.textContent=game.name;
            buttonContent.classList.add("stockMenuButton");
            gameButton.appendChild(buttonContent);

            menu.appendChild(gameButton);
        }
    }
</script>

<div id="game_menu" style="margin:10 0 20 0;">
    <div style="display:inline;"> Games : </div>
</div>

<div style="display:flex;">
    <div style="float:left; margin:0 50 0 0;">
<?php

$cond = "";
if(isset($_GET["gameid"]))
{
    $cond = "game_id=" . $_GET["gameid"];
}
else
{
    $cond = "1 = 1";
}

$sql_get_all_sets = "select sets.name, sets_langs.id, languages.code 
from sets_langs inner join sets on sets_langs.set_id = sets.id inner join languages on sets_langs.lang_id = languages.id where " . $cond . " order by sets_langs.release_date asc";
$result = $connection->query($sql_get_all_sets);
			
while($row = $result->fetch())
{
    $set_lang_id = $row["id"];
    $sql_get_card_count = "select count(*) from card where set_lang_id=" . $set_lang_id;
    $set_count_result = $connection->query($sql_get_card_count);
    $set_count_row = $set_count_result->fetch();
    $set_count = $set_count_row[0];

    $sql_get_owned_card_count = "select count(distinct card_id) as count_owned_cards, round(sum(acq_price), 2) from owned_card inner join card on owned_card.card_id = card.id where card.set_lang_id =" . $set_lang_id;
    $owned_result = $connection->query($sql_get_owned_card_count);
    $owned_card_row = $owned_result->fetch();
    $owned_card = $owned_card_row[0];
    $sum_acq_price = $owned_card_row[1];

    //don't show sets with 0 cards owned.
    if ($owned_card == 0)
    {
        continue;
    }

    $full_set = false;
    $style_name = "progressionSet";
    if($owned_card == $set_count)
    {
        $full_set = true;
        $style_name = "progressionFullSet";
    }

    $onclick = "";
    if(!$full_set)
    {
        $onclick = "onclick=\"toggleShowMissingCard(".$set_lang_id.", this.id)\"";
    }

    echo "<div class=\"".$style_name."\"".$onclick." id=\"".$set_lang_id."\">";
    echo "<div style=\"text-align:center;\">" . $row["name"] . " (" . strtoupper($row["code"]) . ")</div>";

    echo "<div style=\"text-align:center;\">" . $owned_card . "/" . $set_count . "
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$ " . $sum_acq_price . "</div>";

    $HEIGHT = 10;
    $TOTAL_SIZE = 500;
    $COMPLETE_SIZE = $owned_card / $set_count * $TOTAL_SIZE;
    $INCOMPLETE_SIZE = $TOTAL_SIZE - $COMPLETE_SIZE;
    echo "<div style=\"height:".$HEIGHT."px;\">";
    echo "<div style=\"float:left;height:".$HEIGHT."px;width:".$COMPLETE_SIZE.";background-color:green;\"></div>";
    echo "<div style=\"float:left;height:".$HEIGHT."px;width:".$INCOMPLETE_SIZE.";background-color:red;\"></div>";
    echo "</div>";
    echo "</div>";
}
?>
    </div>
    <div id="missingCardsContainer">
        <div id="countMissingCards"></div>
        <div id="missingCards"></div>
    </div>
</div>
<div id="msg"></div>

<script>
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const game_id = urlParams.get('gameid');
    addGamesButton(game_id);
</script>