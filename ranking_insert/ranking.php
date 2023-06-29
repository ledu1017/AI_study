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

// 사용자 이름과 점수 가져오기
$username = $_POST['username'];
$score = $_POST['score'];

// SQL 쿼리
$sql = "INSERT INTO rankings (username, score) VALUES ('{$username}', {$score})";

if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
