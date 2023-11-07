<?php
require_once("access2.php");
$buttonValue = $_POST['button']; 
session_start();
$id_ucznia=$_SESSION['id_uczniaa'];
if (!isset($_SESSION['currentWord'])) {
    $_SESSION['currentWord'] = 0; 
}
?>

<div class="box4">
    <div id='slownik'>
        <b><?php echo $buttonValue ?></b>  
    </div>
    
    <div class="text">
        <?php
        if(isset($_POST['powrot'])) {
            header("Location:wybor.php");
        }
        if(isset($_POST['button'])) {
            $buttonValue = $_POST['button']; 
            $queryb = "SELECT id_tematu FROM tematy WHERE nazwa_tematu=?";
            $preparedst2 = $db->prepare($queryb);
            $preparedst2->bind_param("s", $buttonValue);
            $preparedst2->execute();
            $result3 = $preparedst2->get_result();
            $row2 = $result3->fetch_array(MYSQLI_NUM);
            $id_tematu = $row2[0];
            echo "<script>var id_tematu = $id_tematu;</script>";
            echo "<script>var id_ucznia = $id_ucznia;</script>";
        }
        $query = "SELECT slowka.id_slowka, slowko, tlumaczenie FROM tematy INNER JOIN slowka ON tematy.`id_tematu` = slowka.`id_tematu` WHERE slowka.id_tematu = $id_tematu ORDER BY RAND()";

        $preparedst = $db->prepare($query);
        $preparedst->execute();
        $result = $preparedst->get_result();

        $data = array();
        while ($row = mysqli_fetch_array($result)) {
            $data[] = array(
                'id' => $row[0], 
                'slowo' => ucfirst($row[1]),
                'tlumaczenie' => ucfirst($row[2]), 
                'counter' => 0
            );
        }

        ?>
        <div id="slowa"></div>
        <div id="summary" style="display:none;"></div>

        <div class="input4">
            <input type="text" name="twoje" id="odpowiedz2" value="" placeholder="Wpisz tłumaczenie"/>
            <button type="button" class="button2" name='button12' id="hint-buttone" onclick="sprawdzOdpowiedz()">Sprawdź odpowiedź</button>
            <br>
            <br>
            <button type="button" class="button1" id="hint-button" onclick="podpowiedzlitere()">Podpowiedz literę</button>
            <form action="wybor.php" method="POST">
                <input type="submit" name="powrót" value="Powrót">
            </form>
        </div>
        <div id="poprawnosc"></div>
    </div>
    <div style="display:none" id="poziom"></div>

    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <script>
            var odpowiedzi = 0;
            var counter = 0;
            var endcounter=0;
            var currentWord = 0;
            var data = <?php echo json_encode($data); ?>;
    function displayWord() {
        var wordElement = document.getElementById('slowa');
        var currentWordIndex = currentWord + 1; 
        var totalWords = data.length;
        wordElement.innerHTML = "<div style='float: right;position:relative;bottom:140px;right:5px'>" + currentWordIndex + "/" + totalWords + "</div>" +"&nbsp&nbsp&nbsp&nbsp&nbsp"+ "<div style='position:relative;bottom:62.5px'>"+ data[currentWord].slowo + "</div>";
    }

   function nextWord() {
    currentWord = (currentWord + 1) % data.length;
    displayWord();

    if (currentWord === data.length - 1) {
        showSummary();
    }
}
function sprawdzOdpowiedz() {
    var poprawnoscElement = document.getElementById('poprawnosc');
    var inputElement = document.getElementById('odpowiedz2');
    var inputValue = inputElement.value.toLowerCase();
    var currentWordValue = data[currentWord].slowo.toLowerCase();
    var currenttlumaczvalue = data[currentWord].tlumaczenie.toLowerCase();

    if (inputValue === currenttlumaczvalue) {
        inputElement.value = '';
        poprawnoscElement.innerHTML = "";
        nextWord();
        odpowiedzi++;
    } else {
        data[currentWord].counter++;  
        poprawnoscElement.innerHTML = "<br>" + "Błędna odpowiedź";
        odpowiedzi--;
    }
    hintGiven = false; 
    console.log(odpowiedzi)
}

var hintGiven = false; 


function podpowiedzlitere() {
var currentWordValue = data[currentWord].tlumaczenie.toLowerCase(); 
var odpowiedz = document.getElementById("odpowiedz2");
var litery = currentWordValue.split("");
var poprawneLitery = "";
var poprawneIndex = 0;
if (!hintGiven) {
    odpowiedzi-=1;
    hintGiven = true; 
}


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

function nextWord() {
    currentWord = (currentWord + 1) % data.length;
    displayWord();

    if (currentWord === data.length - 1) {
        var sprawdzButton = document.getElementById('hint-buttone');
        sprawdzButton.textContent = 'Zakończ test';
        sprawdzButton.onclick = zakonczTest;
    }
}function zakonczTest() {
     var poprawnoscElement = document.getElementById('poprawnosc');
    var inputElement = document.getElementById('odpowiedz2');
    var inputValue = inputElement.value.toLowerCase();
    var currentWordValue = data[currentWord].slowo.toLowerCase();
    var currenttlumaczvalue = data[currentWord].tlumaczenie.toLowerCase();
    if (inputValue === currenttlumaczvalue) {
        inputElement.value = '';
        poprawnoscElement.innerHTML = "";
        nextWord();
        odpowiedzi++;
        endcounter++;
        showSummary();
    } else {
        data[currentWord].counter++;  
        poprawnoscElement.innerHTML = "<br>" + "Błędna odpowiedź";
        odpowiedzi--;
    }
    hintGiven = false; 
    
}
            function showSummary() {
                
                var licznikodpowiedzi = (odpowiedzi / data.length);
                var poziom = " ";
                var poziomColor = "";

                if (licznikodpowiedzi == 1) {
                    poziom = "Celujący";
                    poziomColor = "green";
                } else if (licznikodpowiedzi >= 0.75 && licznikodpowiedzi < 1) {
                    poziom = "Bardzo dobry";
                    poziomColor = "lightgreen";
                } else if (licznikodpowiedzi >= 0.6 && licznikodpowiedzi < 0.75) {
                    poziom = "Dobry";
                    poziomColor = "yellow";
                } else if (licznikodpowiedzi >= 0.35 && licznikodpowiedzi < 0.6) {
                    poziom = "Średni";
                    poziomColor = "orange";
                } else if (licznikodpowiedzi >= 0.2 && licznikodpowiedzi < 0.35) {
                    poziom = "Minimalny";
                    poziomColor = "red";
                } else {
                    poziom = "Zerowy";
                    poziomColor = "red";
                }

                var inputElement = document.getElementById('odpowiedz2');
                var hintButton = document.getElementById('hint-button');
                var checkButton = document.getElementById('hint-buttone');
                var summaryElement = document.getElementById('summary');
                var wordElement = document.getElementById('slowa');

                inputElement.style.display = 'none';
                hintButton.style.display = 'none';
                checkButton.style.display = 'none';
                wordElement.style.display = 'none';

                var totalErrors = 0;
                var summaryTable = "<table border='2'><tr><th>Słówko</th><th>Tłumaczenie</th><th>Ilość błędów</th></tr>";

                for (var i = 0; i < data.length; i++) {
                    summaryTable += "<tr>";
                    summaryTable += "<td>" + data[i].slowo + "</td>";
                    summaryTable += "<td>" + data[i].tlumaczenie + "</td>";
                    summaryTable += "<td>" + data[i].counter + "</td>";
                    summaryTable += "</tr>";
                    totalErrors += data[i].counter; // Calculate the total errors
                }

                summaryTable += "<tr><td style='background-color: " + poziomColor + ";'>Poziom</td><td style='background-color: " + poziomColor + ";'>" + poziom + "</td><td style='background-color: " + poziomColor + ";'>" + totalErrors + "</td></tr>";
                summaryTable += "</table>";
                summaryElement.innerHTML = summaryTable;
                summaryElement.style.display = 'block';
  var poziomElement = document.getElementById('poziom');
    poziomElement.innerHTML = poziom;
 wyslijpoziom(poziom, id_tematu,id_ucznia);
    
}
function wyslijpoziom(poziom, id_tematu, id_ucznia) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'danetematow.php', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 400) {
            console.log('Wyslane');
        } else {
            console.error('Error ');
        }
    };
    xhr.send('poziom=' + encodeURIComponent(poziom) + '&id_tematu=' + encodeURIComponent(id_tematu) + '&id_ucznia=' + encodeURIComponent(id_ucznia));
}

            displayWord();
        </script>
    </head>
    <body>
        <style>
            .box4 {
                position:relative;
                top:25%;
                width:100%;
                max-height:500px;
                border: 1px solid black;
                background-color: #343434;
                border-radius: 15px;
            }

            b {
                font-size: 40px; 
                color:white;
            }

            .text {
                position:relative;
                top:100px;
                font-size: 24px; 
                color:white;
                text-align:center;
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
            }

            body {
                background-image: url('New_Project.png');
            }

            #slownik {
                position:relative;
                text-align:left;
                left:5px
            }

            input[name="twoje"] {
                font-size: 20px;
                padding: 10px 10px 10px 5px;
                display: block;
                width:100%;
                border: none;
                border-bottom: 1px solid #757575;
                background-color: #343434;
                color: white;
                border-radius: 15px;
                background-color:black;
            }

            .button1 {
                padding: 10px 30px;
                background-color: rgba(37, 35, 35, 1);
                transition:0.5s;
                border: none;
                border-radius: 25px;
                overflow: hidden;
                color:white;
            }

            .button2 {
                display: inline-block;
                padding: 10px 30px;
                background-color: #4169e1;
                border: none;
                border-radius: 25px;
                overflow: hidden;
                margin-top: 25px;
                color:white;
            }

            table {
                width: 100%; 
                border-collapse: collapse; 
                color:white;
                background-color:rgb(12,12,12);
            }

            input[name="powrót"] {
                position:relative;
                left:42%;
                top:5px;
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
</div>

<?php
$preparedst->close();
$preparedst2->close();
$db->close();
?>
