function openNav() 
{
	document.getElementById("mySidenav").style.width = "200px";
	document.getElementById("main").style.marginLeft = "200px";
	document.getElementById("main-menu-button").style.display = "none";
}

function closeNav() 
{
	document.getElementById("mySidenav").style.width = "0";
	document.getElementById("main").style.marginLeft= "0";
	document.getElementById("main-menu-button").style.display = "block";
}