<!DOCTYPE html>
<html>
<head>
    <title>운동 기록 입력</title>
</head>
<body>
    <h1>운동 기록 입력</h1>
    <form action="save_exercise.php" method="POST">
        <label for="exercise_date">운동 일자:</label>
        <input type="date" id="exercise_date" name="exercise_date" required>
        <br><br>
        <label for="exercise_name">운동 명:</label>
        <input type="text" id="exercise_name" name="exercise_name" required>
        <br><br>
        <input type="submit" value="저장">
    </form>
</body>
</html>