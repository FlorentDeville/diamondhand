<?php
$name=$_GET['buylist_name'];

include("../connection.php");

//first find all the cards of the set with no variation
$sql="insert into buy_list (name) values (?);";
$statement = $connection->prepare($sql);
$statement->execute(array($name));

if($statement == False)
{
	echo "Failed to delete the owned card " . $owned_card_id;
	return;
}

if($statement->rowCount() <= 0)
{
	$res = array("res" => 0);
	echo json_encode($res);
}
else
{
	$res = array("res" => 1);
	echo json_encode($res);
}
?>