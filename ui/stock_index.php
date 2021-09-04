<div id="menu" style="margin:10 0 20 0;">
    <div style="display:inline;"> Stocks : </div>
    <a class="stockMenuButton" href="./index.php?page=stock_index.php&stock_page=stock_overview.php"><div class="stockMenuButton">Overview</div></a>
    <a class="stockMenuButton" href="./index.php?page=stock_index.php&stock_page=stock_view.php"><div class="stockMenuButton">All</div></a>
    <a class="stockMenuButton" href="./index.php?page=stock_index.php&stock_page=stock_view_set.php"><div class="stockMenuButton">Sets</div></a>
    <a class="stockMenuButton" href="./index.php?page=stock_index.php&stock_page=stock_add_card.php"><div class="stockMenuButton">Add single cards</div></a>
    <a class="stockMenuButton" href="./index.php?page=stock_index.php&stock_page=stock_add_card_list.php"><div class="stockMenuButton">Add card lists</div></a>
</div>
<div id="content">
    <?php
        $page = "stock_overview.php";
        if(isset($_GET["stock_page"]))
        {
            $page = $_GET["stock_page"];
        }
        include("./" . $page);
    ?>
</div>