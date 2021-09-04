<script>
    function showMissingCard(set_id, clicked_element_id)
    {
        var sql = "select * from owned_card right join card on owned_card.card_id = card.id where owned_card.id is NULL and set_id=" + set_id;
        console.log(sql);
        $.get('php_scripts/execute_sql.php',{'sql':sql},function(return_data)
        {
            $("#missingCards").empty();
            if(return_data.data.length>0)
            {
                console.log(return_data.data);
                for(var ii = 0; ii < return_data.data.length; ++ii)
                {
                    var card = return_data.data[ii];
                    $("#missingCards").append("<div>" + card.number + " " + card.name + "</div>");
                }
            }
            else
            {
                $('#msg').html('No records Found');
            }
            
            var oldSelectedSets = document.getElementsByClassName("progressionSelectedSet");
            Array.prototype.forEach.call(oldSelectedSets, function(element) 
            {
                element.className = "progressionSet";
            });
            document.getElementById(clicked_element_id).className = "progressionSelectedSet";
        }, "json");
    }
</script>
<div style="display:flex;">
    <div style="float:left; margin:0 50 0 0;">
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

    $full_set = false;
    $style_name = "progressionSet";
    if($owned_card == $set_count)
    {
        $full_set = true;
        $style_name = "progressionFullSet";
    }

    $onclick = "";
    if(!$full_set)
    {
        $onclick = "onclick=\"showMissingCard(".$set_id.", this.id)\"";
    }

    echo "<div class=\"".$style_name."\"".$onclick." id=\"".$set_id."\">";
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

    //select * from owned_card right join card on owned_card.card_id = card.id where set_id=9 and owned_card.id is NULL
}
?>
    </div>
    <div id="missingCards">


    </div>
</div>
<div id="msg"></div>