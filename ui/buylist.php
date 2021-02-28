<script>
	function add_buylist()
	{
		var name = $('#buylist_name').val();
		$.get('php_scripts/command_add_buylist.php',{'buylist_name':name},function(return_data)
		{
			if(return_data.res == 1)
			{
				location.reload();
			}
		}, "json");
	}
	
	function delete_buylist(buylist_id)
	{
		var res = confirm('Are you sure you want to delete the buylist?')
		if(!res)
		{
			return;
		}
		
		$.get('php_scripts/command_delete_entry.php',{'table':"buy_list", "id":buylist_id},function(return_data)
		{
			if(return_data.res == 1)
			{
				location.reload();
			}
		}, "json");
	
	}
</script>
<div style="margin-bottom:20px;">
	New buylist :
	<input type="text" id="buylist_name" name="buylist_name" placeholder="Buylist name"/>
	<input type="submit" name="add_buylist" value="Add" onclick="add_buylist()"/>
</div>

<div>
	<table>
		<tr><th>Name</th><th>Options</th></tr>
	<?php
		$sql = "select * from buy_list;";
		$result = $connection->query($sql);
		while($row = $result->fetch())
		{
			$deleteButton = "<span style='margin:0 10 0 10;' onclick='delete_buylist(".$row["id"].")'>X</span>";
			echo "<tr><td>" . $row["name"] . "</td><td><a href='./index.php?page=buylist_cards.php&buylist_id=" . $row["id"] . "'>Edit</a>" . $deleteButton . " </td></tr>";
		}
	?>
	</table>
</div>