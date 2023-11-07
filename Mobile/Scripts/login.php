<?php
require("access2.php");
session_start();
$message="";
if(isset($_POST['login'])){
    $username = $_POST['username'];
    $password = $_POST['password'];

    $stmt_uczniowie = $db->prepare("SELECT * FROM uczniowie WHERE login = ?");
    $stmt_uczniowie->bind_param("s", $username);
    $stmt_uczniowie->execute();
    $result_uczniowie = $stmt_uczniowie->get_result();
    
    $stmt_nauczyciele = $db->prepare("SELECT * FROM nauczyciele WHERE login = ?");
    $stmt_nauczyciele->bind_param("s", $username);
    $stmt_nauczyciele->execute();
    $result_nauczyciele = $stmt_nauczyciele->get_result();
    
    if ($result_uczniowie->num_rows == 1) {
        $row_uczniowie = $result_uczniowie->fetch_assoc();
        if (password_verify($password, $row_uczniowie['haslo'])) {
            $_SESSION['id_ucznia'] = $row_uczniowie['id_ucznia'];
            header("Location: wybor.php");
            exit();
        } else {
            $message = "Niepoprawne dane";
        }
    } elseif ($result_nauczyciele->num_rows == 1) {
        $row_nauczyciele = $result_nauczyciele->fetch_assoc();
        if (password_verify($password, $row_nauczyciele['haslo'])) {
            $_SESSION['id_nauczyciela'] = $row_nauczyciele['id_nauczyciela'];
            header("Location: wybor.php");
            exit();
        } else {
            $message = "Niepoprawne dane";
        }
        } else {
            $message = "Niepoprawne dane";
        }
}

$db->close();
?>

<!DOCTYPE HTML>
<html>
<head>
    <meta charset="UTF-8"/>
    <title>Strona do nauki angielskiego</title>
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css">
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
</head>
<body>
<div class="center3">
    <form method="POST">
        <h1>Zaloguj się</h1>
        <i class="fa-regular fa-user"></i>
        <input type="text" name="username" placeholder="Wprowadź login" required maxlength="100"/>
        <br><br>
        <i class='bx bx-lock-alt'></i>
        <input type="password" name="password" placeholder="Wprowadź hasło" required maxlength="100"/>
        <br><br>
        <input type="submit" name="login" class="submit3" value="Zaloguj się">
    </form>
    <br>
    <br>
        <form action="register.php">
    <input type="submit" class="submit4" name="Powrót" value="Przejdź do rejestracji">
</form>
    <?php
    if($message) {
        echo "<div class='echo4'>";
        echo $message;
        echo "</div>";
    }
    ?>
</div>
<style>
.center3 {
    position: relative;
    max-width: 150%; 
    top:200px;
    background-color: rgb(35, 35, 35);
    color: white;
    padding: 20px; 
    box-sizing: border-box; 
}

input[type="password"], input[type="text"] {
    position: relative;
    color: white;
    font-size: 16px;
    border: none;
    outline: none;
    border-radius: 20px;
    padding: 10px 15px; 
    width: 80%; 
    margin-bottom: 15px;
    background-color: rgb(57, 59, 58);
}

.submit3 {
    position: relative;
    display: inline-block;
    padding: 7px 30px;
    background-color: rgb(218, 216, 217);
    text-decoration: none;
    transition: 0.5s;
    border: none;
    border-radius: 25px;
    overflow: hidden;
    color: black;
    bottom:20px;
    width: 100%; 
}

body {
    background-image: url('New_Project.png');
    background-attachment: fixed;
}.echo4{
    color:red;
}
.submit4 {
    position: relative;
    display: inline-block;
    padding: 7px 30px;
    background-color: green;
    text-decoration: none;
    transition: 0.5s;
    border: none;
    border-radius: 25px;
    color: black;
    bottom:20px;
    width: 100%; 
}
</style>

</body>
</html>
