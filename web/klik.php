<?php
$status = $_GET['status'];
shell_exec('//home/pi/kaku/switch_kaku_php.sh 8 '.$status.'');
?>
