<?Php
    @$sql=$_GET['sql'];

    include("../connection.php");

    $statement = $connection->query($sql);
    if($statement == False)
    {
        $main = array('data'=>"");
        echo json_encode($main);
        return;
    }
    $result=$statement->fetchAll(PDO::FETCH_ASSOC);

    if($result == False)
    {
        $main = array('data'=>"");
        echo json_encode($main);
        return;
    }

    $main = array('data'=>$result);
    echo json_encode($main);
?>
