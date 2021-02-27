<?Php
@$set_id=$_GET['set_id'];

if(!is_numeric($set_id))
{
	echo "Data Error";
	exit;
 }

include("../connection.php");

$sql="select id, name, number from card where set_id=" . $set_id . " order by number asc;";
$statement = $connection->query($sql);
if($statement == False)
{
	echo "error";
}
$result=$statement->fetchAll(PDO::FETCH_ASSOC);

if($result == False)
{
	echo "error";
}

$main = array('data'=>$result);
echo json_encode($main);
?>