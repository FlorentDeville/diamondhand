<script>

$(document).ready(function()
	{
		$("#set").change(function()
		{
			var set_id=$('#set').val();
			window.location.href = "/index.php?page=stock_view_set.php&set_id=" + set_id;
		});
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
	$set_id = $_GET["set_id"];
	
	$sql = "SELECT round(sum(acq_price), 2) as money FROM owned_card inner join card on owned_card.card_id = card.id where card.set_id = " . $set_id;
	$statement = $connection->query($sql);
	$result = $statement->fetch();
	$money = $result["money"];
	echo "<div>Total Spent : $" . $money . "</div>";
	
	$sql = "select game.name as game_name, sets.name as set_name, sets.code as set_code, card.name, conditions.code as cond, acq_price,
			owned_card.id as owned_card_id
			from owned_card inner join card on owned_card.card_id=card.id inner join conditions on conditions.id=owned_card.condition_id
			inner join sets on sets.id=card.set_id
			inner join game on sets.game_id=game.id
			where card.set_id = " . $set_id;
	$statement = $connection->query($sql);
	if($statement == False)
	{
		echo "Failed to retrieve the owned card";
	}
	
	$all_cards = $statement->fetchAll();
	echo "<div> Found " . count($all_cards) . " cards.</div>";
	
	echo "<table>";
	echo "<tr><th>Card Name</th><th>Set</th><th>Condition</th><th>Acq Price</th><th>Options</th></tr>";
	//while($result=$statement->fetch(PDO::FETCH_ASSOC))
	foreach($all_cards as $result)
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