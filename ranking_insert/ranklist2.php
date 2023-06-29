<?php
// 데이터베이스 연결
$dbhost = 'localhost';
$dbuser = 'root';
$dbpass = '';
$dbname = 'rank';
$conn = new mysqli($dbhost, $dbuser, $dbpass, $dbname);

if ($conn->connect_error) {
    die('Could not connect: ' . $conn->connect_error);
}

// SQL 쿼리
$sql = "SELECT username, score FROM rankings ORDER BY score DESC";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // 랭킹 숫자를 위한 변수
    $rank = 1;
    // 각 행을 출력
    while($row = $result->fetch_assoc()) {
        echo $rank . "위 : " . $row["username"]. " [ score : " . $row["score"]. " ]<br>";
        $rank++;
    }
} else {
    echo "0 results";
}

$conn->close();
?>
