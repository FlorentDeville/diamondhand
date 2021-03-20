<?Php
@$buylist_id=$_GET['buylist_id'];
@$sort_field = $_GET['sort_field'];
@$sort_dir = $_GET['sort_dir'];

include("../connection.php");

$sql = "select buy_list_card.id, card.name as name, sets.code as set_code, sets.name as set_name, card.number 
		from buy_list_card inner join card on buy_list_card.card_id=card.id
		inner join sets on card.set_id=sets.id
		where buy_list_card.buy_list_id=" . $buylist_id . 
		" order by " . $sort_field . " " . $sort_direction . ";";

$statement = $connection->query($sql);
$result=$statement->fetchAll(PDO::FETCH_ASSOC);

$main = array('data'=>$result);
echo json_encode($main);

?>
