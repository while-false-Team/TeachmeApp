<?php
session_start();
require("access2.php");

if(isset($_POST['register'])){
    $username = $_POST['login'];
    $password = $_POST['password'];
    $password2 = $_POST['password2'];

    if ($password == $password2 && (strlen($password) <= 100) && (strlen($username) <= 100)) {
       
        function checkPasswordRequirements($password) {
            $passwordPattern = "/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/";
            return preg_match($passwordPattern, $password);
        }

        if (checkPasswordRequirements($password)) {
            $query = "SELECT `login` FROM `uczniowie` WHERE login=?";
            $stmt = $db->prepare($query);
            $stmt->bind_param("s", $username);
            $stmt->execute();
            $result = $stmt->get_result();
            $rows = $stmt->affected_rows;
            
            if ($rows > 0) {
                echo "<div class='echo4'>";
                echo "Podany przez ciebie login jest zajęty";
                echo "</div>";
            } else {
                $hashed_password = password_hash($password, PASSWORD_ARGON2I);
                $nauczyciel = isset($_POST['nauczycieladd']) ? 1 : 0;
                if ($nauczyciel) {
                    $nazwa_tabeli = "nauczyciele";
                }else {
                    $nazwa_tabeli = "uczniowie";
                }
                
                if ($nazwa_tabeli=="uczniowie")
                {
                $stmt = $db->prepare("INSERT INTO uczniowie(login, haslo,id_klasy) VALUES (?, ?, NULL)");
                $stmt->bind_param("ss", $username, $hashed_password);
                $stmt->execute();

                header("Location: login.php");
                exit();
                }
                else{
                $stmt = $db->prepare("INSERT INTO `nauczyciele`( `login`, `haslo`) VALUES (?,?)");
                $stmt->bind_param("ss", $username, $hashed_password);
                $stmt->execute();
                  header("Location: login.php");
                exit();
                }
               
            }
        } else {
            echo "<div class='echo4'>";
            echo "Hasło nie spełnia odpowiednich wymagań";
            echo "</div>";
        }
    } else {
        echo "<div class='echo4'>";
        echo "Nieprawidłowe hasła";
        echo "</div>";
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
    <form action="register.php" method="POST">
        <h1>Zarejestruj się</h1>
        <i class="fa-regular fa-user"></i>
        <input type="text" name="login" placeholder="Wprowadź login" required maxlength="100"/>
        <br><br>
        <i class='bx bx-lock-alt'></i>
        <input type="password" id="password" name="password" placeholder="Wprowadź hasło" required maxlength="100"/>
        <br>
        <div id="password-requirements"></div>
        <br>
        <i class='bx bx-lock-alt'></i>
        <input type="password" name="password2" placeholder="Powtórz hasło" required maxlength="100" />
        <br><br>
          <input type="checkbox" id="nauczyciel" name="nauczycieladd" value="1">
        <label for="nauczyciel">Nauczyciel</label><br>
        <br>
        <br>
        <input type="submit" name="register" class="submit3" value="Zarejestruj się">
      
    </form>
    <br>
    <br>
    <form action="login.php">
    <input type="submit" class="submit4" name="Powrót" value="Przejdź do logowania">
</form>
</div>

<script>
function checkPasswordRequirements() {
    const passwordInput = document.getElementById("password");
    const password = passwordInput.value;
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    let requirements = [];

    if (!passwordPattern.test(password)) {
        if (!/(?=.*[a-z])/.test(password)) {
            requirements.push("małej litery");
        }
        if (!/(?=.*[A-Z])/.test(password)) {
            requirements.push("dużej litery");
        }
        if (!/(?=.*\d)/.test(password)) {
            requirements.push("cyfry");
        }
        if (!/(?=.*[@$!%*?&])/.test(password)) {
            requirements.push("znaku specjalnego");
        }
        if (password.length < 8) {
            requirements.push("co najmniej 8 znaków");
        }
    }

    const requirementsDiv = document.getElementById("password-requirements");

    if (requirements.length > 0) {
        requirementsDiv.innerHTML = `Brakuje: ${requirements.join(", ")}`;
        passwordInput.classList.remove("valid");
        passwordInput.classList.add("invalid");
    } else {
        requirementsDiv.innerHTML = "";
        passwordInput.classList.remove("invalid");
        passwordInput.classList.add("valid");
    }
}

const passwordInput = document.getElementById("password");
passwordInput.addEventListener("input", checkPasswordRequirements);
</script>

<style>
    .invalid {
        color: red;
    }

    .center3 {
        position: relative;
        max-width: 150%; 
        top:160px;
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
        background-color:lightblue;
        text-decoration: none;
        transition: 0.5s;
        border: none;
        border-radius: 25px;
        color: black;
        bottom:20px;
        width: 100%; 
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

    body {
        background-image: url('New_Project.png');
        background-attachment: fixed;
    }

    .echo4{
        color:red;
    }
</style>

</body>
</html>
