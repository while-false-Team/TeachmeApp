<?php

session_start(); 
require("access2.php");
if(isset($_POST['button15']) && strlen($_POST['twoje']) > 0)
{
    $nazwa = $_POST['twoje']; 
    $id_ucznia=$_SESSION['id_uczniaa'];
    $queryd = "INSERT INTO `tematy`( `nazwa_tematu`, `id_ucznia`) VALUES ('$nazwa','$id_ucznia');";
    $preparedst2 = $db->prepare($queryd);
    $preparedst2->execute();
    $_SESSION['nazwa'] = $nazwa; 
    header('Location: read2.php'); 
    exit(); 
}
?>
<html>
<head>
    <meta charset="UTF-8"/>
</head>
<body>
    <style>
                
        input {
  font-size: 20px;
  padding: 10px 10px 10px 5px;
  display: block;
  width:250px;
  border: none;
  border-bottom: 1px solid #757575;
  background-color: #343434;
  color: white;
  border-radius: 15px;
  
}
         .button15 {
    position: relative;
    left:20%;
    display: inline-block;
    padding: 10px 30px;
    background-color: rgba(37, 35, 35, 1);
    text-decoration: none;
    transition: 0.5s;
    border: none;
    border-radius: 25px;
     color:white;
    overflow: hidden;
}
 body{
           
            background-image: url('New_Project.png');
        }
.input6{
    
    position:relative;
    top:40%;
}
    </style>
    <div class="boxy"></div>
    <div class="input6">
        <form action="nowytemat.php" method="POST"> 
            <input type="text" name="twoje" id="odpowiedz2" value="" maxlength="20" placeholder="Wpisz nazwę tematu"/>
            <div class="buttons">
                <br>
                <button type="submit" class="button15"  name="button15" id="przejdz">Utwórz temat</button>
            </div>
        </form>
                  <form action="wybor.php">
             
    <input type="submit" class="button4" name="Powrót" value="Powrót">
</form>
    </div>
    <?php
      $db->close(); 
    ?>
</body>
</html>