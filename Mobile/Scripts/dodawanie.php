<?php
session_start();
require("access2.php");
$klasy=$_SESSION['id_klasy'];
$id_ucznia=$_SESSION['id_uczniaa'];
$query="UPDATE `uczniowie` SET `id_klasy`='$klasy' WHERE `id_ucznia`= '$id_ucznia'";
mysqli_query($db, $query);
header("Location:wybor.php")

?>
