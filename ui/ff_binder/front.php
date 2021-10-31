<head>
	<link href="http://cdn.jsdelivr.net/npm/keyrune@latest/css/keyrune.css" rel="stylesheet" type="text/css" />
	<link href="http://cdn.jsdelivr.net/npm/mana-font@latest/css/mana.css" rel="stylesheet" type="text/css" />
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

	<style>
		#wrapper
		{
			width: 200px;
			height: 200px;
		}

		.content
		{
			position: relative;
			z-index: 100;
		}

		.background
		{
			position: absolute;
			top: 0;
			left: 0;
			z-index: -100;
		}
	</style>
</head>
<script>
	$(document).ready(function()
	{
		const queryString = window.location.search;
		const urlParams = new URLSearchParams(queryString);
		const set_lang_id = urlParams.get('set_lang_id');
		console.log(set_lang_id);
        var sql = "select name from sets_langs where id=" + set_lang_id;
		console.log(sql);
		$.get('../php_scripts/execute_sql.php',{'sql':sql},function(return_data)
		{
			var sets = return_data.data;
			setNameElement = document.getElementById("set_name");
			setNameElement.textContent = sets[0].name;
		}, "json");

		frontImgElement = document.getElementById("front_img");
		frontImgElement.src = "./img/front/" + set_lang_id + ".jpg";
	});
</script>
<body style="width:8in;height:11in;border: black;border-width: 10px; /*border-style: solid;*/">

	<div id="wrapper">
		<div class="content" style="width:8in;"> 
			</br></br></br></br></br></br></br></br></br></br></br></br></br>
			<div style="text-align:center; font-size:180; font-family:'Runic MT Condensed'; font-weight:bold;">Final Fantasy</div>
			<div style="text-align:center; font-size:20; font-family:'Runic MT Condensed'; font-weight:bold;">Trading Card Game</div>
			</br></br></br>
			<div id="set_name" style="text-align:center; font-size:120; font-family:'Runic MT Condensed'; font-weight:bold;"></div>
			</br></br></br></br></br></br></br></br></br></br></br></br></br></br>
			
			<!-- Color icon -->
			<div style="text-align:center;">
				<img src="./img/fire.png" width="50px"/>
				<img src="./img/ice.png" width="50"/>
				<img src="./img/wind.png" width="50px"/>
				<img src="./img/earth.png" width="50px"/>
				<img src="./img/lightning.png" width="50px"/>
				<img src="./img/water.png" width="50px"/>
				<img src="./img/light.png" width="50px"/>
				<img src="./img/dark.png" width="50px"/>
			</div>
		</div>
		
		<div class="background" style="opacity:0.2; height:11in">
			<img id="front_img" style="width:8in;">
		</div>
	</div>
	
</body>