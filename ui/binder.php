<!-- <div id="menu" style="margin:10 0 20 0;">
    <div style="display:inline;"> Stocks : </div>
    <a class="stockMenuButton" href="./index.php?page=binder.php&stock_page=pokemon_binder/side.html"><div class="stockMenuButton">Pokemon</div></a>
    <a class="stockMenuButton" href="./index.php?page=binder.php&stock_page=stock_view.php"><div class="stockMenuButton">MTG</div></a>
    <a class="stockMenuButton" href="./index.php?page=binder.php&stock_page=ff_binder/side.php"><div class="stockMenuButton">Final Fantasy</div></a>
</div> -->
<div id="content">
    <?php
        $sql = "select sets_langs.name as set_name, sets_langs.id as set_lang_id, game.id as game_id from sets_langs
        inner join sets on sets_langs.set_id = sets.id
        inner join game on sets.game_id = game.id;";
        $result = $connection->query($sql);

        while($row = $result->fetch())
        {
            $MTG = 1;
            $POK = 2;
            $FF = 3;

            $link_side = "";
            $link_front = "";
            switch($row["game_id"])
            {
                case $FF:
                    $link_side = "./ff_binder/side.php?set_lang_id=" . $row["set_lang_id"];
                    $link_front = "./ff_binder/front.php?set_lang_id=" . $row["set_lang_id"];
                    break;

                default:
                break;
            }

            echo "<span>" . $row["set_name"] . "</span>&nbsp;<a target=\"_blank\" href=\"" . $link_side . "\">side</a>&nbsp; <a target=\"_blank\" href=\"" . $link_front . "\">front</a><br/>";
        }
    ?>
</div>