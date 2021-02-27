<div>
<?php
	$sql = "select card.name, conditions.code as cond, acq_price from owned_card inner join card on owned_card.card_id=card.id inner join conditions on conditions.id=owned_card.condition_id";
	$statement = $connection->query($sql);
	if($statement == False)
	{
		echo "Failed to retrieve the owned card";
	}
	while($result=$statement->fetch(PDO::FETCH_ASSOC))
	{
		if($result == False)
		{
			echo "Failed to retrieve the owned card";
		}
		echo "<div>";
		echo $result["name"] . "|" . $result["cond"] . "|" . $result["acq_price"];
		echo "</div>";
	}
?>
</div>