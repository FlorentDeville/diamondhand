<html>
	<head>
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
		<script src="tool.js"></script>
		<?php 
			include("./head.html"); 
			include("./connection.php"); 
		?>
	</head>
		<body style="background-color:#000000;color:white;">
			<?php include("./sidenav.html"); ?>
			
			<div id="main">
				<span id="main-menu-button" style="font-size:30px;cursor:pointer;display:none" onclick="openNav()">&#9776;</span>
				
				<?php
					if(isset($_GET["page"]))
					{
						$page = $_GET["page"];
					}
					else
					{
						$page = "stock_index.php";
					}

					include("./" . $page);
				?>
			</div>
		</body>
</html>