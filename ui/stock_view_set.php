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
			var set_id=$('#set').val();
			new_url = update_url_parameter(window.location.href, "set_id", set_id);
			window.location.href = new_url;
		});

		var set_id=$('#set').val();
		var sort_field = "number";
		var sort_dir = "asc";
		show_set(set_id, sort_field, sort_dir);
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

	function show_set(set_id, sort_field, sort_dir)
	{
		var sql = `select game.name as game_name, sets.name as set_name, sets.code as set_code, card.name, conditions.code as cond, acq_price,
			owned_card.id as owned_card_id, 
			card.number 
			from owned_card inner join card on owned_card.card_id=card.id inner join conditions on conditions.id=owned_card.condition_id
			inner join sets on sets.id=card.set_id
			inner join game on sets.game_id=game.id
			where card.set_id = ` + set_id + ` 
			order by ` + sort_field + " " + sort_dir;

		$.get('php_scripts/execute_sql.php',{'sql':sql},function(return_data)
		{
			obj = JSON.parse(return_data);
			var cards = obj["data"];
			display_array("array_container", cards, sort_field, sort_dir, set_id);

			$("#card_count").empty();

			var card_count = Object.keys(cards).length;
			$("#card_count").prepend("Found " + card_count.toString() + " cards");

		}, "text");
	}

	function get_array_header(field, dir, title, show_arrow, set_id)
	{
		var reverse_dir = "desc";
		var arrow = "▲";
		if(dir == "desc")
		{
			arrow = " ▼";
			reverse_dir = "asc";
		}
		
		if(!show_arrow)
			arrow = "";

		var content = "<span onclick=\"show_set(" + set_id + ",'" + field + "','" + reverse_dir + "')\">" + title + arrow + "</span>";
		return content;
	}

	function display_array(container_id, data, sort_field, sort_dir, set_id)
	{
		var content = "<table>";
		var header_data_array = 
		[
			{field:"number", title:"N"},
			{field:"name", title:"Card Name"},
			{field:"set_name", title:"Set"},
			{field:"cond", title:"Condition"},
			{field:"acq_price", title:"Acq Price"}
		];

		content += "<tr>";
		for(var ii = 0; ii < Object.keys(header_data_array).length; ++ii)
		{
			var header_data = header_data_array[ii];
			var header = get_array_header(header_data["field"], sort_dir, header_data["title"], header_data["field"] == sort_field, set_id);
			content += "<th>" + header + "</th>";
		}
		content += "<th>Options</th>";
		content += "</tr>";

		for(ii=0; ii < Object.keys(data).length; ++ii)
		{
			var card = data[ii];
			
			content += "<tr id='row_" + card["owned_card_id"] + "'>";
			content += "<td>" + card["number"] + "</td>";
			content += "<td>" + card["name"] + "</td>";
			content += "<td style='text-align:center;' title='" + card['set_name'] + "'>" + card["set_code"] + "</td>";
			content += "<td style='text-align:center;'>" + card["cond"] + "</td>";
			content += "<td style='text-align:right;'>" + Number.parseFloat(card["acq_price"]).toFixed(2) + "</td>";
			content += "<td>Edit <a class=\"setButton\" href='#' onclick='delete_owned_card(" + card["owned_card_id"] + ")'>X</a></td>";
			content += "</tr>";
		}
		content += "</table>";

		$("#" + container_id).empty();
		$("#" + container_id).prepend(content);
	}

</script>
<div>
<div style="margin-bottom:20px;">
	Select set :
	<select name="set" id="set">
		<?php
			$sql = "select sets.id, sets.name, game.name as game_name from sets inner join game on sets.game_id=game.id;";
			$result = $connection->query($sql);
			
			if(!isset($_GET["set_id"]))
			{
				echo "<option value=\"\" selected disabled hidden>Select Set</option>";
			}
			
			while($row = $result->fetch())
			{
				if (isset($_GET["set_id"]))
				{
					$option = "";
					$set_id = $_GET["set_id"];
					if ($set_id == $row["id"])
					{
						$option = "selected";
					}
				}
				echo "<option value=\"" . $row["id"] . "\"" . $option . ">(" . $row["game_name"] . ") " . $row["name"] . "</option>";
			}
		?>
	</select>
</div>
	
<?php
	if(!isset($_GET["set_id"]))
	{
		return;
	}

	$sql = "SELECT round(sum(acq_price), 2) as money FROM owned_card inner join card on owned_card.card_id = card.id where card.set_id = " . $set_id;
	$statement = $connection->query($sql);
	$result = $statement->fetch();
	$money = $result["money"];
	echo "<div id='card_count'></div>";
	echo "<div>Total Spent : $" . $money . "</div>";
	
	echo "<div id='array_container'></div>";
?>
</div>