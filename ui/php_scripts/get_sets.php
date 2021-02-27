<?Php
@$game_id=$_GET['game_id'];

if(!is_numeric($game_id))
{
	echo "Data Error";
	exit;
 }

include("../connection.php");

$sql="select * from sets where game_id=" . $game_id;
$statement = $connection->query($sql);
$result=$statement->fetchAll(PDO::FETCH_ASSOC);

$main = array('data'=>$result);
echo json_encode($main);
?>