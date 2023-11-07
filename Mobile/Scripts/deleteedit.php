<?php
require("access2.php");

if(isset($_GET['id'])) {
    $id_to_delete = $_GET['id']; 
    $queryw = "DELETE FROM `slowka` WHERE `id_slowka`=?";
    $stmt = mysqli_prepare($db, $queryw);
    mysqli_stmt_bind_param($stmt, 'i', $id_to_delete);
    mysqli_stmt_execute($stmt);
    mysqli_stmt_close($stmt);
}

mysqli_close($db);
?>
