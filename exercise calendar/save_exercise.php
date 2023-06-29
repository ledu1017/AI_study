<?php
// MySQL 데이터베이스 연결 설정
$servername = "localhost";
$username = "root";
$password = "";

// 데이터베이스 연결 생성
$conn = new mysqli($servername, $username, $password);

// 데이터베이스 연결 확인
if ($conn->connect_error) {
    die("데이터베이스 연결 실패: " . $conn->connect_error);
}

// 데이터베이스 생성 (healthdate)
$createDatabaseQuery = "CREATE DATABASE IF NOT EXISTS healthdate";
if ($conn->query($createDatabaseQuery) === FALSE) {
    die("데이터베이스 생성 실패: " . $conn->error);
}

// 데이터베이스 선택
$conn->select_db("healthdate");

// 운동 기록 테이블 존재 여부 확인
$tableExistsQuery = "SHOW TABLES LIKE 'exercise_records'";
$tableExistsResult = $conn->query($tableExistsQuery);

// 운동 기록 테이블 생성 (테이블이 존재하지 않을 경우에만 생성)
if ($tableExistsResult->num_rows === 0) {
    $createTableQuery = "CREATE TABLE exercise_records (
        id INT AUTO_INCREMENT PRIMARY KEY,
        exercise_date DATE,
        exercise_name VARCHAR(255)
    )";
    if ($conn->query($createTableQuery) === FALSE) {
        die("테이블 생성 실패: " . $conn->error);
    }
}

// POST로 전달된 운동 기록 데이터 가져오기
$exerciseDate = $_POST['exercise_date'];
$exerciseName = $_POST['exercise_name'];

// 운동 기록 데이터 데이터베이스에 저장
$sql = "INSERT INTO exercise_records (exercise_date, exercise_name) VALUES ('$exerciseDate', '$exerciseName')";
if ($conn->query($sql) === TRUE) {
    echo "운동 기록이 성공적으로 저장되었습니다.";

    // 데이터베이스 연결 닫기
    $conn->close();

    // 2초 지연 후 exercise_callendar.php 실행
    sleep(2);
    header("Location: exercise_calendar.php");
    exit();
} else {
    echo "운동 기록 저장 실패: " . $conn->error;
}

// 데이터베이스 연결 닫기
$conn->close();
?>
