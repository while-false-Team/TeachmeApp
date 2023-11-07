<?php
session_start();
if(isset($_POST['delete'])) {
    require_once("access2.php");
    $topic_id = $_POST['topic_id'];
    $stmt = $db->prepare("DELETE FROM `tematy` WHERE `id_tematu` = ?");
    $stmt->bind_param("i", $topic_id);
    $stmt->execute();
    $stmt = $db->prepare("DELETE FROM `slowka` WHERE `id_tematu`= ?");
    $stmt->bind_param("i", $topic_id);
    $stmt->execute();

    $stmt->close();
    $db->close();
    header("Location:wybor.php");
    exit();
}
?>
