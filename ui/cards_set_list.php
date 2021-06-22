<?php
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
	
?>
