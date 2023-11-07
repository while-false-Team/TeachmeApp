<?php
require_once("access2.php");
$id_ucznia = $_POST['id_ucznia'];
$id_tematu = $_POST['id_tematu'];
$queryd = "SELECT `id_ucznia` FROM `dane_tematow` WHERE `id_ucznia`=? and `id_tematu`=?";
$stmt2 = $db->prepare($queryd);
$stmt2->bind_param("ii", $id_ucznia,$id_tematu);
$stmt2->execute();
$result2 = $stmt2->get_result();

while ($row = $result2->fetch_assoc()) {
  $jest=$row['id_ucznia'];
}
if(isset($_POST['poziom']) && $jest >0) {
    $poziom = $_POST['poziom'];
    $query = "UPDATE `dane_tematow` SET `ile_ukonczen`=`ile_ukonczen`+1,`data_ostatniego_uruchomienia`=NOW(),`poziom_przyswojenia`= ? WHERE `id_ucznia`=?";
    $stmt = $db->prepare($query);
    $stmt->bind_param("si",$poziom,$id_ucznia);
    $stmt->execute();
 
}else{
    $poziom = $_POST['poziom'];
    $query = "INSERT INTO dane_tematow (id_tematu, id_ucznia, ile_ukonczen, data_ostatniego_uruchomienia, poziom_przyswojenia) VALUES (?, ?, ?, NOW(), ?)";
    $stmt = $db->prepare($query);
    $ile_ukonczen = 1;
    $stmt->bind_param("iiis", $id_tematu, $id_ucznia, $ile_ukonczen, $poziom);
    $stmt->execute();
}

$stmt->close();
$stmt2->close();
$db->close();

?>