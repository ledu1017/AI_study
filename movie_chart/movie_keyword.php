<?php
$host = 'localhost';
$user = 'root';
$password = '';
$dbname = 'review';

// MySQL에 연결
$conn = new mysqli($host, $user, $password, $dbname);
if ($conn->connect_error) {
    die("MySQL 연결 실패: " . $conn->connect_error);
}

// SELECT 쿼리 실행
$sql = "SELECT keyword, keyword_count FROM reviews";
$result = $conn->query($sql);

// 결과를 저장할 배열
$data = array();

if ($result->num_rows > 0) {
    // 결과를 반복하여 가져와서 배열에 추가
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
} else {
    echo "데이터 없음";
}

// 연결 종료
$conn->close();

// 데이터를 JSON 형식으로 반환 (UTF-8 인코딩)
echo json_encode($data, JSON_UNESCAPED_UNICODE);
?>
