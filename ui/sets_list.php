<script>
	function openTab(evt, cityName) 
	{
		// Declare all variables
		var i, tabcontent, tablinks;

		// Get all elements with class="tabcontent" and hide them
		tabcontent = document.getElementsByClassName("tabcontent");
		for (i = 0; i < tabcontent.length; i++) 
		{
			tabcontent[i].style.display = "none";
		}

		// Get all elements with class="tablinks" and remove the class "active"
		tablinks = document.getElementsByClassName("tablinks");
		for (i = 0; i < tablinks.length; i++) 
		{
			tablinks[i].className = tablinks[i].className.replace(" active", "");
		}

		// Show the current tab, and add an "active" class to the button that opened the tab
		document.getElementById(cityName).style.display = "block";
		//evt.currentTarget.className += " active";
		document.getElementById("tab_button_" + cityName).className += " active";
	}
	
	$( document ).ready(function() 
	{
		$("#tab_button_1").trigger('click');
	});
</script>
<style>
/* Style the tab */
.tab {
  overflow: hidden;
  background-color: #101010;
}

/* Style the buttons that are used to open the tab content */
.tab button {
  background-color: inherit;
  float: left;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  transition: 0.3s;
  color:white;
}

/* Change background color of buttons on hover */
.tab button:hover {
  background-image:linear-gradient(#333333, #111111);
  border-radius:5px;
}

/* Create an active/current tablink class */
.tab button.active {
  background-image:linear-gradient(#222222, #111111);
  border-radius:5px;
}

/* Style the tab content */
.tabcontent {
  display: none;
  padding: 6px 12px;
  animation: fadeEffect 1s; /* Fading effect takes 1 second */
}

/* Go from zero to full opacity */
@keyframes fadeEffect {
  from {opacity: 0;}
  to {opacity: 1;}
}
</style>
<?php
	$game_query = $connection->query("select * from game;");
	
	//Tab Header
	echo "<div class='tab'>";
	$games = $game_query->fetchAll();
	foreach ($games as $game)
	{
		$game_id = $game["id"];
		$game_name = $game["name"];
		echo "<button id='tab_button_" . $game_id . "' class='tablinks' onclick=\"openTab(event, '" . $game_id . "')\">" . $game_name . "</button>";
	}
	echo "</div>";
	
	//Tab content
	foreach ($games as $game)
	{
		$game_id = $game["id"];
		echo "<div id='" . $game_id . "' class='tabcontent'>";
		
		$sql="select sets.name as set_name, sets.id as id from sets where sets.game_id = " . $game_id . " order by release_date desc;";
		$set_query = $connection->query($sql);
		while($row = $set_query->fetch())
		{
			echo "<a class=\"setButton\" href=\"index.php?page=cards_set_list.php&set_id=" . $row["id"] . "\">";
			echo "<div class=\"setButton\">";
			echo $row["set_name"];
			echo "</div>";
			echo "<a/>";
		}
		
		echo "</div>";
	}
	
	$query = null;
	$connection = null;
	
?>
			