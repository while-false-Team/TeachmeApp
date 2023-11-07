<div style="text-align: center;color:white">
    <h1>Wyniki testów</h1>
</div>
<?php
session_start();
require("access2.php");
$id_klasy = $_POST['id_klasy'];
$sql = "SELECT uczniowie.login, tematy.nazwa_tematu, dane_tematow.ile_ukonczen, dane_tematow.data_ostatniego_uruchomienia, dane_tematow.poziom_przyswojenia FROM dane_tematow INNER JOIN uczniowie ON dane_tematow.id_ucznia=uczniowie.id_ucznia INNER JOIN tematy ON dane_tematow.id_tematu=tematy.id_tematu WHERE tematy.id_klasy= $id_klasy;";
        $result = $db->query($sql);
        if ($result->num_rows > 0) {
            echo "<table border='2'>";
            echo "<tr>";
            echo "<th>Login</th>";
            echo "<th>Nazwa </th>";
            echo "<th>Ukończenia</th>";
            echo "<th>Data </th>";
            echo "<th>Poziom</th>";
            echo "</tr>";

        while($row = $result->fetch_assoc())
        {
            echo "<tr>";
            echo "<td>";
            echo $row["login"];
            echo "</td>";
            echo "<td>";
            echo $row["nazwa_tematu"];
            echo "</td>";
            echo "<td>";
            echo $row["ile_ukonczen"];
            echo "</td>";
             echo "<td>";
            echo $row["data_ostatniego_uruchomienia"];
            echo "</td>";
             echo "<td>";
            echo $row["poziom_przyswojenia"];
            echo "</td>";
            echo "</tr>";
            echo "</table>";
        }
      
}

else{
    echo '<div style="text-align: center;color:white;font-size:20px">';
    echo "<h2>Brak danych</h2>";
    echo "</div>";
}
echo '<div style="text-align: center;color:white;font-size:20px">';
?>
<html>
    <head>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <br>
          <form action="wybor.php">
             
    <input type="submit" class="button4" name="Powrót" value="Powrót">
</form>
    </body>
</html>
