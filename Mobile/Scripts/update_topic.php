<?php
require_once("access2.php");

if (isset($_POST['id']) && isset($_POST['name'])) {
    $topicId = $_POST['id'];
    $topicName = $_POST['name'];

    $sql = "UPDATE `tematy` SET `nazwa_tematu`='$topicName' WHERE `id_tematu`='$topicId';";
    $result = $db->query($sql);

    if ($result) {
        echo "Topic updated successfully";
    } else {
        echo "Error updating topic";
    }

    $db->close();
} else {
    echo "Invalid request";
}
?>
