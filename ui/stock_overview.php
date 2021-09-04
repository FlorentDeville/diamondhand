<?php

$sql_get_all_sets = "select * from sets;";
$result = $connection->query($sql_get_all_sets);
			
while($row = $result->fetch())
{
    $set_id = $row["id"];
    $sql_get_card_count = "select count(*) from card where set_id=" . $set_id;
    $set_count_result = $connection->query($sql_get_card_count);
    $set_count_row = $set_count_result->fetch();
    $set_count = $set_count_row[0];

    $sql_get_owned_card_count = "select count(distinct card_id) from owned_card inner join card on owned_card.card_id = card.id where card.set_id =" . $set_id;
    $owned_result = $connection->query($sql_get_owned_card_count);
    $owned_card_row = $owned_result->fetch();
    $owned_card = $owned_card_row[0];

    $style_name = "progressionSet";
    if($owned_card == $set_count)
    {
        $style_name="progressionFullSet";
    }

    echo "<div class=\"".$style_name."\">";
    echo "<div style=\"text-align:center;\">" . $row["name"] . "</div>";

    echo "<div style=\"text-align:center;\">" . $owned_card . "/" . $set_count . "</div>";

    $HEIGHT = 10;
    $TOTAL_SIZE = 500;
    $COMPLETE_SIZE = $owned_card / $set_count * $TOTAL_SIZE;
    $INCOMPLETE_SIZE = $TOTAL_SIZE - $COMPLETE_SIZE;
    echo "<div style=\"height:".$HEIGHT."px;\">";
    echo "<div style=\"float:left;height:".$HEIGHT."px;width:".$COMPLETE_SIZE.";background-color:green;\"></div>";
    echo "<div style=\"float:left;height:".$HEIGHT."px;width:".$INCOMPLETE_SIZE.";background-color:red;\"></div>";
    echo "</div>";
    echo "</div>";
}
?>