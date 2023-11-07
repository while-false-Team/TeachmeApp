<?php
require_once("access2.php");
session_start();
$query = "SELECT `id_klasy` FROM `klasy` WHERE `id_nauczyciela` = ?";
$id_nauczyciela = $_SESSION['id_nauczyciela']; 
$stmt = $db->prepare($query);
$stmt->bind_param("i", $id_nauczyciela);
$stmt->execute();
$stmt->bind_result($id_klasy);
$stmt->fetch();
$stmt->close();
$_SESSION['id_klasy'] = $id_klasy;
header("Location:nowytemat2.php");
?>
