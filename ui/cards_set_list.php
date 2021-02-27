<?php 
	/*$servername = "localhost";
	$username = "root";
	$password = "";
	$db = "wallstreet";


	$connection = new PDO("mysql:host=$servername;dbname=$db", $username, $password);
	// set the PDO error mode to exception
	$connection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	*/
	$setId = $_GET["set_id"];
	$query = $connection->query("select * from card where set_id = " . $setId . ";");
	while($row = $query->fetch())
	{
		//$style = "padding:10 30 10 30;background-image:linear-gradient(white, grey, grey);border-radius:5px;margin:10 0 10 0;";
		$style = "";
		echo "<div style = \"" . $style . "\">";
		echo $row["name"] . "<br/>\n";
		echo "</div>";
	}
	$query = null;
	$connection = null;
	
?>
