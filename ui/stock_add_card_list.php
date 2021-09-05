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
	});

function show_set(sort_field, sort_dir)
{
	var set_id = $('#set').val();
	$.get('php_scripts/get_cards.php',{'set_id':set_id, 'sort_field':sort_field, 'sort_dir':sort_dir},function(return_data)
	{
		obj = JSON.parse(return_data);
		var cards = obj["data"];
		var content = "<table id='cards_table'>";

		var show_arrow = false;
		if(sort_field == "name")
			show_arrow = true;
		
		var name_title = get_sort_arrow("name", sort_dir, "Name", show_arrow);

		show_arrow = false;
		if(sort_field == "number")
			show_arrow = true;
		
		var number_title = get_sort_arrow("number", sort_dir, "N", show_arrow);

		content += "<tr><th>" + number_title + "</th><th>" + name_title +"</th><th>Variation</th><th>Date</th><th>Price</th>";
		for(ii=0; ii < Object.keys(cards).length; ++ii)
		{
			var card = cards[ii];
			content += "<tr id='" + card["id"] + "'><td>" + card["number"] + "</td><td>" + card["name"] + "</td>";

			var variationText = "";
			console.log(card["variation"]);
			if(card["variation"] != "null" && card["variation"] != null)
				variationText = card["variation"];

			content += "<td>" + variationText + "<td>";
			content += "<td><input type=\"date\" id=\"date\" name=\"date\" placeholder=\"Acquisition Date\" onkeydown=\"date_on_keydown(event)\"/></td>";
			content += "<td><input type=\"text\" id=\"price\" name=\"price\" placeholder=\"Price\"/></td></tr>"
		}
		content += "</table>";
		content += "<input type=\"submit\" name=\"add_cards\" value=\"Submit\" onclick=\"submit_cards()\"/>";

		$("#list_container").empty();
		$("#list_container").prepend(content);
	}, "text");
}

function submit_cards()
{
	var all_children = $("#cards_table").find("tr");
	for(var ii = 0; ii < all_children.length; ++ii)
	{
		var row = all_children[ii];
		if(row.id == "")
			continue;

		var card_id = row.id;
		var date = row.querySelector("input[id='date']").value;
		var price = row.querySelector("input[id='price']").value;
		var condition = 1; //near mint

		if(date == "" || price == "")
			continue;

		//$card_id=$_GET['card_id'];
		//$condition_id = $_GET['condition_id'];
		//$price = $_GET['price'];
		//$date = $_GET['date'];

		$.get('php_scripts/add_stock_card.php',{'card_id':card_id, 'date':date, 'price':price, 'condition_id': condition },function(return_data)
		{
			var content = "<div>" + return_data + "</div>";
			$("#list_result").prepend(content);
		}, "text");
	}
}

/////////////////////////////////////////////////////
// date filed with copy paste enabled
/////////////////////////////////////////////////////
var control_pressed = false;

function change_input_type(oldObject, oType) 
{
	var newObject = document.createElement("input");
	newObject.type = oType;
	if(oldObject.size) {newObject.size = oldObject.size;}
	if(oldObject.value) {newObject.value = oldObject.value;}
	if(oldObject.name) {newObject.name = oldObject.name;}
	if(oldObject.id) {newObject.id = oldObject.id;}
	if(oldObject.className) {newObject.className = oldObject.className;}
	oldObject.parentNode.replaceChild(newObject,oldObject);
	newObject.select();
	return newObject;
}

function date_on_keydown(event)
{
	var CONTROL_LEFT = 17;
	if ((event.keyCode == CONTROL_LEFT) && (control_pressed != true)) 
	{
		var srcElement = event.srcElement;
		var txtElement = change_input_type(srcElement, "text");
		txtElement.onkeyup = date_on_keyup;
		control_pressed = true;
	}
}

function date_on_keyup(event)
{
	var CONTROL_LEFT = 17;
	if ((event.keyCode == CONTROL_LEFT) && (control_pressed != false)) 
	{
		var srcElement = event.srcElement;
		var dateElement = change_input_type(srcElement, "date");
		dateElement.onkeydown = date_on_keydown;
		control_pressed = false;
    }
}

/////////////////////////////////////////////////
//
/////////////////////////////////////////////////

</script>
<div>
	<span style='display:inline-block;width:100px;'>Add card</span>
	<?php
		$sort_field = "number";
	 	if(isset($_GET["sort_field"]))
		 	$sort_field = $_GET["sort_field"];

		$sort_dir = "asc";
		if(isset($_GET["sort_dir"]))
			$sort_dir = $_GET["sort_dir"];
		
		$query = $connection->query("select * from game;");
		
		echo "<select name=\"Game\" id=\"game\">";
		echo "<option value=\"\" selected disabled hidden>Select game</option>";
		while($row = $query->fetch())
		{
			echo "<option value=\"" . $row["id"] . "\">" . $row["name"] . "</option>";
		}
		echo "</select>";

		echo 
			"<select name=\"set\" id=\"set\" style=\"width:200px;\">
				<option value=\"\" selected disabled hidden>Select set</option>
			</select>

			<input type=\"submit\" name=\"add_tag\" value=\"Show set\" onclick=\"show_set('".$sort_field."','".$sort_dir."')\"/>";
	?>
</div>

<div id="list_container"></div>
<div id="list_result"></div>