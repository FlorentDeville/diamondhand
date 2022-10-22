
<script>
    $(document).ready(function()
	{
        var sql = `select game.name as game_name, sets.name as set_name, sets.code as set_code, card.name, conditions.code as cond, cast(acq_price as decimal(5, 2)) as acq_price, languages.code as lang,
			owned_card.id as owned_card_id
			from owned_card inner join card on owned_card.card_id=card.id inner join conditions on conditions.id=owned_card.condition_id
			inner join sets_langs on sets_langs.id=card.set_lang_id
			inner join sets on sets_langs.set_id = sets.id
			inner join game on sets.game_id=game.id
			inner join languages on languages.id = sets_langs.lang_id`;

		$.get('php_scripts/execute_sql.php',{'sql':sql},function(return_data)
		{
			var sets = return_data.data;

			var column_array = new Array();
			column_array.push({header_name:"Card Name", field_name:"name", type:"string"});
			column_array.push({header_name:"Set", field_name:"set_name", type:"string"});
			column_array.push({header_name:"Lang", field_name:"lang", type:"string"});
			column_array.push({header_name:"Condition", field_name:"cond", type:"string"});
			column_array.push({header_name:"Acq Price", field_name:"acq_price", type:"float"});
			display_table("table", column_array, sets, "owned_card_id", 4, "desc");
		}, "json");
	});
</script>
<div>
<?php
	$sql = "SELECT round(sum(acq_price), 2) as money FROM owned_card";
	$statement = $connection->query($sql);
	$result = $statement->fetch();
	$money = $result["money"];
	echo "<div>Total Spent : $" . $money . "</div>";
?>
	<div id="table"></div>
</div>