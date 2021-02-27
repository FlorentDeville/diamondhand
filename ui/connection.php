<?php
	$servername = "localhost";
	$username = "root";
	$password = "";
	$db = "wallstreet";


	$connection = new PDO("mysql:host=$servername;dbname=$db;charset=utf8", $username, $password);
	// set the PDO error mode to exception
	$connection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
?>