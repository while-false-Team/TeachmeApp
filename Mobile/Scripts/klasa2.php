<?php
session_start();
$kod=$_SESSION['kod'];
$nazwa=$_SESSION['nazwa'];
?>
<html>
<head>
    <meta charset="UTF-8"/>
</head>
<body>
    <style>
 body{
        background-image: url('New_Project.png');
        }
.boxy{
    text-align:center;
    color:white;
    position:relative;
    font-size:130%;
    top:40%;
  background-color: rgb(50, 50, 50);
  border-radius: 15px;
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
    
    <div class="boxy">
       <?php
       echo "Nazwa klasy:";
echo $nazwa;
echo "<br>";
echo "Kod klasy:";
echo $kod;
?>
    <br>
    <form action="wybor.php" method="POST">
        <input type="submit" class="button4" value="Powrót">
    </form>
</div>
    <?php
      $db->close(); 
    ?>
</body>
</html>

?>
