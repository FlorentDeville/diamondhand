<?Php
$owned_card_id=$_GET['owned_card_id'];

if(! is_numeric($owned_card_id))
{
	echo "Wrong owned card id " . $owned_card_id;
	return;
}

$owned_card_id = intval($owned_card_id);
if(! is_int($owned_card_id))
{
	echo "Wrong owned car id " . $owned_card_id;
	return;
}

include("../connection.php");

//first find all the cards of the set with no variation
$sql="delete from owned_card where id = ?;";
$statement = $connection->prepare($sql);
$statement->execute(array($owned_card_id));

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