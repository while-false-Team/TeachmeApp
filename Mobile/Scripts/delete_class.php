<?php
require_once("access2.php");
session_start();

if(isset($_POST['delete'])) {
    $id_klasy = $_POST['id_klasy'];
    $stmt = $db->prepare("DELETE FROM slowka WHERE slowka.id_tematu IN (SELECT id_tematu FROM tematy WHERE id_klasy=?)
    ");
    $stmt->bind_param("i", $id_klasy);
    $stmt->execute();
    $stmt2 = $db->prepare("DELETE FROM `tematy` WHERE `id_klasy`= ?");
    $stmt2->bind_param("i", $id_klasy);
    $stmt2->execute();
    
    $stmt4 = $db->prepare("UPDATE `uczniowie` SET `id_klasy`=NULL WHERE `id_klasy`= ?");
    $stmt4->bind_param("i", $id_klasy);
    $stmt4->execute();
    $stmt3 = $db->prepare("DELETE FROM `klasy` WHERE `id_klasy`= ?;");
    $stmt3->bind_param("i", $id_klasy);
    $stmt3->execute();
   
    $stmt->close();
    $stmt2->close();
    $stmt3->close();
    $stmt4->close();
    $db->close();
    
    header("Location:wybor.php");
    exit();
}
