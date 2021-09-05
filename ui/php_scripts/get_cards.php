<?Php
@$set_id=$_GET['set_id'];

$sort_field = "number";
if(isset($_GET["sort_field"]))
{
	$sort_field = $_GET["sort_field"];
}

$sort_dir = "asc";
if(isset($_GET["sort_dir"]))
{
	$sort_dir = $_GET["sort_dir"];
}

if(!is_numeric($set_id))
{
	echo "Data Error";
	exit;
 }

include("../connection.php");

$sql="select id, name, number, variation from card where set_id=" . $set_id . " order by ". $sort_field . " " . $sort_dir . ";";
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