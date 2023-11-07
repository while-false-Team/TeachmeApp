<?php
session_start(); 
require("access2.php");
$message="";
if(isset($_POST['button4'])) {
    $id_ucznia=$_SESSION['id_uczniaa'];
    $kod_klasy = $_POST['twoje'];
    $queryd = "SELECT `id_klasy` FROM `klasy` WHERE `kod_klasy`= ?";
    $preparedst2 = $db->prepare($queryd);
    $preparedst2->bind_param('s',$kod_klasy);
    $preparedst2->execute();
    $preparedst2->bind_result($id_klasy); 
    $preparedst2->fetch(); 
    $klasy = $id_klasy;
      if ($klasy) {
        $_SESSION['id_klasy'] = $klasy;
        $_SESSION['id_uczniaa'] = $id_ucznia;
        header("Location:dodawanie.php");
    } else {
        $message="Błędny kod klasy";
    }
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
 .button4 {
    position: relative;
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
    </style>
    <div class="boxy"></div>
    <div class="input6">
         <form action="dolacz.php" method="POST">
             <input type="text" name="twoje" id="odpowiedz2" value="" maxlength="20" placeholder="Wpisz kod klasy"/>
           <br>
         <button type="submit" class="button4"  name="button4" id="przejdz">Dołącz do klasy</button>
            
        </form>
   <form action="wybor.php" method="POST">
          <button type="submit" class="button4">Powrót</button>
          
    </form>
      <?php
    echo "<h2><div style='color:white'>$message</h2></div>";
      $db->close(); 
    ?>
    </div>
   
</body>
</html>
