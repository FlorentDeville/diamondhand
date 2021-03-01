<script>
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
</script>
<div>
<?php
	$sql = "select game.name as game_name, sets.name as set_name, sets.code as set_code, card.name, conditions.code as cond, acq_price,
			owned_card.id as owned_card_id
			from owned_card inner join card on owned_card.card_id=card.id inner join conditions on conditions.id=owned_card.condition_id
			inner join sets on sets.id=card.set_id
			inner join game on sets.game_id=game.id";
	$statement = $connection->query($sql);
	if($statement == False)
	{
		echo "Failed to retrieve the owned card";
	}
	
	echo "<table>";
	echo "<tr><th>Card Name</th><th>Set</th><th>Condition</th><th>Acq Price</th><th>Options</th></tr>";
	while($result=$statement->fetch(PDO::FETCH_ASSOC))
	{
		if($result == False)
		{
			echo "Failed to retrieve the owned card";
		}
		
		echo "<tr id='row_". $result["owned_card_id"] . "'>";
		echo "<td>" . $result["name"] . "</td>";
		echo "<td style='text-align:center;' title='" . $result['set_name'] . "'>" . $result["set_code"] . "</td>";
		echo "<td style='text-align:center;'>" . $result["cond"] . "</td>";
		echo "<td style='text-align:right;'>" . number_format($result["acq_price"], 2) . "</td>";
		echo "<td>Edit <a class=\"setButton\" href='#' onclick='delete_owned_card(" . $result["owned_card_id"] . ")'>X</a></td>";
		echo "</tr>";
	}
	echo "</table>";
?>
</div>