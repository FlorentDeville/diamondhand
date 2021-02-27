<?php 
	/*$servername = "localhost";
	$username = "root";
	$password = "";
	$db = "wallstreet";


	$connection = new PDO("mysql:host=$servername;dbname=$db", $username, $password);
	// set the PDO error mode to exception
	$connection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	*/
	$query = $connection->query("select * from sets order by release_date desc;");
	while($row = $query->fetch())
	{
		echo "<a class=\"setButton\" href=\"index.php?page=cards_set_list.php&set_id=" . $row["id"] . "\">";
		echo "<div class=\"setButton\">";
		echo $row["name"];
		echo "</div>";
		echo "<a/>";
	}
	$query = null;
	$connection = null;
	
?>
			