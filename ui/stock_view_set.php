<script>

	function update_url_parameter(url, param_name, param_value)
	{
		var urlSplit = url.split("?");
		var parameters = urlSplit[1].split("&");

		var found = false;
		for(var ii = 0; ii < parameters.length; ++ii)
		{
			var splitParameter = parameters[ii].split("=");
			if(splitParameter[0] == param_name)
			{
				parameters[ii] = param_name + "=" + param_value;
				found = true;
				break;
			}
		}

		if(found == false)
		{
			parameters.push(param_name + "=" + param_value);
		}

		var new_url = urlSplit[0] + "?"
		for(var ii = 0; ii < parameters.length; ++ii)
		{
			if(ii > 0)
			{
				new_url += "&";
			}
			new_url += parameters[ii];
		}

		return new_url;
	}

	$(document).ready(function()
	{
		$("#set").change(function()
		{
			var set_lang_id=$('#set').val();
			new_url = update_url_parameter(window.location.href, "set_lang_id", set_lang_id);
			window.location.href = new_url;
		});

		var set_lang_id=$('#set').val();
		var sort_field = "printed_number";
		var sort_dir = "asc";
		show_set(set_lang_id, sort_field, sort_dir);
	});
	
	function delete_owned_card(owned_card_id)
	{
		var res = confirm('Are you sure you want to delete this card from your stock?')
		if(!res)
		{
			return;
		}
		
		$.get('php_scripts/command_delete_owned_card.php',{'owned_card_id':owned_card_id},function(return_data)
		{
			if(return_data.res == 1)
			{
				var row_id = "#row_" + owned_card_id;
				$(row_id).remove();
			}
			else
			{
				console.log("error");
			}
		}, "json");
	}

	function show_set(set_lang_id, sort_field, sort_dir)
	{
		var sql = `select game.name as game_name, sets.name as set_name, sets.code as set_code, card.name, conditions.code as cond, cast(acq_price as decimal(10,2)) as acq_price,
			owned_card.id as owned_card_id, card.printed_number, card.id as card_id, card.rarity
			from owned_card 
			inner join card on owned_card.card_id=card.id 
			inner join conditions on conditions.id=owned_card.condition_id
			inner join sets_langs on sets_langs.id = card.set_lang_id
			inner join languages on sets_langs.lang_id = languages.id
			inner join sets on sets.id = sets_langs.set_id
			inner join game on sets.game_id=game.id
			where card.set_lang_id = ` + set_lang_id + ` 
			order by ` + sort_field + " " + sort_dir;

		$.get('php_scripts/execute_sql.php',{'sql':sql},function(return_data)
		{
			cards = return_data.data;
			var card_count = cards.length;
			$("#card_count").empty();
			$("#card_count").prepend("Found " + card_count.toString() + " cards");

			var column_array = new Array();
			column_array.push({header_name:"N", field_name:"printed_number", type:"int"});
			column_array.push({header_name:"Rarity", field_name:"rarity", type:"string"});
			column_array.push({header_name:"Card Name", field_name:"name", type:"string"});
			column_array.push({header_name:"Set", field_name:"set_code", type:"string"});
			column_array.push({header_name:"Condition", field_name:"cond", type:"string"});
			column_array.push({header_name:"Acq Price", field_name:"acq_price", type:"float"});
			display_table("array_container", column_array, cards, "card_id", 0, "asc");
			showCardImage("array_container", "image_container", set_lang_id);
		}, "json");
	}
</script>
<div>
<div style="margin-bottom:20px;">
	Select set :
	<select name="set" id="set">
		<?php
			$sql = "select sets_langs.id, sets.name, languages.code as lang, game.name as game_name from sets inner join game on sets.game_id=game.id
			inner join sets_langs on sets_langs.set_id = sets.id
			inner join languages on languages.id = sets_langs.lang_id;";
			$result = $connection->query($sql);
			
			if(!isset($_GET["set_lang_id"]))
			{
				echo "<option value=\"\" selected disabled hidden>Select Set</option>";
			}
			
			while($row = $result->fetch())
			{
				if (isset($_GET["set_lang_id"]))
				{
					$option = "";
					$set_lang_id = $_GET["set_lang_id"];
					if ($set_lang_id == $row["id"])
					{
						$option = "selected";
					}
				}
				echo "<option value=\"" . $row["id"] . "\"" . $option . ">(" . $row["game_name"] . ") " . $row["name"] . " (" . $row["lang"] . ")</option>";
			}
		?>
	</select>
</div>
	
<?php
	if(!isset($_GET["set_lang_id"]))
	{
		return;
	}

	$sql = "SELECT round(sum(acq_price), 2) as money FROM owned_card 
	inner join card on owned_card.card_id = card.id where card.set_lang_id = " . $set_lang_id;
	$statement = $connection->query($sql);
	$result = $statement->fetch();
	$money = $result["money"];
	echo "<div id='card_count'></div>";
	echo "<div>Total Spent : $" . $money . "</div>";
	
	echo "<div id='array_container'></div>";
	echo "<img id='image_container' style='position:absolute; display:none; pointer-events:none; border:15px; border-color:transparent; border-style:double;'/>"
?>
</div>