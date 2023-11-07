<?php
session_start();
require_once("access2.php");
$id_klasy = $_POST['id_klasy'];
$message="";

$sql = "SELECT `id_tematu`,`nazwa_tematu` FROM `tematy` WHERE `id_klasy` = $id_klasy";
$buttons = [];
$result = $db->query($sql);
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $buttons[] = ['id' => $row['id_tematu'], 'name' => $row['nazwa_tematu']];
    }
}
else{
    $message = "Nie masz jeszcze żadnych tematów";
}
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <title>Strona do nauki angielskiego</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css">
    <style>
        b{
            color:black;
        }
        .buttonwybor{
            width:100%;
            color:black;
            padding: 10px 30px;
            transition: 0.5s;
            border: none;
            border-radius: 25px;
            overflow: hidden;
            font-size:150%;
        }
        p{
            color:white;
            font-size:250%;
        }
        .buttony {
            background-color: grey;
            font-size: 14px;
            color: white;
            border: 1px solid grey; 
        }

        .buttony:hover {
            color: blue;
        }

        #buttony {
            text-align: center;
        }
        table {
            width: 100%; 
            border-collapse: collapse; 
            color:white;
            background-color:rgb(12,12,12);
        }
        th{
            text-align:left;
        }
        button.update-button {
            width: 100%;
            height: 100%;
        }
        h2{
            text-align:center;
            color:white;
             font-size:250%;
        }
            input[name="wyloguj"]{
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
</head>
<body>
    <div id="buttony">
        <p>Tematy</p>
    </div>
    <br>
     <form action='temat.php' method='post'>
        <table border="2">
            <tr>
                <th>Nazwa</th>
                <th>Edytuj</th>
                <th>Usuń</th>
            </tr>
            <?php
            foreach ($buttons as $button){
                echo "<tr>";
                echo "<td>";
                echo "<input type='text' name='topic_name' value='{$button['name']}' data-topic-id='{$button['id']}' style='width: 96%;'>";
                echo "</td>";
                echo "<td>";
                echo "</form>";
                echo "<form action='edit.php' method='post'>";
                echo "<button type='submit' class='update-button' name='button' value='{$button['name']}' data-topic-id='{$button['id']}'><i class='fa-solid fa-pen'></button>";
                echo "</form>";
                echo "</td>";
                echo "<td>";
                echo '<form action="delete_topic.php" method="post">';
                echo '<input type="hidden" name="topic_id" value="' . $button['id'] . '">';
                echo '<button type="submit" name="delete"><i class="fa-solid fa-trash"></i></button>';
                echo "</form>";
                echo "</td>";
                echo "</tr>";
            }
            ?>
        </table>
        
    </form>
    <?php
        echo "<div style='text-align:center'><h2>$message</h2></div> ";
    ?>
      <form action="wybor.php" method="POST">
        <input type="submit" name="powrot" value="Powrót" class="buttony">
    </form>
 ?>
<div style="float:left;position: fixed; bottom: 5px">
<form action="tlumaczenie.php" method="POST">
<input type="submit" name="losowe" class="button4" value="Losowe słowo" class="buttony">
</form>
</div>
<div style="text-align: center; position: fixed; bottom: 40px; width: 100%;">
    <form action="" method="POST">
<input type="submit" name="wyloguj" value="Wyloguj" class="buttony" style="margin: 0;">
</form>
</div>
    <script>
        document.querySelectorAll('.buttony').forEach(button => {
            button.addEventListener('click', () => {
                document.querySelector('form').submit();
            });
        });
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('input[name="topic_name"]').forEach(input => {
            input.addEventListener('blur', function() {
                const topicId = this.getAttribute('data-topic-id');
                const topicName = this.value;

                const xhr = new XMLHttpRequest();
                xhr.open('POST', 'update_topic.php', true);
                xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
                xhr.onload = function () {
                    if (xhr.status >= 200 && xhr.status < 400) {
                        console.log('Zmienione');
                    } else {
                        console.error('Blad');
                    }
                };
                xhr.send(`id=${topicId}&name=${topicName}`);
            });
        });
    });
</script>
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
</body>
</html>