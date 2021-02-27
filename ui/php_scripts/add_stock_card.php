<?Php
$card_id=$_GET['card_id'];
$condition_id = $_GET['condition_id'];
$price = $_GET['price'];
$date = $_GET['date'];

if(! is_numeric($card_id))
{
	echo "Wrong card id " . $card_id;
	return;
}

$card_id = intval($card_id);
if(! is_int($card_id))
{
	echo "Wrong card id " . $card_id;
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

$sql="insert into owned_card (card_id, condition_id, acq_price, acq_date) values (?, ?, ?, ?)";
$statement = $connection->prepare($sql);
$statement->execute([$card_id, $condition_id, $price, $date]);

if($statement->rowCount() <= 0)
{
	echo "Error, card not added";
}

$owned_card_id = $connection->lastInsertId();
$sql="select card.name, conditions.code as cond, acq_price from owned_card inner join card on owned_card.card_id=card.id inner join conditions on conditions.id=owned_card.condition_id where owned_card.id = " . $owned_card_id;
$statement = $connection->query($sql);
if($statement == False)
{
	echo "Failed to retrieve the owned card I just added with id " . $owned_card_id;
}
$result=$statement->fetch(PDO::FETCH_ASSOC);
if($result == False)
{
	echo "Failed to retrieve the owned card I just added with id " . $owned_card_id;
}

echo "Card " . $result["name"] . " (" . $result["cond"] . ") acquired for $" . $result["acq_price"];
?>