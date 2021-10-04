<html>

<head>
	<style>
		.icon
		{
			width:35px;
			vertical-align: middle;
		}

		.iconHelper
		{
			display:inline-block; 
			height:100%; 
			vertical-align:middle;
		}

		.gameName
		{
			font-family:'Runic MT Condensed';
			font-weight:bold; 
			color:black;
			font-size:50px;
			/*letter-spacing:15; */
			text-align: center;
			margin-left: 20px;
		}
	</style>

</head>
<?php

function show_side($set_name)
{
	//show left side
	echo "
	<div style='width:11in;height:1.2in;border: black;border-width:1px; border-style: solid;'>
		<div style='width:100%; height:100%; background-color: white; position: relative;'>
			<!-- Left side set icon -->
			<div style='height:1.2in; width:320px; position:absolute; align-items:center; justify-content:center; /*border-style:solid;border-size:1px*/'>
				<span class='iconHelper'></span>
				<img src='ff_binder/img/fire.png' class='icon'/>
				<img src='ff_binder/img/ice.png' class='icon'/>
				<img src='ff_binder/img/wind.png' class='icon'/>
				<img src='ff_binder/img/earth.png' class='icon'/>
				<img src='ff_binder/img/lightning.png' class='icon'/>
				<img src='ff_binder/img/water.png' class='icon'/>
				<img src='ff_binder/img/light.png' class='icon'/>
				<img src='ff_binder/img/dark.png' class='icon'/>
			</div>";
			
			$length = strlen($set_name);
			$DEFAULT_LETTER_SPACING = 15;
			$letter_spacing = $DEFAULT_LETTER_SPACING;
			if ($length > 10)
				$letter_spacing = 5;

			//Game Name
			echo "<div id='gameName' class='gameName' style='letter-spacing:" . $DEFAULT_LETTER_SPACING . "px;'>Final Fantasy</div>";
		
			//set name
			echo "<div class='gamename' style='letter-spacing:" . $letter_spacing . "px;'>" . $set_name . "</div>";
			
			//right side
			echo "
			<!-- Right side set icon -->
			<div style='height:1.2in; width:320px; position:absolute; right:0; top:0; align-items:center; justify-content:center; padding:0 0 0 0;/*border-style:solid;border-size:1px*/'>
				<span class='iconHelper' style='margin-right:5px;'></span>
				<img src='ff_binder/img/dark.png' class='icon'/>
				<img src='ff_binder/img/light.png' class='icon'/>		
				<img src='ff_binder/img/water.png' class='icon'/>
				<img src='ff_binder/img/lightning.png' class='icon'/>
				<img src='ff_binder/img/earth.png' class='icon'/>
				<img src='ff_binder/img/wind.png' class='icon'/>
				<img src='ff_binder/img/ice.png' class='icon'/>
				<img src='ff_binder/img/fire.png' class='icon'/>
				
			</div>
		</div>
	</div>";
}

$sql = "select sets.name from sets inner join game on sets.game_id = game.id where game.name = \"Final Fantasy\" order by release_date asc;";
$result = $connection->query($sql);

while($row = $result->fetch())
{
	show_side($row["name"]);
}
?>
<script>
function init()
{

		sizeStyle = "font-size:50px;letter-spacing:15;";
		textStyle = "font-family:'Runic MT Condensed';font-weight:bold; color:black;"

		nameElement = document.getElementById("setName");
		
		gameNameElement = document.getElementById("gameName");
}

init();
</script>
</html>