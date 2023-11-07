<?php
require("access2.php");
$id = mysqli_real_escape_string($db, $_POST['id']); 
$field = mysqli_real_escape_string($db, $_POST['field']); 
$value = mysqli_real_escape_string($db, $_POST['value']); 
$query = "UPDATE slowka SET $field='$value' WHERE id_slowka='$id'"; 
mysqli_query($db, $query);
mysqli_close($db);
?>
