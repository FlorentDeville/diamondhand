<div>
<?php
	$sql = "select game.name as game_name, sets.name as set_name, sets.code as set_code, card.name, conditions.code as cond, acq_price 
			from owned_card inner join card on owned_card.card_id=card.id inner join conditions on conditions.id=owned_card.condition_id
			inner join sets on sets.id=card.set_id
			inner join game on sets.game_id=game.id";
	$statement = $connection->query($sql);
	if($statement == False)
	{
		echo "Failed to retrieve the owned card";
	}
	
	echo "<table>";
	echo "<tr><th>Card Name</th><th>Set</th><th>Condition</th><th>Acq Price</th></tr>";
	while($result=$statement->fetch(PDO::FETCH_ASSOC))
	{
		if($result == False)
		{
			echo "Failed to retrieve the owned card";
		}
		
		echo "<tr>";
		echo "<td>" . $result["name"] . "</td>";
		echo "<td style='text-align:center;' title='" . $result['set_name'] . "'>" . $result["set_code"] . "</td>";
		echo "<td style='text-align:center;'>" . $result["cond"] . "</td>";
		echo "<td style='text-align:right;'>" . number_format($result["acq_price"], 2) . "</td>";
		echo "</tr>";
	}
	echo "</table>";
?>
</div>