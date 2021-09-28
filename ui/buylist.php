<script>
	function add_buylist()
	{
		var name = $('#buylist_name').val();
		$.get('php_scripts/command_add_buylist.php',{'buylist_name':name},function(return_data)
		{
			if(return_data.res == 1)
			{
				location.reload();
			}
		}, "json");
	}
	
	function delete_buylist(buylist_id)
	{
		var res = confirm('Are you sure you want to delete the buylist?')
		if(!res)
		{
			return;
		}
		
		$.get('php_scripts/command_delete_entry.php',{'table':"buy_list", "id":buylist_id},function(return_data)
		{
			if(return_data.res == 1)
			{
				location.reload();
			}
		}, "json");
	
	}
	
	function create_buylist_from_set_missing_cards()
	{
		var set_id = $("#set").val();
		var buylist_name = $("#buylist_name_2").val();
		
		sql_missing_card = "SELECT card.id FROM card left join owned_card on card.id = owned_card.card_id where owned_card.id is NULL and card.set_id=" + set_id;
		$.get('php_scripts/execute_sql.php',{'sql':sql_missing_card},function(return_data)
		{
			data = return_data.data;

			$.get('php_scripts/command_add_buylist.php',{'buylist_name':buylist_name},function(return_data)
			{
				if(return_data.res == 1)
				{
				 	buylist_id = return_data.id;
					for(var ii = 0; ii < data.length; ++ii)
					{
						card_id = data[ii]["id"];
						$.get('php_scripts/command_add_card_buylist.php',{'buylist_id':buylist_id, 'card_id':card_id},function(return_data)
						{
							console.log("card added");
						}, "json");
					}
				}	
			}, "json");
		}, "json");
	}
</script>
<div style="margin-bottom:20px;">
	New buylist :
	<input type="text" id="buylist_name" name="buylist_name" placeholder="Buylist name"/>
	<input type="submit" name="add_buylist" value="Add" onclick="add_buylist()"/>
</div>
<div style="margin-bottom:20px;">
	New buylist from missing cards of a set :
	<select name="set" id="set">
	<option value="" selected disabled hidden>Select Set</option>
	<?php
		$sql = "select sets.id, sets.name, game.name as game_name from sets inner join game on sets.game_id=game.id;";
		$result = $connection->query($sql);
		while($row = $result->fetch())
		{
			echo "<option value=\"" . $row["id"] . "\">(" . $row["game_name"] . ") " . $row["name"] . "</option>";
		}
	?>
	</select>
	<input type="text" id="buylist_name_2" name="buylist_name_2" placeholder="Buylist name"/>
	<input type="submit" name="add_buylist" value="Add" onclick="create_buylist_from_set_missing_cards()"/>
</div>

<div>
	<table>
		<tr><th>Name</th><th>Options</th></tr>
	<?php
		$sql = "select * from buy_list;";
		$result = $connection->query($sql);
		while($row = $result->fetch())
		{
			$deleteButton = "<span style='margin:0 10 0 10;' onclick='delete_buylist(".$row["id"].")'>X</span>";
			echo "<tr><td><a class='standard_link' href='./index.php?page=buylist_cards.php&buylist_id=" . $row["id"] . "'>" . $row["name"] . "</a></td><td>" . $deleteButton . " </td></tr>";
		}
	?>
	</table>
</div>