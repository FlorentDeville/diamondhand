<script>
	$(document).ready(function()
	{
		$("#game").change(function()
		{
			var game_id=$('#game').val();
			$("#set").empty();
			var sql = "select sets_langs.id, sets.name, languages.code from sets inner join sets_langs on sets_langs.set_id = sets.id inner join languages on sets_langs.lang_id = languages.id where sets.game_id=" + game_id + " order by sets_langs.release_date asc";
			$.get('php_scripts/execute_sql.php',{'sql':sql},function(return_data)
			{
				var sets = return_data.data;
				$("#set").append("<option value='' selected disabled hidden>Select set</option>");
				for(var ii = 0; ii < Object.keys(sets).length; ++ii)
				{
					var set = sets[ii];
					$("#set").append("<option value='"+set["id"]+"'>"+set["name"] + " (" +set["code"]+")</option>");
				}
			}, "json");
		});
		
		$("#set").change(function()
		{
			var set_lang_id=$('#set').val();
			$("#card").empty();
			var sql = "select card.id, card.printed_number, card.name from card where card.set_lang_id=" + set_lang_id + " order by display_number asc;"
			$.get('php_scripts/execute_sql.php',{'sql':sql},function(return_data)
			{
				var cards = return_data.data;
				$('#msg').html( cards.length + ' records Found');
				$("#card").append("<option value='' selected disabled hidden>Select card</option>");
				for(var ii = 0; ii < Object.keys(cards).length; ++ii)
				{
					var card = cards[ii];
					$("#card").append("<option value='"+card["id"]+"'>(" + card["printed_number"] + ") " + card["name"] + "</option>");
				}
			}, "json");
		});
		
		$("#add_set_game").change(function()
		{
			var game_id=$('#add_set_game').val();
			$("#add_set_set").empty();
			var sql = "select sets_langs.id, sets.name, languages.code from sets inner join sets_langs on sets_langs.set_id = sets.id inner join languages on sets_langs.lang_id = languages.id"
			$.get('php_scripts/execute_sql.php',{'sql':sql},function(return_data)
			{
				var sets = return_data.data;
				$("#add_set_set").append("<option value='' selected disabled hidden>Select set</option>");
				for(var ii = 0; ii < Object.keys(sets).length; ++ii)
				{
					var set = sets[ii];
					$("#add_set_set").append("<option value='"+set["id"]+"'>"+set["name"] + " (" +set["code"]+")</option>");
				}
			}, "json");
		});
	});
	
	function add_card()
	{
		var card_id = $('#card').val();
		var condition_id = $('#condition').val();
		var price = $('#price').val();
		var date = $('#date').val();
		$.get('php_scripts/add_stock_card.php',{'card_id':card_id, 'condition_id':condition_id, 'price':price, 'date':date},function(return_data)
		{
			$("#result").prepend("<div>" + return_data + "</div>");
		}, "text");
	}
	
	function add_set()
	{
		var set_id = $('#add_set_set').val();
		var condition_id = $('#add_set_condition').val();
		var price = $('#add_set_price').val();
		var date = $('#add_set_date').val();
		$.get('php_scripts/add_stock_set.php',{'set_id':set_id, 'condition_id':condition_id, 'price':price, 'date':date},function(return_data)
		{
			$("#result").prepend("<div>" + return_data + "</div>");
		}, "text");
	}
</script>
<div>
	<span style='display:inline-block;width:100px;'>Add card</span>
	<?php 
		$query = $connection->query("select * from game;");
		
		echo "<select name=\"Game\" id=\"game\">";
		echo "<option value=\"\" selected disabled hidden>Select game</option>";
		while($row = $query->fetch())
		{
			echo "<option value=\"" . $row["id"] . "\">" . $row["name"] . "</option>";
		}
		echo "</select>";
	?>
	
	<select name="set" id="set" style="width:200px;">
		<option value="" selected disabled hidden>Select set</option>
	</select>
	
	<select name="card" id="card" style="width:300px;">
		<option value="" selected disabled hidden>Select card</option>
	</select>
	
	<?php
		$query = $connection->query("select * from conditions;");
		
		echo "<select name=\"condition\" id=\"condition\">";
		echo "<option value=\"\" selected disabled hidden>Select Condition</option>";
		while($row = $query->fetch())
		{
			echo "<option value=\"" . $row["id"] . "\">" . $row["name"] . "</option>";
		}
		echo "</select>";
	?>
	
	<input type="text" id="price" name="price" placeholder="Price"/>
	<input type="date" id="date" name="date" placeholder="Acquisition Date"/>
	<input type="submit" name="add_tag" value="Add card" onclick="add_card()"/>
</div>

<div>
	<span style='display:inline-block;width:100px;'>Add set</span>
	<?php 
		$query = $connection->query("select * from game;");
		
		echo "<select name=\"add_set_game\" id=\"add_set_game\">";
		echo "<option value=\"\" selected disabled hidden>Select game</option>";
		while($row = $query->fetch())
		{
			echo "<option value=\"" . $row["id"] . "\">" . $row["name"] . "</option>";
		}
		echo "</select>";
	?>
	
	<select name="add_set_set" id="add_set_set" style="width:200px;">
		<option value="" selected disabled hidden>Select set</option>
	</select>
	
	<?php
		$query = $connection->query("select * from conditions;");
		
		echo "<select name=\"add_set_condition\" id=\"add_set_condition\">";
		echo "<option value=\"\" selected disabled hidden>Select Condition</option>";
		while($row = $query->fetch())
		{
			echo "<option value=\"" . $row["id"] . "\">" . $row["name"] . "</option>";
		}
		echo "</select>";
		
		$query = null;
		$connection = null;
	?>
	
	<input type="text" id="add_set_price" name="add_set_price" placeholder="Price per card"/>
	<input type="date" id="add_set_date" name="add_set_date" placeholder="Acquisition Date"/>
	<input type="submit" name="add_tag" value="Add set" onclick="add_set()"/>
	
	<div id="result">
	</div>
</div>

<div id="result">
	</div>