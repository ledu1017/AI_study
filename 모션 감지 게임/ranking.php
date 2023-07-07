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

// SQL 쿼리
$sql_select = "SELECT username, score FROM rankings ORDER BY score DESC";
$result = $conn->query($sql_select);

if ($result->num_rows > 0) {
    // 결과 배열 생성
    $rankings = array();

    // 결과 출력
    while ($row = $result->fetch_assoc()) {
        $rankings[] = array(
            'username' => $row['username'],
            'score' => $row['score']
        );
    }

    // JSON 형식으로 반환
    header('Content-Type: application/json');
    echo json_encode($rankings);
} else {
    echo "No results found";
}

$conn->close();
?>