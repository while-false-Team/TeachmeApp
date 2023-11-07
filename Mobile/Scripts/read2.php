<?php
session_start(); 
$nazwa = $_SESSION['nazwa'];
echo $nazwa;
?>
<html>
    <head>
        <link rel="stylesheet" href="style.css">
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css">
    </head>
</html>
<?php
require("access2.php");
$query = "SELECT `id_tematu` FROM `tematy` WHERE `nazwa_tematu`='$nazwa'";
$result = $db->query($query);

if ($result) {
    $row = $result->fetch_assoc();
    $id_tematu = $row['id_tematu'];
}
$query = "SELECT * FROM `slowka` WHERE `id_tematu`='$id_tematu';";
$res = mysqli_query($db, $query);
?>
<table border="2">
    <tr>
        <td>Slowko</td>
        <td>Tlumaczenie</td>
        <td>Usuń</td>
    </tr>
    <?php
while ($row = mysqli_fetch_array($res)) {
    $id = trim($row['id_slowka']);
    $word = htmlspecialchars(trim($row['slowko']));
    $translation = htmlspecialchars(trim($row['tlumaczenie']));

    echo '<tr>
        <form action="" method="POST">
            <td class="word-container">
                <input type="hidden" name="id" value="' . $id . '">
                <input type="text" name="word" maxlength="20" value="' . ucfirst($word) . '" onblur="updateField(' . $id . ', \'slowko\', this.value)">
            </td>
            <td class="translation-container">
                <input type="hidden" name="id" value="' . $id . '">
                <input type="text" name="translation" value="' . ucfirst($translation) . '" onblur="updateField(' . $id . ', \'tlumaczenie\', this.value)">
            </td>
          <td class="icon-container">
    </form>
   <form action="delete.php" method="POST">
    <input type="hidden" name="id" value="' . $id . '">
    <button type="submit" name="delete"><i class="fa-solid fa-trash"></i></button>
</form>
</td>
      </tr>';
}

echo '<tr>';
echo '<form action="insert.php" method="POST">';
echo '<input type="hidden" name="id_tematu" value="' . $id_tematu . '">';
echo '<td><input type="text" name="slowko" placeholder="Wpisz słowo" value=""></td>';
echo '<td><input type="text" name="tlumaczenie" placeholder="Wpisz tłumaczenie "value=""></td>';
echo '<td><button type="submit" name="add"><i class="fa-solid fa-circle-plus"></i></button></td>';
echo '</form>';
echo '</tr>';
echo '</table>';
$slowko=$_POST['slowko'];
$tlumaczenie=$_POST['tlumaczenie']; 
if (empty($slowko) || empty($tlumaczenie)) {
    echo "<div class='same'>Aby dodać słowo uzupełnij powyższe pola</div>";
} else {
    echo "<div class='same'></div>";
}

?>
<form action="wybor.php" method="POST">
    <input type="submit" class="button4" value="Przejdź dalej">
</form>

<script>
    function updateField(id, fieldName, value) {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'update.php', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(`id=${id}&field=${fieldName}&value=${encodeURIComponent(value)}`);
}
    setTimeout(function() {
        document.getElementsByClassName('same')[0].style.display = 'none';
    }, 4000);
</script>
<?php
mysqli_close($db);
?>
<style>
    button[name='delete']{
    height:100%;
width:100%;
position:relative;
top:7px;
}
</style>
</body>
</html>

