<?php
// 데이터베이스 연결
$dbhost = 'localhost';
$dbuser = 'root';
$dbpass = '';
$conn = new mysqli($dbhost, $dbuser, $dbpass);

if ($conn->connect_error) {
    die('Could not connect: ' . $conn->connect_error);
}

header("Access-Control-Allow-Origin: *");

// 데이터베이스 선택
$dbname = 'game_rank';
$conn->select_db($dbname);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // POST 요청의 경우 사용자가 입력한 아이디 확인
    $username = $_POST['username'];

    // 아이디를 데이터베이스에서 확인하는 쿼리
    $sql_select = "SELECT * FROM rankings WHERE username = '$username'";
    $result = $conn->query($sql_select);

    if ($result->num_rows > 0) {
        // 아이디가 존재하는 경우
        echo '1';
    } else {
        // 아이디가 존재하지 않는 경우
        echo '0';
    }
} else {
    echo 'Invalid request';
}

$conn->close();
?>
