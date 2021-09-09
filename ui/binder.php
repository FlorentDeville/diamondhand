<div id="menu" style="margin:10 0 20 0;">
    <div style="display:inline;"> Stocks : </div>
    <a class="stockMenuButton" href="./index.php?page=binder.php&stock_page=pokemon_binder/side.html"><div class="stockMenuButton">Pokemon</div></a>
    <a class="stockMenuButton" href="./index.php?page=binder.php&stock_page=stock_view.php"><div class="stockMenuButton">MTG</div></a>
    <a class="stockMenuButton" href="./index.php?page=binder.php&stock_page=stock_view_set.php"><div class="stockMenuButton">Final Fantasy</div></a>
</div>
<div id="content">
    <?php
        if(isset($_GET["stock_page"]))
        {
            $page = $_GET["stock_page"];
            include("./" . $page);
        }
        
    ?>
</div>