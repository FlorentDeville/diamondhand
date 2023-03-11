<script>
    $(document).ready(function()
	{
        var sql = `select count(distinct card_id) as owned_card, round(sum(acq_price), 2) as acq_price, card_count_table.card_count, 
        sets_langs.name as set_name, game.name as game_name,
        sets_langs.id, count(distinct card_id)/card_count as percent_complete
        from owned_card inner join card on owned_card.card_id = card.id 
        inner join sets_langs on card.set_lang_id = sets_langs.id 
        inner join sets on sets.id = sets_langs.set_id 
        inner join game on game.id = sets.game_id 
        inner join (select count(card.id) as card_count, card.set_lang_id as set_lang_id from card group by set_lang_id) card_count_table on sets_langs.id = card_count_table.set_lang_id 
        group by card.set_lang_id;`

		$.get('php_scripts/execute_sql.php',{'sql':sql},function(return_data)
		{
			var sets = return_data.data;

			var column_array = new Array();
			column_array.push({header_name:"Game", field_name:"game_name", type:"string"});
			column_array.push({header_name:"Set", field_name:"set_name", type:"string"});
			column_array.push({header_name:"Count", field_name:"card_count", type:"int"});
			column_array.push({header_name:"Owned", field_name:"owned_card", type:"int"});
			column_array.push({header_name:"Acq Price", field_name:"acq_price", type:"float"});
            column_array.push({header_name:"% Completion", field_name:"percent_complete", type:"float"});
			display_table("table", column_array, sets, "id", 4, "desc");

            var HEIGHT = 10;
            var TOTAL_SIZE = 500;
            containerElement = document.getElementById("table");
            var children = containerElement.children[0].children;
            for(var ii = 0; ii < children.length - 1; ++ii)
            {
                var childRowIndex = ii + 1;
                var row = children[childRowIndex];
                var percentCell = row.children[5];
                var percent_complete = percentCell.textContent;

                var cell = document.createElement("td");
                row.appendChild(cell);
                var COMPLETE_SIZE = percent_complete * TOTAL_SIZE;
                var INCOMPLETE_SIZE = TOTAL_SIZE - COMPLETE_SIZE;

                heightDiv = document.createElement("div");
                heightDiv.style.height = HEIGHT + "px";
                cell.appendChild(heightDiv);

                completeDiv = document.createElement("div");
                completeDiv.style.float = "left";
                completeDiv.style.height = HEIGHT + "px";
                completeDiv.style.width = COMPLETE_SIZE + "px";
                completeDiv.style.backgroundColor = "green";
                cell.appendChild(completeDiv);

                incompleteDiv = document.createElement("div");
                incompleteDiv.style.float = "left";
                incompleteDiv.style.height = HEIGHT + "px";
                incompleteDiv.style.width = INCOMPLETE_SIZE + "px";
                incompleteDiv.style.backgroundColor = "red";
                cell.appendChild(incompleteDiv);
            }
            
		}, "json");
	});

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
</script>
<div>
    <div id="table"></div>
</div>
