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
	});
	
	function add_card_to_buylist(buylist_id)
	{
			var card_id = $("#card").val();
			$.get('php_scripts/command_add_card_buylist.php',{'buylist_id':buylist_id, 'card_id':card_id},function(return_data)
			{
				if(return_data.res == 1)
				{
					location.reload();
				}
			}, "json");
	}
	
	function delete_card(card_id)
	{
		var res = confirm('Are you sure you want to delete this card from the buylist?')
		if(!res)
		{
			return;
		}
		$.get('php_scripts/command_delete_entry.php',{'table':"buy_list_card", 'id':card_id},function(return_data)
		{
			if(return_data.res == 1)
			{
				location.reload();
			}
			else
			{
				console.log(return_data);
			}
			
		}, "json");
	}
	
	function show_buylist(buylist_id, sort_field, sort_dir)
	{
		window.location.href = "http://diamondstreet2/index.php?page=buylist_cards.php&buylist_id=" + buylist_id + "&sort_field=" + sort_field + "&sort_dir=" + sort_dir;
	}

</script>
<div style="margin-bottom:20px;">
	<?php
		$sql = "select * from buy_list where id = " . $_GET["buylist_id"];
		$query = $connection->query($sql);
		$row = $query->fetch();
		echo "<h1>Buylist " . $row["name"] . "</h1>";
	?>
</div>
<div style="margin-bottom:20px;">
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
		echo "<input type='submit' name='add_tag' value='Add card' onclick='add_card_to_buylist(".$_GET["buylist_id"].")'/>";
	?>
</div>

<div>
	<table>
	<?php
		function get_sort_arrow($field, $dir, $title, $show_arrow)
		{
			$reverse_dir = "desc";
			$arrow = "▲";
			if($dir == "desc")
			{
				$arrow = " ▼";
				$reverse_dir = "asc";
			}
			
			if(!$show_arrow)
				$arrow = "";

			$content = "<span onclick=\"show_buylist('" . $_GET['buylist_id'] . "','" . $field . "','" . $reverse_dir . "')\">" . $title . $arrow . "</span>";
			return $content;
		}

		$sort_field = "number";
		$sort_direction = "asc";
		if(isset($_GET["sort_field"]))
			$sort_field = $_GET["sort_field"];
		if(isset($_GET["sort_dir"]))
			$sort_direction = $_GET["sort_dir"];
		
		$show_arrow = false;
		if($sort_field == "name")
			$show_arrow = true;
		
		$name_title = get_sort_arrow("name", $sort_direction, "Name", $show_arrow);

		$show_arrow = false;
		if($sort_field == "number")
			$show_arrow = true;
		
		$number_title = get_sort_arrow("number", $sort_direction, "N", $show_arrow);

		echo "<tr><th>" . $number_title . "</th><th>" . $name_title . "</th><th>Set</th><th>Options</th></tr>";

		$sql = "select buy_list_card.id, card.name as name, sets.code as set_code, sets.name as set_name, card.number 
		from buy_list_card inner join card on buy_list_card.card_id=card.id
		inner join sets on card.set_id=sets.id
		where buy_list_card.buy_list_id=" . $_GET['buylist_id'] . 
		" order by " . $sort_field . " " . $sort_direction . ";";
		$result = $connection->query($sql);
		while($row = $result->fetch())
		{
			$deleteButton = "<span style='margin:0 10 0 10;' onclick='delete_card(".$row["id"].")'>X</span>";
			echo "<tr><td>".$row["number"]."</td><td>" . $row["name"] . "</td><td>".$row["set_code"]."</td><td>".$deleteButton."</td></tr>";
		}
	?>
	</table>
</div>