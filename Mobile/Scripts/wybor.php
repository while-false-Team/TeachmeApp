<?php
session_start();
if (isset($_POST['wyloguj'])) {
    session_destroy();
    header("Location: login.php");
    exit();
}

$id_ucznia = $_SESSION['id_ucznia'] ? $_SESSION['id_ucznia'] : 0;
$id_nauczyciela = $_SESSION['id_nauczyciela'] ? $_SESSION['id_nauczyciela'] : 0;

$_SESSION['id_uczniaa']=$id_ucznia;
$_SESSION['id_nauczycielaa']=$id_nauczyciela;



require_once("access2.php");



$query = "SELECT `id_klasy` FROM `uczniowie` WHERE `id_ucznia`= ? " ;
$stmt = $db->prepare($query);
$stmt->bind_param("i", $id_ucznia);
$stmt->execute();
$stmt->bind_result($id_klasy);
$stmt->fetch(); // $id_klasy
$stmt->close();
$_SESSION['id_klasy']=$id_klasy;

$query2 = "SELECT `id_klasy` FROM `klasy` WHERE `id_nauczyciela`=? " ;
$stmt2 = $db->prepare($query2);
$stmt2->bind_param("i", $id_nauczyciela);
$stmt2->execute();
$stmt2->bind_result($id_klasy_nauczyciela);
$stmt2->fetch(); 
$stmt2->close();



$buttons = [];

$sql = "SELECT `id_tematu`, `nazwa_tematu` FROM `tematy` WHERE `id_klasy` IS NULL and `id_ucznia` IS NULL;";


if (isset($_POST['prywatne'])) {
    $sql = "SELECT `id_tematu`,nazwa_tematu FROM tematy WHERE id_klasy IS NULL and id_ucznia=$id_ucznia";
}
else if ($id_ucznia >0 and (isset($_POST['klasy']) && ($id_klasy>0)))
{
     $sql = "SELECT `id_tematu`,nazwa_tematu FROM tematy WHERE id_klasy=$id_klasy";
}
else if ($id_ucznia >0 and (isset($_POST['klasy']) && ($id_klasy<=0)))
{
    $sql = "SELECT `id_tematu`, `nazwa_tematu` FROM `tematy` WHERE `id_klasy` IS NOT NULL and `id_ucznia` IS NOT NULL;";
}
else if ($id_nauczyciela >0 and (isset($_POST['klasy'])))
{
     $sql = "SELECT `id_tematu`,nazwa_tematu FROM tematy WHERE id_ucznia=$id_nauczyciela";
}

$result = $db->query($sql);
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $buttons[] = ['id' => $row['id_tematu'], 'name' => $row['nazwa_tematu']];
    }
} else if (isset($_POST['prywatne'])) {
    $no_topics_message = "Nie masz jeszcze żadnych tematów";
}else if(isset($_POST['klasy']) && ($id_klasy_nauczyciela <=0))
{
    $no_topics_message = "Nie masz jeszcze żadnych tematów klas";
}
else if(isset($_POST['klasy']) && ($id_klasy_nauczyciela >0))
{
     $no_topics_message = " ";
}
if ($id_nauczyciela>0 and (isset($_POST['klasy'])))
{
        $sql = "SELECT `id_klasy`,`nazwa_klasy`,`kod_klasy` FROM `klasy` WHERE `id_nauczyciela`=$id_nauczyciela";
        $result = $db->query($sql);
        if ($result->num_rows > 0) {
            echo "<table border='2'>";
            echo "<tr>";
            echo "<th>Nazwa</th>";
            echo "<th>Kod</th>";
            echo "<th>Dodaj temat</th>";
            echo "<th>Postępy </th>";
            echo "<th>Zobacz tematy</th>";
            echo "<th>Usuń</th>";
            echo "</tr>";

        while($row = $result->fetch_assoc())
        {
            $nazwaklasy=$row["nazwa_klasy"];
            $id_klasy=$row["id_klasy"];
            echo "<tr>";
            echo "<td>";
          echo '<form action="update_class.php" method="post">';
echo "<input type='hidden' name='id_klasy' value='$id_klasy'>";
echo '<input type="hidden" name="class_id" value="' . $row['id_klasy'] . '">';
echo "<input type='text' name='nowa_nazwa' value='$nazwaklasy'  style='width: 96%;' data-class-id='$id_klasy'>";
echo "</form>";
            echo "</td>";
            echo "<td>";
            echo $row["kod_klasy"];
            echo "</td>";
           echo "<td>";
        echo '<form action="nowytemat2.php" method="POST">';
        echo '<input type="hidden" name="id_klasy" value="' . $row["id_klasy"] . '">';
        echo "<button type='submit' class='update-button2' name='button'><i class='fa-solid fa-plus'></i></button>";
        echo '</form>';
        echo "</td>";
           echo "<td>";
           echo '<form action="postępy.php" method="POST">';
           echo '<input type="hidden" name="id_klasy" value="' . $row["id_klasy"] . '">';
        echo "<button type='submit' class='update-button2' name='button'><i class='fa-solid fa-list-check'></i></button>";
        echo '</form>';
        echo "</td>";
           echo "<td>";
           echo '<form action="przejrzyj.php" method="POST">';
        echo '<input type="hidden" name="id_klasy" value="'.$row["id_klasy"].'">';
        echo "<button type='submit' class='update-button2' name='button'><i class='fa-solid fa-eye'></i></button>";
        echo '</form>';
        echo "</td>";
        echo "<td>";
        echo '<form action="delete_class.php" method="post">';
                    echo '<input type="hidden" name="id_klasy" value="' . $row["id_klasy"] . '">';
                    echo '<button type="submit"  class="update-button2" name="delete"><i class="fa-solid fa-trash"></i></button>';
                    echo "</form>";
        echo "</td>";
        echo "</tr>";
        }
      
}
}
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <title>Strona do nauki angielskiego</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css">
   
</head>
<body>
    <div id="buttony">
        <p>Tematy</p>
        <form action="wybor.php" method="POST">
            <button type="submit" class="buttony" name="ogolne" value="ogolne">Tematy ogólne</button>
            <button type="submit" class="buttony" name="prywatne" value="prywatne">Tematy prywatne</button>
            <button type="submit" class="buttony" name="klasy" value="klasy">Tematy klasy</button>
        </form>
    </div>
    <?php if(isset($no_topics_message)) { ?>
        <h2><?php echo $no_topics_message; ?></h2>
    <?php } else {
        ?>
    <form action='temat.php' method='post'>
        <table border="2">
            <tr>
                <th>Nazwa</th>
                <th>Nauka</th>
                <th>Test</th>
                <th>Edytuj</th>
                <th>Usuń</th>
            </tr>
            <?php
                 
            foreach ($buttons as $button) {
                echo "<tr>";
                echo "<td>";
                if (isset($_POST['prywatne'])){
                  echo "<input type='text' name='topic_name' value='{$button['name']}' data-topic-id='{$button['id']}' style='width: 96%;'>";
                }
                else{
                     echo $button['name'];
                }
                echo "</td>";
                echo "<td>";
                echo "<button type='submit' class='update-button' name='button' value='{$button['name']}' data-topic-id='{$button['id']}'><i class='fa-solid fa-graduation-cap'></i></button>";
                echo "</form>";
                echo "</td>";
                echo "<td>";
                echo "<form action='test.php' method='post'>";
                echo "<button type='submit' class='update-button2' name='button' value='{$button['name']}' data-topic-id='{$button['id']}'><i class='fa-solid fa-graduation-cap'></i></button>";
                echo "</form>";
                echo "</td>";
                echo "<td>";
                if (isset($_POST['prywatne'])){
                    echo "<form action='edit.php' method='post'>";
                    echo "<button type='submit' class='update-button2' name='button' value='{$button['name']}' data-topic-id='{$button['id']}'><i class='fa-solid fa-pen'></button>";
                     echo "</form>";
                    echo "</td>";
                    echo "<td>";
                    echo '<form action="delete_topic.php" method="post">';
                    echo '<input type="hidden" name="topic_id" value="' . $button['id'] . '">';
                    echo '<button type="submit" class="update-button2" name="delete"><i class="fa-solid fa-trash"></i></button>';
                    echo "</form>";
                }
                else if (isset($_POST['klasy'])){
                         echo "<form action='edit.php' method='post'>";
                    echo "<button type='submit' class='update-button2' name='button' value='{$button['name']}' data-topic-id='{$button['id']}' disabled ><i class='fa-solid fa-pen'></button>";
                     echo "</form>";
                    echo "</td>";
                    echo "<td>";
                    echo '<form action="delete_topic.php" method="post">';
                    echo '<input type="hidden" name="topic_id" value="' . $button['id'] . '">';
                    echo '<button type="submit" name="delete" class="update-button2" disabled ><i class="fa-solid fa-trash"></i></button>';
                    echo "</form>";
                }
                else{
                    echo "<button type='submit' class='update-button' name='button' value='{$button['name']}' data-topic-id='{$button['id']}' disabled><i class='fa-solid fa-pen'></button>";
                    echo "</td>";
                    echo "<td>";
                    echo '<button type="submit" name="delete" disabled><i class="fa-solid fa-trash"></i></button>';
                }
                echo "</td>";
                echo "</tr>";
            }
    }
        
            ?>
        </table>
        
    </form>
 <?php if(isset($_POST['prywatne']) && $_SESSION['id_ucznia']>0)
 {
     ?>
       <div style="text-align: center;">
        <form action="nowytemat.php" method="POST">
            <input type="submit" class="button4" value="Dodaj Temat">
        </form>
            <?Php
 }
 else if(isset($_POST['klasy']) && $_SESSION['id_nauczyciela']>0)
 {
     ?>
     <form action="klasa.php" method="POST">
            <input type="submit" class="button4" value="Dodaj klase">
        </form>
    </div>
            <?Php
 }
 else  if(isset($_POST['klasy']) && $_SESSION['id_ucznia']>0 && $id_klasy<=0 )
  {
     ?>
       <div style="text-align: center;">
        <form action="dolacz.php" method="POST">
            <input type="submit" class="button4" value="Dołącz do klasy">
        </form>
            <?Php
 }
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
    
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('input[name="nowa_nazwa"]').forEach(input => {
        input.addEventListener('blur', function() {
            const className = this.value;
            const classId = this.parentElement.querySelector('input[name="class_id"]').value;
            const xhr = new XMLHttpRequest();
            xhr.open('POST', 'update_class.php', true);
            xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            xhr.onload = function () {
                if (xhr.status >= 200 && xhr.status < 400) {
                    console.log('Klasa zaktualizowana');
                } else {
                    console.error('Blad');
                }
            };
            xhr.send(`id=${classId}&name=${className}`);
        });
    });
});
</script>
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
            height:100%;
        }
        button.update-button2,input[name="nowa_nazwa"] {
            position:relative;
            top:7px;
            width: 100%;
            height:100%;
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
</body>
</html>
