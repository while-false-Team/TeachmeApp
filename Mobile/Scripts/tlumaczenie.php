<?php
require("access2.php");
?>
<html>
<head>
    <meta charset="UTF-8"/>
    <link rel="stylesheet" href="style2.css">
</head>
<body>
    <style>
          body{
           
            background-image: url('New_Project.png');
        }
    </style>
<div class="boxy">
            <?php
            $queryd="SELECT * FROM slowka ORDER BY RAND() LIMIT 1;";
            $preparedst2=$db->prepare($queryd);
            $preparedst2->execute();
            $result2 = $preparedst2->get_result();
            while ($wiersz = mysqli_fetch_array($result2))
             {
            ?>
            <p><?php echo $wiersz[2]; $ids=$wiersz[0];$slowo=$wiersz[1] ?></p>
            <form action="" method="post">
                <input type="hidden" name="Id" value="<?php echo $wiersz[0] ?>"/>
                <input type="hidden" name="odpowiedz2" value="<?php echo $wiersz[1]?>"/>
                <input type="hidden" name="xd" value="<?php echo $wiersz[2]; ?>">
        <?php
        }
        ?>
    </div>
    <div class="input5">
                <input type="text" name="twoje" id="odpowiedz2" value="" maxlength="20" placeholder="Wpisz tłumaczenie"/>
                <div class="buttons">
                <button type="button" class="button1"   id="hint-button" onclick="podpowiedzlitere()">Podpowiedz literę</button>
                <button type="button" class="button2"  id="hint-buttone"  onclick="sprawdzOdpowiedz()">Sprawdź słowo </button>
                </div>
                <button type="submit" class="button3"  name="przycisk" id="przejdz">Przejdź dalej</button>
        
    <div style="position: fixed; bottom: 2px;">
</form>
<form action="wybor.php" method="POST">
    <input type="submit" name="przejscie" value="Powrót" class="button5">
</form>
    </div>
    </div>
    <style>
        .button5 {
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
<?php
  $db->close(); 
?>
   <script>
    document.addEventListener('DOMContentLoaded', function() {
    const wordContainers = document.querySelectorAll('.word-container');

    wordContainers.forEach(container => {
        const showWordElement = container.querySelector('.show-word');
        const word = container.dataset.word;

        showWordElement.addEventListener('click', function() {
            showWordElement.innerText = word;
        });
    });
});
    var focus = document.getElementById("odpowiedz2").focus();  //focus 
    var przejdz=document.getElementById('przejdz');
    przejdz.style.display='none';

    function podpowiedzlitere() {
        var currentWordValue = "<?php echo $slowo ?>"; 
        var odpowiedz = document.getElementById("odpowiedz2");
        var litery = currentWordValue.toLowerCase().split("");
        var poprawneLitery = "";
        var poprawneIndex = 0;

        for (var i = 0; i < odpowiedz.value.length; i++) {
            if (odpowiedz.value[i].toLowerCase() === litery[poprawneIndex]) {
                poprawneLitery += odpowiedz.value[i];
                poprawneIndex++;
            } else {
                break;
            }
        }

        odpowiedz.value = poprawneLitery;

        if (poprawneIndex < litery.length) {
            if (litery[poprawneIndex].toUpperCase() === litery[poprawneIndex]) {
                odpowiedz.value += litery[poprawneIndex].toUpperCase();
            } else {
                odpowiedz.value += litery[poprawneIndex];
            }
        }
    }


function sprawdzOdpowiedz() {
    var inputField = document.getElementById('odpowiedz2');
    var userAnswer = inputField.value.toLowerCase();
    var correctAnswer = '<?php echo $slowo; ?>'.toLowerCase();
    var displayedAnswer = userAnswer + '\t(' + correctAnswer + ')';

    if (userAnswer === correctAnswer) {
        inputField.classList.add('correct-answer');
        displayedAnswer = correctAnswer; 
        przejdz.classList.add('green');
    } else {
        inputField.classList.add('incorrect-answer');
        inputField.value = displayedAnswer; 
        przejdz.classList.add('red');
    }

    inputField.style.transition = 'all 0.75s';
    inputField.style.height = '10%';
    inputField.style.width = '72.5%';
    var literahid = document.getElementById('hint-button');
    var sprawdzhid = document.getElementById('hint-buttone');
    literahid.style.display = 'none';
    sprawdzhid.style.display = 'none';
    przejdz.style.display = 'block';
    inputField.disabled = true;


    inputField.value = displayedAnswer;
}
    </script>
     
</div>
            </div>
</body>
</html>