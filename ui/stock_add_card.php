<script>
	$(document).ready(function()
	{
		$("#game").change(function()
		{
			var game_id=$('#game').val();
			$("#set").empty();
			$.get('php_scripts/get_sets.php',{'game_id':game_id},function(return_data)
			{
				if(return_data.data.length>0)
				{
					//$('#msg').html( return_data.data.length + ' records Found');
					$("#set").append("<option value='' selected disabled hidden>Select set</option>");
					$.each(return_data.data, function(key,value)
					{
						$("#set").append("<option value='"+value.id+"'>"+value.name+"</option>");
					});
				}
				else
				{
					$('#msg').html('No records Found');
				}
			}, "json");
		});
		
		$("#set").change(function()
		{
			var set_id=$('#set').val();
			$("#card").empty();
			$.get('php_scripts/get_cards.php',{'set_id':set_id},function(return_data)
			{
				if(return_data.data.length>0)
				{
					//$('#msg').html( return_data.data.length + ' records Found');
					$("#card").append("<option value='' selected disabled hidden>Select card</option>");
					$.each(return_data.data, function(key,value)
					{
						$("#card").append("<option value='"+value.id+"'>(" + value.number + ") " + value.name + "</option>");
					});
				}
				else
				{
					$('#msg').html('No records Found');
				}
			}, "json");
		});
		
		$("#add_set_game").change(function()
		{
			var game_id=$('#add_set_game').val();
			$("#add_set_set").empty();
			$.get('php_scripts/get_sets.php',{'game_id':game_id},function(return_data)
			{
				if(return_data.data.length>0)
				{
					//$('#msg').html( return_data.data.length + ' records Found');
					$("#add_set_set").append("<option value='' selected disabled hidden>Select set</option>");
					$.each(return_data.data, function(key,value)
					{
						$("#add_set_set").append("<option value='"+value.id+"'>"+value.name+"</option>");
					});
				}
				else
				{
					$('#msg').html('No records Found');
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