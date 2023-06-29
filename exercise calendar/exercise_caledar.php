<!DOCTYPE html>
<html>
<head>
    <title>운동 기록 달력</title>
    <style>
        .highlight {
            background-color: #ff0000;
        }
    </style>
</head>
<body>
    <h1>운동 기록 달력</h1>
    <?php
    // MySQL 데이터베이스 연결 설정
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "healthdate";

    // 데이터베이스 연결 생성
    $conn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error) {
        die("데이터베이스 연결 실패: " . $conn->connect_error);
    }

    // 현재 년도와 월 가져오기
    $currentYear = date("Y");
    $currentMonth = date("m");

    // 해당 달의 운동 기록 가져오기
    $sql = "SELECT DATE_FORMAT(exercise_date, '%Y-%m-%d') AS formatted_date FROM exercise_records WHERE DATE_FORMAT(exercise_date, '%Y-%m') = '$currentYear-$currentMonth'";
    $result = $conn->query($sql);
    $exerciseDates = array();
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $exerciseDates[] = $row['formatted_date'];
        }
    }
    // 달력 테이블 생성
    echo "<table>";
    echo "<tr>";
    echo "<th>일</th>";
    echo "<th>월</th>";
    echo "<th>화</th>";
    echo "<th>수</th>";
    echo "<th>목</th>";
    echo "<th>금</th>";
    echo "<th>토</th>";
    echo "</tr>";
    // 첫 번째 주의 날짜 전까지 빈 칸 생성
    echo "<tr>";
    $firstDayOfMonth = date("N", strtotime("$currentYear-$currentMonth-01"));
    for ($i = 1; $i < $firstDayOfMonth; $i++) {
        echo "<td></td>";
    }
    // 날짜 출력
    $dayCount = 1;
    while ($dayCount <= cal_days_in_month(CAL_GREGORIAN, $currentMonth, $currentYear)) {
        echo "<td";
        $date = sprintf("%04d-%02d-%02d", $currentYear, $currentMonth, $dayCount);
        if (in_array($date, $exerciseDates)) {
            echo " class='highlight'"; // 운동 기록 날짜 강조
        }
        echo ">$dayCount</td>";

        if ($firstDayOfMonth == 7) {
            echo "</tr>";
            if ($dayCount != cal_days_in_month(CAL_GREGORIAN, $currentMonth, $currentYear)) {
                echo "<tr>";
            }
            $firstDayOfMonth = 0;
        }	

        $dayCount++;
        $firstDayOfMonth++;
    }
    // 달력 테이블 닫기
    echo "</table>";
    // 데이터베이스 연결 닫기
    $conn->close();
    ?>
</body>
</html>