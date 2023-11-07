<?php
require("access2.php");
if(isset($_POST['id'])) {
    $idd = $_POST['id'];
    $queryw = "DELETE FROM `slowka` WHERE `id_slowka`=?";
    $stmt = mysqli_prepare($db, $queryw);
    mysqli_stmt_bind_param($stmt, 'i', $idd);
    mysqli_stmt_execute($stmt);
    mysqli_stmt_close($stmt);
}
header("Location:read2.php");
mysqli_close($db);


?>
