<?Php
$set_id=$_GET['set_id'];
$condition_id = $_GET['condition_id'];
$price = $_GET['price'];
$date = $_GET['date'];

if(! is_numeric($set_id))
{
	echo "Wrong set id " . $set_id;
	return;
}

$set_id = intval($set_id);
if(! is_int($set_id))
{
	echo "Wrong set id " . $set_id;
	return;
}


if(!is_numeric($condition_id))
{
	echo "Wrong condition id";
	return;
}

$condition_id = intval($condition_id);
if(! is_int($condition_id))
{
	echo "Wrong condition id " . $condition_id;
	return;
}

if(!is_numeric($price))
{
	echo "Wrong price " . $price;
	return;
}
$price = floatval($price);
if(! is_float($price))
{
	echo "Price is not a correct value";
	return;
}

$format = "Y-m-d";
$d = DateTime::createFromFormat($format, $date);
$good_date = ($d && $d->format($format) === $date);
if(! $good_date)
{
	echo "Invalid date";
	return;
}

include("../connection.php");

//first find all the cards of the set with no variation
$sql="select * from card where set_id = " . $set_id . " and variation is NULL;";
$statement = $connection->query($sql);
if($statement == False)
{
	echo "Failed to retrieve the cards from set " . $set_id;
	return;
}
$set_cards = $statement->fetchAll(PDO::FETCH_ASSOC);
foreach($set_cards as $row)
{
	$sql="insert into owned_card (card_id, condition_id, acq_price, acq_date) values (?, ?, ?, ?)";
	$statement = $connection->prepare($sql);
	$statement->execute([$row["id"], $condition_id, $price, $date]);

	if($statement->rowCount() <= 0)
	{
		echo "Error, card" . $row["id"] . " not added";
		return;
	}
}

$sql="select * from sets where id = " . $set_id;
$statement = $connection->query($sql);
if($statement == False)
{
	echo "Failed to retrieve the set with id " . $set_id;
	return;
}
$set_result = $statement->fetch(PDO::FETCH_ASSOC);

$sql="select * from conditions where id = " . $condition_id;
$statement = $connection->query($sql);
if($statement == False)
{
	echo "Failed to retrieve the condition with id " . $condition_id;
	return;
}
$set_condition = $statement->fetch(PDO::FETCH_ASSOC);

echo "Set " . $set_result["name"] . " (" . $set_condition["code"] . ") acquired for $" . $price . " per card";
?>