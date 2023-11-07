<?php
session_start();
require_once("access2.php");

if(isset($_POST['poziom'])) {
    $poziom = $_POST['poziom'];


    $query = "INSERT INTO `dane_tematow`(`poziom_przyswojenia`) VALUES (?)";
    $preparedst = $db->prepare($query);
    $preparedst->bind_param("s", $poziom);
    $preparedst->execute();
    $preparedst->close();
}

$db->close();
?>
