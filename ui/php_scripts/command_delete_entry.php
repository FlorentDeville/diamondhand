<?php
$id=$_GET['id'];
$table=$_GET['table'];

if(! is_numeric($id))
{
	echo "Wrong id " . $id;
	return;
}

$id = intval($id);
if(! is_int($id))
{
	echo "Wrong id " . $id;
	return;
}

include("../connection.php");

$sql="delete from ".$table." where id = ?;";
$statement = $connection->prepare($sql);
$statement->execute(array($id));

if($statement == False)
{
	echo "Failed to delete the row ";
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