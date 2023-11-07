<?php

require_once("access2.php"); 
$id_klasy = $_POST['id'];
$nowa_nazwa = $_POST['name'];

$stmt = $db->prepare("UPDATE klasy SET nazwa_klasy = ? WHERE id_klasy = ?");
$stmt->bind_param("si", $nowa_nazwa, $id_klasy);

if ($stmt->execute()) {
    echo "Class updated successfully";
} else {
    echo "Error updating class: " . $stmt->error;
}

$stmt->close();
$db->close();

?>