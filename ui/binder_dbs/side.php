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
			font-family:'Saiyan Sans';
			/*font-weight:bold; */
			color:black;
			font-size:50px;
			/*letter-spacing:15; */
			text-align: center;
			margin-left: 20px;
		}
	</style>

</head>
<?php
include("../connection.php"); 

function show_side($set_name)
{
	//show left side
	echo "
	<div style='width:11in;height:1.2in;border: black;border-width:1px; border-style: solid;'>
		<div style='width:100%; height:100%; background-color: white; position: relative;'>
			<!-- Left side set icon -->
			<div style='height:1.2in; width:320px; position:absolute; align-items:center; justify-content:center; /*border-style:solid;border-size:1px*/'>
				<span class='iconHelper'></span>
				<img src='./img/1_star.png' class='icon' style=\"margin-left:20px\"/>
				<img src='./img/2_star.png' class='icon'/>
				<img src='./img/3_star.png' class='icon'/>
				<img src='./img/4_star.png' class='icon'/>
				<img src='./img/5_star.png' class='icon'/>
				<img src='./img/6_star.png' class='icon'/>
				<img src='./img/7_star.png' class='icon'/>
			</div>";
			
			$length = strlen($set_name);
			$DEFAULT_LETTER_SPACING = 5;
			$letter_spacing = $DEFAULT_LETTER_SPACING;

			//Game Name
			echo "<div id='gameName' class='gameName' style='letter-spacing:" . $DEFAULT_LETTER_SPACING . "px;'>Dragon Ball Super</div>";
		
			//set name
			echo "<div class='gamename' style='letter-spacing:" . $letter_spacing . "px;'>" . $set_name . "</div>";
			
			//right side
			echo "
			<!-- Right side set icon -->
			<div style='height:1.2in; width:320px; position:absolute; right:0; top:0; align-items:center; justify-content:center; padding:0 0 0 0;/*border-style:solid;border-size:1px*/'>
				<span class='iconHelper' style='margin-right:5px;'></span>
				<img src='./img/7_star.png' class='icon' style=\"margin-left:15px\"/>
				<img src='./img/6_star.png' class='icon'/>		
				<img src='./img/5_star.png' class='icon'/>
				<img src='./img/4_star.png' class='icon'/>
				<img src='./img/3_star.png' class='icon'/>
				<img src='./img/2_star.png' class='icon'/>
				<img src='./img/1_star.png' class='icon'/>
				
			</div>
		</div>
	</div>";
}

$set_lang_id = $_GET["set_lang_id"];
$sql = "select sets_langs.name from sets_langs where id=" . $set_lang_id;
$result = $connection->query($sql);

$row = $result->fetch();
show_side($row["name"]);

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