<html>
<head>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css">
</head>
<body>
<?php
require("access2.php");
session_start();

$buttonValue = $_POST['button']; 

if (isset($_SESSION['buttonValue'])) {
    $buttonValue = $_SESSION['buttonValue'];
}

$query = "SELECT `id_tematu` FROM `tematy` WHERE `nazwa_tematu`='$buttonValue'";
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

        echo '<tr id="row-' . $id . '">
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
                    <button type="button" name="delete" onclick="deleteRow(' . $id . ')"><i class="fa-solid fa-trash"></i></button>
                </td>
            </form>
        </tr>';
    }

    echo '<tr>';
    echo '<form action="" method="POST">';
    echo '<input type="hidden" name="button" value="' . $buttonValue . '">';
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
 
    if (isset($_POST['add']))
    {
        $query_check = "SELECT COUNT(*) as count FROM slowka WHERE slowko='$slowko' AND tlumaczenie='$tlumaczenie'";
        $result = mysqli_query($db, $query_check);
        $row = mysqli_fetch_assoc($result);
        if($row['count'] == 0 && strlen($slowko)>0 && strlen($tlumaczenie)>0) {
            $query="INSERT INTO `slowka`( `slowko`, `tlumaczenie`, `id_tematu`) VALUES ('$slowko','$tlumaczenie','$id_tematu')";
            mysqli_query($db, $query);
            echo '<script>window.location.reload();</script>';
        }
    } else {
        $same=1;
    }
    if (isset($_POST['delete']))
    {
        $queryw = "DELETE FROM `slowka` WHERE `id_slowka`=?";
        $stmt = mysqli_prepare($db, $queryw);
        mysqli_stmt_bind_param($stmt, 'i', $id_to_delete);
        mysqli_stmt_execute($stmt);
        mysqli_stmt_close($stmt);
    }
?>
<div style="text-align: center;">
    <form action="wybor.php" method="POST">
        <input type="submit" name="powrot" value="Powrót" class="buttony">
    </form>
    
    
</div>
<style>
input[name="powrot"]{
        position:relative;
        left:42%;
        top:6px;
        font-size: 14px;
        padding: 10px 10px 10px 10px;
        display: block;
        width:20%;
        border: none;
        background-color: #343434;
        color: black;
        border-radius: 15px;
        background-color:white;
        }
</style>
<script>
    function deleteRow(id) {
        let xhr = new XMLHttpRequest();
        xhr.open('GET', 'deleteedit.php?delete&id=' + id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function () {
            if (xhr.status === 200) {
                let row = document.getElementById('row-' + id);
                if (row) {
                    row.remove();
                }
            } else {
                console.error('Error:', xhr.statusText);
            }
        };
        xhr.send();
    }

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
</body>
</html>
