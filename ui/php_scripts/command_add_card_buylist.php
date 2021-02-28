<?php
$buylist_id=$_GET['buylist_id'];
$card_id = $_GET['card_id'];

include("../connection.php");

//first find all the cards of the set with no variation
$sql="insert into buy_list_card (card_id, buy_list_id) values (?, ?);";
$statement = $connection->prepare($sql);
$statement->execute(array($card_id, $buylist_id));

if($statement == False)
{
	echo "Failed to add card to buylist";
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