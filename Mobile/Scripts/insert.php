<?php
require("access2.php");
$id_tematu = $_POST['id_tematu'];
$slowko=$_POST['slowko'];
$tlumaczenie=$_POST['tlumaczenie']; 
$query_check = "SELECT COUNT(*) as count FROM slowka WHERE slowko='$slowko' AND tlumaczenie='$tlumaczenie'";
$result = mysqli_query($db, $query_check);
$row = mysqli_fetch_assoc($result);
if($row['count'] == 0 && strlen($slowko)>0 && strlen($tlumaczenie)>0) {
    $query="INSERT INTO `slowka`( `slowko`, `tlumaczenie`, `id_tematu`) VALUES ('$slowko','$tlumaczenie','$id_tematu')";
    mysqli_query($db, $query);
    
}else
{
    $same=1;
}
header("Location:read2.php");
?>