<!-- <?php
	$setId = $_GET["set_id"];
	$query = $connection->query("select * from card where set_id = " . $setId . " order by number asc;");
	echo "<table>";
	echo "<tr><th>N</th><th>Name</th><th>Rarity</th><th>Variation</th><th>Links</th>";
	while($row = $query->fetch())
	{
		echo "<tr><td>" . $row["number"] . "</td><td>" . $row["name"] . "</td><td>" . $row["rarity"] . "</td><td>" . $row["variation"] . "</td><td><a class='standard_link' href=\"" . $row["tcg_url"] . "\">TCGP</a></td></tr>";
	}
	echo "</table>";
	$query = null;
	$connection = null;
	
?> -->

<script>
$(document).ready(function()
{
	const queryString = window.location.search;
	const urlParams = new URLSearchParams(queryString);
	const set_id = urlParams.get('set_id');

	var sql = "select * from card where set_id=" + set_id;
	$.get('php_scripts/execute_sql.php',{'sql':sql},function(return_data)
	{
		//show missing cards
		if(return_data.data.length>0)
		{
			$("#card_list_container").empty();
			
			var cards = return_data.data;
			var column_array = new Array();
			column_array.push({header_name:"N", field_name:"number", type:"int"});
			column_array.push({header_name:"Name", field_name:"name", type:"string"});
			column_array.push({header_name:"Rarity", field_name:"rarity", type:"string"});
			column_array.push({header_name:"Variation", field_name:"variation", type:"string"});
			column_array.push({header_name:"Links", field_name:"tcg_url", type:"string"});
			display_table("card_list_container", column_array, cards, "id", 0, "asc");
		}
		else
		{
			$('#card_list_container').html('No records Found');
		}
	}, "json");
});
</script>
<div id="card_list_container"></div>