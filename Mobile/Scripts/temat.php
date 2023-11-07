<?php
require_once("access2.php");
$buttonValue = $_POST['button']; 
?>
    <div class="box4">
                    <div id='slownik'>
    <b><?php echo $buttonValue ?></b>  
    </div>
            <div class="text">
    
                <?php
                if(isset($_POST['button'])) {
                    $buttonValue = $_POST['button']; 
                    $queryb = "SELECT id_tematu FROM tematy WHERE nazwa_tematu=?";
                    $preparedst2 = $db->prepare($queryb);
                    $preparedst2->bind_param("s", $buttonValue);
                    $preparedst2->execute();
                    $result3 = $preparedst2->get_result();
                    $row2 = $result3->fetch_array(MYSQLI_NUM);
                    $id_tematu = $row2[0];
                }

$query = "SELECT slowka.id_slowka, slowko, tlumaczenie FROM tematy INNER JOIN slowka ON tematy.`id_tematu` = slowka.`id_tematu` where slowka.id_tematu = $id_tematu";
$preparedst = $db->prepare($query);
$preparedst->execute();
$result = $preparedst->get_result();

$data = array();
while ($row = mysqli_fetch_array($result)) {
    $data[] = array(
        'id' => $row[0], 
        'slowo' => ucfirst($row[1]),
        'tlumaczenie' => ucfirst($row[2])
        
    );
}
?>
                <!DOCTYPE html>
                
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <script>
        var currentWord = 0;
        var data = <?php echo json_encode($data); ?>;
        
                       function displayWord() {
    var wordElement = document.getElementById('slowa');
    var currentWordIndex = currentWord + 1; 
    var totalWords = data.length;
    wordElement.innerHTML = "<div style='float: right;position:relative;bottom:140px;right:5px'>" + currentWordIndex + "/" + totalWords + "</div>" +"&nbsp&nbsp&nbsp&nbsp&nbsp"+ "<div style='position:relative;bottom:62.5px'>"+ data[currentWord].slowo + " -> " + data[currentWord].tlumaczenie + "</div>";

}
function nextWord() {
    currentWord = (currentWord + 1) % data.length;
    displayWord();
}
function previousWord() {
    currentWord = (currentWord - 1 + data.length) % data.length;
    displayWord();
}
                    </script>
                </head>
                <body>
                    <div id="slowa"></div>
                    
                    <button class="button4" onclick="previousWord()">Poprzednie słowo</button>
                    <button class="button4" onclick="nextWord()">Następne słowo</button>
                    <script>displayWord();</script>
                      <form action="wybor.php" method="POST">
        <br>
        <input type="submit" name="powrót" value="Powrót"></button>
    </form>
                     
                     <style>
.box4 {
    position:relative;
    top:30%;
    width: 100%;
    height: 40%;
    border: 1px solid black;
    margin: 0 auto;
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
    overflow: hidden;
}
body {
    background-image: url('New_Project.png');
}
#slownik{
    position:relative;
    text-align:left;
    left:5px
}
input[name="powrót"]{
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
        </div>
    </div>
</body>
</html>
<?php
$preparedst->close();
$preparedst2->close();
$db->close();
?>
